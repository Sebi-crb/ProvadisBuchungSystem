import sqlite3
from datetime import date


from BckE.Modelle.Gruppe import Gruppe

DB = "WIP2.db"

def create_table(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS Gruppe (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Block TEXT NOT NULL,
        Azubis TEXT NOT NULL,
        AttendedModules TEXT NOT NULL       
    );
    """)
    conn.commit()

def delete(id_):
    with sqlite3.connect(DB) as c: c.execute("DELETE FROM Gruppe WHERE id=?", (id_,))

def insert_sample(conn):
    samples = [
        ("Müller", "Anna", "Firma A", "2024", "Modul1;Modul2", "A"),
        ("Schmidt", "Ben", "Firma B", "2025", "Modul1", "B"),
        ("Meier", "Clara", "Firma C", "2024", "Modul2;Modul3", "A"),
    ]
    conn.executemany(
        "INSERT INTO Gruppe (Name, Block, Azubis, AttendedModules) VALUES (?, ?, ?)",
        samples
    )
    conn.commit()

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
            (Gruppe.name, Gruppe.block, azubiListstr, attendedModstr),
        ]
        conn.executemany(
            "INSERT INTO Gruppe (Name, Block, Azubis, AttendedModules) VALUES (?, ?, ?, ?)",
        samples
        )
        conn.commit()

def get_all():
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT id, Name, Block, Azubis, AttendedModules FROM Gruppe")
        rows = cur.fetchall()
        for r in rows:
            print(r)
        return rows

def drop_table():
    with sqlite3.connect(DB) as conn:
        conn.execute("DROP TABLE IF EXISTS Gruppe")
        conn.commit()

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