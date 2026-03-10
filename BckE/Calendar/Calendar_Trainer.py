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


def createCal():
    available_days = get_available_days()  # die verfügbaren Tage der Azubigruppe
    # Erstelle Modell
    model = cp_model.CpModel()  # Erstellung eines leeren Stundenplans
    # Variablen: Wann startet jeder Kurs?
    dayDateMap = {}  # dict für die Kurse aus der config
    for i in range(available_days.__len__()):
        dayDateMap[i] = available_days[i]
    #print(course_vars)
    return dayDateMap



#Erstellt einen Kalender der die absence rausnimmt
def create_calendar_with_absence(absences):
    days = createCal()
    newAvailableDays = days.copy()
    for day, date in days.items():
        if (day in absences):
            newAvailableDays.pop(day)

    return newAvailableDays

#Nimmt den gebuchten Kalender
def remove_absence(absenceToRemove, bookedCalendar):
    initCalendar = createCal()
    for day in absenceToRemove:
        dateToRestore = initCalendar.get(day)
        bookedCalendar.update({day: dateToRestore})

    return bookedCalendar

def get_available_weeks(calendar):
    available_weeks = []
    count = 1
    for i, startDay in enumerate(calendar):
        startDate = calendar.get(startDay)
        endDay = startDay + 4
        endDate = calendar.get(endDay)
        if endDate is not None and startDate is not None :
            dif = endDate - startDate
            dif: timedelta
            if dif.days == 4:
                available_weeks.append(
                    {
                                 "week_numb": count,
                                 "start": {
                                     "day": startDay,
                                     "date": startDate,
                                 },
                                 "end": {
                                     "day": endDay,
                                     "endDate": endDate,
                                 }
                    }
                )
                count += 1
    return available_weeks




print(createCal())


#bookedHolidayCalendar = (book_absence([2, 0, 4, 1]))
#print(bookedHolidayCalendar)
#restoredCalendar = remove_absence([1], bookedHolidayCalendar)
#print(restoredCalendar)
