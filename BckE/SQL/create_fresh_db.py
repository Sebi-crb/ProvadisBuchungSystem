import BckE.SQL.generate_fakeData_Azubi as generate_fakeData_Azubi
import BckE.SQL.generate_Groups as generate_Groups
import BckE.SQL.SQL_Raum as SQL_Raum
import BckE.SQL.SQL_Trainer as SQL_Trainer

def create_db_with_data():
    generate_fakeData_Azubi.main()
    generate_Groups.main()
    SQL_Raum.insert_Räume()
    SQL_Trainer.insert_trainer_data()


create_db_with_data()