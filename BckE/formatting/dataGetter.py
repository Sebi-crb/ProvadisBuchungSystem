import BckE.SQL.SQL_Trainer as Sql_Trainer

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



print(get_Trainers())