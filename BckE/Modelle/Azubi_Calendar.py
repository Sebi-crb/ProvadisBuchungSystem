from datetime import date, timedelta
from typing import List, Tuple, Dict

# ---------- Hilfsfunktionen ----------
def daterange(start: date, end: date):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)

def iso_week_key(d: date) -> Tuple[int,int]:
    # returns (iso_year, iso_week)
    y, w, _ = d.isocalendar()
    return (y, w)

# Easter (Anonymous Gregorian algorithm)
def easter_sunday(year: int) -> date:
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19*a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2*e + 2*i - h - k) % 7
    m = (a + 11*h + 22*l) // 451
    month = (h + l - 7*m + 114) // 31
    day = ((h + l - 7*m + 114) % 31) + 1
    return date(year, month, day)

# ---------- Feiertage Hessen (berechnet) ----------
def hessen_holidays(year: int) -> List[date]:
    e = easter_sunday(year)
    holidays = []
    # feste Feiertage
    fixed = [
        (1, 1),    # Neujahr
        (5, 1),    # Tag der Arbeit
        (10, 3),   # Tag der Deutschen Einheit
        (12, 25),  # 1. Weihnachtstag
        (12, 26),  # 2. Weihnachtstag
    ]
    for m, d in fixed:
        holidays.append(date(year, m, d))
    # bewegliche Feiertage
    holidays += [
        e - timedelta(days=2),   # Karfreitag
        e + timedelta(days=1),   # Ostermontag
        e + timedelta(days=39),  # Christi Himmelfahrt (39 Tage nach Ostersonntag)
        e + timedelta(days=50),  # Pfingstmontag (50 Tage nach Ostersonntag)
        e + timedelta(days=60),  # Fronleichnam (60 Tage nach Ostersonntag)
    ]
    # Hinweis: Manche Feiertage (z.B. Neujahr) können in Jahreswechsel fallen.
    # Wenn wir Feiertage für ein Schuljahr brauchen, rufen wir hessen_holidays für beide Jahre ab.
    return sorted(holidays)

# ---------- Schulferien (als Liste von (start,end) tuples) ----------
# Default: Beispielwerte für Schuljahr 2025/26 aus Kultus Hessen (kann angepasst werden).
# Quelle: Kultusministerium Hessen Ferientermine.
def default_hessen_vacations_for_schoolyear(start_year: int) -> List[Tuple[date,date]]:
    # start_year = 2025 -> Schuljahr 2025/26
    # Diese Daten sind exemplarisch; für andere Jahre anpassen oder als Parameter übergeben.
    if start_year == 2025:
        return [
            (date(2025,10,6), date(2025,10,18)),   # Herbstferien
            (date(2025,12,22), date(2026,1,10)),   # Weihnachtsferien
            (date(2026,3,30), date(2026,4,10)),    # Osterferien
            (date(2026,6,29), date(2026,8,7)),     # Sommerferien
            # bewegliche Ferientage können zusätzlich angegeben werden
        ]
    # Fallback: keine Ferien (Aufrufer sollte reale Daten übergeben)
    return []

# ---------- Wochen- und Blocklogik ----------
def weeks_in_schoolyear(start_year: int) -> List[Tuple[date,date]]:
    start = date(start_year, 9, 1)
    end = date(start_year + 1, 8, 31)
    # Wir erzeugen Wochen als Montag-Sonntag
    # Bestimme ersten Montag <= start
    first_monday = start
    while first_monday.weekday() != 0:  # 0 = Monday
        first_monday -= timedelta(days=1)
    weeks = []
    wstart = first_monday
    while wstart <= end:
        wend = wstart + timedelta(days=6)
        weeks.append((max(wstart, start), min(wend, end)))
        wstart += timedelta(days=7)
    return weeks

def assign_blocks(weeks: List[Tuple[date,date]], start_block: str = "A") -> Dict[Tuple[date,date], str]:
    # Blocks rotate A,B,C; each block lasts 2 weeks.
    order = ["A","B","C"]
    idx = order.index(start_block)
    block_map = {}
    i = 0
    for w in weeks:
        # every two weeks same block
        block = order[(idx + (i // 2)) % 3]
        block_map[w] = block
        i += 1
    return block_map

# ---------- Verfügbarkeitsprüfung ----------
def week_has_more_than_two_holidays(week: Tuple[date,date], holidays: List[date]) -> bool:
    s, e = week
    count = sum(1 for h in holidays if s <= h <= e)
    return count > 2

def week_overlaps_vacation(week: Tuple[date,date], vacations: List[Tuple[date,date]]) -> bool:
    s, e = week
    for vs, ve in vacations:
        if not (ve < s or vs > e):
            return True
    return False

def is_week_before_silvester(week: Tuple[date,date]) -> bool:
    s, e = week
    # Bestimme ISO-Woche, die den 31.12. enthält
    year_for_silvester = s.year
    # 31.12 kann in ISO-Woche des Jahres s.year oder s.year-1 depending on week
    silvester = date(year_for_silvester, 12, 31)
    iso_sil = iso_week_key(silvester)
    # Falls die Woche in einem anderen ISO-Jahr liegt, prüfen wir beide relevanten Jahre:
    # Wir compute week_before as iso_week - 1 (with wrap to previous iso_year if needed)
    iso_year, iso_week = iso_sil
    # compute week_before key
    if iso_week > 1:
        week_before = (iso_year, iso_week - 1)
    else:
        # need last ISO week of previous year
        last_day_prev = date(iso_year - 1, 12, 31)
        week_before = iso_week_key(last_day_prev)
    return iso_week_key(s) == week_before

def check_availability_for_period(
    start_date: date,
    end_date: date,
    start_block: str = "A",
    holidays_override: List[date] = None,
    vacations_override: List[Tuple[date,date]] = None
) -> Dict:
    # Determine schoolyear start year from start_date (if start_date between 1 Sep and 31 Aug next year)
    if start_date.month >= 9:
        sy = start_date.year
    else:
        sy = start_date.year - 1
    weeks = weeks_in_schoolyear(sy)
    block_map = assign_blocks(weeks, start_block=start_block)
    # collect holidays for both calendar years involved
    holidays = []
    holidays += hessen_holidays(sy)
    holidays += hessen_holidays(sy + 1)
    if holidays_override:
        holidays = sorted(set(holidays + holidays_override))
    vacations = default_hessen_vacations_for_schoolyear(sy)
    if vacations_override:
        vacations = vacations_override

    # iterate weeks overlapping the requested period
    relevant_weeks = [w for w in weeks if not (w[1] < start_date or w[0] > end_date)]
    results = []
    overall_available = True
    reasons = []
    for w in relevant_weeks:
        s, e = w
        block = block_map[w]
        week_holidays = [h for h in holidays if s <= h <= e]
        in_vacation = week_overlaps_vacation(w, vacations)
        before_silvester = is_week_before_silvester(w)
        too_many_holidays = len(week_holidays) > 2

        week_available = True
        if in_vacation:
            week_available = False
            reasons.append(f"Woche {s}–{e}: Ferien")
        if before_silvester:
            week_available = False
            reasons.append(f"Woche {s}–{e}: Woche vor Silvester")
        if too_many_holidays:
            week_available = False
            reasons.append(f"Woche {s}–{e}: mehr als 2 Feiertage ({len(week_holidays)})")

        if not week_available:
            overall_available = False

        results.append({
            "week_start": s,
            "week_end": e,
            "block": block,
            "holidays": week_holidays,
            "in_vacation": in_vacation,
            "before_silvester": before_silvester,
            "too_many_holidays": too_many_holidays,
            "available": week_available
        })

    return {
        "schoolyear_start": sy,
        "weeks_checked": len(relevant_weeks),
        "overall_available": overall_available,
        "reasons": reasons,
        "details": results
    }

# ---------- Beispielaufruf ----------
if __name__ == "__main__":
    # Beispiel: Prüfe Verfügbarkeit für Zeitraum 01.12.2025 - 15.01.2026 im Schuljahr 2025/26, Startblock A
    start = date(2025, 12, 1)
    end = date(2026, 1, 15)
    report = check_availability_for_period(start, end, start_block="A")
    print("Overall available:", report["overall_available"])
    for d in report["details"]:
        print(d["week_start"], "-", d["week_end"], "Block", d["block"], "Available:", d["available"],
              "Holidays:", [h.isoformat() for h in d["holidays"]])
    if report["reasons"]:
        print("Gründe (erste 10):")
        for r in report["reasons"][:10]:
            print("-", r)
