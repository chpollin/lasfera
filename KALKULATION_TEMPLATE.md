# La Sfera - Kalkulation Bug-Fixes & IIIF-Integration

**Datum:** 28. Oktober 2025
**Anbieter:** DH Craft - Christopher Pollin
**Stundensatz:** 150€/h
**Kunde:** Laura Morreale, RRCHNM

---

## Kalkulationsmethodik

```
Entwicklungszeit (rein)
+ Einarbeitung (10%)
+ Kommunikation/Meetings (10%)
+ Testing (15%)
+ Puffer (20%)
─────────────────────────
= Gesamtstunden × 150€
```

**Overhead-Faktor:** 1.55 (55% Aufschlag)

**Beispiel:**
- 30h Entwicklung → 30h × 1.55 = 46.5h → **6.975€**

---

## Szenario A: MINIMUM (Quick Fixes)

### Annahme:
Nur kritische Bugs, keine neuen Features, keine Refactorings

### Umfang:
- [ ] Gazetteer: 2-3 konkrete Bug-Fixes (CSS, Links, JavaScript)
- [ ] IIIF: Viewer auf Stanzas-Seite einbinden (existierender Tify-Code)
- [ ] Testing: Basis-Tests auf Live-Site
- [ ] Dokumentation: Minimal

### Zeitschätzung:
```
Gazetteer-Fixes:           8-12h
IIIF Viewer-Einbindung:    6-10h
Testing:                   4-6h
Dokumentation:             2-3h
─────────────────────────────
REINE ENTWICKLUNG:        20-31h

× Overhead (1.55):        31-48h
─────────────────────────────
GESAMT:                   31-48h
```

### Preis:
**4.650€ - 7.200€**

### Risiko:
- Wenn mehr Bugs gefunden werden als erwartet: +20-30%
- Wenn IIIF-Integration komplexer: +30-40%

### Nicht enthalten:
- Mirador Upgrade (bleibt bei Alpha)
- Dependency Updates
- Neue Features
- Hosting-Migration
- Refactorings

---

## Szenario B: STANDARD (Vollständige Bugs + IIIF)

### Annahme:
Alle bekannten Bugs + vollständige IIIF-Integration

### Umfang:
- [ ] Gazetteer: Alle Bugs (Map, Links, Performance, UI)
- [ ] IIIF: Mirador in Stanzas-Seite + Canvas-Sync + Line-Code-Links
- [ ] Mirador: Upgrade von Alpha zu Stable (KRITISCH!)
- [ ] Testing: Umfassend auf allen Seiten
- [ ] Dokumentation: Deployment-Guide, User-Guide

### Zeitschätzung:
```
Gazetteer-Fixes:          15-20h
  - Map Bugs                5-8h
  - Links/Navigation        3-5h
  - Performance             4-5h
  - UI/UX                   3-4h

IIIF-Integration:         25-35h
  - Mirador Upgrade        12-16h
  - Stanzas-Viewer         8-12h
  - Canvas-Sync            3-5h
  - Testing                2-4h

Testing:                   8-12h
Dokumentation:             4-6h
─────────────────────────────
REINE ENTWICKLUNG:        52-73h

× Overhead (1.55):        81-113h
─────────────────────────────
GESAMT:                   81-113h
```

### Preis:
**12.150€ - 16.950€**

### Enthält:
- ✅ Alle Gazetteer-Bugs
- ✅ Vollständige IIIF-Integration
- ✅ Mirador Stable-Upgrade
- ✅ Umfassendes Testing
- ✅ Dokumentation

### Nicht enthalten:
- Hosting-Migration
- Neue Features (die nicht in Issues sind)
- Dependency Updates (außer Mirador)

---

## Szenario C: PREMIUM (Full Production-Ready)

### Annahme:
Alles aus Standard + Produktionsreife + Export

### Umfang:
- [ ] Alles aus Szenario B
- [ ] Dependency Updates (Django, Wagtail, npm packages)
- [ ] Security Audit
- [ ] Test-Suite schreiben (Django Tests)
- [ ] CI/CD Pipeline Setup (GitHub Actions)
- [ ] Hosting-Migration Support
- [ ] Post-Launch Support (4 Wochen)

### Zeitschätzung:
```
SZENARIO B:               52-73h

Dependency Updates:        8-12h
Security Audit:            4-6h
Test-Suite:               12-18h
CI/CD Pipeline:            8-12h
Hosting-Migration:         6-10h
Post-Launch Support:      12-16h (4 Wochen à 3-4h)
─────────────────────────────
REINE ENTWICKLUNG:       102-147h

× Overhead (1.55):       158-228h
─────────────────────────────
GESAMT:                  158-228h
```

### Preis:
**23.700€ - 34.200€**

### Enthält:
- ✅ Alles aus Szenario B
- ✅ Produktionsreife Codebase
- ✅ Test-Coverage
- ✅ CI/CD Pipeline
- ✅ Hosting-Migration Support
- ✅ 4 Wochen Post-Launch Support

---

## Empfehlung DH Craft

### Für Launch Juni 2026:

**Empfehlung: Szenario B (STANDARD)**

**Begründung:**
1. Website ist LIVE → Nutzer erwarten funktionierende Features
2. Mirador Alpha ist Produktionsrisiko → Upgrade notwendig
3. IIIF-Integration ist Core-Feature → muss vollständig sein
4. Timeline 7 Monate ist ausreichend für 81-113h

**Timeline bei 20h/Woche:**
- 81h: 4 Wochen
- 113h: 5.5 Wochen
- **Puffer bis Juni 2026:** Komfortabel ✅

### Optional Post-Launch:
Szenario C Features als separate Phase nach Launch:
- Testing & CI/CD: +20-30h (3.000-4.500€)
- Hosting-Migration: +6-10h (900-1.500€)

---

## Zahlungsmodalitäten

### Option 1: Milestone-basiert (empfohlen)
```
Vertragsunterzeichnung:  30% (z.B. 3.645€ bei 12.150€)
Milestone 1 (Gazetteer): 30% (z.B. 3.645€)
Milestone 2 (IIIF):      30% (z.B. 3.645€)
Abnahme:                 10% (z.B. 1.215€)
```

**Vorteil:** Planungssicherheit für beide Seiten

### Option 2: Time & Materials
```
Monatliche Abrechnung nach tatsächlichen Stunden
Stundennachweis per Toggl/Clockify
```

**Vorteil:** Flexibilität bei Scope-Changes

---

## Scope-Änderungen & Change Requests

**Prozess:**
1. Kunde stellt Change Request
2. DH Craft schätzt Mehraufwand (Stunden + €)
3. Kunde genehmigt schriftlich
4. Arbeit wird durchgeführt

**Change Request Rate:** 150€/h (gleich wie Basis-Rate)

**Beispiel:**
- Kunde will zusätzlich "Crowdsourcing-Feature" (aus Issue #65)
- Schätzung: 40-60h = 6.000-9.000€
- Entscheidung: Zusätzlich oder Post-Launch?

---

## Ausschlüsse & Abhängigkeiten

### DH Craft liefert NICHT:
- ❌ Content-Eingabe (Texte, Bilder, Transkriptionen)
- ❌ IIIF-Manifeste erstellen (müssen vorhanden sein)
- ❌ Server-Administration nach Migration
- ❌ Neue Features außerhalb definierter Scope

### Kunde stellt bereit:
- ✅ Zugang zu Dev/Staging/Prod-Servern
- ✅ IIIF-Manifeste für alle Manuscripts
- ✅ Technischer Ansprechpartner bei RRCHNM
- ✅ Zeitnahe Reviews (48h Turnaround)
- ✅ Test-Accounts & Sample-Data

---

## Garantien & Support

### Garantie:
- **Bug-Free:** 30 Tage nach Abnahme
- **Fixes included:** Bugs die aus unserer Arbeit resultieren

### Post-Launch Support (nicht included):
**Option 1:** Retainer (10h/Monat = 1.500€)
**Option 2:** On-Demand (150€/h, min. 2h)

---

## Timeline

### Szenario B (STANDARD): 81-113h

**Phase 1: Gazetteer (2-3 Wochen)**
- Wochen 1-2: Bug-Fixes
- Woche 3: Testing & Review

**Phase 2: IIIF (3-4 Wochen)**
- Wochen 4-5: Mirador Upgrade
- Wochen 6-7: Stanzas-Integration
- Woche 8: Testing & Deployment

**Total: 6-8 Wochen**

**Möglicher Start:** Mitte November 2025
**Möglicher Launch:** Ende Dezember 2025 / Anfang Januar 2026

**Deadline Juni 2026:** ✅ **Komfortabel machbar mit 4-5 Monaten Puffer**

---

## Risiken & Mitigation

### Technische Risiken:

**Risiko 1: Mirador Upgrade komplexer als erwartet**
- Wahrscheinlichkeit: Mittel
- Impact: +10-20h
- Mitigation: 2-Tage Proof-of-Concept vorab (included)

**Risiko 2: Mehr Bugs als identifiziert**
- Wahrscheinlichkeit: Mittel-Hoch
- Impact: +10-30h
- Mitigation: Puffer (20%) bereits eingerechnet

**Risiko 3: IIIF-Manifeste fehlerhaft/nicht vorhanden**
- Wahrscheinlichkeit: Niedrig
- Impact: BLOCKER
- Mitigation: Pre-Check im Kick-off

### Organisatorische Risiken:

**Risiko 4: Langsame Review-Zyklen**
- Impact: Timeline-Verzögerung
- Mitigation: SLA vereinbaren (48h Review-Zeit)

**Risiko 5: Scope Creep**
- Impact: Budget-Überschreitung
- Mitigation: Change Request Prozess

---

## Vertragliche Punkte

### Intellectual Property:
- Code → RRCHNM (Open Source, GitHub)
- DH Craft behält Referenz-Recht

### Haftung:
- Begrenzt auf Vertragssumme
- Keine Haftung für Datenverlust (Kunde macht Backups)

### Kündigung:
- Beidseitig mit 2 Wochen Frist
- Bereits geleistete Arbeit wird abgerechnet

### Gerichtsstand:
- Österreich (DH Craft Sitz)

---

## Angebotsdetails

**Gültigkeit:** 30 Tage ab Ausstellungsdatum
**Vertragsbeginn:** Nach Vertragsunterzeichnung
**Zahlungsziel:** 14 Tage netto
**Währung:** Euro (€)
**MwSt:** (je nach Kunde - EU B2B = Reverse Charge)

---

## Nächste Schritte

1. [ ] Kunde wählt Szenario (A/B/C)
2. [ ] Detaillierte Bug-Liste im Meeting durchgehen
3. [ ] Finale Kalkulation erstellen
4. [ ] Vertrag aufsetzen
5. [ ] Kick-off Meeting
6. [ ] Entwicklung starten

---

## Kontakt

**DH Craft**
Christopher Pollin
christopher.pollin@dhcraft.org
[Adresse]
[Steuernummer]

**Rückfragen?**
- Meeting vereinbaren
- E-Mail-Diskussion
- Proof-of-Concept gewünscht?
