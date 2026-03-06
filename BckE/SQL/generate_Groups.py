import BckE.SQL.SQL_Azubi as Azubi_SQL
import BckE.SQL.SQL_Gruppe as Gruppe_SQL
import BckE.Modelle.Gruppe as Gruppe
import BckE.Modelle.Azubi as Azubi
import pprint as pp
def get_db_Azubis():
    return Azubi_SQL.get_all()

def convert_db_Azubi(db_azubi):
    azubis = []
    for Azubi in db_azubi:
        Azubi = Azubi()
        azubis.append(Azubi)

    return azubis

raw = get_db_Azubis()

def parse_numbers(s: str) -> list[int]:

    return [int(x.strip()) for x in s.split(',') if x.strip()]

# Konvertiert in eine Liste von Dictionaries mit geparsten Nummern
records = [
    {
        "id": r[0],
        "nachname": r[1],
        "vorname": r[2],
        "firma": r[3],
        "jahr": r[4],
        "Module": parse_numbers(r[5]),
        "note": r[6],
    }
    for r in raw
]


save = pp.pprint(records)
#print(convert_db_Azubi(get_db_Azubis()))