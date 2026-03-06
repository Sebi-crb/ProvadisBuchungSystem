from datetime import datetime

import BckE.SQL.SQL_Trainer as Sql_Trainer
import BckE.SQL.SQL_Azubi as Sql_Azubi

def get_Trainers():
    data = Sql_Trainer.get_all_Trainers()
    formated_dataArray = []

    for set in data:
        formated_dataObj = {
            "id": set[0],
            "nachname": set[1],
            "vorname": set[2],
        }
        array = [x.strip() for x in set[3].split(",")]
        formated_dataObj.update({"abwesenheiten": array})

        formated_dataArray.append(formated_dataObj)
    return formated_dataArray


def calculateYear(startDate):
    start_int = int(startDate)
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    years_passed = current_year - start_int

    if current_month < 8 and years_passed > 0:
        actual_year = years_passed
    else:
        actual_year = years_passed + 1

    if 1 <= actual_year <= 3:
        return actual_year

    return None


def get_Azubis():
    data = Sql_Azubi.get_all()
    formated_dataArray = []

    for set in data:
        formated_dataObj = {
            "id": set[0],
            "nachname": set[1],
            "vorname": set[2],
            "unternehmen": set[3],
            "ausbildungsJahr": calculateYear(set[4]),
            "block": set[6],
        }
        array = [x.strip() for x in set[3].split(",")]
        formated_dataObj.update({"attendedModules": array})
        formated_dataArray.append(formated_dataObj)
    return formated_dataArray


print(get_Trainers())
print (get_Azubis())