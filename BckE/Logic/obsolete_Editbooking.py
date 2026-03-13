"""
EditBooking.py – Bestehende Kurse bearbeiten.

Funktionen:
  get_all_possible_slots()   → alle möglichen Termine für einen Kurs (Gruppe + Modul)
  change_trainer()           → Trainer eines Kurses ersetzen
  change_room()              → Raum eines Kurses ersetzen
  change_timeframe()         → Zeitraum eines Kurses verschieben
                               (verschiebt gleichzeitig Trainer + Raum)

Jede Änderungsfunktion:
  1. Validiert die neue Auswahl
  2. Gibt _fail() zurück wenn nicht möglich
  3. Schreibt bei Erfolg in die DB und gibt _ok() zurück
  4. Rollt den alten Slot im Kalender frei, bucht den neuen
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

# ── Stammdaten ────────────────────────────────────────────────────────────────

con_moduls   = cModule.get_Modules()
all_groups   = dataGetter.get_Gruppen()
all_trainers = dataGetter.get_Trainers()
all_rooms    = dataGetter.get_Rooms()


# ─────────────────────────────────────────────────────────────────────────────
# Interne Hilfsfunktionen
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


def _get_trainer_calendar(trainer_id: int) -> dict:
    raw      = SQL_Trainer.get_Trainer_absence(trainer_id)
    absences = _parse_absence_raw(raw)
    return trainer_calender.create_calendar_with_absence(absences)


def _get_room_calendar(room_id: int) -> dict:
    raw      = SQL_Raum.get_room_absence(room_id)
    absences = _parse_absence_raw(raw)
    return raum_calendar.create_calendar_with_absence(absences)


def _get_gruppe_calendar(block: str, gruppe_id: int) -> dict:
    """Azubi-Kalender der Gruppe minus bereits gebuchte Tage."""
    gruppe_absence = []
    for row in SQL_Gruppe.get_all():
        if row[0] == gruppe_id and row[5]:
            gruppe_absence = [int(x.strip()) for x in row[5].split(',') if x.strip()]
            break
    cal = azubi_calendar.createAzubiCal(block)
    for idx in gruppe_absence:
        cal.pop(idx, None)
    return cal


def _cal_contains_full_slot(cal: dict, start_date: date, needed_weeks: int) -> bool:
    """
    True wenn der Kalender alle Arbeitstage des Zeitraums (start_date +
    needed_weeks Wochen Mo–Fr) enthält.
    """
    date_set = set(cal.values())
    for w in range(needed_weeks):
        week_monday = start_date + timedelta(days=7 * w)
        for d in range(5):
            if (week_monday + timedelta(days=d)) not in date_set:
                return False
    return True


def _get_key_for_date(cal: dict, target_date: date):
    """Gibt den Index-Schlüssel eines Datums im Kalender zurück."""
    for key, val in cal.items():
        if val == target_date:
            return key
    return None


def _get_group_booked_week_starts(gruppe_id: int, block: str,
                                   exclude_kurs_id: int = None) -> set:
    """
    Alle gebuchten Wochen-Startdaten einer Gruppe.
    exclude_kurs_id: Den aktuell bearbeiteten Kurs herausrechnen,
                     damit sein Zeitraum als 'frei' gilt.
    """
    booked_starts = set()

    # Gebuchte Daten des auszuschließenden Kurses ermitteln
    exclude_dates = set()
    if exclude_kurs_id is not None:
        kurs_row = SQL_Kurs.get_Kurs(exclude_kurs_id)
        if kurs_row:
            try:
                ex_start = date.fromisoformat(str(kurs_row[3]))
                ex_end   = date.fromisoformat(str(kurs_row[4]))
                d = ex_start
                while d <= ex_end:
                    exclude_dates.add(d)
                    d += timedelta(days=1)
            except (ValueError, TypeError):
                pass

    for row in SQL_Gruppe.get_all():
        if row[0] != gruppe_id or not row[5]:
            continue
        absence_indices = {int(x.strip()) for x in row[5].split(',') if x.strip()}
        all_cal = azubi_calendar.createCal()
        for idx, d in all_cal.items():
            if d in exclude_dates:
                continue
            end_d = all_cal.get(idx + 4)
            if end_d and (end_d - d).days == 4:
                if any(i in absence_indices for i in range(idx, idx + 5)):
                    booked_starts.add(d)

    return booked_starts


def _check_6week_rule(booked_starts: set, week_start: date, needed_weeks: int) -> dict:
    for i in range(needed_weeks):
        w = week_start + timedelta(days=7 * i)
        consecutive = 0
        prev = w - timedelta(days=7)
        while prev in booked_starts:
            consecutive += 1
            prev -= timedelta(days=7)
        if consecutive >= 6:
            return _fail(
                f"6-Wochen-Regel: Woche ab {w} wäre die {consecutive + 1}. "
                f"Woche in Folge (max. 6 erlaubt)."
            )
        for gap in [1, 2]:
            run_end = w - timedelta(days=7 * gap)
            if run_end not in booked_starts:
                continue
            run_len, c = 0, run_end
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
                        f"6-Wochen-Regel: Woche ab {w} liegt in der "
                        f"Pflichtpause nach einem 6-Wochen-Block."
                    )
    return _ok()


def _free_slot_in_calendar(cal_module, free_func, entity_id: int,
                            start_date: date, end_date: date):
    """
    Gibt die Tages-Indizes des gebuchten Zeitraums frei (entfernt sie aus
    den Abwesenheiten). Wird beim Ändern von Trainer/Raum/Zeitraum verwendet.
    """
    base_cal = cal_module.createCal()
    day_keys = [k for k, v in base_cal.items() if start_date <= v <= end_date]
    free_func(entity_id, day_keys)


def _get_lernjahr_from_group_name(group_name: str):
    try:
        start_year = 2000 + int(group_name[:2])
        now = datetime.now()
        schuljahr_start = now.year if now.month >= 8 else now.year - 1
        lj = schuljahr_start - start_year + 1
        return lj if 1 <= lj <= 3 else None
    except (ValueError, IndexError):
        return None


def _resolve_kurs(kurs_id: int) -> tuple:
    """
    Gibt (kurs_row, group, modul, trainer, raum) zurück oder wirft ValueError.
    kurs_row: DB-Zeile (id, Name, GruppenID, StartDate, EndDate, TrainerID, Raum, ModulID)
    """
    kurs_row = SQL_Kurs.get_Kurs(kurs_id)
    if not kurs_row:
        raise ValueError(f"Kurs {kurs_id} nicht gefunden.")

    gruppe_id  = int(kurs_row[2])
    trainer_id = int(kurs_row[5])
    modul_id   = int(kurs_row[7])
    raum_name  = kurs_row[6]

    group   = next((g for g in all_groups   if g['id'] == gruppe_id),   None)
    trainer = next((t for t in all_trainers if t['id'] == trainer_id),  None)
    raum    = next((r for r in all_rooms    if r['name'] == raum_name),  None)
    modul   = con_moduls.get(modul_id)

    return kurs_row, group, modul, trainer, raum


# ─────────────────────────────────────────────────────────────────────────────
# ABFRAGE: Alle möglichen Termine für einen Kurs
# ─────────────────────────────────────────────────────────────────────────────

def get_all_possible_slots(kurs_id: int) -> list:
    """
    Gibt alle möglichen Zeiträume zurück, in denen der Kurs stattfinden könnte,
    basierend auf der Gruppe (Block-Kalender, 6-Wochen-Regel) – unabhängig von
    Trainer- und Raumverfügbarkeit.

    Das erlaubt dem Frontend zunächst einen Überblick aller Optionen zu zeigen,
    bevor Trainer und Raum gewählt werden.

    Rückgabe: Liste von Dicts:
      {
        "start":          date,     # Montag der ersten Woche
        "end":            date,     # Freitag der letzten Woche
        "weeks":          int,      # 1 oder 2
        "trainers_free":  list,     # Trainer die in diesem Slot frei sind
        "rooms_free":     list,     # passende Räume die frei sind
        "fully_bookable": bool      # True wenn mindestens 1 Trainer + 1 Raum frei
      }
    """
    try:
        kurs_row, group, modul, current_trainer, current_raum = _resolve_kurs(kurs_id)
    except ValueError as e:
        return []

    start_date_old = date.fromisoformat(str(kurs_row[3]))
    end_date_old   = date.fromisoformat(str(kurs_row[4]))
    dauer          = int(modul['dauer'])
    needed_weeks   = 1 if dauer <= 5 else 2
    modul_pc       = modul['pcKennzeichnung']
    block          = group['block']
    gruppe_id      = group['id']

    # Gruppe-Kalender: aktuellen Kurs als frei behandeln
    gruppe_absence_raw = []
    for row in SQL_Gruppe.get_all():
        if row[0] == gruppe_id and row[5]:
            gruppe_absence_raw = [int(x.strip()) for x in row[5].split(',') if x.strip()]
            break

    base_cal = azubi_calendar.createCal()
    # Indizes des aktuellen Kurses ermitteln und temporär freigeben
    old_indices = {k for k, v in base_cal.items()
                   if start_date_old <= v <= end_date_old}
    freie_absence = [i for i in gruppe_absence_raw if i not in old_indices]

    temp_cal = azubi_calendar.createAzubiCal(block)
    for idx in freie_absence:
        temp_cal.pop(idx, None)

    gruppe_weeks  = azubi_calendar.get_available_weeks(temp_cal)
    booked_starts = _get_group_booked_week_starts(gruppe_id, block,
                                                   exclude_kurs_id=kurs_id)

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

        # 6-Wochen-Regel
        if not _check_6week_rule(booked_starts, start, needed_weeks)['ok']:
            continue

        # Welche Trainer sind frei?
        trainers_free = []
        for t in all_trainers:
            t_cal = _get_trainer_calendar(t['id'])
            # Alten Slot temporär freigeben
            old_t_indices = {k for k, v in trainer_calender.createCal().items()
                             if start_date_old <= v <= end_date_old}
            for idx in old_t_indices:
                if t['id'] == (current_trainer['id'] if current_trainer else -1):
                    t_cal[idx] = trainer_calender.createCal().get(idx)
            if _cal_contains_full_slot(t_cal, start, needed_weeks):
                trainers_free.append({"id": t['id'], "name": t['nachname']})

        # Welche Räume sind frei und haben passende PC-Kennzeichnung?
        rooms_free = []
        for r in all_rooms:
            raum_pc = str(r['istPCRaum']).strip() == '1'
            if modul_pc != raum_pc:
                continue
            r_cal = _get_room_calendar(r['id'])
            # Alten Slot freigeben wenn es der aktuelle Raum ist
            if current_raum and r['id'] == current_raum['id']:
                old_r_base = raum_calendar.createCal()
                for idx in {k for k, v in old_r_base.items()
                            if start_date_old <= v <= end_date_old}:
                    r_cal[idx] = old_r_base.get(idx)
            if _cal_contains_full_slot(r_cal, start, needed_weeks):
                rooms_free.append({"id": r['id'], "name": r['name']})

        slots.append({
            "start":          start,
            "end":            end,
            "weeks":          needed_weeks,
            "trainers_free":  trainers_free,
            "rooms_free":     rooms_free,
            "fully_bookable": bool(trainers_free and rooms_free),
        })

    return slots


# ─────────────────────────────────────────────────────────────────────────────
# ÄNDERUNG: Trainer wechseln
# ─────────────────────────────────────────────────────────────────────────────

def change_trainer(kurs_id: int, new_trainer_id: int) -> dict:
    """
    Ersetzt den Trainer eines bestehenden Kurses.

    Prüft:
      - Existiert der neue Trainer?
      - Ist er im Zeitraum des Kurses verfügbar?

    Aktualisiert Trainer-Abwesenheiten in der DB (alt frei, neu belegt).
    """
    try:
        kurs_row, group, modul, old_trainer, raum = _resolve_kurs(kurs_id)
    except ValueError as e:
        return _fail(str(e))

    new_trainer = next((t for t in all_trainers if t['id'] == new_trainer_id), None)
    if not new_trainer:
        return _fail(f"Trainer mit ID {new_trainer_id} nicht gefunden.")

    if old_trainer and new_trainer_id == old_trainer['id']:
        return _fail("Das ist bereits der aktuelle Trainer.")

    start_date = date.fromisoformat(str(kurs_row[3]))
    end_date   = date.fromisoformat(str(kurs_row[4]))
    dauer      = int(modul['dauer'])
    needed_weeks = 1 if dauer <= 5 else 2

    # Neuen Trainer-Kalender prüfen (ohne seinen alten Kurs falls gleicher Trainer)
    new_t_cal = _get_trainer_calendar(new_trainer_id)
    if not _cal_contains_full_slot(new_t_cal, start_date, needed_weeks):
        return _fail(
            f"Trainer {new_trainer['nachname']} ist im Zeitraum "
            f"{start_date} – {end_date} nicht verfügbar."
        )

    # DB aktualisieren: alten Trainer-Slot freigeben
    if old_trainer:
        base_cal = trainer_calender.createCal()
        old_keys = [k for k, v in base_cal.items() if start_date <= v <= end_date]
        trainer_calender.remove_absence(old_keys,
            _get_trainer_calendar(old_trainer['id']))
        SQL_Trainer.change_absence(old_trainer['id'], old_keys)

    # Neuen Trainer blockieren
    SQL_Trainer.add_absence(new_trainer_id,
        [k for k, v in trainer_calender.createCal().items()
         if start_date <= v <= end_date])

    # Kurs-Eintrag aktualisieren
    import sqlite3
    from pathlib import Path
    proj_root = next(
        (p for p in Path(__file__).resolve().parents
         if p.name == "ProvadisBuchungSystem"), None
    )
    db_path = str(proj_root / "BckE" / "SQL" / "Main.db")
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "UPDATE Kurse SET TrainerID = ? WHERE id = ?",
            (new_trainer_id, kurs_id)
        )

    return _ok(
        f"Trainer erfolgreich geändert: "
        f"{old_trainer['nachname'] if old_trainer else '?'} → "
        f"{new_trainer['nachname']} "
        f"(Kurs '{kurs_row[1]}', {start_date} – {end_date})"
    )


# ─────────────────────────────────────────────────────────────────────────────
# ÄNDERUNG: Raum wechseln
# ─────────────────────────────────────────────────────────────────────────────

def change_room(kurs_id: int, new_room_id: int) -> dict:
    """
    Ersetzt den Raum eines bestehenden Kurses.

    Prüft:
      - Existiert der Raum?
      - Passt die PC-Kennzeichnung zum Modul?
      - Ist der Raum im Zeitraum frei?

    Aktualisiert Raum-Abwesenheiten in der DB.
    """
    try:
        kurs_row, group, modul, trainer, old_raum = _resolve_kurs(kurs_id)
    except ValueError as e:
        return _fail(str(e))

    new_raum = next((r for r in all_rooms if r['id'] == new_room_id), None)
    if not new_raum:
        return _fail(f"Raum mit ID {new_room_id} nicht gefunden.")

    if old_raum and new_room_id == old_raum['id']:
        return _fail("Das ist bereits der aktuelle Raum.")

    modul_pc = modul['pcKennzeichnung']
    raum_pc  = str(new_raum['istPCRaum']).strip() == '1'
    if modul_pc != raum_pc:
        benötigt = "PC-Raum" if modul_pc else "normalen Raum"
        return _fail(
            f"Modul '{modul['name']}' benötigt einen {benötigt}, "
            f"'{new_raum['name']}' passt nicht."
        )

    start_date   = date.fromisoformat(str(kurs_row[3]))
    end_date     = date.fromisoformat(str(kurs_row[4]))
    dauer        = int(modul['dauer'])
    needed_weeks = 1 if dauer <= 5 else 2

    new_room_cal = _get_room_calendar(new_room_id)
    if not _cal_contains_full_slot(new_room_cal, start_date, needed_weeks):
        return _fail(
            f"Raum '{new_raum['name']}' ist im Zeitraum "
            f"{start_date} – {end_date} bereits belegt."
        )

    # DB: alten Raum freigeben
    if old_raum:
        base_cal = raum_calendar.createCal()
        old_keys = [k for k, v in base_cal.items() if start_date <= v <= end_date]
        SQL_Raum.change_absence(old_raum['id'], old_keys)

    # Neuen Raum blockieren
    SQL_Raum.add_absence(new_room_id,
        [k for k, v in raum_calendar.createCal().items()
         if start_date <= v <= end_date])

    # Kurs-Eintrag aktualisieren
    import sqlite3
    from pathlib import Path
    proj_root = next(
        (p for p in Path(__file__).resolve().parents
         if p.name == "ProvadisBuchungSystem"), None
    )
    db_path = str(proj_root / "BckE" / "SQL" / "Main.db")
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "UPDATE Kurse SET Raum = ? WHERE id = ?",
            (new_raum['name'], kurs_id)
        )

    return _ok(
        f"Raum erfolgreich geändert: "
        f"{old_raum['name'] if old_raum else '?'} → {new_raum['name']} "
        f"(Kurs '{kurs_row[1]}', {start_date} – {end_date})"
    )


# ─────────────────────────────────────────────────────────────────────────────
# ÄNDERUNG: Zeitraum verschieben
# ─────────────────────────────────────────────────────────────────────────────

def change_timeframe(kurs_id: int,
                     new_start: date,
                     new_trainer_id: int = None,
                     new_room_id: int = None) -> dict:
    """
    Verschiebt einen bestehenden Kurs auf einen neuen Zeitraum.
    Trainer und Raum können optional gleichzeitig gewechselt werden,
    bleiben sonst dieselben (werden dann für den neuen Slot geprüft).

    Prüft:
      - Gruppe im neuen Zeitraum frei? (6-Wochen-Regel inklusive)
      - Trainer im neuen Zeitraum verfügbar?
      - Raum im neuen Zeitraum frei + passende PC-Kennzeichnung?

    Aktualisiert alle Kalender (Gruppe, Trainer, Raum) in der DB.
    """
    try:
        kurs_row, group, modul, old_trainer, old_raum = _resolve_kurs(kurs_id)
    except ValueError as e:
        return _fail(str(e))

    old_start    = date.fromisoformat(str(kurs_row[3]))
    old_end      = date.fromisoformat(str(kurs_row[4]))
    dauer        = int(modul['dauer'])
    needed_weeks = 1 if dauer <= 5 else 2
    modul_pc     = modul['pcKennzeichnung']
    new_end      = new_start + timedelta(days=needed_weeks * 7 - 3)

    # Trainer und Raum: falls nicht angegeben, alte übernehmen
    eff_trainer_id = new_trainer_id if new_trainer_id is not None else (
        old_trainer['id'] if old_trainer else None)
    eff_room_id    = new_room_id if new_room_id is not None else (
        old_raum['id'] if old_raum else None)

    eff_trainer = next((t for t in all_trainers if t['id'] == eff_trainer_id), None)
    eff_raum    = next((r for r in all_rooms    if r['id'] == eff_room_id),    None)

    if not eff_trainer:
        return _fail(f"Trainer mit ID {eff_trainer_id} nicht gefunden.")
    if not eff_raum:
        return _fail(f"Raum mit ID {eff_room_id} nicht gefunden.")

    # ── Gruppe prüfen ────────────────────────────────────────────────────────
    # Alten Kurs aus Abwesenheiten herausrechnen
    gruppe_absence_raw = []
    gruppe_id = group['id']
    for row in SQL_Gruppe.get_all():
        if row[0] == gruppe_id and row[5]:
            gruppe_absence_raw = [int(x.strip()) for x in row[5].split(',') if x.strip()]
            break

    base_cal   = azubi_calendar.createCal()
    old_g_keys = {k for k, v in base_cal.items() if old_start <= v <= old_end}
    temp_absence = [i for i in gruppe_absence_raw if i not in old_g_keys]

    temp_cal = azubi_calendar.createAzubiCal(group['block'])
    for idx in temp_absence:
        temp_cal.pop(idx, None)

    if not _cal_contains_full_slot(temp_cal, new_start, needed_weeks):
        return _fail(
            f"Gruppe '{group['name']}' hat im neuen Zeitraum "
            f"{new_start} – {new_end} bereits einen anderen Kurs."
        )

    booked_starts = _get_group_booked_week_starts(gruppe_id, group['block'],
                                                   exclude_kurs_id=kurs_id)
    rule_check = _check_6week_rule(booked_starts, new_start, needed_weeks)
    if not rule_check['ok']:
        return rule_check

    # ── Trainer prüfen ───────────────────────────────────────────────────────
    t_cal    = _get_trainer_calendar(eff_trainer_id)
    t_base   = trainer_calender.createCal()
    # Alten Slot des (evtl. selben) Trainers freigeben
    if old_trainer and eff_trainer_id == old_trainer['id']:
        for k, v in t_base.items():
            if old_start <= v <= old_end:
                t_cal[k] = v

    if not _cal_contains_full_slot(t_cal, new_start, needed_weeks):
        return _fail(
            f"Trainer {eff_trainer['nachname']} ist im neuen Zeitraum "
            f"{new_start} – {new_end} nicht verfügbar."
        )

    # ── Raum prüfen ──────────────────────────────────────────────────────────
    raum_pc = str(eff_raum['istPCRaum']).strip() == '1'
    if modul_pc != raum_pc:
        benötigt = "PC-Raum" if modul_pc else "normalen Raum"
        return _fail(
            f"Modul '{modul['name']}' benötigt einen {benötigt}, "
            f"'{eff_raum['name']}' passt nicht."
        )

    r_cal  = _get_room_calendar(eff_room_id)
    r_base = raum_calendar.createCal()
    if old_raum and eff_room_id == old_raum['id']:
        for k, v in r_base.items():
            if old_start <= v <= old_end:
                r_cal[k] = v

    if not _cal_contains_full_slot(r_cal, new_start, needed_weeks):
        return _fail(
            f"Raum '{eff_raum['name']}' ist im neuen Zeitraum "
            f"{new_start} – {new_end} bereits belegt."
        )

    # ── DB aktualisieren ─────────────────────────────────────────────────────

    # 1) Alte Kalendereinträge freigeben
    g_old_keys = [k for k, v in base_cal.items() if old_start <= v <= old_end]
    SQL_Gruppe.change_absence(gruppe_id, g_old_keys)   # alte Abwesenheiten entfernen

    if old_trainer:
        t_old_keys = [k for k, v in t_base.items() if old_start <= v <= old_end]
        SQL_Trainer.change_absence(old_trainer['id'], t_old_keys)

    if old_raum:
        r_old_keys = [k for k, v in r_base.items() if old_start <= v <= old_end]
        SQL_Raum.change_absence(old_raum['id'], r_old_keys)

    # 2) Neue Kalendereinträge setzen
    g_new_keys = [k for k, v in base_cal.items() if new_start <= v <= new_end]
    SQL_Gruppe.add_absence(gruppe_id, g_new_keys)

    t_new_keys = [k for k, v in t_base.items() if new_start <= v <= new_end]
    SQL_Trainer.add_absence(eff_trainer_id, t_new_keys)

    r_new_keys = [k for k, v in r_base.items() if new_start <= v <= new_end]
    SQL_Raum.add_absence(eff_room_id, r_new_keys)

    # 3) Kurs-Eintrag in DB aktualisieren
    SQL_Kurs.update_course_dates(kurs_id, new_start, new_end)

    import sqlite3
    from pathlib import Path
    proj_root = next(
        (p for p in Path(__file__).resolve().parents
         if p.name == "ProvadisBuchungSystem"), None
    )
    db_path = str(proj_root / "BckE" / "SQL" / "Main.db")
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "UPDATE Kurse SET TrainerID = ?, Raum = ? WHERE id = ?",
            (eff_trainer_id, eff_raum['name'], kurs_id)
        )

    trainer_info = (
        f"Trainer: {old_trainer['nachname']} → {eff_trainer['nachname']}"
        if old_trainer and eff_trainer_id != old_trainer['id']
        else f"Trainer: {eff_trainer['nachname']} (unverändert)"
    )
    raum_info = (
        f"Raum: {old_raum['name']} → {eff_raum['name']}"
        if old_raum and eff_room_id != old_raum['id']
        else f"Raum: {eff_raum['name']} (unverändert)"
    )

    return _ok(
        f"Kurs '{kurs_row[1]}' erfolgreich verschoben: "
        f"{old_start} – {old_end} → {new_start} – {new_end}. "
        f"{trainer_info}. {raum_info}."
    )