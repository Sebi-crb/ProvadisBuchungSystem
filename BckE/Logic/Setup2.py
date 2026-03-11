"""
Setup.py – Automatische Kursbuchung für alle Gruppen und alle Module.

Fixes gegenüber alter Version:
  - Alle Gruppen und alle Module werden durchlaufen (kein vorzeitiges break)
  - dauer-Vergleich: String → int konvertiert
  - neededWeeks==2 Logik repariert (korrekte Indexnutzung, keine UnboundLocalError)
  - Raum wird passend zu PC-Kennzeichnung und Verfügbarkeit gewählt
  - Gruppen-Abwesenheiten werden korrekt aus der DB gelesen und berücksichtigt
  - Nach jeder Buchung werden Trainer-, Gruppen- und Raumkalender in der DB aktualisiert
"""

from datetime import timedelta

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
import sqlite3


# ── Stammdaten einmalig laden ─────────────────────────────────────────────────

con_moduls = cModule.get_Modules()       # {id: modul_dict}
groups     = dataGetter.get_Gruppen()    # [{id, name, block, azubis, attendedModules}]
trainers   = dataGetter.get_Trainers()   # [{id, nachname, vorname, abwesenheiten}]
räume      = dataGetter.get_Rooms()      # [{id, name, plätze, istPCRaum, abwesenheiten}]

# dauer als int speichern (in config_Module sind es Strings wie "5" oder "10")
modul_list = {mid: int(m['dauer']) for mid, m in con_moduls.items()}


# ── Hilfsfunktionen ───────────────────────────────────────────────────────────

def _parse_absence_raw(raw) -> list:
    """
    Konvertiert DB-Rohwert (tuple oder str) in eine sortierte int-Liste.
    Verarbeitet sowohl fetchone-Tuples ('1, 2, 3',) als auch einfache Strings.
    """
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
    """Frischer Trainer-Kalender (Abwesenheiten aus DB) als Wochenliste."""
    raw      = SQL_Trainer.get_Trainer_absence(trainer_id)
    absences = _parse_absence_raw(raw)
    cal      = trainer_calender.create_calendar_with_absence(absences)
    return trainer_calender.get_available_weeks(cal)


def get_gruppe_weeks(block: str, gruppe_id: int) -> list:
    """
    Azubi-Kalender einer Gruppe als Wochenliste.
    Berücksichtigt bereits gebuchte Wochen aus der DB (Abwesenheiten-Spalte).
    """
    # Abwesenheiten direkt aus der Gruppe-Tabelle lesen
    gruppe_rows = SQL_Gruppe.get_all()   # (id, Name, Block, Azubis, AttendedModules, Abwesenheiten)
    gruppe_absence = []
    for row in gruppe_rows:
        if row[0] == gruppe_id and row[5]:
            gruppe_absence = [int(x.strip()) for x in row[5].split(',') if x.strip()]
            break

    # Block-Kalender erstellen und gebuchte Tage entfernen
    base_cal = azubi_calendar.createAzubiCal(block)
    for day_idx in gruppe_absence:
        base_cal.pop(day_idx, None)
    return azubi_calendar.get_available_weeks(base_cal)


def get_room_weeks(room_id: int) -> list:
    """Raumkalender als Wochenliste (Abwesenheiten aus DB)."""
    raw      = SQL_Raum.get_room_absence(room_id)
    absences = _parse_absence_raw(raw)
    cal      = raum_calendar.create_calendar_with_absence(absences)
    return raum_calendar.get_available_weeks(cal)


def find_first_match(needed_weeks: int, trainer_weeks: list, azubi_weeks: list):
    """
    Liefert das früheste Zeitfenster, in dem Trainer UND Gruppe gleichzeitig frei sind.

    Rückgabe: {"start": {"day": ..., "date": ...}, "end": {"day": ..., "endDate": ...}}
    oder None wenn kein Slot gefunden.
    """
    # Azubi-Verfügbarkeit als Set für schnelle Suche (nach Startdatum)
    azubi_by_date = {w['start']['date']: w for w in azubi_weeks}

    for i, tw in enumerate(trainer_weeks):
        tw_start_date = tw['start']['date']

        if needed_weeks == 1:
            # Einfacher 1-Wochen-Match: Startdaten müssen übereinstimmen
            if tw_start_date in azubi_by_date:
                return {
                    "start": tw['start'],
                    "end":   tw['end'],
                }

        elif needed_weeks == 2:
            # 2-Wochen-Match: Trainer braucht 2 aufeinanderfolgende freie Wochen,
            # Gruppe muss in beiden Wochen ebenfalls frei sein.
            if i + 1 >= len(trainer_weeks):
                continue

            next_tw = trainer_weeks[i + 1]

            # Sind die beiden Trainer-Wochen wirklich aufeinanderfolgend (genau 7 Tage)?
            diff_trainer = (next_tw['start']['date'] - tw_start_date).days
            if diff_trainer != 7:
                continue

            # Gruppe frei in Woche 1?
            if tw_start_date not in azubi_by_date:
                continue

            # Gruppe frei in Woche 2?
            week2_start = tw_start_date + timedelta(days=7)
            if week2_start not in azubi_by_date:
                continue

            return {
                "start": tw['start'],
                "end":   next_tw['end'],
            }

    return None


def find_available_room(match: dict, modul_pc: bool, needed_weeks: int):
    """
    Sucht den ersten verfügbaren Raum, der:
      - die PC-Anforderung des Moduls erfüllt
      - in der gebuchten Woche(n) frei ist
    Gibt das Raum-Dict zurück oder None.
    """
    start_date = match['start']['date']
    week2_date = start_date + timedelta(days=7)

    for raum in räume:
        # PC-Filter: IstPcRaum ist als '1'/'0' in der DB gespeichert
        raum_pc = str(raum['istPCRaum']).strip() == '1'
        if modul_pc != raum_pc:
            continue

        # Raumverfügbarkeit prüfen
        room_weeks       = get_room_weeks(raum['id'])
        avail_start_dates = {w['start']['date'] for w in room_weeks}

        if needed_weeks == 1:
            if start_date in avail_start_dates:
                return raum
        else:
            # Beide Wochen müssen frei sein
            if start_date in avail_start_dates and week2_date in avail_start_dates:
                return raum

    return None


def book_room_in_db(room_id: int, start_date, end_date):
    """Markiert die Tage des gebuchten Zeitraums im Raumkalender als belegt."""
    base_cal = raum_calendar.createCal()
    day_keys = [k for k, v in base_cal.items() if start_date <= v <= end_date]
    SQL_Raum.add_absence(room_id, day_keys)


# ── Hauptfunktion ─────────────────────────────────────────────────────────────

def book_all_courses():
    """
    Iteriert über alle Gruppen × alle Module und bucht automatisch Kurse.
    Trainer- und Gruppenkalender werden nach jeder Buchung aktualisiert.
    """
    total_booked  = 0
    total_skipped = 0

    for group in groups:
        group_id    = group['id']
        group_name  = group['name']
        group_block = group['block']

        # Bereits absolvierte Module dieser Gruppe überspringen
        already_done = set()
        for m in group.get('attendedModules', []):
            if str(m).strip().isdigit():
                already_done.add(int(m))

        print(f"\n📋 Gruppe {group_name} (Block {group_block})")

        for modul_id, dauer in modul_list.items():

            if modul_id in already_done:
                print(f"   ⏭  {cModule.get_name(modul_id):30} – bereits absolviert")
                continue

            needed_weeks = 1 if dauer <= 5 else 2
            modul_pc     = con_moduls[modul_id]['pcKennzeichnung']
            modul_name   = cModule.get_name(modul_id)

            booked = False

            for trainer in trainers:
                trainer_id = trainer['id']

                # Frische Kalender aus DB (nach jeder Buchung aktualisiert)
                trainer_weeks = get_trainer_weeks(trainer_id)
                azubi_weeks   = get_gruppe_weeks(group_block, group_id)

                match = find_first_match(needed_weeks, trainer_weeks, azubi_weeks)
                if match is None:
                    # Dieser Trainer hat keinen freien Slot mit der Gruppe → nächsten versuchen
                    continue

                # Passenden Raum suchen
                raum = find_available_room(match, modul_pc, needed_weeks)
                if raum is None:
                    print(f"   ⚠️  {modul_name:30} – kein passender Raum (Trainer: {trainer['nachname']})")
                    continue

                # Kurs anlegen und in DB schreiben
                # (insert_Kurs aktualisiert automatisch Trainer- und Gruppenkalender)
                kurs         = KursModell.Kurs()
                kurs.name    = modul_name
                kurs.modul   = modul_id
                kurs.trainer = trainer
                kurs.gruppe  = group
                kurs.start   = match['start']['date']
                kurs.end     = match['end']['endDate']
                kurs.raum    = raum['name']

                SQL_Kurs.insert_Kurs(kurs)
                book_room_in_db(raum['id'], kurs.start, kurs.end)

                print(
                    f"   ✅ {modul_name:30} | {str(kurs.start)} – {str(kurs.end)}"
                    f" | {trainer['nachname']:15} | {raum['name']}"
                )
                total_booked += 1
                booked = True
                break  # Ersten passenden Trainer nehmen und weiter zum nächsten Modul

            if not booked:
                print(f"   ❌ {modul_name:30} – kein freier Slot gefunden")
                total_skipped += 1

    print(f"\n{'=' * 65}")
    print(f"  ✅ Erfolgreich gebucht : {total_booked}")
    print(f"  ❌ Kein Slot gefunden  : {total_skipped}")
    print(f"{'=' * 65}")


# ── Einstiegspunkt ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    book_all_courses()