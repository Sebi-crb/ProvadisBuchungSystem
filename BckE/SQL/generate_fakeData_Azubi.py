from faker import Faker
import Modelle.Azubi
import random
import SQL.SQL_Azubi as SQL_Azubi


class Generate_Fake_Data:
    def __init__(self):
        self.fake = Faker()


    def generate_azubi(self, firmen):
        fake = Faker('de_DE')
        Azubi = Modelle.Azubi.Azubi()
        Azubi.name = fake.last_name()
        Azubi.vorname = fake.first_name()
        Azubi.ausbildungsunternehmen = random.choice(firmen)
        Azubi.lehrjahr = str(random.randint(1, 3))
        Azubi.block = random.choice(["A", "B", "C"])
        Azubi.attendedModules = [random.choice(["1", "2", "3", ]), random.choice(["4", "5", "6", "7"]), random.choice(["8", "9", "10", "11",])]
        Azubi.ausbildungsStart = random.choice([y := __import__("datetime").date.today().year, y-1, y-2])

        return Azubi






    def generate_azubis(self, amount):
        fake = Faker('de_DE')
        Azubis = []
        firmen = []
        for _ in range(12):
            firmen.append( fake.company())
        for i in range(amount):
            Azubis.append(self.generate_azubi(firmen))


        return Azubis

    def db_azubi(self):
        SQL_Azubi.insert_Azubi(self.generate_azubi())


if(__name__ == "__main__"):
    #GFD = Generate_Fake_Data()
    #liste = GFD.generate_addresses(10)
    GFD = Generate_Fake_Data()
    a_list = GFD.generate_azubis(250)
    for az in a_list:
        SQL_Azubi.insert_Azubi(az)
    #print(SQL_Azubi.print_all())
    SQL_Azubi.print_all()
    #for Azubi in liste:
        #print(Azubi., end="\n\n ")
        #print(Azubi)