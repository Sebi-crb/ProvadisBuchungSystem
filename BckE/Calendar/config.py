"""
Alle Daten in einer Datei
"""
from datetime import date

# TRAINER
TRAINERS = {
    "T001": {"name": "Herr Schmidt", "unavailable": [date(2026, 9, 7)]},
    "T002": {"name": "Frau Müller", "unavailable": []},
}

# MODULE (Kurse)
MODULES = {
    "M001": {"name": "Python", "trainer": "T001", "days": 5},
    "M002": {"name": "Datenbanken", "trainer": "T002", "days": 3},
}

# BLÖCKE
BLOCKS = ["A", "B", "C"]

# KURSE = Modul + Block
COURSES = [
    {"module": "M001", "block": "BlockA"},
    {"module": "M001", "block": "BlockB"},
    {"module": "M002", "block": "BlockA"},
]

# SCHULJAHR
SCHOOL_YEAR_START = date(2026, 9, 1)
SCHOOL_YEAR_END = date(2027, 8, 31)

# FERIEN (einfach als Liste)
HOLIDAYS = [
    date(2026, 10, 3),  # Feiertag
    date(2026, 12, 25),  # Weihnachten
]

# Ferienzeiten
HOLIDAY_RANGES = [
    (date(2026, 10, 5), date(2026, 10, 16)),    # Herbstferien
    (date(2026, 12, 21), date(2027, 1, 8)),     # Weihnachtsferien
]