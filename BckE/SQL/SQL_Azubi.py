import sqlite3
from datetime import date


from Modelle.Azubi import Azubi

DB = "WIP.db"

def create_table(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS Azubi (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Vorname TEXT NOT NULL,
        Ausbildungsunternehmen TEXT NOT NULL,
        StartDate TEXT NOT NULL,
        AttendedModules TEXT NOT NULL,
        Block TEXT NOT NULL
    );
    """)
    conn.commit()

def delete(id_):
    with sqlite3.connect(DB) as c: c.execute("DELETE FROM Azubi WHERE id=?", (id_,))

def insert_sample(conn):
    samples = [
        ("Müller", "Anna", "Firma A", "2024", "Modul1;Modul2", "A"),
        ("Schmidt", "Ben", "Firma B", "2025", "Modul1", "B"),
        ("Meier", "Clara", "Firma C", "2024", "Modul2;Modul3", "A"),
    ]
    conn.executemany(
        "INSERT INTO Azubi (Name, Vorname, Ausbildungsunternehmen, StartDate, AttendedModules, Block) VALUES (?, ?, ?, ?, ?, ?)",
        samples
    )
    conn.commit()

def insert_Azubi(Azubi):
    with sqlite3.connect(DB) as conn:
        attendedModstr = ""
        for m in Azubi.attendedModules:
            attendedModstr += m + ", "
        samples = [
            (Azubi.name, Azubi.vorname, Azubi.ausbildungsunternehmen, Azubi.ausbildungsStart, attendedModstr, Azubi.block),
        ]
        conn.executemany(
            "INSERT INTO Azubi (Name, Vorname, Ausbildungsunternehmen, StartDate, AttendedModules, Block) VALUES (?, ?, ?, ?, ?, ?)",
            samples
        )
        conn.commit()

def print_all():
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT id, Name, Vorname, Ausbildungsunternehmen, StartDate, AttendedModules, Block FROM Azubi")
        rows = cur.fetchall()
        for r in rows:
            print(r)
        return rows

def main():
    with sqlite3.connect(DB) as conn:
        create_table(conn)
        #insert_sample(conn)
        #azubi = GFD.generate_azubi()
        #insert_Azubi(azubi)
        print("Aktuelle Einträge in Azubi:")
        print_all()

#if __name__ == "__main__":
#    main()
with sqlite3.connect(DB) as conn:
    create_table(conn)