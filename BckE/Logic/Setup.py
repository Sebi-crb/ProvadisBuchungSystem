from datetime import timedelta

import BckE.SQL.config_Module as cModule
import BckE.Calendar.Calendar_Azubi as azubi_calendar
import BckE.Calendar.Calendar_Trainer as trainer_Calender
import BckE.SQL.SQL_Trainer as SQL_Trainer
import BckE.SQL.SQL_Gruppe as SQL_Gruppe
import BckE.SQL.SQL_Raum as SQL_Raum
import BckE.formatting.dataGetter as dataGetter
import BckE.Modelle.Kurs as Kurs


import datetime

con_moduls = cModule.get_Modules()
modul_list = []

azubi_calendar_BlockA = azubi_calendar.createAzubiCal('A')
azubi_calendar_BlockB = azubi_calendar.createAzubiCal('B')
azubi_calendar_BlockC = azubi_calendar.createAzubiCal('C')

groups = dataGetter.get_Gruppen()
trainers = dataGetter.get_Trainers()
räume = dataGetter.get_Rooms()


for id, modul in con_moduls.items():
    samples = [
        (modul['id'], modul['dauer']),
    ]
    modul_list.append(modul['dauer'])
    #print(samples)

for i, modul in modul_list:
    dauer = modul['dauer']
    for group in groups:
        group_id = group['block']


def find_group_trainer_modul_match(gruppe, dauer):
    if dauer == 3 or dauer == 5:
        neededWeeks = 1
    elif dauer == 10:
        neededWeeks = 2
    group_block = gruppe['block']
    if (group_block == 'A'):
        azubi_available_weeks = azubi_calendar.get_available_weeks(azubi_calendar_BlockA)
        for trainer in trainers:
            absences = SQL_Trainer.get_Trainer_absence(trainer['id'])
            trainer_cal_with_absences = trainer_Calender.create_calendar_with_absence(absences)
            trainer_available_weeks = trainer_Calender.get_available_weeks(trainer_cal_with_absences)
            print(trainer_available_weeks[2])
            for trainer_week in trainer_available_weeks:
                trainer_week : dict
                for azubi_week in azubi_available_weeks:
                    if neededWeeks == 1:
                        if trainer_week.get("start").get("day") == azubi_week.get("start").get("day"):
                            print(trainer_week.get("start"), " and ", trainer_week.get("start"))
                    elif neededWeeks == 2:
                        current_week_trainer = trainer_week.get("start").get("date")
                        if (int(trainer_week.get("week_numb")) + 1 <= trainer_week.__len__()):
                            next_week_trainer = trainer_available_weeks[int(trainer_week.get("week_numb")) + 1].get("start").get("date")
                        differenz = abs((next_week_trainer - current_week_trainer).days)
                        if differenz >= 7:
                            trainer_2WeeksTime = True
                        current_week_azubi = azubi_week.get("start").get("date")
                        if (int(azubi_week.get("week_numb")) + 1 <= azubi_week.__len__()):
                            next_week_azubi = azubi_available_weeks[int(azubi_week.get("week_numb")) + 1].get("start").get("date")
                        differenz = abs((next_week_azubi - current_week_azubi).days)
                        if differenz >= 7:
                            azubi_2WeeksTime = True
                        if trainer_2WeeksTime and azubi_2WeeksTime and trainer_week.get("start").get("day") == azubi_week.get("start").get("day"):
                            print(azubi_week, "and", trainer_week)


def getModuleTime(neededWeeks, trainer_week, azubi_week, trainer_available_weeks, azubi_available_weeks):
    if neededWeeks == 1:
        if trainer_week.get("start").get("day") == azubi_week.get("start").get("day"):
            print(trainer_week.get("start"), " and ", trainer_week.get("start"))
    elif neededWeeks == 2:
        current_week_trainer = trainer_week.get("start").get("date")
        if (int(trainer_week.get("week_numb")) + 1 <= trainer_week.__len__()):
            next_week_trainer = trainer_available_weeks[int(trainer_week.get("week_numb")) + 1].get("start").get("date")
        differenz = abs((next_week_trainer - current_week_trainer).days)
        if differenz >= 7:
            trainer_2WeeksTime = True
        current_week_azubi = azubi_week.get("start").get("date")
        if (int(azubi_week.get("week_numb")) + 1 <= azubi_week.__len__()):
            next_week_azubi = azubi_available_weeks[int(azubi_week.get("week_numb")) + 1].get("start").get("date")
        differenz = abs((next_week_azubi - current_week_azubi).days)
        if differenz >= 7:
            azubi_2WeeksTime = True
        if trainer_2WeeksTime and azubi_2WeeksTime and trainer_week.get("start").get("day") == azubi_week.get(
                "start").get("day"):
            print(azubi_week, "and", trainer_week)

print(find_group_trainer_modul_match({"block" : "A"}, 10))
