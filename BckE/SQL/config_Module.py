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
    "zuordnungLernjahr": "1",
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
    "zuordnungLernjahr": "1",
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

Office_Professional_Teil_1 = {
    "id": 11,
    "name": "Office Professional Teil 1",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu folgendem in der Lage (erwartete "
                    "Lernergebnisse und zu erwerbenden Kompetenzen): - Sie sind in der Lage, die Applikationen der Office-"
                    "Suite zielführend und effizient in üblichen Szenarien einzusetzen. - Sie verfügen über erweitere "
                    "Kenntnisse der Textverarbeitung, Tabellenkalkulation und Kommunikations- / Organisationssoftware. "
                    "- Sie sind in der Lage, neue Funktionen eigenständig zu erschließen und anzuwenden.",
    "dauer": "5",
    "zuordnungLernjahr": "1",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [],
    "pcKennzeichnung": True,
}

Office_Professional_Teil_2 = {
    "id": 12,
    "name": "Office Professional Teil 2",
    "beschreibung": "Sie sind in der Lage erweiterte Funktionen der Office-Programme zu nutzen, um IT spezifische Themengebiete" 
                    "optimal zu behandeln. - Sie sind in der Lage mit einer Vielzahl von Daten umzugehen, diese in den Office-"
                    "Programmen auszuwerten, zu analysieren und adäquat darzustellen - Sie sind in derLage Dokumente zu designen."
                    "- Sie sind in der Lage ein Zusammenspiel innerhalb eines Dokumentes mithilfe anderer Office-Programme herzustellen."
                    "- Sie sind in der Lage Grafiken und Bilder aufzubereiten und Office-Dokumente gestalterisch zu entwickeln.",
    "dauer": "5",
    "zuordnungLernjahr": "1",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [11],
    "pcKennzeichnung": True,
}

Arbeitssicherheit = {
    "id": 13,
    "name": "Arbeitssicherheit",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete"
                    "Lernergebnisse und zu erwerbende Kompetenzen): - Sie kennen die rechtlichen Grundlagen, die die"
                    "Sicherheit betreffen.- Sie werden für mögliche Gefahrenquellen im Unternehmensumfeld / Büro"
                    "sensibilisiert.- Sie können Gefährdungen vermeiden.",
    "dauer": "3",
    "zuordnungLernjahr": "1",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [],
    "pcKennzeichnung": True,
}

Lerntechniken = {
    "id": 14,
    "name": "Lerntechniken",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete "
                    "Lernergebnisse und zu erwerbende Kompetenzen): - Sie sind in der Lage, eine für sie geeignete "
                    "Lernumgebung zu schaffen. - Sie können ihre Voraussetzungen zum Lernen - wie Motivation, "
                    "Konzentration und Disziplin - reflektieren, bewerten und weiterentwickeln. - Sie können den eigenen "
                    "Lerntyp einschätzen und kennen Techniken um zu lernen. - Sie kennen verschiedene praktische "
                    "Methoden passend zum eigenen Lerntyp. - Sie sind in der Lage, sich durch Methodensammlung und "
                    "Quellenverzeichnis selbstständig weitere Methoden anzueignen.",
    "dauer": "3",
    "zuordnungLernjahr": "1",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [],
    "pcKennzeichnung": True,
}

Präsentieren_ohne_Powerpoint = {
    "id": 15,
    "name": "Präsentieren ohne Powerpoint",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu folgendem in der Lage (erwartete Lernergebnisse und zu erwerbenden Kompetenzen): - Sie kennen die unterschiedlichen Wirkungen und Bedeutung von Präsentationen. "
                    "- Sie sind in der Lage persönliche Hemmungen abzubauen. "
                    "- Sie können konkrete Ziele einer Präsentation definieren. "
                    "- Sie sind in der Lage Ihre Präsentation zu planen und zu strukturieren. "
                    "- Sie kennen verschiedene Medien, die Sie adäquat einzusetzen wissen. "
                    "- Sie verstehen die vielfältigen Herausforderungen beim Präsentieren und können diese behandeln. "
                    "- Sie sind in der Lage mit dem Publikum zu interagieren und das Engagement des Publikums anzuregen. "
                    "- Sie haben ein Verständnis für die verschiedenen Moderations-/Präsentationstechniken und können diese adäquat anzuwenden.",
    "dauer": "3",
    "zuordnungLernjahr": "2",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [],
    "pcKennzeichnung": True,
}

Prüfungsvorbereitung_für_IT_Berufe_AP_Teil_1 = {
    "id": 16,
    "name": "Prüfungsvorbereitung für IT-Berufe AP Teil 1",
    "beschreibung": "Sie sind in der Lage, eigene Wissenslücken zu erkennen und diese methodisch zu füllen. "
                    "Sie erlangen Sicherheit im Umgang mit realen IHK-Prüfungsaufgaben vergangener Prüfungen. "
                    "Sie sind durch simulierte Prüfungssituationen darauf vorbereitet, unter Zeitdruck das in der Ausbildung erlangte Wissen effektiv abzurufen.",
    "dauer": "3",
    "zuordnungLernjahr": "2",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [],
    "pcKennzeichnung": True,
}

Qualität_und_Kundenorientierung_in_der_IT = {
    "id": 17,
    "name": "Qualität und Kundenorientierung in der IT",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete Lernergebnisse und zu erwerbende Kompetenzen): - Sie sind für das Thema Qualität grundsätzlich sensibilisiert. "
                    "- Sie erkennen die elementare Wichtigkeit der Kunden (intern und extern). "
                    "- Sie sind befähigt, kundenorientiert und qualitätsbewußt zu denken. "
                    "- Sie sind in der Lage, Kunden- und qualitätsorientiertes Handeln im eigenen Unternehmen zu erkennen und anzuwenden. "
                    "- Sie kennen technische Tools für die Kundenverwaltung.",
    "dauer": "3",
    "zuordnungLernjahr": "2",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [],
    "pcKennzeichnung": True,
}

Robotik_Grundlagen = {
    "id": 18,
    "name": "Robotik Grundlagen",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete Lernergebnisse und zu erwerbende Kompetenzen): - Sie kennen die Grundbegriffe der Robotik und können logische Zusammenhänge zwischen Mathematik, Physik und Programmierung anwenden. "
                    "- Sie kennen die Unterschiede und Arbeitsweisen verschiedener Sensoren und können deren mögliche Einsatzgebiete aufzeigen. "
                    "- Sie erkennen logische Zusammenhänge zwischen Sensoren und Aktoren und können diese gezielt ansprechen. "
                    "- Sie sind in der Lage, auf Basis einer Anforderung an ein Robotik-System eine Analyse durchzuführen, Lösungen zu konzipieren und diese umzusetzen.",
    "dauer": "5",
    "zuordnungLernjahr": "2",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [4],
    "pcKennzeichnung": True,
}

SAP_4_HANA = {
    "id": 19,
    "name": "SAP 4 HANA",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete"
                    "Lernergebnisse und zu erwerbende Kompetenzen): - Sie kennen die betriebswirtschaftlichen Abläufe"
                    "der mySAP ERP Wertschöpfungskette. "
                    "- Sie haben Grundkompetenzen für die Bearbeitung von "
                    "Geschäftsvorfällen im SAP System. "
                    "- Sie erkennen abteilungsübergreifende Wertschöpfungsketten und "
                    "deren Auswirkungen (Seiteneffekte in anderen Abteilungen).",
    "dauer": "5",
    "zuordnungLernjahr": "2",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [],
    "pcKennzeichnung": True,
}

Prüfungsvorbereitung_für_IT_Berufe_AP_Teil_2 = {
    "id": 20,
    "name": "Prüfungsvorbereitung für IT-Berufe AP Teil 2",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete"
                    "Lernergebnisse und zu erwerbende Kompetenzen): - Sie sind in der Lage, eigene Wissenslücken zu"
                    "erkennen und diese methodisch zu füllen."
                    "- Sie erlangen Sicherheit im Umgang mit realen IHK-"
                    "Prüfungsaufgaben vergangener Prüfungen."
                    "- Sie sind durch simulierte Prüfungssituationen darauf"
                    "vorbereitet, unter Zeitdruck das in der Ausbildung erlangte Wissen effektiv abzurufen.",
    "dauer": "5",
    "zuordnungLernjahr": "2",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [],
    "pcKennzeichnung": True,
}

Netzwerke_und_Protokolle = {
    "id": 21,
    "name": "Netzwerke und Protokolle",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete"
                    "Lernergebnisse und zu erwerbende Kompetenzen): - Sie kennen die Netzkoppelsysteme und deren"
                    "typischen Einsatzgebiete."
                    "- Sie haben grundlegende Kenntnisse zu gängigen Netzwerkprotokollen und"
                    "deren Abläufen."
                    "- Sie kennen Möglichkeiten, die Netzwerkkommunikation vor unberechtigtem Zugriff"
                    "abzusichern."
                    "- Sie können Fehlerquellen identifizieren und beseitigen. Bei der Fehlersuche mittels"
                    "aktueller Datenanalyse-Werkzeuge hilft ihnen das erworbene Fachwissen über mögliche Fehlerquellen."
                    "- Sie kennen die Systeme zur Namensauflösung und können deren Konfiguration vornehmen."
                    "- Sie sind in der Lage, die Systemwerkzeuge einzusetzen – sowohl als Kommandozeilentools als auch in der GUI.",
    "dauer": "5",
    "zuordnungLernjahr": "1",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [25,23,22],
    "pcKennzeichnung": True,
}

Prozesse_und_Methoden = {
    "id": 22,
    "name": "Prozesse und Methoden",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete"
                    "Lernergebnisse und zu erwerbende Kompetenzen): - Sie verfügen über ein grundlegendes Verständnis"  
                    "für Unternehmensprozesse. - Durch die Betrachtung von ITIL und dem Servicelifecycle eines Prozesses"
                    "können sie die Zusammenhänge von Abläufen verstehen und das Service-Value-System mit dem Vier-"
                    "Dimensionenmodell verknüpfen."
                    "- Sie kennen agile Arbeitsmethoden und Abläufe und können in Teams"
                    "mit diesen Abläufen mitwirken."
                    "- Sie sind fähig, Vor- oder Nachteile des Einsatzes agiler"
                    "Arbeitsmethoden in Projekten einzuschätzen.",
    "dauer": "3",
    "zuordnungLernjahr": "1",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [25,23,21],
    "pcKennzeichnung": True,
}

Virtualisierung = {
    "id": 23,
    "name": "Virtualisierung",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete"
                    "Lernergebnisse und zu erwerbende Kompetenzen): - Sie kennen die Grundlagen der Entwicklung vom"
                    "physischen Host zur virtualisierten Architektur."
                    "- Sie sind in der Lage, Virtualisierungsstrategien zu"
                    "entwickeln und mit den Unternehmens-zielen zu verknüpfen sowie Vor- und Nachteile zu identifizieren"
                    "und für den Einsatz zu formulieren."
                    "- Sie kennen die Funktionsweise und Architektur der Applikations-"
                    "Virtualisierung am Beispiel der Container-Plattform Docker."
                    "- Sie sind fähig, auf Docker-Basis einen"
                    "Applikations-Container zu erstellen und diesen zu administrieren.",
    "dauer": "5",
    "zuordnungLernjahr": "1",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [25,22,21],
    "pcKennzeichnung": True,
}

Scripting = {
    "id": 24,
    "name": "Scripting",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete"
                    "Lernergebnisse und zu erwerbende Kompetenzen): - Sie kennen die Grundlagen des Windows Script"
                    "Host (WSH) und unterschiedliche Arten der Skript-Programmierung."
                    "- Sie sind in die Lage, eigene"
                    "Skripte zu entwerfen, zu testen und für die Netzwerkpraxis einzusetzen."
                    "- Sie kennen die Möglichkeiten"
                    "der Windows PowerShell (WPS) zur Verwaltung einer bestehenden Windows Infrastruktur.",
    "dauer": "5",
    "zuordnungLernjahr": "2",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [],
    "pcKennzeichnung": True,
}

System_Administration = {
    "id": 25,
    "name": "System Administration",
    "beschreibung": "Durch Absolvierung dieses Moduls sind die Auszubildenden zu Folgendem in der Lage (erwartete"
                    "Lernergebnisse und zu erwerbende Kompetenzen): - Sie können einen Windows-Client aufsetzen und in"
                    "Betrieb nehmen."
                    "- Sie sind in der Lage, einen Windows Server angepasst an die fachlichen und"
                    "systemtechnischen Anforderungen aufzusetzen, zu administrieren und mit den notwendigen Rollen"
                    "auszurüsten."
                    "- Sie besitzen grundlegende Kenntnisse zur Konfiguration einer Domäne und für deren"
                    "Betrieb."
                    "- Sie kennen neben Windows auch Linux als Netzwerkbetriebssystem und können dieses"
                    "System in eine heterogene IT-Systemlandschaft integrieren."
                    "- Sie können vollumfänglich die Erstellung"
                    "und Konfiguration eines Web-Servers durchführen."
                    "- Sie können Anforderungen an eine Datensicherung"
                    "evaluieren und Konzepte für diverse Anwendungsfälle ausarbeiten."
                    "- Sie kennen Systeme und Techniken"
                    "für die Softwareverteilung und können Konzepte für deren Umsetzung erstellen."
                    "- Sie können"
                    "Sicherungsmechanismen für eine Serverlandschaft oder Domäne konfigurieren und administrieren.",
    "dauer": "10",
    "zuordnungLernjahr": "1",
    "optionaleVorgängermodule": [],
    "verpflichtendeVorgängermodule": [24,22,21],
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
    10:Web_Design_Programmierung,
    11:Office_Professional_Teil_1,
    12:Office_Professional_Teil_2,
    13:Arbeitssicherheit,
    14:Lerntechniken,
    15:Präsentieren_ohne_Powerpoint,
    16:Prüfungsvorbereitung_für_IT_Berufe_AP_Teil_1,
    17:Qualität_und_Kundenorientierung_in_der_IT,
    18:Robotik_Grundlagen,
    19:SAP_4_HANA,
    20:Prüfungsvorbereitung_für_IT_Berufe_AP_Teil_2,
    21:Netzwerke_und_Protokolle,
    22:Prozesse_und_Methoden,
    23:Virtualisierung,
    24:Scripting,
    25:System_Administration,


}

def get_Modules():
    return modules