import ProvadisBuchungSystem.BckE.SQL.SQL_Trainer as SQL_Trainer

def get_Trainers():
    return SQL_Trainer.get_all_Trainers()

print(get_Trainers())