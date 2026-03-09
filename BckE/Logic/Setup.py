import BckE.SQL.config_Module as cModule
import BckE.Calendar.Calendar_Azubi as azubi_calendar
import BckE.SQL.SQL_Trainer as SQL_Trainer
import BckE.SQL.SQL_Gruppe as SQL_Gruppe


con_moduls = cModule.get_Modules()
modul_list = []

azubi_calendar_BlockA = azubi_calendar.createAzubiCal('A')
azubi_calendar_BlockB = azubi_calendar.createAzubiCal('B')
azubi_calendar_BlockC = azubi_calendar.createAzubiCal('C')

groups = SQL_Gruppe.get_all()




for id, raum in con_moduls.items():
    samples = [
        (raum['id'], raum['dauer']),
    ]
    modul_list.append(raum['dauer'])
    #print(samples)


