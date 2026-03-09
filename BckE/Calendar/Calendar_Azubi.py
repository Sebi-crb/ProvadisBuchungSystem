from datetime import timedelta

from ortools.sat.python import cp_model

import BckE.Calendar.config as config


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


def isDayInBlock(block_id, check_date):
    """Ist Block an diesem Tag in der Schule?"""
    days = (check_date - config.SCHOOL_YEAR_START).days
    week = days // 7
    cycle_week = week % 6

    if block_id == "A":
        return cycle_week in (0, 1)
    elif block_id == "B":
        return cycle_week in (2, 3)
    elif block_id == "C":
        return cycle_week in (4, 5)
    else:
        raise ValueError("Unbekannter Block: " + block_id)


def createCal():
    available_days = get_available_days()  # die verfügbaren Tage der Azubigruppe
    # Erstelle Modell
    model = cp_model.CpModel()  # Erstellung eines leeren Stundenplans
    # Variablen: Wann startet jeder Kurs?
    course_vars = {}  # dict für die Kurse aus der config
    for i in range(available_days.__len__()):
        course_vars[i] = available_days[i]
    #print(course_vars)
    return course_vars


def trimBlockDays(Block):
    days = get_available_days()
    for i in range(len(days)-1):
        if(isDayInBlock(Block, days[i])):
            #print( day)
            days.remove(days[i])

    return days


def createAzubiCal(block):
    days = createCal()
    newAvailableDays = days.copy()
    for day, date in days.items():
        if (isDayInBlock(block, date)):
            newAvailableDays.pop(day)

    return newAvailableDays

def get_available_weeks(block_plan):
    available_weeks = []
    for i, day in enumerate(block_plan):
        startDay = block_plan.get(day)
        endDay = block_plan.get(day + 4)
        if endDay is not None and startDay is not None:
            dif = endDay - startDay
            dif: timedelta
            if dif.days == 4:
                #print(startDay, "-", endDay)
                available_weeks.append(
                    {
                                 "week_numb": i,
                                 "start": startDay,
                                 "end": endDay
                    }
                )
    return available_weeks

#print(createAzubiCal("A"))


# from datetime import date
#
# # Deine Liste vorbereiten
# booking_list = []
#
# # Beispiel-Werte (in einer Schleife)
# for i in range(5):
#     start_dt = date(2025, 9, 15)  # Dein Startdatum
#     end_dt = date(2025, 9, 20)  # Dein Enddatum
#
#     # Als Dictionary zur Liste hinzufügen
#     booking_list.append({
#         "id": i,
#         "start": start_dt,
#         "end": end_dt
#     })
#
# # Zugriff auf den ersten Eintrag:
# print(booking_list[0]["start"])




