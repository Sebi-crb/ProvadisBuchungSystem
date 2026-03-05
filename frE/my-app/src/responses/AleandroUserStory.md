# 📋 User Story: Azubi Info Page

## Ressourcen
- **Datei:** `fre/src/responses/azubiPageSrc.json`
- **Zieldatei:** `pages/Azubi.tsx` _(kann vollständig überschrieben werden)_
- **Weitere Seite:** `/modules`

---

## Kontext

Eine JSON-Datei mit realistischen Beispieldaten liegt bereits vor.
Die Applikation hat insgesamt **750 Azubis** — **250 pro Ausbildungsjahr**.

---

## Anforderungen

### Azubi-Übersicht (`pages/Azubi.tsx`)

- Anzeige, **welcher Azubi zu welcher Gruppe gehört**
- Zusätzliche Azubi-Daten sollen **übersichtlich dargestellt** werden
- Da 750 Einträge zu viel für eine Liste sind → **Gruppen-Tabs** als empfohlene Lösung
  - Jeder Tab zeigt zunächst nur die **Namen der Azubis**
  - Klick auf einen Namen öffnet ein **Popup / Modal** mit allen Detaildaten

### Modul-Verlinkung ⭐ _[Highlight-Feature]_

> **Krasse Variante (bevorzugt):**
> Jedes **abgeschlossene Modul** eines Azubis ist **klickbar** und navigiert direkt
> zur `/modules`-Seite — mit **automatisch geöffnetem / hervorgehobenem Modul**.

- Alternativ (minimal): einfacher Button `→ Zur Modulübersicht`

---

## Seiten-Übersicht

| Seite            | Datei              | Status        |
|------------------|--------------------|---------------|
| Azubi-Übersicht  | `pages/Azubi.tsx`  | 🔨 Neu bauen  |
| Modul-Übersicht  | `pages/Modules.tsx`| 🔨 Neu bauen  |

---

## Akzeptanzkriterien

- [ ] Azubis sind **ihrer Gruppe zugeordnet** sichtbar
- [ ] Detaildaten je Azubi sind **abrufbar** (Modal / Popup)
- [ ] Abgeschlossene Module sind **klickbar** und verlinken korrekt
- [ ] `/modules` zeigt bei direktem Aufruf das **richtige Modul** an
- [ ] Seite ist bei **750 Einträgen** performant nutzbar