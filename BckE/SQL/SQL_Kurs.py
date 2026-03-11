import sqlite3
from pathlib import Path
from datetime import date
import BckE.Modelle.Trainer as Trainer
import BckE.SQL.SQL_Trainer as SQL_Trainer
import BckE.Calendar.Calendar_Trainer as Calendar_Trainer
import BckE.Calendar.Calendar_Azubi as Calendar_Azubi

import BckE.SQL.SQL_Gruppe as SQL_Gruppe
#from ProvadisBuchungSystem.BckE.Calendar.Calendar_Trainer import remove_absence



PROJECT_ROOT_NAME = "ProvadisBuchungSystem"
TARGET_SUBPATH = Path("BckE") / "SQL" / "WIP2.db"   # gewünschter Pfad ab Projektwurzel

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
        CREATE TABLE IF NOT EXISTS Kurse (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            GruppenID TEXT NOT NULL,
            StartDate DATETIME NOT NULL
            EndDate DATETIME NOT NULL,
            TrainerID Text NOT NULL,
            Raum Text NOT NULL,
            ModulID Text NOT NULL,
            
        );
        """)
        conn.commit()

def delete(id_):
    with sqlite3.connect(DB) as c: c.execute("DELETE FROM Gruppe WHERE id=?", (id_,))

def insert_Kurs(Kurs):
    with sqlite3.connect(DB) as conn:
        samples = [
            (Kurs.name, Kurs.gruppe, Kurs.start, Kurs.end, Kurs.trainer, Kurs.raum, Kurs.modul),
        ]
        conn.executemany(
            "INSERT INTO Kurse (Name, GruppenID, StartDate, EndDate, TrainerID, Raum, ModulID) VALUES (?, ?, ?, ?, ?, ?, ?)",
            samples
        )
        conn.commit()

def get_all_Kurse():
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT * FROM Kurse")
        rows = cur.fetchall()
        #for r in rows:
            #print(r)
        return rows

def get_Kurs(id_):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT * FROM Kurse WHERE id=?", (id_,))
        row = cur.fetchone()
        return row

def get_kurs_start(id_):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT StartDate FROM Kurse WHERE id=?", (id_,))
        row = cur.fetchone()
        return row

def get_kurs_end(id_):
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("SELECT EndDate FROM Kurse WHERE id=?", (id_,))
        row = cur.fetchone()
        return row


def update_course_dates( id_, start_date_, end_date_):
    """
    Updates StartDate and EndDate for a given course.
    """
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    query = """
        UPDATE Kurse
        SET StartDate = ?, 
            EndDate = ?
        WHERE id = ?;
    """

    # Convert date objects to ISO strings (SQLite-friendly)
    cursor.execute(query, (start_date_.isoformat(), end_date_.isoformat(), id_))

    conn.commit()
    conn.close()


def drop_table():
    with sqlite3.connect(DB) as conn:
        cur = conn.execute("DROP TABLE IF EXISTS Kurse")
        conn.commit()
        conn.close()
        create_table()

def insert_kurs_dates_into_trainer(trainerID_, start_date_, end_date_):
    trainer_cal = Calendar_Trainer.createCal()
    key_of_start_date = get_key_for_date(trainer_cal, start_date_)
    key_of_end_date = get_key_for_date(trainer_cal, end_date_)
    absences = list(range(key_of_start_date, key_of_end_date + 1))
    SQL_Trainer.add_absence(trainerID_, absences)


def insert_kurs_dates_into_gruppen(gruppenID_, start_date_, end_date_):
    block_tup = SQL_Gruppe.get_block(gruppenID_)
    block = block_tup[0]
    a_calendar = Calendar_Azubi.createAzubiCal(block)
    key_of_start_date = get_key_for_date(a_calendar, start_date_)
    key_of_end_date = get_key_for_date(a_calendar, end_date_)
    absences = list(range(key_of_start_date, key_of_end_date + 1))
    SQL_Gruppe.add_absence(gruppenID_, absences)




def get_key_for_date(dates_dict, target_date):
    for key, value in dates_dict.items():
        if value == target_date:
            return key
    return None

insert_kurs_dates_into_gruppen(1, date(2025, 9, 1), date(2025, 9, 3))

#insert_kurs_dates_into_trainer(1, date(2025, 9, 1), date(2025, 9, 3))


def main():
    import BckE.Modelle.Trainer as Trainer
    with sqlite3.connect(DB) as conn:

        print("Aktuelle Einträge in Trainer:")
        #get_all_Trainers()
        #print_all()

#main()
#if __name__ == "__main__":
#main()
#print(get_all_Trainers())

#create_table()