from faker import Faker

import random
import BckE.SQL.SQL_Azubi as SQL_Azubi


class Generate_Fake_Data:

    def __init__(self):
        self.fake = Faker()

    lehrjahre = ["2025", "2024", "2023"]
    def generate_azubi(self, firmen, lehrjahr):
        import BckE.Modelle.Azubi as Azubi
        fake = Faker('de_DE')
        Azubi =  Azubi.Azubi()
        Azubi.name = fake.last_name()
        Azubi.vorname = fake.first_name()
        Azubi.ausbildungsunternehmen = random.choice(firmen)
        Azubi.lehrjahr = str(random.randint(1, 3))
        Azubi.block = random.choice(["A", "B", "C"])
        Azubi.attendedModules = [random.choice(["1", "2", "3", ]), random.choice(["4", "5", "6", "7"]), random.choice(["8", "9", "10", "11",])]
        Azubi.ausbildungsStart = lehrjahr #random.choice(["2025", "2024", "2023"])
        return Azubi






    def generate_azubis(self, amount, lehrjahr):
        fake = Faker('de_DE')
        Azubis = []
        firmen = []
        for _ in range(12):
            firmen.append( fake.company())
        for i in range(amount):
            Azubis.append(self.generate_azubi(firmen, lehrjahr))


        return Azubis

    def db_azubi(self):
        SQL_Azubi.insert_Azubi(self.generate_azubi())


def main():
    SQL_Azubi.create_table()
    GFD = Generate_Fake_Data()
    for lehrjahr in GFD.lehrjahre:
        a_list = GFD.generate_azubis(250, lehrjahr)
        #print(a_list)
        for az in a_list:
            SQL_Azubi.insert_Azubi(az)
    #print(SQL_Azubi.print_all())
    SQL_Azubi.get_all()
    #for Azubi in liste:
        #print(Azubi., end="\n\n ")
        #print(Azubi)
