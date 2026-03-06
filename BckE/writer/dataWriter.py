from datetime import datetime

from pandas import date_range

import BckE.SQL.SQL_Trainer as Sql_Trainer
import BckE.Calendar.Calendar_Trainer as calendar_trainer

def add_absence(start, end, id):
    startDate = datetime.fromisoformat(start)
    endDate = datetime.fromisoformat(end)
    dayDateMap = calendar_trainer.createCal()
    invertedMap = {v: k for k, v in dayDateMap.items()}
    keyArr = []
    for day in date_range(startDate, endDate):
        if day.weekday() >= 5:
            continue
        key = invertedMap[day.date()]
        keyArr.append(key)
    print(keyArr)
    newAbsenceList = Sql_Trainer.add_absence(id, keyArr)
    return newAbsenceList


if __name__ == '__main__':
    add_absence("2026-03-02", "2026-03-06", 1)