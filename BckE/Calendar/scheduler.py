"""
Minimalistischer Schulplaner
Nur das Nötigste!
"""
from datetime import date, timedelta
from ortools.sat.python import cp_model
import config


# ============================================================================
# HILFSFUNKTIONEN
# ============================================================================

def get_available_days():
    """Alle Arbeitstage (Mo-Fr, keine Ferien)"""
    all_holidays = set(config.HOLIDAYS)
    for start, end in config.HOLIDAY_RANGES:
        current = start
        while current <= end:
            all_holidays.add(current)
            current += timedelta(days=1)

    available = []
    current = config.SCHOOL_YEAR_START
    while current <= config.SCHOOL_YEAR_END:
        if current.weekday() < 5 and current not in all_holidays:
            available.append(current)
        current += timedelta(days=1)
    #print(available)
    return available


def is_block_in_school(block_id, check_date):
    """Ist Block an diesem Tag in der Schule?"""
    days = (check_date - config.SCHOOL_YEAR_START).days
    print(days)
    week = days // 7
    cycle_week = week % 6

    if block_id == "BlockA":
        return cycle_week < 2
    elif block_id == "BlockB":
        return 2 <= cycle_week < 4
    else:  # BlockC
        return 4 <= cycle_week < 6


# ============================================================================
# SCHEDULER
# ============================================================================

def create_schedule():
    """Erstelle Stundenplan"""

    available_days = get_available_days()
    print(f"📅 {len(available_days)} verfügbare Tage")

    # Erstelle Modell
    model = cp_model.CpModel()

    # Variablen: Wann startet jeder Kurs?
    course_vars = {}
    for i, course in enumerate(config.COURSES):
        course_vars[i] = {}
        for j, day in enumerate(available_days):
            course_vars[i][j] = (model.NewBoolVar(f"c{i}_d{j}"), day)

    # CONSTRAINT 1: Jeder Kurs startet genau 1x
    for i in range(len(config.COURSES)):
        model.Add(sum([course_vars[i][j][0] for j in range(len(available_days))]) == 1)

    # CONSTRAINT 2: Genug Tage?
    for i, course in enumerate(config.COURSES):
        module = config.MODULES[course["module"]]
        duration = module["days"]
        for j in range(len(available_days) - duration + 1, len(available_days)):
            model.Add(course_vars[i][j][0] == 0)

    # CONSTRAINT 3: Block muss extern sein (nicht in Schule)
    for i, course in enumerate(config.COURSES):
        module = config.MODULES[course["module"]]
        block = course["block"]
        duration = module["days"]

        for j, start_day in enumerate(available_days):
            # Prüfe alle Tage des Kurses
            valid = True
            for d in range(duration):
                if is_block_in_school(block, start_day + timedelta(days=d)):
                    valid = False
                    break

            if not valid:
                model.Add(course_vars[i][j][0] == 0)

    # CONSTRAINT 4: Trainer unterrichtet nicht 2 Kurse gleichzeitig
    for trainer_id in config.TRAINERS:
        trainer_courses = [i for i, c in enumerate(config.COURSES)
                           if config.MODULES[c["module"]]["trainer"] == trainer_id]

        if len(trainer_courses) <= 1:
            continue

        for j, day in enumerate(available_days):
            running = []
            for i in trainer_courses:
                module = config.MODULES[config.COURSES[i]["module"]]
                duration = module["days"]

                is_running = model.NewBoolVar(f"t{trainer_id}_c{i}_d{j}")

                constraints = []
                for k, start_day in enumerate(available_days):
                    end_day = start_day + timedelta(days=duration - 1)
                    if start_day <= day <= end_day:
                        constraints.append(course_vars[i][k][0])

                if constraints:
                    model.Add(is_running == sum(constraints))
                    running.append(is_running)

            if running:
                model.Add(sum(running) <= 1)

    # CONSTRAINT 5: Trainer-Urlaub
    for trainer_id in config.TRAINERS:
        unavailable = config.TRAINERS[trainer_id]["unavailable"]
        trainer_courses = [i for i, c in enumerate(config.COURSES)
                           if config.MODULES[c["module"]]["trainer"] == trainer_id]

        for i in trainer_courses:
            module = config.MODULES[config.COURSES[i]["module"]]
            duration = module["days"]

            for j, start_day in enumerate(available_days):
                has_conflict = any(
                    start_day + timedelta(days=d) in unavailable
                    for d in range(duration)
                )
                if has_conflict:
                    model.Add(course_vars[i][j][0] == 0)

    # Löse
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10
    status = solver.Solve(model)

    if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        print("❌ Keine Lösung gefunden!")
        return None

    return solver, course_vars, available_days


# ============================================================================
# AUSGABE
# ============================================================================

def print_schedule(solver, course_vars, available_days):
    """Gib Stundenplan aus"""

    print("\n" + "=" * 100)
    print("📅 STUNDENPLAN\n")

    # Finde Startdaten
    schedule = {}
    for i in range(len(config.COURSES)):
        for j in range(len(available_days)):
            if solver.Value(course_vars[i][j][0]) == 1:
                course = config.COURSES[i]
                module = config.MODULES[course["module"]]
                start = course_vars[i][j][1]
                end = start + timedelta(days=module["days"] - 1)
                trainer = config.TRAINERS[module["trainer"]]["name"]

                schedule[i] = {
                    "module": module["name"],
                    "block": course["block"],
                    "trainer": trainer,
                    "start": start,
                    "end": end,
                    "days": module["days"],
                }

    # Ausgabe
    for i in sorted(schedule.keys()):
        s = schedule[i]
        print(f"✅ {s['module']:20} | {s['block']:10} | {s['start']} - {s['end']} ({s['days']}d) | {s['trainer']}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("🏫 Schulplaner - Minimalist\n")
    result = create_schedule()
    if result:
        solver, course_vars, available_days = result
        print_schedule(solver, course_vars, available_days)
        print("\n✅ Fertig!\n")
    else:
        print("\n⚠️ Fehler!\n")