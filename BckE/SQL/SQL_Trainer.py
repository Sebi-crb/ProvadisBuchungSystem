import sqlite3
from datetime import date
import Modelle.Trainer


from Modelle.Trainer import Trainer

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

def print_all():
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT id, Name, Vorname, Module, Urlaub, BlockedWeeks FROM Trainer")
        rows = cur.fetchall()
        for r in rows:
            print(r)
        return rows

def main():
    with sqlite3.connect(DB) as conn:
        #create_table(conn)
        #insert_sample(conn)
        #azubi = GFD.generate_azubi()
        #insert_Azubi(azubi)
        Trainer = Modelle.Trainer.Trainer()
        Trainer.name = "Stark"
        Trainer.vorname = "Tony"
        Trainer.modulTeacher = "9, 10, 11"
        insert_Trainer(Trainer)

        print("Aktuelle Einträge in Trainer:")
        print_all()

#if __name__ == "__main__":
#   main()
print_all()

#create_table()