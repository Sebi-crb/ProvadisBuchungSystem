from datetime import timedelta

import BckE.SQL.config_Module as cModule
import BckE.Calendar.Calendar_Azubi as azubi_calendar
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
trainer = dataGetter.get_Trainers()
räume = dataGetter.get_Rooms()


for id, modul in con_moduls.items():
    samples = [
        (modul['id'], modul['dauer']),
    ]
    modul_list.append(modul['dauer'])
    #print(samples)



for i in range(len(modul_list)):
    kurs = Kurs.Kurs()
    dauer = modul_list[i]
    for group in groups:
        group_block = group['block']
        if (group_block == 'A'):
            # for i, day in enumerate(azubi_calendar_BlockA):
            #     startDay = azubi_calendar_BlockA.get(day)
            #     endDay = azubi_calendar_BlockA.get(day+4)
            #     if endDay is not None and startDay is not None  :
            #         dif = endDay - startDay
            #         dif : timedelta
            #         if dif.days == 4:
            #             print(startDay, "-", endDay)
            print(azubi_calendar.get_available_weeks(azubi_calendar_BlockA))

