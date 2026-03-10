from datetime import date

def ist_mindestens_eine_woche_her(datum1, datum2):
    # Die Subtraktion liefert ein timedelta-Objekt zurück
    differenz = abs((datum1 - datum2).days)
    return differenz >= 7, differenz

# Beispielanwendung
d1 = date(2026, 3, 1)
d2 = date(2026, 3, 8)

if ist_mindestens_eine_woche_her(d1, d2):
    print(ist_mindestens_eine_woche_her(d1, d2))