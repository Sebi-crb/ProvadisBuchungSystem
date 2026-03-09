import random
import BckE.SQL.config_Raum as Räume



räume = Räume.get_Räume()
"INSERT INTO Räume (Name, Plätze, IstPcRaum, Abwesenheiten) VALUES (?, ?, ?, ?)",
# Einen Raum über ID abrufen
räume[1]                    # → {'id': 1, 'name': 'Raum 1', ...}

# Einzelne Werte
räume[1]['name']            # → 'Raum 1'
räume[1]['Plätze']          # → '18'
räume[1]['pcKennzeichnung'] # → True

# Alle Räume durchlaufen
for id, raum in räume.items():
    print(raum['name'],raum['Plätze'], raum['pcKennzeichnung'])


# Nur Räume mit PC
mit_pc = {id: r for id, r in räume.items() if r['pcKennzeichnung']}

# Nur Räume ohne PC
ohne_pc = {id: r for id, r in räume.items() if not r['pcKennzeichnung']}

# Raum mit bestimmter Mindestanzahl Plätze
große_räume = {id: r for id, r in räume.items() if int(r['Plätze']) >= 24}





