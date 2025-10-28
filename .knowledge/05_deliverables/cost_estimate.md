# La Sfera - Kost enkalkulation (VERIFIZIERT)

**Datum:** 28. Oktober 2025 (aktualisiert nach Code-Verifikation)
**Anbieter:** DH Craft - Christopher Pollin
**Stundensatz:** 150€/h
**Kunde:** Laura Morreale, RRCHNM

---

## ⚠️ WICHTIGE AKTUALISIERUNG

**Ursprüngliche Schätzung (vor Verifikation):**
- Annahme: 5 Bugs
- Aufwand: 35-40h
- Kosten: ~10.000€

**Nach vollständiger Code-Verifikation:**
- **Tatsächlich:** 2 Bugs (3 waren Fehlannahmen!)
- **Aufwand:** 7-11h reine Entwicklung
- **Kosten:** ~2.340€ (mit Overhead)

**Einsparung: -77% (-7.660€)**

---

## Kalkulationsmethodik

```
Reine Entwicklungszeit
+ Testing (15%)
+ Code Review (10%)
+ Deployment (5%)
───────────────────────
= Overhead-Faktor: 1.3x
× Stundensatz 150€
───────────────────────
= Gesamtpreis
```

---

## SZENARIO A: Verifizierte Bugs (EMPFOHLEN)

### Umfang

**Bug #1: Urb1-Hardcoding entfernen**
- 5 Hardcoded-Stellen in manuscript/views.py
- Konfigurierbare Fallback-Logik implementieren
- Sichere Exception-Handling

**Bug #3: page_number Parameter implementieren**
- Canvas-ID Berechnung aus IIIF-Manifest
- Template-Variable übergeben
- Bounds-Checking & Error-Handling

### Zeitschätzung

```
Bug #1: Urb1 Hardcoding
  - Fallback-Logik refactoren       2-3h
  - 5 Hardcodes ändern               1-2h
  - Testing                          1h
  Subtotal:                          4-6h

Bug #3: page_number Parameter
  - Canvas-ID Berechnung             2-3h
  - Template-Variable                0.5h
  - Error-Handling                   0.5h
  - Testing                          1h
  Subtotal:                          3-5h

Code Review:                         1h
Deployment & Testing:                1h
─────────────────────────────────────
REINE ENTWICKLUNG:                   9-13h

× Overhead (1.3x):                   12-17h
─────────────────────────────────────
GESAMT:                              12-17h
```

### Preis

```
Best Case:   12h × 150€ = 1.800€
Realistic:   14h × 150€ = 2.100€
Worst Case:  17h × 150€ = 2.550€
─────────────────────────────────────
EMPFOHLEN:                2.340€ (15.6h)
```

### Enthält

- ✅ Bug #1: Urb1-Hardcoding komplett entfernt
- ✅ Bug #3: page_number Navigation funktioniert
- ✅ Code Review
- ✅ Unit Tests für beide Fixes
- ✅ Deployment zu Dev/Staging
- ✅ 2 Wochen Bug-Fix Garantie

### Nicht enthalten

- ❌ Bug #2 (IIIF Viewer) - **existiert nicht**, Viewer ist im Code vorhanden
- ❌ Bug #4 (Silent Exceptions) - **bereits gefixt** im aktuellen Code
- ❌ Gazetteer-Fix - **unklar ob kaputt**, Browser-Test nötig

---

## SZENARIO B: Mit Gazetteer (falls nötig)

### Zusätzlicher Umfang

**Gazetteer Map-Rendering** (NUR wenn Browser-Test Bug bestätigt!)
- Leaflet.js Debugging
- Marker-Rendering Fix
- Optional: Performance-Optimierung (Clustering)

### Zeitschätzung

```
Szenario A:                          12-17h
+ Gazetteer Fix:                     2-6h
─────────────────────────────────────
GESAMT:                              14-23h
```

### Preis

```
Szenario A:                          2.340€
+ Gazetteer (4h avg):                  600€
─────────────────────────────────────
TOTAL:                               2.940€
```

### Voraussetzung

**Browser-Test MUSS durchgeführt werden:**
1. https://lasfera.rrchnm.org/toponyms öffnen
2. Developer Console prüfen
3. Marker auf Karte sichtbar? → Ja = kein Fix nötig
4. JavaScript-Errors? → Ja = Fix nötig

---

## SZENARIO C: Nicht empfohlen (alte Schätzung)

**Status:** VERALTET - Basierte auf falschen Annahmen

**Warum nicht:**
- Bug #2 existiert nicht (Viewer ist vorhanden)
- Bug #4 ist bereits gefixt
- 20-30h IIIF-Integration ist unnötig

**Alte Schätzung:** ~10.000€
**Tatsächlich nötig:** ~2.340€

---

## Zahlungsmodalitäten

### Option 1: Pauschalpreis (empfohlen)

**Szenario A:**
```
Anzahlung (50%):          1.170€
Bei Abnahme (50%):        1.170€
─────────────────────────────
TOTAL:                    2.340€
```

**Vorteil:** Planungssicherheit, klare Kosten

### Option 2: Time & Materials

```
Monatliche Abrechnung nach tatsächlichen Stunden
Stundennachweis per Toggl/Clockify
Stundensatz: 150€/h
```

**Vorteil:** Nur bezahlen was tatsächlich gearbeitet wird
**Nachteil:** Keine feste Obergrenze

---

## Timeline

### Szenario A (12-17h)

**Woche 1 (Start nach Beauftragung):**
- Tag 1-2: Bug #1 (Urb1) implementieren
- Tag 3: Bug #3 (page_number) implementieren
- Tag 4: Testing & Code Review
- Tag 5: Pull Request erstellen

**Woche 2:**
- Tag 1: Code Review Feedback einarbeiten
- Tag 2: Merge & Deploy to Dev
- Tag 3-4: Testing auf Dev-Environment
- Tag 5: Deploy to Production

**Gesamt:** 2 Wochen (10 Arbeitstage)

### Szenario B (14-23h)

Woche 1-2 wie Szenario A, plus:

**Woche 3:**
- Tag 1-2: Gazetteer-Debugging
- Tag 3: Fix implementieren
- Tag 4: Testing
- Tag 5: Deploy

**Gesamt:** 3 Wochen (15 Arbeitstage)

---

## Vergleich der Szenarien

| Aspekt | Szenario A | Szenario B | Alt (C) |
|--------|-----------|-----------|---------|
| **Bugs gefixt** | 2 | 3 | 5 (falsch!) |
| **Aufwand** | 12-17h | 14-23h | 35-40h |
| **Kosten** | 2.340€ | 2.940€ | 10.000€ |
| **Timeline** | 2 Wochen | 3 Wochen | 6-8 Wochen |
| **Risiko** | NIEDRIG | MITTEL | HOCH |
| **Empfehlung** | ✅ JA | ⚠️ Nur wenn nötig | ❌ NEIN |

---

## Was ist NICHT included (in allen Szenarien)

### Code-Bugs die nicht existieren

- ❌ **Bug #2:** IIIF-Viewer auf /stanzas/ fehlt
  - **Grund:** Viewer ist im Template vorhanden (verifiziert)
  - **Code:** templates/stanzas.html:265-275 hat Tify-Container
  - **Evtl. Problem:** Browser/Daten, nicht Code

- ❌ **Bug #4:** Silent Exception Handling
  - **Grund:** Bereits gefixt, alle Exceptions sind spezifisch
  - **Code:** Nur `except ObjectDoesNotExist:`, kein bare `except:`

### Andere Ausschlüsse

- ❌ Neue Features (außer Bug-Fixes)
- ❌ Mirador Upgrade (Alpha → Stable)
- ❌ Dependency Updates (Django, Wagtail)
- ❌ Test-Suite schreiben (nur Bug-spezifische Tests)
- ❌ CI/CD Pipeline
- ❌ Hosting-Migration
- ❌ Content-Eingabe
- ❌ IIIF-Manifeste erstellen

---

## Garantien & Support

### Bug-Fix Garantie

**Dauer:** 2 Wochen nach Production-Deployment
**Umfang:** Bugs die aus unseren Änderungen resultieren
**Nicht enthalten:** Pre-existierende Bugs, Daten-Probleme

### Post-Launch Support (optional, nicht included)

**Option 1:** Retainer
```
10h/Monat = 1.500€
Verfällt nicht, rolliert
```

**Option 2:** On-Demand
```
150€/h, minimum 2h
48h Response-Zeit
```

---

## Änderungsmanagement

### Change Requests

**Prozess:**
1. Kunde stellt Change Request
2. DH Craft schätzt Mehraufwand (h + €)
3. Kunde genehmigt schriftlich
4. Work Order erstellt
5. Arbeit wird durchgeführt

**Change Request Rate:** 150€/h (gleich wie Basis)

**Beispiel:**
- Laura: "Könnt ihr auch Manuscript-Dropdown in Header einbauen?"
- DH Craft: "Ja, Schätzung 3-4h (450-600€), genehmigen?"
- Laura: "Ja" → Work Order → Implementation

---

## Risiken & Mitigation

### Technische Risiken

**Risiko 1: Mehr Bugs als identifiziert**
- Wahrscheinlichkeit: NIEDRIG (Code vollständig analysiert)
- Impact: +5-10h
- Mitigation: 20% Puffer bereits eingerechnet

**Risiko 2: IIIF-Manifeste ändern sich**
- Wahrscheinlichkeit: NIEDRIG
- Impact: BLOCKER
- Mitigation: Manifest-Caching (bereits implementiert)

**Risiko 3: Gazetteer ist tatsächlich kaputt**
- Wahrscheinlichkeit: MITTEL
- Impact: +2-6h (300-900€)
- Mitigation: Browser-Test VOR Beauftragung

### Organisatorische Risiken

**Risiko 4: Langsame Review-Zyklen**
- Impact: Timeline-Verzögerung
- Mitigation: SLA vereinbaren (48h Response)

**Risiko 5: Kein Dev-Environment Zugang**
- Impact: Testing blockiert
- Mitigation: Im Kick-off klären

---

## Angebots-Details

**Gültigkeit:** 30 Tage ab Ausstellungsdatum
**Vertragsbeginn:** Nach Vertragsunterzeichnung & Anzahlung
**Zahlungsziel:** 14 Tage netto
**Währung:** Euro (€)
**MwSt:** Reverse Charge (B2B, EU)

**Zahlungsart:**
- Banküberweisung
- PayPal (+3% Gebühr)

---

## Nächste Schritte

### Wenn Szenario A gewünscht

1. [ ] Angebot unterzeichnen
2. [ ] Anzahlung 50% (1.170€) überweisen
3. [ ] Kick-off Meeting (Zoom, 30 min)
4. [ ] Dev-Environment Zugang klären
5. [ ] Start: Tag nach Anzahlung

### Wenn Szenario B gewünscht

1. [ ] **Zuerst:** Browser-Test Gazetteer durchführen
2. [ ] Bug bestätigen oder widerlegen
3. [ ] Dann: Angebot für A oder B unterzeichnen

### Wenn Budget nicht passt

**Alternativen:**
- **Mini-Fix:** Nur Bug #1 (900€, 6h)
- **Phasen-Weise:** Bug #1 jetzt, Bug #3 später
- **DIY:** Wir liefern Code-Review statt Implementation (300€, 2h)

---

## Kontakt & Fragen

**DH Craft**
Christopher Pollin
christopher.pollin@dhcraft.org
www.dhcraft.org

**Rückfragen?**
- Zoom-Call gewünscht? (kostenlos, 30 min)
- Detaillierte Code-Analyse gewünscht? (in bug_inventory.md)
- Proof-of-Concept für Bug #1 gewünscht?

---

## Anhänge

1. [Bug Inventory (Verifiziert)](../03_bugs/bug_inventory.md) - Detaillierte Code-Analyse
2. [Tech Stack](../02_technical/tech_stack.md) - System-Übersicht
3. [Project Overview](../01_project/overview.md) - Kontext & Team

---

**Version:** 2.0 (verifiziert nach Code-Analyse)
**Nächstes Update:** Nach Beauftragung
