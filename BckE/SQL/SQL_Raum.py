import sqlite3
from datetime import date


from BckE.Modelle.Raum import Raum

DB = "test.db"

def create_table(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS Raum (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        PCRaum TEXT NOT NULL,
        BlockiertIn TEXT NOT NULL
    );
    """)
    conn.commit()

def delete(id_):
    with sqlite3.connect(DB) as c: c.execute("DELETE FROM Raum WHERE id=?", (id_,))

def insert_sample(conn):
    samples = [
        ("1.12", "True", ["6", "16", "45", "46", "47"]),
        ("1.11", "False", ["3", "5", "23", "12", "43"]),
        ("1.10", "True", ["1", "2", "4", "43", "52"]),
    ]
    conn.executemany(
        "INSERT INTO Raum (Name, PCRaum, BlockiertIn) VALUES (?, ?, ?, )",
        samples
    )
    conn.commit()

def insert_Raum(Raum):
    with sqlite3.connect(DB) as conn:
        blocked = ""
        for b in Raum.isBlocked:
            blocked += b + ", "
        samples = [
            (Raum.name, Raum.isPC, blocked)
        ]
        conn.executemany(
            "INSERT INTO Raum (Name, PCRaum, BlockiertIn) VALUES (?, ?, ?, )",
            samples
        )
        conn.commit()

def print_all():
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT Name, PCRaum, BlockiertIn FROM Raum")
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