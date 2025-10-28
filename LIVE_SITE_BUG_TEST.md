# La Sfera - Live-Site Bug-Testing Checkliste

**Datum:** 28. Oktober 2025
**Tester:** Christopher Pollin, DH Craft
**Site:** https://lasfera.rrchnm.org/

---

## Testing-Methodik

**Browser:** Chrome/Firefox mit DevTools
**Tools:**
- Browser Console (F12)
- Network Tab
- Screenshots
- Screen Recording (optional)

**Ziel:** Konkrete, reproduzierbare Bugs finden die Nutzer JETZT erleben

---

## 1. Homepage (https://lasfera.rrchnm.org/)

### Zu testen:
- [ ] Seite lädt vollständig
- [ ] Bilder werden angezeigt
- [ ] Navigation funktioniert
- [ ] Links zu allen Hauptsektionen funktionieren
- [ ] Console Errors? (F12 → Console)

### Befunde:
```
Status: [ ] OK | [ ] BUGS GEFUNDEN

Bugs:
1.
```

---

## 2. Edition/Stanzas (https://lasfera.rrchnm.org/stanzas/)

### Zu testen:
- [ ] Text wird angezeigt
- [ ] Manuscript Dropdown funktioniert
- [ ] Book Navigation funktioniert
- [ ] **KRITISCH: Sind Manuscript-Bilder sichtbar?**
- [ ] **KRITISCH: Ist ein IIIF-Viewer (Mirador/Tify) eingebettet?**
- [ ] Line Codes klickbar/linkbar?
- [ ] Übersetzungen umschaltbar (IT/EN)?
- [ ] Console Errors?

### Erwartung vs. Realität:
```
ERWARTET: Side-by-side Text + IIIF-Viewer mit Manuscript-Bildern
REALITÄT:

Screenshots:
-
```

### JavaScript Errors:
```
Console Output:
(alle Errors hier einfügen)
```

### Network Errors:
```
Failed Requests (Network Tab):
-
```

---

## 3. Gazetteer (https://lasfera.rrchnm.org/toponyms/)

### Zu testen:
- [ ] Seite lädt
- [ ] Toponym-Liste wird angezeigt (links)
- [ ] **KRITISCH: Wird die Karte angezeigt?**
- [ ] **KRITISCH: Werden Marker auf der Karte angezeigt?**
- [ ] Search-Box funktioniert
- [ ] Hover über Toponym → Marker highlightet?
- [ ] Click auf Toponym → Detail-Seite lädt?
- [ ] API-Call zu /api/toponyms erfolgreich? (Network Tab)
- [ ] Console Errors?

### API-Check:
```bash
# Manuell testen:
curl https://lasfera.rrchnm.org/api/toponyms | jq

Status: [ ] 200 OK | [ ] ERROR
Response: [ ] JSON mit Daten | [ ] Leer | [ ] Error
```

### Map-Status:
```
Karte sichtbar: [ ] JA | [ ] NEIN | [ ] TEILWEISE
Marker sichtbar: [ ] JA | [ ] NEIN
Anzahl Marker: ca. ___ Stück

Wenn NEIN:
- Console Error?
- Leaflet geladen? (Suche "Leaflet" in Sources Tab)
- OpenStreetMap Tiles laden? (Network Tab → Bilder)
```

### Hover-Interaktion:
```
Hover über "Roma" in Liste → Marker auf Karte:
[ ] Highlightet korrekt
[ ] Keine Reaktion
[ ] Error

Console Output beim Hover:
```

---

## 4. Gazetteer Detail-Seite (https://lasfera.rrchnm.org/toponyms/[slug]/)

**Beispiel-Test:** https://lasfera.rrchnm.org/toponyms/roma/

### Zu testen:
- [ ] Seite lädt
- [ ] Toponym-Name angezeigt
- [ ] Variants-Tabelle angezeigt
- [ ] Line Codes angezeigt und klickbar
- [ ] **Karte mit einzelnem Marker sichtbar?**
- [ ] Coordinates angezeigt
- [ ] Copy-Coordinates Button funktioniert?
- [ ] Links zu Manuscripts funktionieren?
- [ ] Console Errors?

### Befunde:
```
Status: [ ] OK | [ ] BUGS

Bugs:
```

---

## 5. Manuscripts Detail (https://lasfera.rrchnm.org/manuscripts/Urb1/)

### Zu testen:
- [ ] Seite lädt
- [ ] Manuscript Metadaten angezeigt
- [ ] **KRITISCH: Ist IIIF-Viewer sichtbar?**
- [ ] **Welcher Viewer? Mirador | Tify | Anderer**
- [ ] Viewer zeigt Bilder korrekt?
- [ ] Navigation im Viewer funktioniert?
- [ ] Zoom funktioniert?
- [ ] Console Errors?

### Viewer-Check:
```
Viewer-Typ: [ ] Mirador | [ ] Tify | [ ] Universal Viewer | [ ] Keiner | [ ] Kaputt

Wenn Viewer vorhanden:
- Bilder laden: [ ] JA | [ ] NEIN | [ ] LANGSAM
- Navigation: [ ] Funktioniert | [ ] Kaputt
- Zoom: [ ] Funktioniert | [ ] Kaputt

IIIF Manifest URL:
(aus Console/Network kopieren)

Console Errors:
```

---

## 6. Gallery (https://lasfera.rrchnm.org/gallery/)

### Zu testen:
- [ ] Seite lädt
- [ ] Bilder werden angezeigt
- [ ] Thumbnail-Grid funktioniert
- [ ] Theme-Filter funktioniert?
- [ ] Click auf Bild → Detail-Seite?
- [ ] Console Errors?

### Befunde:
```
Status: [ ] OK | [ ] BUGS

Bugs:
```

---

## 7. Cross-Page Funktionalität

### Line Code Links testen:
```
1. Gehe zu Gazetteer → Toponym Detail
2. Click auf Line Code (z.B. "01.01.04")
3. Erwartung: Springt zu Stanzas-Seite, Zeile highlighted
4. Realität:

Status: [ ] Funktioniert | [ ] Link tot | [ ] Falsche Seite | [ ] Kein Highlight
```

### Manuscript Links testen:
```
1. Gehe zu Stanzas
2. Wähle Manuscript aus Dropdown
3. Erwartung: Manuscript-Bilder laden im Viewer
4. Realität:

Status: [ ] Funktioniert | [ ] Keine Reaktion | [ ] Error
```

---

## 8. Performance-Check

### Ladezeiten:
```
Homepage: ___ Sekunden
Stanzas: ___ Sekunden (größte Seite!)
Gazetteer: ___ Sekunden
Manuscripts/Urb1: ___ Sekunden

Langsam (>5s): [ ] Liste hier
```

### Large Requests (Network Tab):
```
Größte Dateien:
1. ___ MB - ___
2. ___ MB - ___
3. ___ MB - ___

IIIF Images: ca. ___ MB pro Bild
```

---

## 9. Mobile/Responsive Check (Optional)

### Zu testen:
- [ ] Toggle Device Toolbar (Chrome DevTools)
- [ ] Teste auf iPhone/iPad Größe
- [ ] Navigation-Menu (Mobile Burger-Icon)
- [ ] Gazetteer-Map auf Mobile
- [ ] IIIF-Viewer auf Mobile

### Befunde:
```
Mobile Experience: [ ] OK | [ ] BUGS | [ ] NICHT GETESTET

Bugs:
```

---

## 10. Console Errors Zusammenfassung

### JavaScript Errors:
```
Seite: ___
Error: ___
File: ___
Line: ___

Seite: ___
Error: ___
```

### Network Failed Requests (4xx, 5xx):
```
URL: ___
Status: ___
Error: ___
```

### Missing Resources:
```
404 Not Found:
-
-

403 Forbidden:
-
```

---

## 11. Kritische Bugs Zusammenfassung

### BLOCKER (Site funktioniert nicht):
```
1.
```

### KRITISCH (Major Features kaputt):
```
1.
```

### HOCH (UX beeinträchtigt):
```
1.
```

### MITTEL (Kosmetisch/Minor):
```
1.
```

---

## 12. User-Flow Test

### Szenario: "Student sucht Toponym im Text"
```
Schritte:
1. Homepage → Edition
2. Suche nach "Roma" im Text (Ctrl+F)
3. Finde Line Code
4. Click auf Line Code (falls linkbar)
5. Erwartung: Gehe zu Gazetteer "Roma"

Funktioniert: [ ] JA | [ ] NEIN

Wenn NEIN, warum:
```

### Szenario: "Forscher vergleicht Manuscript-Varianten"
```
Schritte:
1. Edition → Stanza 01.01
2. Wähle Manuscript "Urb1" aus Dropdown
3. Erwartung: Sehe Folio-Bild neben Text
4. Realität:

Funktioniert: [ ] JA | [ ] NEIN
```

---

## Testing-Ergebnis

**Gesamtstatus:** [ ] PRODUKTIONSREIF | [ ] MINOR BUGS | [ ] MAJOR BUGS | [ ] KAPUTT

**Anzahl Bugs gefunden:**
- Blocker: ___
- Kritisch: ___
- Hoch: ___
- Mittel: ___
- **GESAMT: ___**

**Geschätzter Fix-Aufwand:**
- Blocker/Kritisch: ___ Stunden
- Hoch/Mittel: ___ Stunden
- **TOTAL: ___ Stunden**

**Dringend mit Laura klären:**
```
1.
2.
3.
```

---

## Screenshots & Screen Recordings

**Speichern unter:** `screenshots/[datum]_[seite]_[bug-beschreibung].png`

Liste:
- [ ] Homepage Overview
- [ ] Stanzas - fehlender IIIF-Viewer
- [ ] Gazetteer - Map Status
- [ ] Console Errors (alle kritischen)
- [ ] Network Tab (failed requests)

**Screen Recording (optional):**
- [ ] Gazetteer Bug-Reproduktion (30s)
- [ ] IIIF-Problem (30s)

---

## Nächste Schritte nach Testing

1. [ ] Screenshots organisieren
2. [ ] Bug-Liste priorisieren
3. [ ] Zeitschätzung pro Bug
4. [ ] Kalkulation erstellen
5. [ ] Mit Laura im Meeting durchgehen
