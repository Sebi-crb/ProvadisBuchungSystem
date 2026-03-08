import sqlite3
from datetime import date
from BckE.Modelle.Modul import Modul


from BckE.Modelle.Gruppe import Gruppe

DB = "WIP2.db"

def create_table(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS Modul (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Beschreibung TEXT NOT NULL,
        Lehrjahr INTEGER NOT NULL,
        OptionaleVorgängerModule TEXT NOT NULL,
        VerpflichtendeVorgängerModule TEXT NOT NULL,
        _PcKennzeichnung Text NOT NULL,  
    );
    """)
    conn.commit()

def delete(id_):
    with sqlite3.connect(DB) as c: c.execute("DELETE FROM Modul WHERE id=?", (id_,))

def insert_Modul(Modul):
    with sqlite3.connect(DB) as conn:
        OptModule = ""
        for i, o in enumerate(Modul.optionaleVorgängermodule):
            if (i == len(Modul.optionaleVorgängermodule) - 1):
                VerModule += str(o)
            else:
                VerModule += str(o) + ", "
        VerModule = ""
        for i, v in enumerate(Modul.verpflichtendeVorgängermodule):
            if(i == len(Modul.verpflichtendeVorgängermodule) - 1):
                VerModule += str(v)
            else:
                VerModule += str(v) + ", "
        samples = [
            (Modul.name, Modul.beschreibung, Modul.zuordnungLernjahr, Modul.optionaleVorgängermodule, Modul.verpflichtendeVorgängermodule, Modul.pcKennzeichnung),
        ]
        conn.executemany(
            "INSERT INTO Modul (Name, Beschreibung, Lehrjahr, OptionaleVorgängerModule, VerpflichtendeVorgängerModule, _PcKennzeichnung) VALUES (?, ?, ?, ?, ?, ?)",
        samples
        )
        conn.commit()

def get_all():
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT * FROM Modul")
        rows = cur.fetchall()
        #for r in rows:
            #print(r)
        return rows

def drop_table():
    with sqlite3.connect(DB) as conn:
        conn.execute("DROP TABLE IF EXISTS Modul")
        conn.commit()

def main():
    with sqlite3.connect(DB) as conn:
        create_table(conn)
        #insert_sample(conn)
        #azubi = GFD.generate_azubi()
        #insert_Azubi(azubi)
        drop_table()
        print("Aktuelle Einträge in Modul:")
        get_all()

#if __name__ == "__main__":
#    main()

#drop_table()
with sqlite3.connect(DB) as conn:
    create_table(conn)