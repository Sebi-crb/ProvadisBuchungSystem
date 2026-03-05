import sqlite3
from datetime import date
import ProvadisBuchungSystem.BckE.Modelle.Trainer as Trainer


DB = "WIP.db"

def create_table():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS Trainer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Vorname TEXT NOT NULL,
            Module TEXT NOT NULL,
            Urlaub TEXT NOT NULL,
            BlockedWeeks TEXT NOT NULL
            
        );
        """)
        conn.commit()

def delete(id_):
    with sqlite3.connect(DB) as c: c.execute("DELETE FROM Trainer WHERE id=?", (id_,))

def insert_Trainer(Trainer):
    with sqlite3.connect(DB) as conn:
        samples = [
            (Trainer.name, Trainer.vorname, Trainer.modulTeacher, "2, 3, 5", "21, 31, 51"),
        ]
        conn.executemany(
            "INSERT INTO Trainer (Name, Vorname, Module, Urlaub, BlockedWeeks) VALUES (?, ?, ?, ?, ?)",
            samples
        )
        conn.commit()

def get_all_Trainers():
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT id, Name, Vorname, Module, Urlaub, BlockedWeeks FROM Trainer")
        rows = cur.fetchall()
        for r in rows:
            print(r)
        return rows

def get_Trainer(id_):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT * FROM Trainer WHERE id=?", (id_,))
        row = cur.fetchone()
        return row


def change_absence(id_, toRemove):
    with sqlite3.connect(DB) as conn:
        conn.execute("SELECT Abwesenheiten FROM Trainer WHERE id = ?", (id_,))
        row = conn.fetchone()
        if not row:
            conn.close()
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
            f"UPDATE Trainer SET Abwesenheiten = ? WHERE id = ?",
            (neuer_text, id_)
        )

        conn.commit()
        conn.close()

        return neuer_text


def main():
    import ProvadisBuchungSystem.BckE.Modelle.Trainer as Trainer
    with sqlite3.connect(DB) as conn:
        #create_table(conn)
        #insert_sample(conn)
        #azubi = GFD.generate_azubi()
        #insert_Azubi(azubi)
        Trainer = Trainer.Trainer()
        Trainer.name = "Stark"
        Trainer.vorname = "Tony"
        Trainer.modulTeacher = "9, 10, 11"
        insert_Trainer(Trainer)

        print("Aktuelle Einträge in Trainer:")
        #print_all()

#if __name__ == "__main__":
#   main()
print(get_all_Trainers())

#create_table()