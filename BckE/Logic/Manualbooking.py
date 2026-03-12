"""
ManualBooking.py – Manuelle Kursbuchung mit schrittweiser Frontend-Validierung.

Ablauf (entspricht der Auswahl im Frontend):
  Schritt 1: Gruppe auswählen
  Schritt 2: Modul auswählen......→ check_modul_valid()
  Schritt 3: Zeitraum auswählen   → get_available_slots() / check_slot_valid()
  Schritt 4: Trainer auswählen    → get_available_trainers_for_slot() / check_trainer_valid()
  Schritt 5: Raum auswählen       → get_available_rooms_for_slot() / check_room_valid()
  Schritt 6: Buchen               → book_manual_course()

Jede check_*-Methode gibt ein Dict zurück:
  { "ok": True/False, "reason": "..." }
So kann das Frontend direkt den Grund einer Ablehnung anzeigen.
"""

from datetime import date, timedelta, datetime

import BckE.SQL.config_Module as cModule
import BckE.Calendar.Calendar_Azubi as azubi_calendar
import BckE.Calendar.Calendar_Trainer as trainer_calender
import BckE.Calendar.Calendar_Raum as raum_calendar
import BckE.SQL.SQL_Trainer as SQL_Trainer
import BckE.SQL.SQL_Gruppe as SQL_Gruppe
import BckE.SQL.SQL_Raum as SQL_Raum
import BckE.SQL.SQL_Kurs as SQL_Kurs
import BckE.formatting.dataGetter as dataGetter
import BckE.Modelle.Kurs as KursModell

# ── Stammdaten ────────────────────────────────────────────────────────────────

con_moduls = cModule.get_Modules()          # {id: modul_dict}
all_groups = dataGetter.get_Gruppen()       # [{id, name, block, ...}]
all_trainers = dataGetter.get_Trainers()    # [{id, nachname, vorname, ...}]
all_rooms = dataGetter.get_Rooms()          # [{id, name, plätze, istPCRaum, ...}]


# ─────────────────────────────────────────────────────────────────────────────
# Interne Hilfsfunktionen (gemeinsam mit Setup.py)
# ─────────────────────────────────────────────────────────────────────────────

def _ok(reason: str = "") -> dict:
    return {"ok": True, "reason": reason}

def _fail(reason: str) -> dict:
    return {"ok": False, "reason": reason}


def _parse_absence_raw(raw) -> list:
    result = []
    if raw is None:
        return result
    items = raw if isinstance(raw, (list, tuple)) else [raw]
    for item in items:
        if not item:
            continue
        for part in str(item).split(','):
            part = part.strip()
            if part:
                result.append(int(part))
    return sorted(result)


def _get_lernjahr_from_group_name(group_name: str):
    try:
        start_year = 2000 + int(group_name[:2])
        now = datetime.now()
        schuljahr_start = now.year if now.month >= 8 else now.year - 1
        lehrjahr = schuljahr_start - start_year + 1
        return lehrjahr if 1 <= lehrjahr <= 3 else None
    except (ValueError, IndexError):
        return None


def _get_modul_lernjahr(modul: dict):
    raw = modul.get('zuordnungLernjahr')
    if isinstance(raw, str) and raw.strip().isdigit():
        return int(raw.strip())
    if isinstance(raw, int):
        return raw
    return None


def _parse_vorgaenger(raw_list: list) -> set:
    result = set()
    for v in raw_list:
        try:
            result.add(int(v))
        except (ValueError, TypeError):
            pass
    return result


def _get_group_done_modules(group_id: int) -> set:
    attended_modules_sql = SQL_Gruppe.get_attendedModules(group_id)
    attended_modules_liste = [x.strip() for x in attended_modules_sql[0].split(',')]
    """Absolvierte Module einer Gruppe als int-Set."""
    done = set()
    for m in attended_modules_liste:
        if str(m).strip().isdigit():
            done.add(int(m))
    return done


def _get_gruppe_calendar(block: str, gruppe_id: int) -> dict:
    """Azubi-Kalender minus bereits gebuchte Tage."""
    gruppe_absence = []
    for row in SQL_Gruppe.get_all():
        if row[0] == gruppe_id and row[5]:
            gruppe_absence = [int(x.strip()) for x in row[5].split(',') if x.strip()]
            break
    cal = azubi_calendar.createAzubiCal(block)
    for idx in gruppe_absence:
        cal.pop(idx, None)
    return cal


def _get_trainer_calendar(trainer_id: int) -> dict:
    """Trainer-Kalender minus Abwesenheiten."""
    raw = SQL_Trainer.get_Trainer_absence(trainer_id)
    absences = _parse_absence_raw(raw)
    return trainer_calender.create_calendar_with_absence(absences)


def _get_room_calendar(room_id: int) -> dict:
    """Raumkalender minus Abwesenheiten."""
    raw = SQL_Raum.get_room_absence(room_id)
    absences = _parse_absence_raw(raw)
    return raum_calendar.create_calendar_with_absence(absences)


def _get_group_booked_week_starts(gruppe_id: int, block: str) -> set:
    """
    Gibt alle Wochen-Startdaten (date) zurück, in denen die Gruppe
    bereits einen Kurs hat. Wird für die 6-Wochen-Regel benötigt.
    """
    booked_starts = set()
    for row in SQL_Gruppe.get_all():
        if row[0] != gruppe_id or not row[5]:
            continue
        absence_indices = {int(x.strip()) for x in row[5].split(',') if x.strip()}
        all_cal = azubi_calendar.createCal()
        for idx, d in all_cal.items():
            end_d = all_cal.get(idx + 4)
            if end_d and (end_d - d).days == 4:
                if any(i in absence_indices for i in range(idx, idx + 5)):
                    booked_starts.add(d)
    return booked_starts


def _check_6week_rule(booked_starts: set, week_start: date, needed_weeks: int) -> dict:
    """
    Gibt _fail() zurück wenn die 6-Wochen-Regel verletzt wird, sonst _ok().
    Regel: Nach 6 aufeinanderfolgenden Unterrichtswochen mindestens 2 Wochen Pause.
    """
    for i in range(needed_weeks):
        w = week_start + timedelta(days=7 * i)

        # Prüfe: Wäre w die 7. Woche in Folge?
        consecutive = 0
        prev = w - timedelta(days=7)
        while prev in booked_starts:
            consecutive += 1
            prev -= timedelta(days=7)
        if consecutive >= 6:
            return _fail(
                f"6-Wochen-Regel verletzt: Die Woche ab {w} wäre die "
                f"{consecutive + 1}. Woche in Folge (max. 6 erlaubt)."
            )

        # Prüfe: Liegt w in einer erzwungenen Pause?
        for gap in [1, 2]:
            run_end = w - timedelta(days=7 * gap)
            if run_end not in booked_starts:
                continue
            run_len = 0
            c = run_end
            while c in booked_starts:
                run_len += 1
                c -= timedelta(days=7)
            if run_len >= 6:
                between_free = all(
                    (run_end + timedelta(days=7 * g)) not in booked_starts
                    for g in range(1, gap)
                )
                if between_free:
                    return _fail(
                        f"6-Wochen-Regel: Die Woche ab {w} liegt in der "
                        f"Pflichtpause nach einem 6-Wochen-Block."
                    )
    return _ok()


def _cal_contains_full_slot(cal: dict, start_date: date, needed_weeks: int) -> bool:
    """
    Prüft ob ein Kalender (Tag-Index → Datum) den gesamten Zeitraum
    (start_date + needed_weeks Wochen) lückenfrei enthält.
    """
    date_set = set(cal.values())
    for i in range(needed_weeks * 5):  # 5 Arbeitstage pro Woche
        check = start_date + timedelta(days=i + (i // 5) * 2)  # Mo–Fr überspringt Wochenende
        # Einfachere Variante: alle Wochentage zwischen start und end prüfen
    # Variante: Woche(n) als Montag-Startdaten prüfen
    for w in range(needed_weeks):
        week_start = start_date + timedelta(days=7 * w)
        for d in range(5):  # Mo bis Fr
            day = week_start + timedelta(days=d)
            if day not in date_set:
                return False
    return True


# ─────────────────────────────────────────────────────────────────────────────
# SCHRITT 2: Modul-Validierung
# ─────────────────────────────────────────────────────────────────────────────

def check_modul_valid(group: dict, modul_id: int) -> bool:
    """
    Prüft ob das gewählte Modul für die Gruppe buchbar ist.

    Prüft:
      - Existiert das Modul?
      - Passt das Lehrjahr?
      - Wurde es bereits absolviert?
      - Sind alle verpflichtenden Vorgänger absolviert?
      - (Info) Optionale Vorgänger noch offen?

    Gibt zurück:
      { "ok": True/False, "reason": str, "warning": str }
      'warning' ist gesetzt wenn optionale Vorgänger noch offen sind.
    """
    if modul_id not in con_moduls:
        return False

    modul      = con_moduls[modul_id]
    modul_name = modul['name']
    done   = _get_group_done_modules(group)

    # Bereits absolviert?
    if modul_id in done:
        return False

    # Lehrjahr
    lehrjahr_ = SQL_Gruppe.get_Lehrjahr(group)
    gruppe_lj = _get_lernjahr_from_group_name(lehrjahr_)
    modul_lj  = _get_modul_lernjahr(modul)
    if gruppe_lj is None:
        return False
    if modul_lj != gruppe_lj:
        return False

    # Verpflichtende Vorgänger
    verpflichtend = _parse_vorgaenger(modul.get('verpflichtendeVorgängermodule', []))
    fehlende      = verpflichtend - done
    if fehlende:
        fehlende_namen = [con_moduls[fid]['name'] for fid in fehlende if fid in con_moduls]
        return False

    # Optionale Vorgänger (nur Warnung)
    optional = _parse_vorgaenger(modul.get('optionaleVorgängermodule', []))
    warning  = ""
    if optional and not (optional & done):
        opt_namen = [con_moduls[oid]['name'] for oid in optional if oid in con_moduls]
        warning = (f"Empfehlung: Die optionalen Vorgänger "
                   f"'{', '.join(opt_namen)}' sind noch nicht absolviert.")

    return True


# ─────────────────────────────────────────────────────────────────────────────
# SCHRITT 3: Zeitraum
# ─────────────────────────────────────────────────────────────────────────────

def get_available_slots(group: dict, modul_id: int) -> list:
    """
    Gibt alle verfügbaren Wochen-Slots zurück, in denen die Gruppe
    frei ist (ohne Trainer/Raum-Prüfung – die folgt in Schritt 4/5).

    Jeder Slot ist ein Dict:
      {
        "start": date,   # Montag der ersten Woche
        "end":   date,   # Freitag der letzten Woche
        "weeks": int     # 1 oder 2
      }
    """
    modul        = con_moduls[modul_id]
    dauer        = int(modul['dauer'])
    needed_weeks = 1 if dauer <= 5 else 2
    block        = group['block']
    gruppe_id    = group['id']

    gruppe_cal      = _get_gruppe_calendar(block, gruppe_id)
    gruppe_weeks    = azubi_calendar.get_available_weeks(gruppe_cal)
    booked_starts   = _get_group_booked_week_starts(gruppe_id, block)

    slots = []
    for i, w in enumerate(gruppe_weeks):
        start = w['start']['date']

        if needed_weeks == 2:
            if i + 1 >= len(gruppe_weeks):
                continue
            next_w = gruppe_weeks[i + 1]
            if (next_w['start']['date'] - start).days != 7:
                continue
            end = next_w['end']['endDate']
        else:
            end = w['end']['endDate']

        # 6-Wochen-Regel prüfen
        if not _check_6week_rule(booked_starts, start, needed_weeks)['ok']:
            continue

        slots.append({
            "start": start,
            "end":   end,
            "weeks": needed_weeks,
        })

    return slots


def check_slot_valid(group: dict, modul_id: int, start_date: date) -> dict:
    """
    Prüft ob der vom User gewählte Startzeitpunkt für Gruppe + Modul gültig ist.

    Prüft:
      - Ist der Slot in der Gruppe frei?
      - Wird die 6-Wochen-Regel eingehalten?
    """
    modul        = con_moduls.get(modul_id)
    if not modul:
        return _fail(f"Modul {modul_id} nicht gefunden.")

    dauer        = int(modul['dauer'])
    needed_weeks = 1 if dauer <= 5 else 2
    block        = group['block']
    gruppe_id    = group['id']

    gruppe_cal   = _get_gruppe_calendar(block, gruppe_id)
    booked_starts = _get_group_booked_week_starts(gruppe_id, block)

    # Gruppe frei im gewählten Zeitraum?
    if not _cal_contains_full_slot(gruppe_cal, start_date, needed_weeks):
        return _fail(
            f"Die Gruppe hat im Zeitraum ab {start_date} bereits einen Kurs "
            f"oder ist in der Schule."
        )

    # 6-Wochen-Regel
    return _check_6week_rule(booked_starts, start_date, needed_weeks)


# ─────────────────────────────────────────────────────────────────────────────
# SCHRITT 4: Trainer
# ─────────────────────────────────────────────────────────────────────────────

def get_available_trainers_for_slot(start_date: date, modul_id: int) -> list:
    """
    Gibt alle Trainer zurück, die im gewählten Zeitraum verfügbar sind.

    Rückgabe: Liste von Trainer-Dicts (id, nachname, vorname)
    """
    modul        = con_moduls.get(modul_id, {})
    dauer        = int(modul.get('dauer', 5))
    needed_weeks = 1 if dauer <= 5 else 2

    available = []
    for trainer in all_trainers:
        trainer_cal = _get_trainer_calendar(trainer['id'])
        if _cal_contains_full_slot(trainer_cal, start_date, needed_weeks):
            available.append(trainer)

    return available


def check_trainer_valid(trainer_id: int, start_date: date, modul_id: int) -> dict:
    """
    Prüft ob der gewählte Trainer im gewählten Zeitraum verfügbar ist.
    """
    modul        = con_moduls.get(modul_id)
    if not modul:
        return _fail(f"Modul {modul_id} nicht gefunden.")

    dauer        = int(modul['dauer'])
    needed_weeks = 1 if dauer <= 5 else 2

    trainer = next((t for t in all_trainers if t['id'] == trainer_id), None)
    if not trainer:
        return _fail(f"Trainer mit ID {trainer_id} nicht gefunden.")

    trainer_cal = _get_trainer_calendar(trainer_id)
    if not _cal_contains_full_slot(trainer_cal, start_date, needed_weeks):
        return _fail(
            f"Trainer {trainer['nachname']} ist im Zeitraum ab {start_date} "
            f"nicht verfügbar (Abwesenheit oder anderer Kurs)."
        )

    return _ok(f"Trainer {trainer['nachname']} ist verfügbar.")


# ─────────────────────────────────────────────────────────────────────────────
# SCHRITT 5: Raum
# ─────────────────────────────────────────────────────────────────────────────

def get_available_rooms_for_slot(start_date: date, modul_id: int) -> list:
    """
    Gibt alle Räume zurück, die im gewählten Zeitraum frei sind
    und zur PC-Kennzeichnung des Moduls passen.

    Rückgabe: Liste von Raum-Dicts (id, name, plätze, istPCRaum)
    """
    modul        = con_moduls.get(modul_id, {})
    dauer        = int(modul.get('dauer', 5))
    needed_weeks = 1 if dauer <= 5 else 2
    modul_pc     = modul.get('pcKennzeichnung', False)

    available = []
    for raum in all_rooms:
        raum_pc = str(raum['istPCRaum']).strip() == '1'
        if modul_pc != raum_pc:
            continue
        room_cal = _get_room_calendar(raum['id'])
        if _cal_contains_full_slot(room_cal, start_date, needed_weeks):
            available.append(raum)

    return available


def check_room_valid(room_id: int, start_date: date, modul_id: int) -> dict:
    """
    Prüft ob der gewählte Raum im Zeitraum frei ist und zur
    PC-Kennzeichnung des Moduls passt.
    """
    modul = con_moduls.get(modul_id)
    if not modul:
        return _fail(f"Modul {modul_id} nicht gefunden.")

    raum = next((r for r in all_rooms if r['id'] == room_id), None)
    if not raum:
        return _fail(f"Raum mit ID {room_id} nicht gefunden.")

    dauer        = int(modul['dauer'])
    needed_weeks = 1 if dauer <= 5 else 2
    modul_pc     = modul['pcKennzeichnung']
    raum_pc      = str(raum['istPCRaum']).strip() == '1'

    # PC-Kennzeichnung
    if modul_pc != raum_pc:
        benötigt = "PC-Raum" if modul_pc else "normalen Raum"
        return _fail(
            f"Modul '{modul['name']}' benötigt einen {benötigt}, "
            f"'{raum['name']}' erfüllt diese Anforderung nicht."
        )

    # Raum frei?
    room_cal = _get_room_calendar(room_id)
    if not _cal_contains_full_slot(room_cal, start_date, needed_weeks):
        return _fail(
            f"Raum '{raum['name']}' ist im Zeitraum ab {start_date} bereits belegt."
        )

    return _ok(f"Raum '{raum['name']}' ist verfügbar.")


# ─────────────────────────────────────────────────────────────────────────────
# SCHRITT 6: Kurs buchen
# ─────────────────────────────────────────────────────────────────────────────

def book_manual_course(
    group: dict,
    modul_id: int,
    start_date: date,
    trainer_id: int,
    room_id: int,
) -> dict:
    """
    Führt die manuelle Buchung durch – validiert alle Schritte nochmals
    bevor in die DB geschrieben wird (defensiv gegen Race Conditions).

    Rückgabe:
      { "ok": True, "kurs_id": int, "reason": str }
      { "ok": False, "reason": str }
    """
    modul = con_moduls.get(modul_id)
    if not modul:
        return _fail(f"Modul {modul_id} nicht gefunden.")

    dauer        = int(modul['dauer'])
    needed_weeks = 1 if dauer <= 5 else 2
    end_date     = start_date + timedelta(days=needed_weeks * 7 - 3)  # letzter Freitag

    trainer = next((t for t in all_trainers if t['id'] == trainer_id), None)
    raum    = next((r for r in all_rooms    if r['id'] == room_id),    None)

    # Alle Checks nochmal gebündelt
    checks = [
        check_modul_valid(group, modul_id),
        check_slot_valid(group, modul_id, start_date),
        check_trainer_valid(trainer_id, start_date, modul_id),
        check_room_valid(room_id, start_date, modul_id),
    ]
    for chk in checks:
        if not chk['ok']:
            return chk  # gibt den ersten Fehler zurück

    # Kurs anlegen
    kurs         = KursModell.Kurs()
    kurs.name    = modul['name']
    kurs.modul   = modul_id
    kurs.trainer = trainer
    kurs.gruppe  = group
    kurs.start   = start_date
    kurs.end     = end_date
    kurs.raum    = raum['name']

    SQL_Kurs.insert_Kurs(kurs)

    # Raum-Kalender in DB aktualisieren
    base_cal = raum_calendar.createCal()
    day_keys = [k for k, v in base_cal.items() if start_date <= v <= end_date]
    SQL_Raum.add_absence(room_id, day_keys)

    return {
        "ok":     True,
        "reason": (f"Kurs '{modul['name']}' erfolgreich gebucht: "
                   f"{start_date} – {end_date}, "
                   f"Trainer: {trainer['nachname']}, Raum: {raum['name']}"),
        "warning": checks[0].get("warning", ""),   # optionale Vorgänger-Warnung
    }