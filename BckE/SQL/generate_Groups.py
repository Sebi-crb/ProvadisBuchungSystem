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
        if(azubi.ausbildungsStart == "2025"):
            year1Azubis.append(azubi)
        elif(azubi.ausbildungsStart == "2024"):
            year2Azubis.append(azubi)
        elif(azubi.ausbildungsStart == "2023"):
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


def set_up_groups(formated_dataArray):
    Jahrgang = []
    Gruppe = []
    for firma, values in formated_dataArray.items():
        #print(firma, values, values.__len__())
        if((Gruppe.__len__())<_max_Group_size):
            for v in values:
                #print(v)
                Gruppe.append(v)
        else:
            Jahrgang.append(Gruppe)
            Gruppe = []
            for v in values:
                Gruppe.append(v)
    Jahrgang.append(Gruppe)
    return Jahrgang



def main():
    block_list = {}
    list_azubis = get_Azubis()
    convertedAz = convert_db_Azubi(list_azubis)
    ABlock, BBlock, CBlock = sortBlock_Azubis(convertedAz)
    A2025, A2024, A2023 = sort_Startyear(ABlock)
    B2025, B2024, B2023 = sort_Startyear(BBlock)
    C2025, C2024, C2023 = sort_Startyear(CBlock)
    block_list.update({"A2025": A2025})
    block_list.update({"A2024": A2024})
    block_list.update({"A2023": A2023})
    block_list.update({"B2025": B2025})
    block_list.update({"B2024": B2024})
    block_list.update({"B2023": B2023})
    block_list.update({"C2025": C2025})
    block_list.update({"C2024": C2024})
    block_list.update({"C2023": C2023})

    company_indexing_list = []
    for block, item in block_list.items():
        #print(item)
        company_indexing_list.append(build_company_index(item))


    year_block_group = []
    for b in company_indexing_list:
        #print(set_up_groups(b))
        year_block_group.append(set_up_groups(b))



    #dumm = build_company_index(A2025)
    #print(dumm)
    #set_up_groups(dumm)
    #print(set_up_groups(dumm))
    gruppen_class = []
    # j = 0
    # print(year_block_group)
    # for i, (block, group_azubi_list) in enumerate(year_block_group):
    #
    #     group = Gruppe.Gruppe("", [])
    #     if (i <= 2):
    #         group.block = "A"
    #     elif (2 < i <= 5):
    #         group.block = "B"
    #     else:
    #         group.block = "C"
    #
    #     if ((i + 1) % 3 == 0):
    #         group.name = "23FA0" + str(j)
    #     elif ((i + 1) % 3 == 1):
    #         group.block = "25FA0" + str(j)
    #     else:
    #         group.block = "24FA0" + str(j)
    #
    #     group.azubiList = group_azubi_list
    #     j = j + 1

    finishedGroupList = []
    for i, (block) in enumerate(year_block_group):
        #print("block ",block)
        for j, group_azubi_list in enumerate(block):
            #print("group ", group_azubi_list)
            group = Gruppe.Gruppe(None, [])
            if (i <= 2):
                group.block = "A"
            elif (2 < i <= 5):
                group.block = "B"
            else:
                group.block = "C"

            if ((i + 1) % 3 == 0):
                group.name = "23FA0" + str(j + 1)
            elif ((i + 1) % 3 == 1):
                group.name = "25FA0" + str(j + 1)
            else:
                group.name = "24FA0" + str(j + 1)


            group.azubiList = group_azubi_list
            group.countAzubis = len(group_azubi_list)
            # es fehlen die fertigen module
            # und die gruppen in den blöcken wurden nich richtig geteilt, es gibt nur 2 statt 3
            # liegt aber vll an der länge der azubi oder so idk

            finishedGroupList.append(group)
    #print(finishedGroupList)
    for group in finishedGroupList:
        Gruppe_SQL.insert_AzubiGruppe(group)
    Gruppe_SQL.get_all()


if __name__ == '__main__':
    main()
#print(convert_db_Azubi(list_azubis))
#print(convert_db_Azubi(get_db_Azubis()))