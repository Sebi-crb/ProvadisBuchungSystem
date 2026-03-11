import sqlite3
from datetime import date
import BckE.SQL.config_Raum as import_Räume
from pathlib import Path
from BckE.Modelle.Raum import Raum

PROJECT_ROOT_NAME = "ProvadisBuchungSystem"
TARGET_SUBPATH = Path("BckE") / "SQL" / "Main.db"   # gewünschter Pfad ab Projektwurzel

here = Path(__file__).resolve()
proj_root = next((p for p in here.parents if p.name == PROJECT_ROOT_NAME), None)
if proj_root is None:
    raise RuntimeError(f"Projektordner '{PROJECT_ROOT_NAME}' nicht gefunden in {here}")

DB_PATH = proj_root / TARGET_SUBPATH
DB_PATH.parent.mkdir(parents=True, exist_ok=True)   # stellt sicher, dass Ordner existiert
DB = str(DB_PATH.resolve())

def create_table():
    with sqlite3.connect(DB) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS Raum (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Plätze TEXT NOT NULL,
            IstPcRaum TEXT NOT NULL,
            Abwesenheiten TEXT NOT NULL
        );
        """)
        conn.commit()



def delete(id_):
    with sqlite3.connect(DB) as c: c.execute("DELETE FROM Raum WHERE id=?", (id_,))

def insert_Räume():
    with sqlite3.connect(DB) as conn:
        Räume = import_Räume.get_Räume()
        for id, raum in Räume.items():
            samples = [
                (raum['name'], raum['Plätze'], raum['pcKennzeichnung'], ""),
            ]
            conn.executemany(
                "INSERT INTO Raum (Name, Plätze, IstPcRaum, Abwesenheiten) VALUES (?, ?, ?, ?)",
                samples
            )
            conn.commit()

def get_all_Rooms():
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT * FROM Raum")
        rows = cur.fetchall()
        #for r in rows:
        #    print(r)
        return rows

def get_Room(id_):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT * FROM Raum WHERE id=?", (id_,))
        row = cur.fetchone()
        return row


def get_room_IDs():
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT id FROM Raum")
        rows = cur.fetchall()
        result = []
        return rows

def get_room_absence(id_):
        with sqlite3.connect(DB) as conn:
            cur = conn.execute("SELECT Abwesenheiten FROM Raum WHERE id=?", (id_,))
            row = cur.fetchone()
            return row

def get_PCKennung(id_):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT IstPcRaum FROM Raum WHERE id=?", (id_,))
        row = cur.fetchone()
        bool = [int(x.strip()) for x in row[0].split(',') if x.strip()]

        if(bool[0] == 0):
            return False
        else:
            return True



def change_absence(id_, toRemove):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT Abwesenheiten FROM Raum WHERE id = ?", (id_,))
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
            "UPDATE Raum SET Abwesenheiten = ? WHERE id = ?",
            (neuer_text, id_)
        )

        return neuer_text


def add_absence(id_, toAdd):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT Abwesenheiten FROM Raum WHERE id = ?", (id_,))
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
            "UPDATE Raum SET Abwesenheiten = ? WHERE id = ?",
            (neuer_text, id_)
        )

        return neuer_text



def main():
    import BckE.Modelle.Trainer as Trainer
    with sqlite3.connect(DB) as conn:
        #create_table()
        #insert_sample(conn)
        #azubi = GFD.generate_azubi()
        #insert_Azubi(azubi)
        #insert_Räume()
        get_all_Rooms()
        #add_absence(1, [str(2), str(3), str(4)])
        #change_absence(1, [str(3)])

        #print("Aktuelle Einträge in Trainer:")
        #get_all_Trainers()
        #print_all()
#print(get_PCKennung(12))
#main()
#if __name__ == "__main__":
#main()
create_table()

