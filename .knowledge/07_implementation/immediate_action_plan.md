# Sofort-Umsetzung: Was JETZT tun?

**Datum:** 28. Oktober 2025
**Status:** PRE-MEETING Vorbereitung
**Deadline:** Meeting 3. oder 11. November 2025

---

## Executive Decision

**PLAN: VORBEREITEN statt DEPLOYEN**

**Begründung:**
1. ✅ Bugs sind Code-verifiziert (3 konkrete Bugs gefunden)
2. ❌ Bugs sind NICHT User-verifiziert (Laura hat sie nicht demonstriert)
3. ⚠️ Deployment ohne Bestätigung = Risiko + unprofessionell
4. ✅ Vorbereitung zeigt Kompetenz und ermöglicht informierte Entscheidung

**Strategie:** "Show, don't tell"
- Im Meeting: Live-Demo der Fixes
- Laura sieht: Bugs existieren + Fixes funktionieren
- Laura entscheidet: Was fixen, was Budget, wann deployen

---

## Phase 1: SOFORT machbar (Heute - 2./10. Nov)

### Task 1: E-Mail an Laura (HEUTE!)

**Zeitaufwand:** 15 Minuten
**Priorität:** KRITISCH

**Email-Content:**
```
Betreff: La Sfera - Bug-Analyse abgeschlossen + Meeting-Vorbereitung

Hallo Laura,

ich habe die Code-Analyse für La Sfera abgeschlossen und bereits 3 konkrete
Bugs im Code gefunden (mit exakten Zeilen-Nummern und File-Locations).

Im Anhang findest du:
1. MEETING_BRIEF.md - 1-seitige Agenda für unser Meeting (45 min)
2. KONKRETE_BUGS_GEFUNDEN.md - Detaillierte Bug-Analyse mit Code-Beweisen

Grobe Kosten-Schätzung: 6.000-10.000€ (je nachdem was wirklich gefixt werden muss)

Im Meeting möchte ich:
- Die Bugs auf der live Site mit dir demonstrieren
- Dir meine Fix-Vorschläge zeigen
- Budget und Timeline besprechen

Können wir den Termin bestätigen? (3. oder 11. November, 17:00 CET)

Beste Grüße,
Christopher Pollin
DH Craft

Anhänge:
- MEETING_BRIEF.md
- KONKRETE_BUGS_GEFUNDEN.md
```

**Action:**
```bash
# Dateien aus .knowledge/ kopieren für Email
cp .knowledge/04_meetings/2025-11-03_preparation.md MEETING_BRIEF.md
cp .knowledge/03_bugs/bug_inventory.md KONKRETE_BUGS_GEFUNDEN.md
# Dann Email senden
```

---

### Task 2: Dev-Environment aufsetzen

**Zeitaufwand:** 1-2 Stunden
**Priorität:** HOCH

**Voraussetzungen prüfen:**
```bash
# Python Version
python --version  # Sollte: 3.11+

# Poetry installiert?
poetry --version

# Docker installiert?
docker --version
docker-compose --version

# PostgreSQL Client
psql --version
```

**Setup-Steps:**

#### Step 2.1: Repository klonen (FALLS nicht schon gemacht)
```bash
cd ~/Documents/GitHub/Cloned/
git clone https://github.com/chnm/lasfera.git
cd lasfera
```

#### Step 2.2: Dependencies installieren
```bash
# Virtual Environment via Poetry
poetry install

# Node.js Dependencies (für Tailwind + Mirador)
npm install
```

#### Step 2.3: PostgreSQL via Docker starten
```bash
# docker-compose.yml sollte vorhanden sein
docker-compose up -d

# Prüfen ob DB läuft
docker-compose ps
```

#### Step 2.4: Environment Variables
```bash
# .env.example kopieren
cp .env.example .env

# .env editieren (wichtigste Werte):
# DEBUG=True
# SECRET_KEY=<generieren>
# DATABASE_URL=postgres://lasfera:lasfera@localhost:5432/lasfera
```

**Generate SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

#### Step 2.5: Django Setup
```bash
# Poetry shell aktivieren
poetry shell

# Migrations anwenden
python manage.py migrate

# Superuser erstellen (für Admin)
python manage.py createsuperuser

# Static files sammeln
python manage.py collectstatic --noinput

# Tailwind starten (separates Terminal)
python manage.py tailwind start
```

#### Step 2.6: Dev-Server starten
```bash
# In einem Terminal:
python manage.py runserver

# Browser öffnen:
# http://localhost:8000/
```

**Erfolgskriterien:**
- [ ] Server läuft ohne Errors
- [ ] Homepage lädt
- [ ] Admin-Panel erreichbar (http://localhost:8000/admin/)
- [ ] Database-Connection funktioniert

**Troubleshooting:**
```bash
# FALLS PostgreSQL Connection Fehler:
docker-compose logs db

# FALLS Migrations Fehler:
python manage.py showmigrations
python manage.py migrate --fake-initial

# FALLS Static Files fehlen:
python manage.py collectstatic --clear
```

---

### Task 3: Bug-Fix Branches erstellen und Code schreiben

**Zeitaufwand:** 12-14 Stunden
**Priorität:** HOCH
**Deadline:** 2./10. November (1 Tag vor Meeting)

---

#### Sub-Task 3.1: Bug #1 Fix - Urb1 Hardcoding (4-6h)

**Branch erstellen:**
```bash
git checkout main
git pull origin main
git checkout -b fix/urb1-hardcoding
```

**Dateien zu editieren:** manuscript/views.py

**Code-Änderungen (5 Locations):**

**Location 1: views.py:489 (mirador_view)**
```python
# ALT (Zeile 489):
except SingleManuscript.DoesNotExist:
    manuscript = SingleManuscript.objects.get(siglum="Urb1")

# NEU:
except SingleManuscript.DoesNotExist:
    logger.warning(
        f"Manuscript with ID {manuscript_id} not found, using default manuscript"
    )
    manuscript = SingleManuscript.objects.filter(siglum="Urb1").first()
    if not manuscript:
        raise Http404("No default manuscript available")
```

**Location 2: views.py:492 (iiif_url Check)**
```python
# ALT (Zeile 492):
if not manuscript.iiif_url:
    manuscript = SingleManuscript.objects.get(siglum="Urb1")

# NEU:
if not manuscript.iiif_url:
    logger.warning(
        f"Manuscript {manuscript.siglum} has no IIIF URL, using default"
    )
    default = SingleManuscript.objects.filter(
        siglum="Urb1", iiif_url__isnull=False
    ).first()
    if default:
        manuscript = default
    else:
        raise Http404("No IIIF-enabled manuscript available")
```

**Location 3: views.py:498 (stanzas_manuscript)**
- Ähnliches Pattern wie oben

**Location 4: views.py:537 (stanzas view)**
```python
# ALT (Zeile 537):
default_manuscript = SingleManuscript.objects.get(siglum="Urb1")

# NEU:
default_manuscript = SingleManuscript.objects.filter(siglum="Urb1").first()
if not default_manuscript:
    default_manuscript = SingleManuscript.objects.first()
    logger.warning(f"Using {default_manuscript.siglum} as default (Urb1 not found)")
```

**Location 5: views.py:694**
- Ähnliches Pattern

**Logging hinzufügen (Top of file):**
```python
import logging
logger = logging.getLogger(__name__)
```

**Testing:**
```bash
# Server starten
python manage.py runserver

# Browser-Tests:
# 1. Versuche nicht-existierendes Manuscript
curl http://localhost:8000/manuscripts/999/

# 2. Prüfe Logs
tail -f logs/django.log  # (falls log file configured)

# 3. Teste andere Manuscripts (Cambridge, Florence)
# http://localhost:8000/manuscripts/Cambridge/
```

**Commit:**
```bash
git add manuscript/views.py
git commit -m "Fix: Replace Urb1 hardcoding with dynamic fallback logic

- Replace all hardcoded 'Urb1' references with configurable defaults
- Add proper logging for fallback scenarios
- Use .filter().first() instead of .get() to avoid DoesNotExist exceptions
- Add Http404 for cases where no manuscript is available

Affected locations: views.py:489, 492, 498, 537, 694

Fixes: Bug #1 from code analysis
Estimated fix time: 6h"
```

---

#### Sub-Task 3.2: Bug #3 Fix - page_number Parameter (3-5h)

**Branch erstellen:**
```bash
git checkout main
git checkout -b fix/mirador-page-number
```

**Dateien zu editieren:**
- manuscript/views.py (mirador_view function)
- templates/manuscript/mirador.html (optional, canvas_id schon vorhanden)

**Code-Änderung: views.py:485-506**
```python
def mirador_view(request, manuscript_id, page_number):
    """Display IIIF manuscript in Mirador viewer, optionally starting at specific page"""

    try:
        manuscript = SingleManuscript.objects.get(pk=manuscript_id)
    except SingleManuscript.DoesNotExist:
        logger.warning(f"Manuscript {manuscript_id} not found, using default")
        manuscript = SingleManuscript.objects.filter(siglum="Urb1").first()
        if not manuscript:
            raise Http404("Manuscript not found")

    if not manuscript.iiif_url:
        logger.warning(f"Manuscript {manuscript.siglum} has no IIIF URL")
        default = SingleManuscript.objects.filter(
            siglum="Urb1", iiif_url__isnull=False
        ).first()
        if default:
            manuscript = default

    # NEU: Calculate canvas_id from page_number
    canvas_id = None
    if page_number and manuscript.iiif_url:
        try:
            manifest_data = get_manifest_data(manuscript.iiif_url)
            if manifest_data and "sequences" in manifest_data:
                canvases = manifest_data["sequences"][0].get("canvases", [])
                # page_number is 1-indexed, array is 0-indexed
                if 0 < page_number <= len(canvases):
                    canvas_id = canvases[page_number - 1]["@id"]
                    logger.info(
                        f"Opening manuscript {manuscript.siglum} at page {page_number} "
                        f"(canvas: {canvas_id})"
                    )
                else:
                    logger.warning(
                        f"Page {page_number} out of range for {manuscript.siglum} "
                        f"(has {len(canvases)} pages)"
                    )
        except Exception as e:
            logger.error(f"Failed to calculate canvas_id: {e}", exc_info=True)
            # Fall back to opening at first page

    return render(
        request,
        "manuscript/mirador.html",
        {
            "manifest_url": manuscript.iiif_url,
            "canvas_id": canvas_id,  # ← NEU!
            "page_number": page_number,
            "manuscript": manuscript,
        },
    )
```

**Template-Check:** templates/manuscript/mirador.html
```html
<!-- Sollte bereits vorhanden sein (Zeile ~19): -->
window.viewer = Mirador.viewer({
  id: 'mirador-viewer',
  windows: [{
    manifestId: "{{ manifest_url }}",
    {% if canvas_id %}
    canvasId: "{{ canvas_id }}",
    {% endif %}
  }]
});
```

**Testing:**
```bash
# Test verschiedene page_numbers:
# http://localhost:8000/manuscripts/Urb1/mirador/1/   (Seite 1)
# http://localhost:8000/manuscripts/Urb1/mirador/42/  (Seite 42)
# http://localhost:8000/manuscripts/Urb1/mirador/999/ (Out of range)

# Prüfe Browser Console auf Mirador Errors
# Prüfe Django Logs
```

**Commit:**
```bash
git add manuscript/views.py
git commit -m "Fix: Use page_number parameter in Mirador viewer

- Calculate canvas_id from page_number and IIIF manifest
- Pass canvas_id to template for Mirador initialization
- Add bounds checking for page_number
- Add logging for debugging

Fixes: Bug #3 from code analysis
Estimated fix time: 4h"
```

---

#### Sub-Task 3.3: Silent Exceptions Fix (2-3h)

**Branch erstellen:**
```bash
git checkout main
git checkout -b fix/silent-exceptions
```

**Files zu editieren:**
- manuscript/models.py (Zeilen 426, 539)
- manuscript/resources.py (Zeile 244)

**Code-Änderung 1: manuscript/models.py:426**
```python
# ALT:
try:
    # ... existing code ...
except:
    pass

# NEU:
try:
    # ... existing code ...
except SpecificExpectedException as e:
    # Replace SpecificExpectedException with actual exception type from code
    logger.warning(f"Expected error in [function_name]: {e}")
    # Add fallback behavior if needed
except Exception as e:
    logger.error(f"Unexpected error in [function_name]: {e}", exc_info=True)
    # Decide: re-raise or continue with default value
    raise  # ODER: return default_value
```

**NOTE:** Erst Code an Zeilen 426, 539, 244 LESEN um zu verstehen:
1. Was passiert im try-Block?
2. Was könnte schiefgehen?
3. Was ist erwartetes vs. unerwartetes Error-Verhalten?

**Action:**
```bash
# Erst lesen bevor wir fixen:
# manuscript/models.py lines 420-430
# manuscript/models.py lines 535-545
# manuscript/resources.py lines 240-250
```

**Testing:**
```bash
# Trigger die Stellen die vorher silent fails hatten
# Check logs ob Exceptions jetzt geloggt werden
# Verify: App funktioniert weiterhin
```

**Commit:**
```bash
git add manuscript/models.py manuscript/resources.py
git commit -m "Fix: Replace silent exception handling with proper logging

- Replace bare 'except: pass' with specific exception handlers
- Add logging for debugging production issues
- Preserve existing fallback behavior

Locations: models.py:426, 539; resources.py:244
Fixes: Bug #4 (Silent Exceptions) from code analysis
Estimated fix time: 3h"
```

---

### Task 4: Meeting-Demo vorbereiten

**Zeitaufwand:** 2-3 Stunden
**Priorität:** HOCH
**Deadline:** 1 Tag vor Meeting

---

#### Sub-Task 4.1: Screenshots erstellen

**Erstelle Verzeichnis:**
```bash
mkdir -p .knowledge/08_demo/screenshots
```

**Screenshots für jedes Bug:**

**Bug #1: Urb1 Hardcoding**
- `before_urb1_hardcoding.png` - Code mit hardcoded "Urb1"
- `after_urb1_dynamic.png` - Code mit dynamic fallback
- `urb1_logs_before.png` - Keine Logs bei Fallback
- `urb1_logs_after.png` - Proper logging

**Bug #3: page_number**
- `before_page_number_ignored.png` - URL sagt Seite 42, Viewer zeigt Seite 1
- `after_page_number_works.png` - Viewer öffnet bei Seite 42
- `mirador_canvas_id_code.png` - Code der canvas_id berechnet

**Bug #2: IIIF Viewer fehlt**
- `stanzas_no_viewer.png` - /stanzas/ ohne Viewer
- `manuscript_stanzas_viewer.png` - /manuscripts/Urb1/stanzas/ MIT Viewer
- `comparison_side_by_side.png` - Beide Screenshots nebeneinander

---

#### Sub-Task 4.2: Demo-Script schreiben

**Datei:** .knowledge/08_demo/demo_script.md

```markdown
# Meeting Demo Script - 3./11. November 2025

## TIMING: 20 Minuten für Bug-Demo

---

### Bug #1: Urb1 Hardcoding (5 min)

**Christopher sagt:**
> "Ich habe im Code gefunden dass 'Urb1' an 5 Stellen hardcoded ist.
> Das bedeutet: Wenn ein anderes Manuscript nicht existiert oder keine
> IIIF-URL hat, fällt das System IMMER auf Urb1 zurück - auch wenn
> der User Cambridge sehen wollte."

**Screen-Share:**
1. Zeige Code: views.py:489 (ALT)
2. Zeige Code: views.py:489 (NEU mit Logging)

**Frage an Laura:**
> "Ist euch das aufgefallen? Funktionieren Cambridge/Florence/Yale richtig?"

**Laura antwortet:**
- FALLS JA: "Gut, dann fixen wir das. 6h Arbeit, 900€"
- FALLS NEIN: "Okay, vielleicht ist es nicht so wichtig. Eure Entscheidung."

---

### Bug #3: page_number ignoriert (5 min)

**Christopher sagt:**
> "Die URL erlaubt einen page_number Parameter: /mirador/Urb1/42/
> Aber dieser Parameter wird im Code ignoriert. Der Viewer öffnet
> immer bei Seite 1."

**Live-Demo:**
1. Browser: http://localhost:8000/manuscripts/Urb1/mirador/42/
2. Zeige: Viewer öffnet bei Seite 1 (ALT)
3. Git checkout fix/mirador-page-number
4. Restart server
5. Browser: Same URL
6. Zeige: Viewer öffnet bei Seite 42 (NEU)

**Frage an Laura:**
> "Braucht ihr diese Funktion? Wollt ihr dass User direkt zu Seiten springen können?"

**Laura antwortet:**
- FALLS JA: "Fix kostet 600€, 4h Arbeit"
- FALLS NEIN: "Okay, sparen wir uns"

---

### Bug #2: IIIF Viewer fehlt (8 min)

**Christopher sagt:**
> "Das ist der größte Bug. Auf /stanzas/ fehlt der IIIF-Viewer komplett.
> Aber auf /manuscripts/Urb1/stanzas/ funktioniert er mit Tify.
> Die Frage ist: SOLL er auf /stanzas/ sein?"

**Screen-Share:**
1. Browser: https://lasfera.rrchnm.org/stanzas/
2. Zeige: Nur Text, kein Viewer
3. Browser: https://lasfera.rrchnm.org/manuscripts/Urb1/stanzas/
4. Zeige: Text + Tify Viewer

**Christopher fragt:**
> "Laura, wie soll /stanzas/ aussehen? Soll es wie die Manuscript-Version sein?"

**Laura antwortet (möglich):**
- "Ja, genau so!" → Christopher: "Okay, das sind 20-30h Arbeit, 3.000-4.500€"
- "Nein, nur Text ist okay" → Christopher: "Dann kein Bug, alles gut!"
- "Vielleicht später" → Christopher: "Okay, machen wir später wenn Budget da ist"

---

### Kosten-Zusammenfassung (2 min)

**Christopher zeigt Tabelle:**

| Bug                     | Aufwand | Kosten  | Status        |
|-------------------------|---------|---------|---------------|
| #1: Urb1 Hardcoding     | 6h      | 900€    | [Laura: Y/N]  |
| #3: page_number         | 4h      | 600€    | [Laura: Y/N]  |
| #4: Silent Exceptions   | 3h      | 450€    | [Empfohlen]   |
| #2: IIIF Viewer         | 25h     | 3.750€  | [Optional]    |
| Deployment + Testing    | 4h      | 600€    | [Immer]       |

**Szenarien:**
- **Minimum (Bugs #1+#3+#4):** 2.500€
- **Standard (+ Bug #2):** 6.250€

---

### Fragen an Laura (noch 5 min Zeit)

1. "Gibt es ANDERE Bugs die dir aufgefallen sind?"
2. "Funktioniert die Gazetteer-Karte bei euch?"
3. "Wann brauchen wir Zugang zum Dev-Environment?"
4. "Wer ist technischer Ansprechpartner für Code-Reviews?"

---

## OUTCOME

**Laura genehmigt:**
- [ ] Bug #1 - Urb1 Hardcoding
- [ ] Bug #3 - page_number
- [ ] Bug #4 - Silent Exceptions
- [ ] Bug #2 - IIIF Viewer

**Budget genehmigt:** ______€

**Timeline:** Start _____, Fertig _____

**Next Step:** Christopher schickt detailliertes Angebot in 2-3 Tagen
```

---

#### Sub-Task 4.3: Kosten-Breakdown aktualisieren

**Datei:** .knowledge/05_deliverables/cost_estimate_v2.md

Basierend auf tatsächlichem Code-Aufwand:

```markdown
# Kosten-Kalkulation - La Sfera Bug-Fixes

**Datum:** 28. Oktober 2025
**Stundensatz:** 150€
**Overhead-Faktor:** 1.55x (55% für Testing, Deployment, Meetings)

---

## Szenario A: MINIMUM (Quick Fixes)

| Task                          | Dev  | Overhead | Total | Kosten  |
|-------------------------------|------|----------|-------|---------|
| Bug #1: Urb1 Hardcoding       | 6h   | 3.3h     | 9.3h  | 1.395€  |
| Bug #3: page_number           | 4h   | 2.2h     | 6.2h  | 930€    |
| Bug #4: Silent Exceptions     | 3h   | 1.7h     | 4.7h  | 705€    |
| Code Review                   | -    | 2h       | 2h    | 300€    |
| Deployment to Dev             | -    | 2h       | 2h    | 300€    |
| Production Deployment         | -    | 2h       | 2h    | 300€    |
| **TOTAL**                     | 13h  | 13.2h    | 26.2h | **3.930€** |

**Timeline:** 2 Wochen
**Zahlungsplan:** 50% Start, 50% bei Abnahme

---

## Szenario B: STANDARD (+ IIIF Viewer)

| Task                          | Dev  | Overhead | Total | Kosten   |
|-------------------------------|------|----------|-------|----------|
| Szenario A                    | -    | -        | -     | 3.930€   |
| Bug #2: IIIF Viewer Integration | 25h | 13.8h   | 38.8h | 5.820€   |
| Additional Testing            | -    | 3h       | 3h    | 450€     |
| **TOTAL**                     | 38h  | 30h      | 68h   | **10.200€** |

**Timeline:** 5 Wochen
**Zahlungsplan:** 30% Start, 40% nach 3 Wochen, 30% bei Abnahme

---

## Pay-per-Bug (falls Laura nur einzelne Bugs will)

| Bug                     | Kosten (inkl. Overhead) |
|-------------------------|-------------------------|
| #1: Urb1 Hardcoding     | 1.395€                  |
| #3: page_number         | 930€                    |
| #4: Silent Exceptions   | 705€                    |
| #2: IIIF Viewer         | 5.820€                  |

**Deployment** (mindestens einmal nötig): 600€

---

## Hinweise

- Alle Preise inkl. Code Review, Testing, Deployment
- Dev-Environment Zugang erforderlich (Laura organisiert)
- Code wird als Pull Request geliefert
- 2 Wochen Bugfix-Garantie nach Deployment
```

---

### Task 5: Risiko-Mitigation Checklist

**Zeitaufwand:** 30 Minuten

**Datei:** .knowledge/07_implementation/risk_mitigation.md

```markdown
# Risiko-Mitigation Checklist

## VOR Meeting

- [ ] E-Mail an Laura versendet
- [ ] Meeting-Termin bestätigt (3. oder 11. Nov)
- [ ] Dev-Environment funktioniert lokal
- [ ] Alle 3 Bug-Fix Branches erstellt
- [ ] Code kompiliert ohne Errors
- [ ] Screenshots erstellt
- [ ] Demo-Script reviewed

## WÄHREND Meeting

- [ ] Laura zeigt ihre Perspektive der Bugs (Screen-Share)
- [ ] Christopher zeigt Fixes (Live-Demo auf localhost)
- [ ] Budget GENAU besprochen (keine "ungefähr"-Schätzungen)
- [ ] Timeline GENAU besprochen (Start-Datum, End-Datum)
- [ ] Dev-Environment Zugang geklärt
- [ ] Technischer Ansprechpartner identifiziert
- [ ] Code-Review Prozess geklärt (wer? wie schnell?)

## NACH Meeting (falls genehmigt)

- [ ] Schriftliches Angebot versendet (2-3 Tage)
- [ ] Vertrag unterschrieben
- [ ] 50% Anzahlung erhalten
- [ ] Dev-Environment Zugang erhalten
- [ ] Pull Request erstellt
- [ ] Code Review durchgeführt
- [ ] Deploy to Dev
- [ ] Laura tested auf Dev (48h Window)
- [ ] Deploy to Production
- [ ] Monitoring (1 Woche)
- [ ] Final Invoice

## Red Flags (Projekt NICHT starten)

- [ ] Laura kann Bugs NICHT reproduzieren → Vielleicht kein echtes Problem
- [ ] Kein Dev-Environment Zugang → Können nicht testen
- [ ] Budget < 2.000€ → Nicht lohnend, zu viel Risiko
- [ ] Timeline < 1 Woche → Unmöglich, würde in schlechte Quality resultieren
- [ ] Laura will KEINE Code-Reviews → Quality-Risiko
```

---

## Phase 2: Meeting (3. oder 11. Nov, 45 min)

**Siehe:** .knowledge/08_demo/demo_script.md

**Kritische Fragen für Laura:**
1. Funktionieren andere Manuscripts (Cambridge, Florence, Yale)?
2. Braucht ihr page_number Funktionalität?
3. Soll IIIF-Viewer auf /stanzas/ sein?
4. Funktioniert Gazetteer-Karte?
5. Welches Budget steht zur Verfügung?
6. Wann muss was fertig sein?

---

## Phase 3: Nach Meeting (ab 12. Nov)

### FALLS Szenario A genehmigt (2.500€, 2 Wochen):

**Woche 1 (11.-15. Nov):**
```bash
# Tag 1-2: Bug #1
git checkout fix/urb1-hardcoding
# Finalize code, create PR
gh pr create --title "Fix: Urb1 Hardcoding" --body "..."

# Tag 3: Bug #3
git checkout fix/mirador-page-number
# Finalize code, create PR

# Tag 4: Bug #4
git checkout fix/silent-exceptions
# Finalize code, create PR

# Tag 5: Code Review Feedback
# Address review comments
```

**Woche 2 (18.-22. Nov):**
```bash
# Tag 1: Merge PRs
git checkout main
git pull origin main

# Tag 2: Deploy to Dev
# (via CI/CD oder manuell)

# Tag 3-4: Laura Testing auf Dev
# Christopher: Stand-by für Bugfixes

# Tag 5: Deploy to Production
# Monitoring
```

---

### FALLS Szenario B genehmigt (6.250€, 5 Wochen):

**Woche 1-2:** Wie Szenario A

**Woche 3 (25.-29. Nov):**
- templates/stanzas.html analysieren
- Mirador Layout mit Laura abstimmen
- Start IIIF Integration

**Woche 4 (2.-6. Dez):**
- Canvas-ID aus Line Code berechnen
- Sync-Logik Text ↔ Bild
- Testing

**Woche 5 (9.-13. Dez):**
- Finalization
- Code Review
- Deploy

---

## Zusammenfassung: Was JETZT tun?

### HEUTE (28. Okt):
1. ✅ E-Mail an Laura schicken
2. ✅ Dev-Environment aufsetzen (1-2h)

### Diese Woche (29. Okt - 1./9. Nov):
3. ✅ Bug-Fix Branches + Code (12-14h)
4. ✅ Screenshots erstellen (1h)
5. ✅ Demo-Script finalisieren (1h)

### 1 Tag vor Meeting (2./10. Nov):
6. ✅ Demo durchspielen (dry-run, 30 min)
7. ✅ Laptop + Screen-Share Setup testen
8. ✅ Fragen-Liste finalisieren

### Meeting (3./11. Nov):
9. ⏳ Demo präsentieren
10. ⏳ Budget verhandeln
11. ⏳ Timeline festlegen

### Nach Meeting (ab 12. Nov):
12. ⏳ Deployment (FALLS genehmigt)

---

## CRITICAL PATH

**Was blockiert was?**

```
E-Mail → Meeting-Termin bestätigt
  ↓
Dev-Environment → Bug-Fixes Code
  ↓
Bug-Fixes Code → Screenshots → Demo-Script
  ↓
Demo-Script → Meeting
  ↓
Meeting → Genehmigung
  ↓
Genehmigung → Dev-Access
  ↓
Dev-Access → Deployment
```

**Bottlenecks:**
- Laura's Response Zeit (E-Mail → Meeting)
- Meeting-Entscheidung (Go/No-Go)
- Dev-Environment Zugang (kann 3-5 Tage dauern)

---

## FINAL ANSWER: Was können wir JETZT umsetzen?

### ✅ SOFORT (Heute):
1. E-Mail an Laura (15 min)
2. Dev-Environment Setup (2h)
3. Bug #1 Code anfangen (2-3h)

### ✅ Diese Woche (15-20h total):
4. Bug #1 Code fertig (4-6h)
5. Bug #3 Code fertig (3-5h)
6. Bug #4 Code fertig (2-3h)
7. Screenshots + Demo (2-3h)

### ❌ NICHT JETZT:
- Deployment zu Production (braucht Laura's Genehmigung)
- Bug #2 IIIF Viewer (braucht Laura's Input + 25h)
- Gazetteer (erst verifizieren ob kaputt)

### ⏳ Nach Meeting:
- Deployment (FALLS genehmigt)
- Pull Requests mergen
- Production-Release

---

**BEGRÜNDUNG:**

Wir implementieren **VORBEREITUNG statt DEPLOYMENT** weil:

1. **Respekt für Client:** Laura muss Bugs sehen und bestätigen
2. **Risk Management:** Keine Deployments ohne Genehmigung
3. **Professionalität:** Vorbereitung zeigt Kompetenz
4. **Flexibilität:** Laura kann im Meeting sagen "Bug #2 ist wichtiger als #1"
5. **Budget-Sicherheit:** Erst Genehmigung, dann Rechnung

**RESULTAT:**

Nach Meeting haben wir:
- ✅ 3 fertige Bug-Fixes
- ✅ Laura's Bestätigung welche sie will
- ✅ Genehmigtes Budget
- ✅ Klare Timeline
- ✅ Deployment kann in 1-2 Wochen passieren

**DAS IST DER PLAN!** 🚀
