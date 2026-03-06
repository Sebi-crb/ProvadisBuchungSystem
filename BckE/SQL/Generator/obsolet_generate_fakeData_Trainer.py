from faker import Faker
import random
import BckE.SQL.SQL_Trainer as SQL_Trainer
import BckE.Modelle.Trainer


class Generate_Fake_Data:
    def __init__(self):
        self.fake = Faker()


    def generate_azubi(self):
        fake = Faker('de_DE')

        Trainer = BckE.Modelle.Trainer.Trainer()
        Trainer.name = fake.last_name()
        Trainer.vorname = fake.first_name()
        Trainer.ausbildungsunternehmen = fake.company()
        Trainer.lehrjahr = str(random.randint(1, 3))
        return Trainer






    def generate_azubis(self, amount):
        mitarbeiter = []

        for i in range(amount):
            mitarbeiter.append(self.generate_address_entry())


        return mitarbeiter

    def db_azubi(self):
        SQL_Trainer.insert_Azubi(self.generate_azubi())


if(__name__ == "__main__"):
    #GFD = Generate_Fake_Data()
    #liste = GFD.generate_addresses(10)
    GFD = Generate_Fake_Data()
    GFD.db_azubi()
    #print(SQL_Azubi.print_all())
    SQL_Trainer.print_all()
    #for Azubi in liste:
        #print(Azubi., end="\n\n ")
        #print(Azubi)