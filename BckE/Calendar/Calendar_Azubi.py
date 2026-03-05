from datetime import timedelta

from ortools.sat.python import cp_model

import config


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


print(createAzubiCal("A"))






