import BckE.SQL.SQL_Azubi as Azubi_SQL
import BckE.SQL.SQL_Gruppe as Gruppe_SQL
import BckE.Modelle.Gruppe as Gruppe
import BckE.Modelle.Azubi as Azubi
from collections import defaultdict

_max_Group_size = 20

def access_db_Azubis():
    return Azubi_SQL.get_all()




def convert_db_Azubi(db_azubi):
    azubis_list = []
    for a in db_azubi:
        azubi = Azubi.Azubi()

        azubi.name = a['Nachname']
        azubi.vorname = a['Vorname']
        azubi.block =a['Block']
        azubi.id = a['id']
        azubi.ausbildungsunternehmen = a['Ausbildungsunternehmen']
        azubi.attendedModules = a['AttendedModules']
        azubi.ausbildungsStart = a['StartDate']
        azubis_list.append(azubi)

    return azubis_list



def get_Azubis():

    data = access_db_Azubis()
    formated_dataArray = []
    for set in data:
        formated_dataObj = {
            "id": set[0],
            "Nachname": set[1],
            "Vorname": set[2],
            "Ausbildungsunternehmen": set[3],
            "StartDate": set[4],
            "AttendedModules": set[5],
            "Block": set[6],
        }
        array = [x.strip() for x in set[3].split(",")]
        formated_dataArray.append(formated_dataObj)
    return formated_dataArray



def sortBlock_Azubis(formated_dataArray):


    #Einteilung der Blöcke
    Aazubis = []
    Bazubis = []
    Cazubis = []

    for azubi in formated_dataArray:
        if(azubi.block == "A"):
            Aazubis.append(azubi)
        elif(azubi.block == "B"):
            Bazubis.append(azubi)
        elif(azubi.block == "C"):
            Cazubis.append(azubi)

    return Aazubis,Bazubis,Cazubis
    #Jetzt folgt die Lehrjahrunterscheidung


def sort_Startyear(formated_dataArray):
    year1Azubis = []
    year2Azubis = []
    year3Azubis = []

    for azubi in formated_dataArray:
        #print(azubi.ausbildungsStart)
        if(azubi.ausbildungsStart == "2026"):
            year1Azubis.append(azubi)
        elif(azubi.ausbildungsStart == "2025"):
            year2Azubis.append(azubi)
        elif(azubi.ausbildungsStart == "2024"):
            year3Azubis.append(azubi)
    return year1Azubis,year2Azubis,year3Azubis

def sort_Firma(formated_dataArray):
    Firmen = {}
    #for azubi in formated_dataArray:
       # if(azubi.ausbildungsunternehmen not in Firmen):
           #  Firmen.keys() = azubi.ausbildungsunternehmen

def build_company_index(azubis):
    Firmen = defaultdict(list)
    seen = set()  # (firma, id) Paare, um Duplikate zu verhindern

    for a in azubis:
        firma = a.ausbildungsunternehmen
        aid = a.id
        key = (firma, aid)
        if key in seen:
            continue
        seen.add(key)
        Firmen[firma].append(aid)

    return dict(Firmen)





def main():
    list_azubis = get_Azubis()
    convertedAz = convert_db_Azubi(list_azubis)
    ABlock, BBlock, CBlock = sortBlock_Azubis(convertedAz)
    A2026, A2025, A2024 = sort_Startyear(ABlock)
    B2026, B2025, B2024 = sort_Startyear(BBlock)
    C2026, C2025, C2024 = sort_Startyear(CBlock)
    print(len(A2026), len(A2025), len(A2024))
    build_company_index(A2026)
if __name__ == '__main__':
    main()
#print(convert_db_Azubi(list_azubis))
#print(convert_db_Azubi(get_db_Azubis()))