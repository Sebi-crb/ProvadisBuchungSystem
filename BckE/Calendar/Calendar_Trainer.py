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


def book_holiday(holidays):
    days = createCal()
    newAvailableDays = days.copy()
    for day, date in days.items():
        if (day in holidays):
            newAvailableDays.pop(day)

    return newAvailableDays

def remove_holidays(holidaysToRemove, bookedCalendar):
    initCalendar = createCal()
    for day in holidaysToRemove:
        dateToRestore = initCalendar.get(day)
        bookedCalendar.update({day: dateToRestore})

    return bookedCalendar




#print(createCal())


bookedHolidayCalendar = (book_holiday([2, 0, 4, 1]))
print(bookedHolidayCalendar)
restoredCalendar = remove_holidays([1], bookedHolidayCalendar)
print(restoredCalendar)
