"""
Schulkalender-Planer mit Google OR-Tools
BERUFSCHULSYSTEM MIT 3-ER BLÖCKEN (A, B, C)
TRAINER unterrichten EXTERN (nicht während Blockwochen)

Block-Rotation:
- Woche 1-2: Block A in Schule, Block B & C extern (Trainer unterrichtet sie)
- Woche 3-4: Block B in Schule, Block A & C extern (Trainer unterrichtet sie)
- Woche 5-6: Block C in Schule, Block A & B extern (Trainer unterrichtet sie)
"""

from datetime import date, timedelta
from ortools.sat.python import cp_model

# ============================================================================
# HESSISCHE FEIERTAGE
# ============================================================================

def get_hessian_holidays(school_year_start: date):
    """Gibt alle hessischen Feiertage für das Schuljahr zurück."""
    year = school_year_start.year
    next_year = year + 1

    holidays = [
        ("Neujahr", date(year, 1, 1), date(year, 1, 1)),
        ("Karfreitag", date(year, 4, 3), date(year, 4, 3)),
        ("Ostermontag", date(year, 4, 13), date(year, 4, 13)),
        ("Tag der Arbeit", date(year, 5, 1), date(year, 5, 1)),
        ("Christi Himmelfahrt", date(year, 5, 14), date(year, 5, 14)),
        ("Pfingstmontag", date(year, 5, 25), date(year, 5, 25)),
        ("Fronleichnam", date(year, 6, 4), date(year, 6, 4)),
        ("Tag der Deutschen Einheit", date(year, 10, 3), date(year, 10, 3)),
        ("Allerheiligen", date(year, 11, 1), date(year, 11, 1)),
        ("Buß- und Bettag", date(year, 11, 18), date(year, 11, 18)),
        ("Weihnachtstag 1", date(year, 12, 25), date(year, 12, 25)),
        ("Weihnachtstag 2", date(year, 12, 26), date(year, 12, 26)),
        ("Neujahr", date(next_year, 1, 1), date(next_year, 1, 1)),
    ]

    school_holidays = [
        ("Herbstferien", date(year, 10, 5), date(year, 10, 16)),
        ("Weihnachtsferien", date(year, 12, 21), date(year, 1, 8)),
        ("Winterferien", date(year + 1, 2, 1), date(year + 1, 2, 5)),
        ("Osterferien", date(year + 1, 3, 29), date(year + 1, 4, 16)),
        ("Pfingstferien", date(year + 1, 5, 24), date(year + 1, 6, 4)),
        ("Sommerferien", date(year + 1, 7, 19), date(year + 1, 8, 31)),
    ]

    return holidays + school_holidays

# ============================================================================
# DATEN
# ============================================================================

# TRAINER (externe Lehrkräfte)
TRAINERS = {
    "T001": {"name": "Herr Schmidt", "unavailable": [date(2026, 9, 7), date(2026, 9, 8)]},
    "T002": {"name": "Frau Müller", "unavailable": [date(2026, 10, 12)]},
    "T003": {"name": "Herr Weber", "unavailable": []},
}

# BLÖCKE (Schülergruppen: A, B, C)
BLOCKS = {
    "BlockA": {"name": "Block A", "weeks_in_school": 2, "weeks_rotation": 6},
    "BlockB": {"name": "Block B", "weeks_in_school": 2, "weeks_rotation": 6},
    "BlockC": {"name": "Block C", "weeks_in_school": 2, "weeks_rotation": 6},
}

# MODULE (Kurse / Fächer)
MODULES = {
    "M001": {"name": "Python Programmierung", "trainer": "T001", "days": 5},
    "M002": {"name": "Datenbanken", "trainer": "T002", "days": 3},
    "M003": {"name": "Web Development", "trainer": "T003", "days": 10},
    "M004": {"name": "Netzwerk", "trainer": "T001", "days": 4},
}

# KURSE = Trainer unterrichtet Modul für Block (außerhalb von deren Schulwochen)
COURSES = [
    {"module": "M001", "block": "BlockA"},  # Python für Block A (wenn A NICHT in Schule)
    {"module": "M001", "block": "BlockB"},  # Python für Block B (wenn B NICHT in Schule)
    {"module": "M001", "block": "BlockC"},  # Python für Block C (wenn C NICHT in Schule)
    {"module": "M002", "block": "BlockA"},  # Datenbanken für Block A
    {"module": "M003", "block": "BlockB"},  # Web Dev für Block B
    {"module": "M004", "block": "BlockC"},  # Netzwerk für Block C
]

# ============================================================================
# BLOCK-VERWALTUNG
# ============================================================================

def get_block_availability(block_id: str, day: int, school_year_start: date) -> dict:
    """
    Gibt an, welche Blöcke an einem bestimmten Tag in der Schule sind.

    Block-Rotation:
    - 2 Wochen in Schule
    - 4 Wochen extern (Trainer unterrichtet sie)
    - Insgesamt 6-Wochen-Zyklus

    Rückgabe:
    {
        "BlockA": True/False (ob in Schule),
        "BlockB": True/False,
        "BlockC": True/False,
    }
    """

    current_date = school_year_start + timedelta(days=day)
    week_of_year = (current_date - school_year_start).days // 7

    # Zyklus: 6 Wochen (jeder Block 2 Wochen in Schule)
    cycle_week = week_of_year % 6

    # Block-Zuweisung im 6-Wochen-Zyklus:
    # Woche 0-1: Block A in Schule (B & C extern)
    # Woche 2-3: Block B in Schule (A & C extern)
    # Woche 4-5: Block C in Schule (A & B extern)

    return {
        "BlockA": cycle_week < 2,      # Woche 0-1
        "BlockB": 2 <= cycle_week < 4,  # Woche 2-3
        "BlockC": 4 <= cycle_week < 6,  # Woche 4-5
    }

# ============================================================================
# SCHEDULING
# ============================================================================

def create_schedule():
    """Erstellt einen Stundenplan mit Tages-Blöcken"""

    school_year_start = date(2026, 9, 1)
    school_year_end = date(2027, 8, 31)

    num_days = (school_year_end - school_year_start).days + 1

    # Ferien/Feiertage sammeln
    all_holidays = get_hessian_holidays(school_year_start)
    holiday_dates = set()

    for name, start, end in all_holidays:
        current = start
        while current <= end:
            if school_year_start <= current <= school_year_end:
                holiday_dates.add(current)
            current += timedelta(days=1)

    # Verfügbare Arbeitstage (Mo-Fr, keine Ferien/Feiertage)
    available_days = []
    for day in range(num_days):
        current_date = school_year_start + timedelta(days=day)
        if current_date.weekday() < 5 and current_date not in holiday_dates:
            available_days.append(day)

    print(f"📅 Schuljahr: {school_year_start} bis {school_year_end}")
    print(f"📅 Verfügbare Arbeitstage: {len(available_days)} Tage")
    print()

    # ========================================================================
    # MODELL ERSTELLEN
    # ========================================================================

    model = cp_model.CpModel()

    # Variablen: course_start[course_id][day]
    course_start = {}
    for course_idx, course in enumerate(COURSES):
        course_start[course_idx] = {}
        for day in available_days:
            var = model.NewBoolVar(f"course_{course_idx}_start_day_{day}")
            course_start[course_idx][day] = var

    # ========================================================================
    # CONSTRAINTS
    # ========================================================================

    # Constraint 1: Jeder Kurs startet genau einmal
    for course_idx in range(len(COURSES)):
        model.Add(sum(course_start[course_idx].values()) == 1)

    # Constraint 2: Kurs hat genug freie Tage nach Start
    for course_idx, course in enumerate(COURSES):
        module_id = course["module"]
        duration = MODULES[module_id]["days"]

        for day_idx, day in enumerate(available_days):
            if day_idx + duration > len(available_days):
                model.Add(course_start[course_idx][day] == 0)

    # Constraint 3: WICHTIG! Kurs kann NUR stattfinden, wenn Block NICHT in Schule ist
    # (Block ist extern, wird vom Trainer unterrichtet)
    for course_idx, course in enumerate(COURSES):
        block_id = course["block"]
        module_id = course["module"]
        duration = MODULES[module_id]["days"]

        for start_day_idx, start_day in enumerate(available_days):
            end_day_idx = start_day_idx + duration - 1

            if end_day_idx < len(available_days):
                # Alle Tage des Kurses prüfen
                course_days = available_days[start_day_idx:end_day_idx + 1]

                # Alle Tage müssen AUSSERHALB der Block-Schulzeit liegen
                valid = True
                for course_day in course_days:
                    block_status = get_block_availability(block_id, course_day, school_year_start)
                    if block_status[block_id]:  # Wenn Block in Schule ist -> NICHT erlaubt
                        valid = False
                        break

                if not valid:
                    model.Add(course_start[course_idx][start_day] == 0)

    # Constraint 4: Trainer unterrichtet nicht gleichzeitig 2 Kurse
    for trainer_id in TRAINERS:
        trainer_courses = [i for i, c in enumerate(COURSES) if MODULES[c["module"]]["trainer"] == trainer_id]

        if len(trainer_courses) > 1:
            for day in available_days:
                course_running = []

                for course_idx in trainer_courses:
                    module_id = COURSES[course_idx]["module"]
                    duration = MODULES[module_id]["days"]

                    day_in_course = model.NewBoolVar(f"t{trainer_id}_c{course_idx}_running_day_{day}")

                    possible_starts = []
                    for start_day_idx, start_day in enumerate(available_days):
                        end_day_idx = start_day_idx + duration - 1
                        if end_day_idx < len(available_days) and available_days[start_day_idx] <= day <= available_days[end_day_idx]:
                            possible_starts.append(course_start[course_idx][start_day])

                    if possible_starts:
                        model.Add(day_in_course == sum(possible_starts))
                        course_running.append(day_in_course)

                if course_running:
                    model.Add(sum(course_running) <= 1)

    # Constraint 5: Trainer nicht verfügbar an bestimmten Tagen
    for trainer_id in TRAINERS:
        trainer_courses = [i for i, c in enumerate(COURSES) if MODULES[c["module"]]["trainer"] == trainer_id]
        unavailable = TRAINERS[trainer_id]["unavailable"]

        for course_idx in trainer_courses:
            module_id = COURSES[course_idx]["module"]
            duration = MODULES[module_id]["days"]

            for start_day_idx, start_day in enumerate(available_days):
                end_day_idx = start_day_idx + duration - 1

                if end_day_idx < len(available_days):
                    course_days = available_days[start_day_idx:end_day_idx + 1]

                    conflict = False
                    for course_day in course_days:
                        current_date = school_year_start + timedelta(days=course_day)
                        if current_date in unavailable:
                            conflict = True
                            break

                    if conflict:
                        model.Add(course_start[course_idx][start_day] == 0)

    # ========================================================================
    # SOLVER
    # ========================================================================

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 30.0
    status = solver.Solve(model)

    if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        print("❌ Keine Lösung gefunden!")
        return None

    return solver, course_start, COURSES, school_year_start, available_days

# ============================================================================
# AUSGABE
# ============================================================================

def print_schedule(solver, course_start, courses, school_year_start, available_days):
    """Gibt den erstellten Stundenplan aus"""

    print("\n" + "="*140)
    print("📅 SCHULSTUNDENPLAN MIT BLOCK-ROTATION")
    print("   (TRAINER unterrichten Blöcke, die NICHT in der Schule sind)")
    print("="*140)

    # Finde Start-Tag für jeden Kurs
    course_schedule = {}
    for course_idx in range(len(courses)):
        for day in available_days:
            if solver.Value(course_start[course_idx][day]) == 1:
                course = courses[course_idx]
                module_id = course["module"]
                duration = MODULES[module_id]["days"]
                trainer_id = MODULES[module_id]["trainer"]

                course_schedule[course_idx] = {
                    "start_day": day,
                    "duration": duration,
                    "module": MODULES[module_id]["name"],
                    "trainer": TRAINERS[trainer_id]["name"],
                    "block": BLOCKS[course["block"]]["name"],
                }

    # Erstelle Kalender
    calendar = {}
    for day in available_days:
        calendar[day] = []

    for course_idx, schedule in course_schedule.items():
        start_day = schedule["start_day"]
        duration = schedule["duration"]

        start_idx = available_days.index(start_day)

        for i in range(duration):
            if start_idx + i < len(available_days):
                day = available_days[start_idx + i]
                calendar[day].append({
                    "course": course_idx,
                    "module": schedule["module"],
                    "trainer": schedule["trainer"],
                    "block": schedule["block"],
                })

    # Ausgabe (erste 12 Wochen)
    for day_idx, day in enumerate(available_days[:60]):
        current_date = school_year_start + timedelta(days=day)
        week_num = (current_date - school_year_start).days // 7 + 1

        # Block-Status anzeigen
        block_status = get_block_availability(day, current_date, school_year_start)
        in_school = [b for b, status in block_status.items() if status]
        extern = [b for b, status in block_status.items() if not status]

        print(f"\n📆 Woche {week_num:2d} | {current_date.strftime('%a, %d.%m.%Y')}", end="")
        print(f" | 🏫 Schule: {', '.join(in_school):20} | 🏭 Extern: {', '.join(extern)}", end="")

        if calendar[day]:
            print()
            for event in calendar[day]:
                print(f"      ✅ {event['block']:10} | {event['module']:25} | {event['trainer']}")
        else:
            print(" | ⚪ FREI")

    print("\n" + "="*140)
    print("\n📊 KURSZUSAMMENFASSUNG (EXTERN-UNTERRICHT):")
    for course_idx, schedule in sorted(course_schedule.items()):
        start_date = school_year_start + timedelta(days=schedule["start_day"])
        end_date = start_date + timedelta(days=schedule["duration"] - 1)
        print(f"   {schedule['module']:25} | {schedule['block']:10} | {start_date} - {end_date} ({schedule['duration']} Tage) | {schedule['trainer']}")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("🏫 Starte Schulkalender-Planer (Externe Trainer)")
    print("🔄 Block-Zyklus: 2 Wochen Schule, 4 Wochen extern (TRAINER unterrichtet)")
    print()

    result = create_schedule()

    if result:
        solver, course_start, courses, school_year_start, available_days = result
        print_schedule(solver, course_start, courses, school_year_start, available_days)
        print("\n✅ Stundenplan erfolgreich erstellt!")
    else:
        print("\n⚠️ Es war nicht möglich, einen gültigen Stundenplan zu erstellen.")