import sqlite3
from datetime import date
from pathlib import Path

from BckE.Modelle.Gruppe import Gruppe

PROJECT_ROOT_NAME = "ProvadisBuchungSystem"
TARGET_SUBPATH = Path("BckE") / "SQL" / "WIP2.db"   # gewünschter Pfad ab Projektwurzel

here = Path(__file__).resolve()
proj_root = next((p for p in here.parents if p.name == PROJECT_ROOT_NAME), None)
if proj_root is None:
    raise RuntimeError(f"Projektordner '{PROJECT_ROOT_NAME}' nicht gefunden in {here}")

DB_PATH = proj_root / TARGET_SUBPATH
DB_PATH.parent.mkdir(parents=True, exist_ok=True)   # stellt sicher, dass Ordner existiert
DB = str(DB_PATH.resolve())

def create_table(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS Gruppe (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Block TEXT NOT NULL,
        Azubis TEXT NOT NULL,
        AttendedModules TEXT NOT NULL,
        Abwesenheiten TEXT        
    );
    """)
    conn.commit()

def delete(id_):
    with sqlite3.connect(DB) as c: c.execute("DELETE FROM Gruppe WHERE id=?", (id_,))


def insert_AzubiGruppe(Gruppe):
    with sqlite3.connect(DB) as conn:
        attendedModstr = ""
        for i, m in enumerate(Gruppe.attendedModules):
            if (i == len(Gruppe.attendedModules) - 1):
                attendedModstr += m
            else:
                attendedModstr += m + ", "
        azubiListstr = ""
        for i, a in enumerate(Gruppe.azubiList):
            if(i == len(Gruppe.azubiList) - 1):
                azubiListstr += str(a)
            else:
                azubiListstr += str(a) + ", "

        samples = [
            (Gruppe.name, Gruppe.block, azubiListstr, attendedModstr, ""),
        ]
        conn.executemany(
            "INSERT INTO Gruppe (Name, Block, Azubis, AttendedModules, Abwesenheiten) VALUES (?, ?, ?, ?, ?)",
        samples
        )
        conn.commit()

def get_all():
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT id, Name, Block, Azubis, AttendedModules, Abwesenheiten FROM Gruppe")
        rows = cur.fetchall()
        #for r in rows:
            #print(r)
        return rows

def get_block(id_):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT Block FROM Gruppe WHERE id=?", (id_,))
        row = cur.fetchone()
        return row

def drop_table():
    with sqlite3.connect(DB) as conn:
        conn.execute("DROP TABLE IF EXISTS Gruppe")
        conn.commit()
        create_table(conn)

def add_absence(id_, toAdd):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT Abwesenheiten FROM Gruppe WHERE id = ?", (id_,))
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
            "UPDATE Gruppe SET Abwesenheiten = ? WHERE id = ?",
            (neuer_text, id_)
        )

        return neuer_text


def main():
    with sqlite3.connect(DB) as conn:
        create_table(conn)
        #insert_sample(conn)
        #azubi = GFD.generate_azubi()
        #insert_Azubi(azubi)
        drop_table()
        print("Aktuelle Einträge in Gruppe:")
        get_all()

#if __name__ == "__main__":
#    main()

#drop_table()
with sqlite3.connect(DB) as conn:
    create_table(conn)
#print(get_all())