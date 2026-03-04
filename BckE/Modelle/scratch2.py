import random
from datetime import date

def random_start_date(min_year=2023, max_year=2026):
    y = random.randint(min_year, max_year)
    return date(y, 9, 1)

def lehrjahr(start_date: date, ref: date | None = None, max_year: int | None = 3) -> int:
    if ref is None:
        ref = date.today()
    # Lehrjahr zählt akademisch ab 01.09.: +1, wenn Referenzmonat >= September
    y = ref.year - start_date.year + (1 if ref.month >= 9 else 0)
    if y < 1:
        y = 1
    if max_year is not None and y > max_year:
        y = max_year
    return y

# Beispiel
sd = random_start_date(2023, 2025)
print(sd.isoformat(), "-> Lehrjahr", lehrjahr(sd))
