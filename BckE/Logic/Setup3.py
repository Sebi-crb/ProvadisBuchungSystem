"""
Setup.py – Automatische Kursbuchung für alle Gruppen und alle Module.

Constraints:
  1. Trainer + Gruppe müssen gleichzeitig frei sein
  2. Raum muss zur PC-Kennzeichnung des Moduls passen und frei sein
  3. Lehrjahr: Gruppe darf nur Module ihres aktuellen Lehrjahrs erhalten
  4. 6-Wochen-Regel: Nach 6 aufeinanderfolgenden Unterrichtswochen
     müssen für die Gruppe mindestens 2 Wochen ohne Kurs folgen
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


# ── Stammdaten einmalig laden ─────────────────────────────────────────────────

con_moduls = cModule.get_Modules()
groups     = dataGetter.get_Gruppen()
trainers   = dataGetter.get_Trainers()
raeume     = dataGetter.get_Rooms()

# dauer als int (Werte in config_Module sind Strings wie "5" oder "10")
modul_list = {mid: int(m['dauer']) for mid, m in con_moduls.items()}

# In-Memory-Tracker: gruppe_id -> set der gebuchten Wochen-Startdaten (date)
_group_booked_weeks: dict = {}


# ─────────────────────────────────────────────────────────────────────────────
# Lehrjahr-Logik
# ─────────────────────────────────────────────────────────────────────────────

def _get_lernjahr_from_group_name(group_name: str):
    """
    Leitet das aktuelle Lehrjahr einer Gruppe aus dem Gruppenname ab.
      '25FA01'  ->  Startjahr 2025  ->  Lehrjahr 1 im Schuljahr 2025/26
      '24FA01'  ->  Startjahr 2024  ->  Lehrjahr 2
      '23FA01'  ->  Startjahr 2023  ->  Lehrjahr 3
    Gibt None zurück wenn nicht ermittelbar.
    """
    try:
        short_year = int(group_name[:2])      # '25' -> 25
        start_year = 2000 + short_year         # -> 2025
        now        = datetime.now()
        # Schuljahr beginnt im September; ab August zählt das neue Schuljahr
        if now.month >= 8:
            schuljahr_start = now.year
        else:
            schuljahr_start = now.year - 1
        lehrjahr = schuljahr_start - start_year + 1
        return lehrjahr if 1 <= lehrjahr <= 3 else None
    except (ValueError, IndexError):
        return None


def _get_modul_lernjahr(modul: dict):
    """
    Gibt das Lehrjahr eines Moduls als int zurück.
    Behandelt fehlerhafte Werte (z.B. dict statt str) robust -> None.
    """
    raw = modul.get('zuordnungLernjahr')
    if isinstance(raw, str) and raw.strip().isdigit():
        return int(raw.strip())
    if isinstance(raw, int):
        return raw
    return None   # fehlerhafter Wert (z.B. Modul 4 hat ein dict)


def _modul_passt_zu_gruppe(modul: dict, gruppe_lj) -> bool:
    """True wenn das Modul dem Lehrjahr der Gruppe entspricht."""
    if gruppe_lj is None:
        return False
    modul_lj = _get_modul_lernjahr(modul)
    return modul_lj == gruppe_lj


# ─────────────────────────────────────────────────────────────────────────────
# 6-Wochen-Regel
# ─────────────────────────────────────────────────────────────────────────────

def _init_group_booked_weeks(group_id: int, group_block: str) -> set:
    """
    Liest die bereits in der DB eingetragenen Abwesenheiten einer Gruppe
    und leitet daraus die bisher gebuchten Wochen-Startdaten ab.
    Wird einmalig pro Gruppe beim ersten Zugriff aufgerufen.
    """
    booked_starts = set()
    for row in SQL_Gruppe.get_all():
        if row[0] != group_id or not row[5]:
            continue
        absence_indices = {int(x.strip()) for x in row[5].split(',') if x.strip()}
        # Basiskalender: alle Schultage mit ihrem Index
        all_cal = azubi_calendar.createCal()
        for idx, d in all_cal.items():
            end_idx = idx + 4
            end_d   = all_cal.get(end_idx)
            if end_d and (end_d - d).days == 4:
                # Vollständige Woche - als gebucht markieren wenn mind. 1 Tag belegt
                if any(i in absence_indices for i in range(idx, idx + 5)):
                    booked_starts.add(d)
    return booked_starts


def _is_valid_6week_rule(booked_starts: set, week_start: date, needed_weeks: int) -> bool:
    """
    Gibt False zurück wenn das Buchen von 'needed_weeks' Wochen ab 'week_start'
    die 6-Wochen-Regel verletzen würde.

    Regel: Nach 6 aufeinanderfolgenden Unterrichtswochen >= 2 Wochen Pause.
    """
    for i in range(needed_weeks):
        w = week_start + timedelta(days=7 * i)

        # Check 1: Wäre w die 7. oder spätere Woche in Folge?
        consecutive_before = 0
        prev = w - timedelta(days=7)
        while prev in booked_starts:
            consecutive_before += 1
            prev -= timedelta(days=7)
        if consecutive_before >= 6:
            return False

        # Check 2: Liegt w in einer erzwungenen Pause nach einem 6er-Block?
        # gap=1 -> w ist direkt nach dem Block; gap=2 -> w ist 2 Wochen danach
        for gap in [1, 2]:
            run_end = w - timedelta(days=7 * gap)
            if run_end not in booked_starts:
                continue
            # Länge des Blocks messen, der bei run_end endet
            run_len = 0
            c = run_end
            while c in booked_starts:
                run_len += 1
                c -= timedelta(days=7)
            if run_len >= 6:
                # Alle Wochen zwischen run_end und w müssen frei sein
                between_free = all(
                    (run_end + timedelta(days=7 * g)) not in booked_starts
                    for g in range(1, gap)
                )
                if between_free:
                    return False   # w liegt in der Pflichtpause

    return True


def _mark_group_booked(group_id: int, week_start: date, needed_weeks: int):
    """Trägt gebuchte Wochen in den In-Memory-Tracker ein."""
    booked = _group_booked_weeks.setdefault(group_id, set())
    for i in range(needed_weeks):
        booked.add(week_start + timedelta(days=7 * i))


# ─────────────────────────────────────────────────────────────────────────────
# Kalender-Hilfsfunktionen
# ─────────────────────────────────────────────────────────────────────────────

def _parse_absence_raw(raw) -> list:
    """Konvertiert DB-Rohwert (tuple oder str) in sortierte int-Liste."""
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


def get_trainer_weeks(trainer_id: int) -> list:
    raw      = SQL_Trainer.get_Trainer_absence(trainer_id)
    absences = _parse_absence_raw(raw)
    cal      = trainer_calender.create_calendar_with_absence(absences)
    return trainer_calender.get_available_weeks(cal)


def get_gruppe_weeks(block: str, gruppe_id: int) -> list:
    """Freie Wochen einer Gruppe (Blockkalender minus DB-Abwesenheiten)."""
    gruppe_absence = []
    for row in SQL_Gruppe.get_all():
        if row[0] == gruppe_id and row[5]:
            gruppe_absence = [int(x.strip()) for x in row[5].split(',') if x.strip()]
            break
    base_cal = azubi_calendar.createAzubiCal(block)
    for day_idx in gruppe_absence:
        base_cal.pop(day_idx, None)
    return azubi_calendar.get_available_weeks(base_cal)


def get_room_weeks(room_id: int) -> list:
    raw      = SQL_Raum.get_room_absence(room_id)
    absences = _parse_absence_raw(raw)
    cal      = raum_calendar.create_calendar_with_absence(absences)
    return raum_calendar.get_available_weeks(cal)


def book_room_in_db(room_id: int, start_date: date, end_date: date):
    base_cal = raum_calendar.createCal()
    day_keys = [k for k, v in base_cal.items() if start_date <= v <= end_date]
    SQL_Raum.add_absence(room_id, day_keys)


# ─────────────────────────────────────────────────────────────────────────────
# Matching
# ─────────────────────────────────────────────────────────────────────────────

def find_first_match(needed_weeks: int,
                     trainer_weeks: list,
                     azubi_weeks: list,
                     group_id: int):
    """
    Gibt den frühesten Slot zurück, in dem Trainer und Gruppe gleichzeitig
    frei sind und die 6-Wochen-Regel eingehalten wird.
    Gibt None zurück wenn kein passender Slot existiert.
    """
    azubi_by_date = {w['start']['date']: w for w in azubi_weeks}
    booked        = _group_booked_weeks.get(group_id, set())

    for i, tw in enumerate(trainer_weeks):
        tw_start = tw['start']['date']

        if needed_weeks == 1:
            if tw_start not in azubi_by_date:
                continue
            if not _is_valid_6week_rule(booked, tw_start, 1):
                continue
            return {"start": tw['start'], "end": tw['end']}

        elif needed_weeks == 2:
            if i + 1 >= len(trainer_weeks):
                continue
            next_tw = trainer_weeks[i + 1]
            # Trainer braucht 2 direkt aufeinanderfolgende freie Wochen
            if (next_tw['start']['date'] - tw_start).days != 7:
                continue
            # Gruppe muss in beiden Wochen frei sein
            week2_start = tw_start + timedelta(days=7)
            if tw_start not in azubi_by_date or week2_start not in azubi_by_date:
                continue
            if not _is_valid_6week_rule(booked, tw_start, 2):
                continue
            return {"start": tw['start'], "end": next_tw['end']}

    return None


def find_available_room(match: dict, modul_pc: bool, needed_weeks: int):
    """Ersten freien Raum mit passender PC-Kennzeichnung zurückgeben."""
    start_date  = match['start']['date']
    week2_date  = start_date + timedelta(days=7)

    for raum in raeume:
        raum_pc = str(raum['istPCRaum']).strip() == '1'
        if modul_pc != raum_pc:
            continue
        room_avail = {w['start']['date'] for w in get_room_weeks(raum['id'])}
        if needed_weeks == 1 and start_date in room_avail:
            return raum
        if needed_weeks == 2 and start_date in room_avail and week2_date in room_avail:
            return raum

    return None


# ─────────────────────────────────────────────────────────────────────────────
# Hauptfunktion
# ─────────────────────────────────────────────────────────────────────────────

def book_all_courses():
    total_booked  = 0
    total_skipped = 0

    for group in groups:
        group_id    = group['id']
        group_name  = group['name']
        group_block = group['block']

        # Lehrjahr der Gruppe ermitteln
        gruppe_lj = _get_lernjahr_from_group_name(group_name)
        if gruppe_lj is None:
            print(f"\n⚠️  Gruppe {group_name}: Lehrjahr nicht ermittelbar – übersprungen")
            continue

        # Bereits gebuchte Wochen aus DB in Memory-Tracker laden (einmalig)
        if group_id not in _group_booked_weeks:
            _group_booked_weeks[group_id] = _init_group_booked_weeks(group_id, group_block)

        # Bereits absolvierte Module dieser Gruppe
        already_done = set()
        for m in group.get('attendedModules', []):
            if str(m).strip().isdigit():
                already_done.add(int(m))

        print(f"\n{'─'*70}")
        print(f"📋 Gruppe {group_name}  |  Block {group_block}  |  Lehrjahr {gruppe_lj}")

        for modul_id, dauer in modul_list.items():
            modul      = con_moduls[modul_id]
            modul_name = modul['name']

            # Filter 1: bereits absolviert
            if modul_id in already_done:
                print(f"   ⏭  {modul_name:45} – bereits absolviert")
                continue

            # Filter 2: Lehrjahr
            if not _modul_passt_zu_gruppe(modul, gruppe_lj):
                modul_lj_display = _get_modul_lernjahr(modul) or '?'
                print(f"   ⏭  {modul_name:45} – Lehrjahr {modul_lj_display} ≠ {gruppe_lj}")
                continue

            needed_weeks = 1 if dauer <= 5 else 2
            modul_pc     = modul['pcKennzeichnung']
            booked_ok    = False

            for trainer in trainers:
                trainer_id    = trainer['id']
                trainer_weeks = get_trainer_weeks(trainer_id)
                azubi_weeks   = get_gruppe_weeks(group_block, group_id)

                match = find_first_match(needed_weeks, trainer_weeks, azubi_weeks, group_id)
                if match is None:
                    continue   # Trainer hat keinen gemeinsamen freien Slot

                raum = find_available_room(match, modul_pc, needed_weeks)
                if raum is None:
                    print(f"   ⚠️  {modul_name:45} – kein Raum (Trainer: {trainer['nachname']})")
                    continue

                # Kurs anlegen
                kurs         = KursModell.Kurs()
                kurs.name    = modul_name
                kurs.modul   = modul_id
                kurs.trainer = trainer
                kurs.gruppe  = group
                kurs.start   = match['start']['date']
                kurs.end     = match['end']['endDate']
                kurs.raum    = raum['name']

                # DB-Buchung (aktualisiert Trainer- & Gruppenkalender intern)
                SQL_Kurs.insert_Kurs(kurs)
                book_room_in_db(raum['id'], kurs.start, kurs.end)

                # 6-Wochen-Tracker aktualisieren
                _mark_group_booked(group_id, match['start']['date'], needed_weeks)

                print(
                    f"   ✅ {modul_name:45} | {str(kurs.start)} – {str(kurs.end)}"
                    f" | {trainer['nachname']:15} | {raum['name']}"
                )
                total_booked += 1
                booked_ok = True
                break   # Ersten passenden Trainer nehmen, weiter zum nächsten Modul

            if not booked_ok:
                print(f"   ❌ {modul_name:45} – kein freier Slot gefunden")
                total_skipped += 1

    print(f"\n{'=' * 70}")
    print(f"  ✅ Erfolgreich gebucht : {total_booked}")
    print(f"  ❌ Kein Slot gefunden  : {total_skipped}")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    book_all_courses()