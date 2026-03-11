from datetime import timedelta

import BckE.SQL.config_Module as cModule
import BckE.Calendar.Calendar_Azubi as azubi_calendar
import BckE.Calendar.Calendar_Trainer as trainer_Calender
import BckE.Calendar.Calendar_Raum as raum_calendar
import BckE.SQL.SQL_Trainer as SQL_Trainer
import BckE.SQL.SQL_Gruppe as SQL_Gruppe
import BckE.SQL.SQL_Raum as SQL_Raum
import BckE.formatting.dataGetter as dataGetter
import BckE.Modelle.Kurs as Kurs
import datetime

from BckE.Calendar.Calendar_Azubi import createCal

con_moduls = cModule.get_Modules()
modul_list = {}

azubi_calendar_BlockA = azubi_calendar.createAzubiCal('A')
azubi_calendar_BlockB = azubi_calendar.createAzubiCal('B')
azubi_calendar_BlockC = azubi_calendar.createAzubiCal('C')

groups = dataGetter.get_Gruppen()
#print(groups)
trainers = dataGetter.get_Trainers()
räume = dataGetter.get_Rooms()


for id, modul in con_moduls.items():
    modul_list.update({id: modul['dauer']})


#print(modul_list)




def find_group_trainer_modul_match(gruppe, dauer):
    if dauer == 3 or dauer == 5:
        neededWeeks = 1
    elif dauer == 10:
        neededWeeks = 2
    group_block = gruppe['block']
    azubi_available_weeks = azubi_calendar.get_available_weeks(
        azubi_calendar_BlockA if group_block == 'A' else
        azubi_calendar_BlockB if group_block == 'B' else
        azubi_calendar_BlockC
    )
    for trainer in trainers:
        absences = SQL_Trainer.get_Trainer_absence(trainer['id'])

        result = []
        for tup in absences:
            s = tup
            if not s:
                continue
            for part in s.split(','):
                part = part.strip()
                if part:
                    result.append(int(part))
        absences = result
        trainer_cal_with_absences = trainer_Calender.create_calendar_with_absence(absences)
        trainer_available_weeks = trainer_Calender.get_available_weeks(trainer_cal_with_absences)
        # matchingDate = getFirstTrainerMatch(neededWeeks, trainer_available_weeks, azubi_available_weeks)
        # print(matchingDate)
        matchingDates = getFirstTrainerMatch(neededWeeks, trainer_available_weeks, azubi_available_weeks)
        return matchingDates


def getAllTrainerMatches(neededWeeks, trainer_available_weeks, azubi_available_weeks, trainerID):
    trainerMatches= []
    for i, trainer_week in enumerate(trainer_available_weeks):
        trainer_week: dict
        for azubi_week in azubi_available_weeks:
            if neededWeeks == 1:
                if trainer_week.get("start").get("day") == azubi_week.get("start").get("day"):
                    trainerMatches.append({
                        "id": trainerID,
                        "start": trainer_week.get("start"),
                        "end": trainer_week.get("end"),
                    })
            elif neededWeeks == 2:
                current_week_trainer = trainer_week.get("start").get("date")
                if (int(trainer_week.get("week_numb")) + 1 <= trainer_week.__len__()):
                    next_week_trainer = trainer_available_weeks[int(trainer_week.get("week_numb")) + 1].get(
                        "start").get("date")
                differenz = abs((next_week_trainer - current_week_trainer).days)
                if differenz >= 7:
                    trainer_2WeeksTime = True
                current_week_azubi = azubi_week.get("start").get("date")
                if (int(azubi_week.get("week_numb")) + 1 <= azubi_week.__len__()):
                    next_week_azubi = azubi_available_weeks[int(azubi_week.get("week_numb")) + 1].get("start").get(
                        "date")
                differenz = abs((next_week_azubi - current_week_azubi).days)
                if differenz >= 7:
                    azubi_2WeeksTime = True
                if trainer_2WeeksTime and azubi_2WeeksTime and trainer_week.get("start").get("day") == azubi_week.get(
                        "start").get("day"):
                    azubi_week, "and", trainer_week
                    if (int(trainer_week.get("week_numb")) + 1 <= trainer_available_weeks.__len__()):
                        trainerMatches.append({
                            "id": trainerID,
                            "start": trainer_week.get("start"),
                            "end": trainer_available_weeks[i + 1].get("end"),
                        })
    return trainerMatches


def getFirstTrainerMatch(neededWeeks, trainer_available_weeks, azubi_available_weeks):
    for i, trainer_week in enumerate(trainer_available_weeks):
        trainer_week: dict
        for azubi_week in azubi_available_weeks:
            if neededWeeks == 1:
                if trainer_week.get("start").get("day") == azubi_week.get("start").get("day"):
                    return{
                        "start": trainer_week.get("start"),
                        "end": trainer_week.get("end"),
                    }
            elif neededWeeks == 2:
                current_week_trainer = trainer_week.get("start").get("date")
                if (int(trainer_week.get("week_numb")) + 1 <= trainer_week.__len__()):
                    next_week_trainer = trainer_available_weeks[int(trainer_week.get("week_numb")) + 1].get(
                        "start").get("date")
                differenz = abs((next_week_trainer - current_week_trainer).days)
                if differenz >= 7:
                    trainer_2WeeksTime = True
                current_week_azubi = azubi_week.get("start").get("date")
                if (int(azubi_week.get("week_numb")) + 1 <= azubi_week.__len__()):
                    next_week_azubi = azubi_available_weeks[int(azubi_week.get("week_numb")) + 1].get("start").get(
                        "date")
                differenz = abs((next_week_azubi - current_week_azubi).days)
                if differenz >= 7:
                    azubi_2WeeksTime = True
                if trainer_2WeeksTime and azubi_2WeeksTime and trainer_week.get("start").get("day") == azubi_week.get(
                        "start").get("day"):
                    return {
                        "start": trainer_week.get("start"),
                        "end": trainer_available_weeks[i + 1].get("end"),
                    }



def get_room_absences():
    room_id_raw = SQL_Raum.get_room_IDs()
    room_ids = [t[0] for t in room_id_raw]
    room_absences = []
    #SQL_Raum.add_absence(2, [1, 2, 4, 8, 19])
    roomsList = []
    for room_id in room_ids:
        room_absences_raw = SQL_Raum.get_room_absence(room_id)
        room_absences = [int(x.strip()) for x in room_absences_raw[0].split(',') if x.strip()]
        #print(room_absences)
        room= {
            "id": room_id,
            "abwesenheiten": room_absences,
        }
        roomsList.append(room)
    return roomsList
    print(roomsList)


def get_room_available_weeks():
    room_absences = get_room_absences()
    roomCalendarMap = {}
    for room in room_absences:
        room : dict
        absences = room.get("abwesenheiten")
        calendar = raum_calendar.create_calendar_with_absence(absences)
        calendar_available_weeks = raum_calendar.get_available_weeks(calendar)
        roomCalendarMap.update({room.get("id"): calendar_available_weeks})
    print(roomCalendarMap)
    return roomCalendarMap

def find_room_trainer_group_modul_match():
    #for group in groups:
     #   print(find_group_trainer_modul_match(group, dauer))
    group = groups[0]
    print(group)

    for modules in modul_list:
        for trainer in trainers:
            trainer_cal = trainer_Calender.get_available_weeks(trainer_Calender.create_calendar_with_absence(SQL_Trainer.get_Trainer_absence(trainer.get("id"))))

            #print(trainer_cal)
            azubi_cal = azubi_calendar.get_available_weeks(azubi_calendar.createAzubiCal(group.get("block")))
            #print(azubi_cal)
            dauer = modul_list[modules]
            if(dauer == 5):
                match = getFirstTrainerMatch(1, trainer_cal, azubi_cal)
            else:
                match = getFirstTrainerMatch(2, trainer_cal, azubi_cal)
            print(match)

            break
        break



find_room_trainer_group_modul_match()

#find_room_trainer_group_modul_match(5)
