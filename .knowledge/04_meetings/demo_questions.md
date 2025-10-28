# Demo-Fragen für Laura - Meeting

**Meeting-Datum:** 3. oder 11. November 2025, 17:00 CET
**Zweck:** Laura zeigt konkrete Bugs auf der live Site

---

## Vorbereitung für Laura

**Bitte bereithalten:**
- [ ] Browser geöffnet auf https://lasfera.rrchnm.org/
- [ ] Screen-Share aktiviert
- [ ] Console geöffnet (F12) falls möglich
- [ ] Liste der 3 schlimmsten Probleme

---

## Demo 1: Gazetteer (10 Min)

### Grundfunktionalität

**Christopher fragt:**
> "Geh bitte auf die Gazetteer-Seite. Was siehst du?"

**Zu beobachten:**
- [ ] Lädt die Seite?
- [ ] Ist die Karte sichtbar?
- [ ] Werden Marker angezeigt?
- [ ] Wenn ja: Wie viele ungefähr?

### Interaktionen testen

**Christopher fragt:**
> "Kannst du auf einen Marker klicken?"

**Zu dokumentieren:**
- Was passiert beim Click?
- Erscheint ein Popup?
- Funktioniert der Link im Popup?

**Christopher fragt:**
> "Gibt es eine Suchfunktion? Kannst du nach 'Roma' suchen?"

**Zu dokumentieren:**
- Funktioniert die Suche?
- Werden Ergebnisse angezeigt?
- Wenn ja: Springt die Karte zum Ort?

### Hover-Effekte

**Christopher fragt:**
> "Wenn du in der Liste über einen Ortsnamen mit der Maus gehst - highlightet dann der Marker auf der Karte?"

**Zu dokumentieren:**
- Hover-Interaktion funktioniert? Ja/Nein
- Wenn nein: JavaScript-Error in Console?

### Performance

**Christopher beobachtet:**
- Wie lange dauert das Laden der Karte?
- Ruckelt die Seite?
- Wie viele Marker sind es insgesamt?

---

## Demo 2: IIIF-Viewer auf Stanzas-Seite (10 Min)

### Stanzas-Hauptseite

**Christopher fragt:**
> "Geh bitte auf /stanzas/ - die Hauptedition. Was siehst du?"

**Zu dokumentieren:**
- [ ] Wird Text angezeigt?
- [ ] Siehst du irgendwo Manuskript-Bilder?
- [ ] Gibt es einen IIIF-Viewer (Mirador oder ähnlich)?

**Christopher fragt:**
> "Wo SOLLTE der Viewer sein? Zeig mir die Stelle."

### Manuscript-Dropdown

**Christopher fragt:**
> "Gibt es ein Dropdown um Manuscripts auszuwählen?"

**Zu testen:**
- Dropdown funktioniert?
- Was passiert wenn du ein anderes Manuscript wählst?
- Erscheinen dann Bilder?

### Vergleich: Was funktioniert?

**Christopher fragt:**
> "Geh jetzt bitte auf /manuscripts/Urb1/stanzas/ - funktioniert da der Viewer?"

**Zu vergleichen:**
- `/stanzas/` hat KEINEN Viewer
- `/manuscripts/Urb1/stanzas/` hat Viewer?
- Was ist der Unterschied aus User-Sicht?

---

## Demo 3: Andere Manuscripts (5 Min)

### Manuscript-Auswahl

**Christopher fragt:**
> "Welche Manuscripts gibt es außer Urb1?"

**Zu listen:**
- Cambridge
- Florence
- Yale
- Andere?

### Funktionalität testen

**Christopher fragt:**
> "Geh bitte auf /manuscripts/Florence/ (oder ein anderes) - funktioniert das genauso wie Urb1?"

**Zu dokumentieren:**
- Seite lädt?
- Bilder werden angezeigt?
- Oder Fehler?
- Oder wird Urb1 angezeigt statt Florence?

---

## Demo 4: Mirador Page-Navigation (5 Min)

### Direkter Link zu Folio

**Christopher fragt:**
> "Wenn du auf einen Link zu einem spezifischen Folio klickst - z.B. 'Folio 5r' - öffnet sich dann der Viewer auf dieser Seite?"

**Zu testen:**
- Link existiert?
- Viewer öffnet sich?
- Richtige Seite wird angezeigt?
- Oder immer Seite 1?

### URL-Parameter

**Christopher beobachtet:**
- Hat die URL einen page_number Parameter?
- z.B. `/mirador/1/5/` oder ähnlich?
- Wird dieser ignoriert?

---

## Demo 5: Line Code Links (5 Min)

### Vom Gazetteer zur Edition

**Christopher fragt:**
> "Im Gazetteer steht bei jedem Ort eine Liste von Line Codes (z.B. 01.02.15). Kannst du auf so einen Code klicken?"

**Zu dokumentieren:**
- Link funktioniert?
- Wohin führt der Link?
- Wird die richtige Stelle im Text highlighted?
- Wird das entsprechende Folio-Bild angezeigt?

---

## Zusätzliche Fragen

### User-Perspektive

**Christopher fragt:**
> "Was sind aus deiner Sicht die 3 größten Probleme die Nutzer haben würden?"

**Christopher fragt:**
> "Gibt es Funktionen die du erwartet hättest aber nicht findest?"

### Bekannte Workarounds

**Christopher fragt:**
> "Gibt es Dinge die du umgehen musst? Z.B. 'Ich muss immer erst X machen damit Y funktioniert'?"

---

## Console-Errors (falls Laura kann)

**Christopher fragt:**
> "Kannst du die Browser-Console öffnen (F12)? Siehst du rote Fehler?"

**Zu dokumentieren:**
- Screenshot von Errors
- Welche Seite produziert welche Errors?

---

## Was Christopher NICHT braucht

❌ Detaillierte Code-Erklärungen
❌ Technische Spezifikationen
❌ Lange Diskussionen über Features

**Christopher braucht:**
✅ "Das funktioniert nicht" (zeigen)
✅ "Das sollte so aussehen" (beschreiben)
✅ "User beschweren sich über X"

---

## Nach der Demo

**Christopher fasst zusammen:**
- Bug #1: [Beschreibung]
- Bug #2: [Beschreibung]
- Bug #3: [Beschreibung]
- Zusätzliche Bugs: [Liste]

**Christopher fragt:**
- "Habe ich alles verstanden?"
- "Gibt es noch was das ich übersehen habe?"

---

## Meeting-Notizen-Template

```
DEMO-NOTIZEN - La Sfera Meeting

Datum: _______
Dauer: _______

GAZETTEER:
- Karte sichtbar: Ja/Nein
- Marker angezeigt: Ja/Nein (Anzahl: ~___)
- Click funktioniert: Ja/Nein
- Suche funktioniert: Ja/Nein
- Hover-Effect: Ja/Nein
- JavaScript Errors: _______

STANZAS VIEWER:
- /stanzas/ hat Viewer: Ja/Nein
- /manuscripts/Urb1/stanzas/ hat Viewer: Ja/Nein
- Unterschied: _______
- Sollte so aussehen: _______

MANUSCRIPTS:
- Florence funktioniert: Ja/Nein
- Cambridge funktioniert: Ja/Nein
- Yale funktioniert: Ja/Nein
- Fallback zu Urb1: Ja/Nein

MIRADOR NAVIGATION:
- Page-Parameter in URL: _______
- Richtige Seite öffnet: Ja/Nein
- Immer Seite 1: Ja/Nein

LINE CODE LINKS:
- Links existieren: Ja/Nein
- Links funktionieren: Ja/Nein
- Folio wird gezeigt: Ja/Nein

ZUSÄTZLICHE BUGS:
1. _______
2. _______
3. _______

PRIORITÄT (Laura's Einschätzung):
1. [MUST FIX] _______
2. [WICHTIG] _______
3. [NICE TO HAVE] _______
```

---

**Version:** 1.0
**Verwendung:** Meeting-Checkliste
