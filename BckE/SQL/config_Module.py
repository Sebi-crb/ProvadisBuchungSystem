from datetime import date

modules = {}
modules : dict



Basis_Softwarelogik = {
    "id": 1,
    "name": "Basis_Softwarelogik",
    "beschreibung":
        "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete Lernergebnisse "
        "und zu erwerbende Kompetenzen): - Sie verstehen die Grundprinzipien der Informatik. - Sie verfügen über die "
        "Fähigkeit zur Abstraktion von realen Problemstellungen. - Sie kennen die Basismethoden zur Modellierung von "
        "Anwendungsszenarien mit dem Ziel der softwaretechnischen Umsetzung - unabhängig von einer konkreten "
        "Programmier-sprache. - Sie verfügen über ein universelles Verständnis der Logik von Anwendungs¬programmen "
        "und ihrer standardisierten Darstellungsformen. - Sie sind befähigt, Möglichkeiten und Prinzipien des "
        "Einsatzes von Softwaresystemen in Unternehmen zu erkennen und zu bewerten. - Sie sind befähigt, sich schnell "
        "in aktuelle Programmier¬sprachen einzuarbeiten. - Sie kennen Standard-Algorithmen und -Datenstrukturen, "
        "können die Leistungsfähigkeit verschiedener Verfahren und Strukturen beurteilen und Varianten bedarfsgerecht "
        "entwerfen und implementieren. - Sie können selbstständig Algorithmen erklären und deren Einsatz vermitteln."
    ,
    "dauer": "5",
    "zuordnungLernjahr": "1",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [],
    "pcKennzeichnung": False,
}


UML_Applikationsdesign = {
    "id": 2,
    "name": "UML-Applikationsdesign",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete "
                    "Lernergebnisse und zu erwerbende Kompetenzen): - Sie verstehen die Grundbegriffe des "
                    "objektorientierten Softwareentwurfs und des modellgestützten Softwaredesigns. - Sie sind "
                    "befähigt, eigenständig Analysen bezüglich Softwareanforderungen durchzuführen. - Sie können "
                    "erforderliche Objekte des jeweiligen Anwendungsgebietes (Fachklassen) identifizieren und "
                    "erstellen. - Sie kennen die wichtigsten UML-Diagramme und UML-Modelle, die für die "
                    "Anforderungsanalyse und das Applikationsdesign verwendet werden können und kennen deren "
                    "Zusammenhänge. - Sie lernen die Vorgehensweisen und das Zusammenwirken von objektorientierter "
                    "Analyse (OOA), objektorientiertem Design (OOD) und objektorientierter Programmierung (OOP) "
                    "kennen.",
    "dauer": "5",
    "zuordnungLernjahr": "1",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": ["1"],
    "pcKennzeichnung": False,
}


Software_Engineering = {
    "id": 3,
    "name": "Software-Engineering",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete "
                    "Lernergebnisse und zu erwerbende Kompetenzen): - Durch die grundlegende Programmierausbildung "
                    "sind sie in die Lage, sich schnell in neue Programmiersprachen einzuarbeiten und bei ersten "
                    "Praxiseinsätzen in Softwareentwicklungsprojekten mitzuarbeiten. - Sie können eigenständig "
                    "fachliche Anforderungen und bestehende Prozesse analysieren und aufgrund ihrer Analyse "
                    "erfolgreich Konzepte zur Umsetzung entwickeln. - Sie kennen den gesamten "
                    "Softwareentstehungsprozess und auch die Gefahren bei der Durchführung von "
                    "Softwareentwicklungsprojekten. - Sie können Methoden und Prinzipien des klassischen und agilen "
                    "Software-Entwicklungs-prozesses anwenden und diese auch in bestehende Teams einbringen. ",
    "dauer": "5",
    "zuordnungLernjahr": "2",
    "optionaleVorgängermodule": ["4"],
    "verpflichtendeVorgängermodule": ["1","2"],
    "pcKennzeichnung": True,
}

Softwareentwicklung = {
    "id": 4,
    "name": "Softwareentwicklung",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete "
                    "Lernergebnisse und zu erwerbende Kompetenzen): - Sie haben eine grundlegende, praxisorientierte "
                    "Programmierausbildung in den drei weit verbreiteten Programmiersprachen Java, C# und Python. - "
                    "Sie kennen die praktische, programmiersprachen-unabhängige Anwendung objekt-orientierter "
                    "Ansätze und die effiziente Verwendung von Frameworks und Klassen-bibliotheken. - Sie sind in "
                    "der Lage, komplexe Aufgabenstellungen zu analysieren, Lösungs¬algorithmen umzusetzen und die "
                    "passende Entwicklungsumgebung auszuwählen. - Sie verstehen es, eigenständig und kommunikativ im "
                    "Team moderne Frontend-, Backend- und Desktopsoftware zu designen und nach einer strukturierten "
                    "Vorgehensweise zu realisieren. - Sie können sich schnell in den Quellcode bestehender Software "
                    "einarbeiten und somit die Pflege, Weiterentwicklung oder Konvertierung älterer Anwendungen "
                    "sicherstellen.",
    "dauer": "5",
    "zuordnungLernjahr": {"name": "Lernjahr", "unavailable": []},
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": ["1","2"],
    "pcKennzeichnung": True,
}

Softwareprojekt = {
    "id": 5,
    "name": "Softwareprojekt",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete "
                    "Lernergebnisse und zu erwerbende Kompetenzen): - Sie haben eine grundlegende, praxisorientierte "
                    "Programmierausbildung in den drei weit verbreiteten Programmiersprachen Java, C# und Python. - "
                    "Sie kennen die praktische, programmiersprachen-unabhängige Anwendung objekt-orientierter "
                    "Ansätze und die effiziente Verwendung von Frameworks und Klassen-bibliotheken. - Sie sind in "
                    "der Lage, komplexe Aufgabenstellungen zu analysieren, Lösungs¬algorithmen umzusetzen und die "
                    "passende Entwicklungsumgebung auszuwählen. - Sie verstehen es, eigenständig und kommunikativ im "
                    "Team moderne Frontend-, Backend- und Desktopsoftware zu designen und nach einer strukturierten "
                    "Vorgehensweise zu realisieren. - Sie können sich schnell in den Quellcode bestehender Software "
                    "einarbeiten und somit die Pflege, Weiterentwicklung oder Konvertierung älterer Anwendungen "
                    "sicherstellen.",
    "dauer": "10",
    "zuordnungLernjahr": "2",
    "optionaleVorgängermodule": ["3"],
    "verpflichtendeVorgängermodule": ["1","2"],
    "pcKennzeichnung": True,
}

Datenbanken_SQL = {
    "id": 6,
    "name": "Datenbank-SQL",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete "
                    "Lernergebnisse und zu erwerbende Kompetenzen): - Sie haben eine umfassende, "
                    "herstellerunabhängige Datenbankausbildung. - Sie verstehen Aufgaben, Einsatz und technische "
                    "Grundkonzepte von Datenbanksystemen. - Sie sind in die Lage, bestehende relationale "
                    "Datenmodelle zu analysieren und zu interpretieren. - Sie können neue Datenmodelle aufgrund "
                    "praktischer, abstrakter Problemstellungen konzipieren, erstellen und in gängigen "
                    "Datenbank-Management-Systemen (DBMS) implementieren. - Sie wissen die Rahmenbedingungen und "
                    "Komplexität praktischer Datenbank-Projekte einzuschätzen. - Sie können die Konzepte einer "
                    "Datenbankprogrammiersprache bei der Lösung von praktischen Datenbankaufgaben anwenden.",
    "dauer": "10",
    "zuordnungLernjahr": "1",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [],
    "pcKennzeichnung": True,
}

Projektmanagement = {
    "id": 7,
    "name": "Projektmanagement",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete "
                    "Lernergebnisse und zu erwerbende Kompetenzen): - Sie haben eine grundlegende und handlungsorientierte "
                    "Projektmanagement¬ausbildung. - Sie sind in die Lage, im Betrieb in komplexen Projekten mitzuarbeiten "
                    "und in überschaubaren Projekten erste Erfahrungen in Projektleitungsaufgaben zu sammeln. - Sie kennen "
                    "neben Methoden und Standards des klassischen Projektmanagements auch die Verwendung von agilen Methoden "
                    "und Vorgehens¬modellen. - Sie können Vor- und Nachteile von klassischen und agilen Tools und Techniken "
                    "bewerten und wissen diese erfolgreich anzuwenden sowie zielgerichtet in bestehende Projekte "
                    "einzubringen.",
    "dauer": "5",
    "zuordnungLernjahr": "3",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [],
    "pcKennzeichnung": True,
}


IT_Security = {
    "id": 8,
    "name": "IT_Security",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete "
                    "Lernergebnisse und zu erwerbende Kompetenzen): - Sie sind in der Lage, verschiedene "
                    "Problemszenarien zu erkennen und leiten daraus entsprechende Maßnahmen ab. - Sie erkennen "
                    "mögliche Bedrohungen und sind in der Lage, Präventivmaßnahmen zu generieren. - Sie sind mit den "
                    "Themen Datensicherheit und -sicherung vertraut und können diese umsetzen. - Sie kennen die "
                    "rechtlichen Grundlagen im Unternehmensumfeld. - Sie sind in der Lage, eigenständig "
                    "Responsestrategien zu entwickeln.",
    "dauer": "5",
    "zuordnungLernjahr": "2",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [],
    "pcKennzeichnung": True,
}

Netzwerke = {
    "id": 9,
    "name": "Netzwerke",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete "
                    "Lernergebnisse und zu erwerbende Kompetenzen): - Sie kennen gängige Netzwerkprotokolle und "
                    "deren Abläufe bzw. Einsatzzwecke. - Durch ihr erworbenes Wissen über verschiedene "
                    "Netzwerkkomponenten können sie Netze planen. - Sie können Fehlerquellen identifizieren und "
                    "beheben. Bei der Fehlersuche in Netzwerksystemen hilft ihnen das erworbene Fachwissen über "
                    "mögliche Fehlerquellen. - Sie kennen die Grundlagen der Entwicklung vom physischen Host zur "
                    "virtualisierten Architektur. - Sie können einen Windows-Client aufsetzen und in Betrieb nehmen.",
    "dauer": "5",
    "zuordnungLernjahr": "2",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [],
    "pcKennzeichnung": True,
}


Web_Design_Programmierung = {
    "id": 10,
    "name": "Web-Design-Programmierung",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete "
                    "Lernergebnisse und zu erwerbende Kompetenzen): - Sie sind vertraut mit den grundsätzlichen "
                    "Techniken eines Web-Auftritts. - Sie kennen Aufbau und Funktionsweise von statischen und "
                    "dynamischen Webseiten. - Sie beherrschen den Umgang mit HTML5 und Cascading Style Sheets ("
                    "CSS3). - Sie können dynamische Webseiten mittels JavaScript und PHP erstellen und diese auf "
                    "einem Web-Server veröffentlichen. - Sie sind in der Lage mittels einer verbreiteten "
                    "Programmiersprache einfache, Server-basierte Programme zu entwickeln. - Sie können einfache "
                    "externe Quellen (Beispiel: Datenbankverbindungen) einfügen",
    "dauer": "10",
    "zuordnungLernjahr": "1",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [],
    "pcKennzeichnung": True,
}

modules = {
    1: Basis_Softwarelogik,
    2: UML_Applikationsdesign,
    3:Software_Engineering,
    4:Softwareentwicklung,
    5:Softwareprojekt,
    6:Datenbanken_SQL,
    7:Projektmanagement,
    8:IT_Security,
    9:Netzwerke,
    10:Web_Design_Programmierung
}

def get_Modules():
    return modules

def get_name(id):
    return modules[id]['name']

