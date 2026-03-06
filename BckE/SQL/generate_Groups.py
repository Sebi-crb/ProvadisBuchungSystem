import ProvadisBuchungSystem.BckE.SQL.SQL_Azubi as Azubi_SQL
import ProvadisBuchungSystem.BckE.SQL.SQL_Gruppe as Gruppe_SQL
import ProvadisBuchungSystem.BckE.Modelle.Gruppe as Gruppe
import ProvadisBuchungSystem.BckE.Modelle.Azubi as Azubi

def get_all_Azubis():
    return Azubi_SQL.get_all()

print(get_all_Azubis())