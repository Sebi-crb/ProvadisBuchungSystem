import sqlite3
from pathlib import Path
from datetime import date
import BckE.Modelle.Trainer as Trainer
#from ProvadisBuchungSystem.BckE.Calendar.Calendar_Trainer import remove_absence



PROJECT_ROOT_NAME = "ProvadisBuchungSystem"
TARGET_SUBPATH = Path("BckE") / "SQL" / "Main.db"   # gewünschter Pfad ab Projektwurzel

here = Path(__file__).resolve()
proj_root = next((p for p in here.parents if p.name == PROJECT_ROOT_NAME), None)
if proj_root is None:
    raise RuntimeError(f"Projektordner '{PROJECT_ROOT_NAME}' nicht gefunden in {here}")

DB_PATH = proj_root / TARGET_SUBPATH
DB_PATH.parent.mkdir(parents=True, exist_ok=True)   # stellt sicher, dass Ordner existiert
DB = str(DB_PATH.resolve())


conn = sqlite3.connect(DB)
def create_table():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS Trainer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Vorname TEXT NOT NULL,
            Abwesenheiten TEXT NOT NULL
        );
        """)
        conn.commit()

def delete(id_):
    with sqlite3.connect(DB) as c: c.execute("DELETE FROM Trainer WHERE id=?", (id_,))

def insert_Trainer(Trainer):
    create_table()
    with sqlite3.connect(DB) as conn:
        samples = [
            (Trainer.name, Trainer.vorname, Trainer.abwesenheiten),
        ]
        conn.executemany(
            "INSERT INTO Trainer (Name, Vorname, Abwesenheiten) VALUES (?, ?, ?)",
            samples
        )
        conn.commit()

def get_all_Trainers():
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT id, Name, Vorname, Abwesenheiten FROM Trainer")
        rows = cur.fetchall()
        #for r in rows:
            #print(r)
        return rows

def get_Trainer(id_):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT * FROM Trainer WHERE id=?", (id_,))
        row = cur.fetchone()
        return row

def get_Trainer_absence(id_):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT Abwesenheiten FROM Trainer WHERE id=?", (id_,))
        row = cur.fetchone()
        return row


def change_absence(id_, toRemove):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT Abwesenheiten FROM Trainer WHERE id = ?", (id_,))
        row = cur.fetchone()
        if not row:
            return

        # Text in Liste umwandeln
        werte = row[0]  # z.B. "1, 2, 3, 4, 5"
        liste = [x.strip() for x in werte.split(",")]

        # Werte entfernen (als Strings vergleichen)
        werte_entfernen = set(str(w) for w in toRemove)
        neue_liste = [x for x in liste if x not in werte_entfernen]

        # Neue Zeichenkette erzeugen
        neuer_text = ", ".join(neue_liste)

        # Update in DB schreiben
        conn.execute(
            "UPDATE Trainer SET Abwesenheiten = ? WHERE id = ?",
            (neuer_text, id_)
        )

        return neuer_text


def add_absence(id_, toAdd):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT Abwesenheiten FROM Trainer WHERE id = ?", (id_,))
        row = cur.fetchone()
        if not row:
            return

        # Aktuelle Werte in Liste umwandeln
        werte = row[0]  # z.B. "1, 3, 5"
        liste = [x.strip() for x in werte.split(",") if x.strip()]

        # Neue Werte hinzufügen (als Strings)
        for w in toAdd:
            w_str = str(w)
            if w_str not in liste:
                liste.append(w_str)

        # Sortieren optional (falls du die Reihenfolge sauber halten willst)
        liste = sorted(liste, key=lambda x: int(x))

        # Neue Zeichenkette erzeugen
        neuer_text = ", ".join(liste)

        # Update in DB schreiben
        conn.execute(
            "UPDATE Trainer SET Abwesenheiten = ? WHERE id = ?",
            (neuer_text, id_)
        )

        return neuer_text


def drop_table():
    with sqlite3.connect(DB) as conn:
        conn.execute("DROP TABLE IF EXISTS Trainer")
        conn.commit()



def insert_trainer_data():
    create_table()
    import BckE.Modelle.Trainer as Trainer
    Trainer = Trainer.Trainer()

    nachnamen = [
        "Horn", "Christoph-Chan", "Oxlong", "Winkler", "Bolika",
        "Janus", "Hartmann", "Saar", "Redem", "Bino",
        "Jet", "Bacon", "Lord", "Bilyty", "Lester"
    ]

    vornamen = [
        "Gabe", "Jan", "Mike", "Rainer", "Anna",
        "Hugh", "Fixie", "Pajeet", "Donot", "Al",
        "Mit", "Chris-P", "Gai", "Diza", "Moe"
    ]


    for i in range(len(vornamen)):
        t = Trainer
        t.name = nachnamen[i]
        t.vorname = vornamen[i]
        t.abwesenheiten = ""
        insert_Trainer(t)


drop_table()
insert_trainer_data()


def main():
    import BckE.Modelle.Trainer as Trainer
    with sqlite3.connect(DB) as conn:
        #create_table()
        #insert_sample(conn)
        #azubi = GFD.generate_azubi()
        #insert_Azubi(azubi)
        Trainer = Trainer.Trainer()
        Trainer.name = "Netanyahu"
        Trainer.vorname = "Bibi"
        Trainer.abwesenheiten = "9, 11"
        insert_Trainer(Trainer)
        #add_absence(1, [str(2), str(3), str(4)])
        #change_absence(1, [str(3)])

        print("Aktuelle Einträge in Trainer:")
        #get_all_Trainers()
        #print_all()

#main()
#if __name__ == "__main__":
#main()
#print(get_all_Trainers())

create_table()