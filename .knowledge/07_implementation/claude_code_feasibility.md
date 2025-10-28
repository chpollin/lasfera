# Claude Code Implementation - Feasibility Analysis

**Datum:** 28. Oktober 2025
**Kontext:** Meeting mit Laura am 3. oder 11. November 2025
**Status:** PRE-MEETING (Bugs noch nicht mit Client bestätigt)

---

## Executive Summary

**EMPFEHLUNG: NICHT JETZT implementieren, sondern VORBEREITEN**

Warum:
- Meeting mit Laura steht noch aus (3./11. Nov)
- Bugs sind Code-verifiziert, aber nicht User-facing verifiziert
- Risiko: Wir fixen Dinge die Laura vielleicht nicht als Problem sieht
- Besserer Ansatz: **Vorbereitung + Demonstration im Meeting**

---

## Analyse der vorgeschlagenen Claude Code Tasks

### ✅ SOFORT MACHBAR (Vorbereitung, kein Deployment)

#### 1. Bug #1 Fix vorbereiten: Urb1 Hardcoding
**Status:** BEREIT ZUM IMPLEMENTIEREN
**Aufwand:** 4-6h

**Code-Standorte:** manuscript/views.py:489, 492, 498, 537, 694

**Lösung:**
```python
# Statt:
except SingleManuscript.DoesNotExist:
    manuscript = SingleManuscript.objects.get(siglum="Urb1")

# Implementieren:
DEFAULT_MANUSCRIPT = "Urb1"  # Config-Variable
try:
    manuscript = SingleManuscript.objects.get(siglum=manuscript_id)
except SingleManuscript.DoesNotExist:
    logger.warning(f"Manuscript {manuscript_id} not found, using default {DEFAULT_MANUSCRIPT}")
    manuscript = SingleManuscript.objects.get(siglum=DEFAULT_MANUSCRIPT)
except SingleManuscript.MultipleObjectsReturned:
    logger.error(f"Multiple manuscripts found for {manuscript_id}")
    manuscript = SingleManuscript.objects.filter(siglum=manuscript_id).first()
```

**Warum jetzt machbar:**
- ✅ Code-Locations bekannt
- ✅ Lösung eindeutig
- ✅ Keine Template-Änderungen nötig
- ✅ Rückwärts-kompatibel

**Warum NICHT deployen:**
- ❌ Laura hat Bug noch nicht demonstriert
- ❌ Vielleicht ist "Urb1 als Default" gewollt?
- ❌ Risiko: Fix ohne Bestätigung

**EMPFEHLUNG:** Code schreiben, Branch erstellen, im Meeting demonstrieren

---

#### 2. Bug #3 Fix vorbereiten: page_number Parameter
**Status:** BEREIT ZUM IMPLEMENTIEREN
**Aufwand:** 3-5h

**Code-Location:** manuscript/views.py:485-506

**Lösung:**
```python
def mirador_view(request, manuscript_id, page_number):
    try:
        manuscript = SingleManuscript.objects.get(pk=manuscript_id)
    except SingleManuscript.DoesNotExist:
        manuscript = SingleManuscript.objects.get(siglum=DEFAULT_MANUSCRIPT)

    # NEU: Canvas ID aus page_number berechnen
    canvas_id = None
    if page_number and manuscript.iiif_url:
        manifest_data = get_manifest_data(manuscript.iiif_url)
        if manifest_data and "sequences" in manifest_data:
            canvases = manifest_data["sequences"][0]["canvases"]
            if 0 < page_number <= len(canvases):
                canvas_id = canvases[page_number - 1]["@id"]

    return render(request, "manuscript/mirador.html", {
        "manifest_url": manuscript.iiif_url,
        "canvas_id": canvas_id,  # ← NEU!
        "page_number": page_number,
    })
```

**Warum jetzt machbar:**
- ✅ Code-Location bekannt
- ✅ get_manifest_data() Funktion existiert bereits
- ✅ Mirador Template akzeptiert canvas_id

**Warum NICHT deployen:**
- ❌ Laura hat vielleicht nie versucht, direkt zu Seite X zu springen
- ❌ URL-Schema könnte anders sein als gedacht

**EMPFEHLUNG:** Code schreiben, Branch erstellen, im Meeting Live-Demo

---

#### 3. Silent Exception Handling fixen
**Status:** BEREIT ZUM IMPLEMENTIEREN
**Aufwand:** 2-3h

**Code-Locations:**
- manuscript/models.py:426, 539
- manuscript/resources.py:244

**Lösung:**
```python
# Statt:
try:
    # ... code ...
except:
    pass

# Implementieren:
import logging
logger = logging.getLogger(__name__)

try:
    # ... code ...
except SpecificException as e:
    logger.error(f"Failed to process X: {e}", exc_info=True)
    # Optional: Fallback-Verhalten
except Exception as e:
    logger.critical(f"Unexpected error in Y: {e}", exc_info=True)
    raise  # Re-raise wenn kritisch
```

**Warum jetzt machbar:**
- ✅ Einfaches Refactoring
- ✅ Keine funktionale Änderung (nur Logging)
- ✅ Best Practice

**Warum VORSICHTIG:**
- ⚠️ Wir wissen NICHT was die bare excepts verstecken
- ⚠️ Könnte versteckte Bugs aufdecken → Production-Crash

**EMPFEHLUNG:** In Dev-Branch fixen, ausgiebig testen, erst nach Meeting deployen

---

### ⚠️ BRAUCHT LAURA'S INPUT (Meeting First)

#### 4. Bug #2: IIIF Viewer in /stanzas/ integrieren
**Status:** BLOCKIERT BIS MEETING
**Aufwand:** 20-30h

**Problem:**
- Wir haben templates/stanzas.html NICHT gelesen
- Wir wissen NICHT ob Laura das Feature überhaupt will
- Wir wissen NICHT welches Layout sie bevorzugt (Side-by-side? Tabs? Modal?)

**Fragen für Laura:**
1. "Soll auf /stanzas/ ein Manuscript-Viewer sein?"
2. "Wenn ja: Wie soll das Layout aussehen?" (zeigen: manuscript_stanzas vs stanzas)
3. "Welcher Viewer? Mirador oder Tify?"
4. "Soll Viewer mit Text synchronisiert sein?"

**EMPFEHLUNG:** Im Meeting screen-sharen, Laura zeigen:
- `/stanzas/` (aktuell: nur Text)
- `/manuscripts/Urb1/stanzas/` (hat Tify-Viewer)
- Fragen: "Soll das erste wie das zweite aussehen?"

**ERST NACH Meeting implementieren** (potentiell 20-30h = 3.000-4.500€!)

---

#### 5. Gazetteer API Optimierung
**Status:** BLOCKIERT BIS VERIFIZIERUNG
**Aufwand:** 4-8h (FALLS kaputt)

**Problem:**
- WebFetch zeigte: API funktioniert (/api/toponyms/ gibt Daten)
- Browser-Test FEHLT: Werden Leaflet-Marker gerendert?
- Laura hat NICHT gesagt dass Gazetteer kaputt ist

**Fragen für Laura:**
1. "Funktioniert die Gazetteer-Karte bei dir?"
2. "Siehst du Marker auf der Karte?"
3. "Ist es langsam?" (700+ Toponyme)

**EMPFEHLUNG:** Im Meeting: Laura screenshart Gazetteer
- Wenn funktioniert → NICHT FIXEN (don't fix what ain't broke)
- Wenn kaputt → DANN Pagination/Caching implementieren

---

### ❌ NICHT JETZT (Out of Scope)

#### 6. Test-Suite erstellen
**Warum nicht:**
- ❌ Nicht in Kalkulation (KONKRETE_BUGS_GEFUNDEN.md)
- ❌ 40-60h Aufwand (6.000-9.000€)
- ❌ Laura zahlt für Bug-Fixes, nicht für Tests
- ❌ Kommt NACH Bug-Fixes (wenn überhaupt)

**Alternative:** Basic smoke tests für die 3 Bug-Fixes schreiben (2-3h, im Overhead enthalten)

---

#### 7. Mirador Alpha → Stable Upgrade
**Warum nicht:**
- ❌ RIESIGES Risiko (Breaking Changes von Alpha → Stable)
- ❌ Könnte NEUE Bugs einführen
- ❌ Müsste ALLE IIIF-Templates testen
- ❌ 10-15h Aufwand + Risiko
- ❌ Nicht in Laura's Bug-Liste

**Alternative:** In Meeting erwähnen als "Future Enhancement" (Premium-Szenario)

---

#### 8. Performance-Optimierung
**Warum nicht:**
- ❌ Kein Performance-Problem bekannt
- ❌ Premature Optimization
- ❌ Laura hat nicht über Geschwindigkeit geklagt

**Alternative:** WENN Laura sagt "Seite ist langsam" → dann profilen → dann optimieren

---

## Konkreter Implementierungsplan

### Phase 1: VOR Meeting (28. Okt - 2./10. Nov)

**Ziel:** Vorbereitung, keine Production-Deployments

#### Task 1.1: Bug-Fix Branches erstellen
```bash
git checkout -b fix/urb1-hardcoding
git checkout -b fix/mirador-page-number
git checkout -b fix/silent-exceptions
```

#### Task 1.2: Code schreiben (lokale Dev-Environment)
- Bug #1 Fix (4-6h)
- Bug #3 Fix (3-5h)
- Silent Exceptions (2-3h)
**Total:** 9-14h

#### Task 1.3: Lokales Testing
- `python manage.py runserver`
- Manuell testen:
  - Cambridge Manuscript (statt Urb1)
  - Direct page jump in Mirador
  - Check logs für proper exceptions
**Total:** 2-3h

#### Task 1.4: Meeting-Demo vorbereiten
- Screenshots: Before/After
- Live-Demo Script
- Kosten-Kalkulation pro Fix
**Total:** 1-2h

**PHASE 1 TOTAL:** 12-19h (NUR Vorbereitung, kein Deployment)

---

### Phase 2: WÄHREND Meeting (3. oder 11. Nov, 45 min)

#### Agenda-Punkt 1: Bug-Demonstration (20 min)

**Christopher demonstriert:**
1. **Bug #1 reproduzieren:**
   - Versuche Cambridge-Manuscript zu öffnen
   - Zeige: Fällt auf Urb1 zurück (FALLS das passiert)

2. **Bug #1 Fix zeigen:**
   - Zeige Code: vorher/nachher
   - Zeige: Funktioniert jetzt mit allen Manuscripts
   - Kosten: 900€ (6h × 150€)

3. **Bug #3 reproduzieren:**
   - URL: /manuscripts/Urb1/mirador/42/
   - Zeige: Öffnet immer Seite 1, ignoriert "42"

4. **Bug #3 Fix zeigen:**
   - Zeige Code: canvas_id Berechnung
   - Zeige: Springt zu korrekter Seite
   - Kosten: 600€ (4h × 150€)

5. **Bug #2 zeigen:**
   - Laura: "Soll hier ein Viewer sein?" → `/stanzas/`
   - Christopher: "Das wäre 20-30h Arbeit, ca. 3.000-4.500€. Wollt ihr das?"

**Laura entscheidet:**
- [ ] Bug #1: Ja, fixen
- [ ] Bug #3: Ja, fixen
- [ ] Bug #2: Ja/Nein/Später

---

#### Agenda-Punkt 2: Budget (15 min)

**Szenarien anpassen basierend auf Laura's Feedback:**

**Szenario A - Quick Fixes (BESTÄTIGT):**
```
Bug #1: Urb1 Hardcoding         900€
Bug #3: page_number              600€
Silent Exceptions                450€
Deployment & Testing             550€
                               ──────
TOTAL:                         2.500€   (2 Wochen)
```

**Szenario B - Mit IIIF (FALLS Laura will):**
```
Szenario A                     2.500€
+ Bug #2: IIIF in Stanzas      3.750€
                               ──────
TOTAL:                         6.250€   (4-5 Wochen)
```

**Szenario C - Gazetteer auch (FALLS kaputt):**
```
Szenario B                     6.250€
+ Gazetteer Optimierung        1.200€
                               ──────
TOTAL:                         7.450€   (5-6 Wochen)
```

---

#### Agenda-Punkt 3: Timeline (10 min)

**WENN Szenario A genehmigt:**
```
Woche 1 (11.-15. Nov):  Bug #1 + #3 implementieren, testen
Woche 2 (18.-22. Nov):  Silent Exceptions, Code Review, Deployment
                        → FERTIG
```

**WENN Szenario B genehmigt:**
```
Woche 1-2:              Quick Fixes (wie oben)
Woche 3 (25.-29. Nov):  IIIF Viewer Design + Implementation Start
Woche 4 (2.-6. Dez):    IIIF Viewer Canvas-Sync + Testing
Woche 5 (9.-13. Dez):   Final Review + Deployment
                        → FERTIG vor Weihnachten
```

---

### Phase 3: NACH Meeting (ab 12. Nov)

#### Szenario A genehmigt:

**Woche 1:**
- [ ] Merge fix/urb1-hardcoding Branch
- [ ] Merge fix/mirador-page-number Branch
- [ ] Merge fix/silent-exceptions Branch
- [ ] Create Pull Request
- [ ] Code Review mit RRCHNM (48h?)
- [ ] Deploy to Dev (dev.lasfera.rrchnm.org)

**Woche 2:**
- [ ] Laura testet auf Dev
- [ ] Fix any issues
- [ ] Deploy to Production
- [ ] Monitoring (1 Woche)
- [ ] Invoice schicken (2.500€)

---

#### Szenario B genehmigt:

**Woche 1-2:** (wie Szenario A)

**Woche 3-4:**
- [ ] templates/stanzas.html analysieren
- [ ] Mirador Layout designen (mit Laura abstimmen!)
- [ ] Canvas-ID aus Line Code berechnen
- [ ] Sync-Logik implementieren
- [ ] Testing (verschiedene Manuscripts)

**Woche 5:**
- [ ] Final adjustments
- [ ] Deploy to Production
- [ ] Invoice (6.250€)

---

## Risiko-Analyse

### Technische Risiken

**Risiko 1: Wir fixen Dinge die nicht kaputt sind**
- **Wahrscheinlichkeit:** MITTEL
- **Impact:** Zeit-Verschwendung, Laura zahlt für Unnötiges
- **Mitigation:** Meeting-Demo BEVOR wir deployen

**Risiko 2: Fixes brechen andere Features**
- **Wahrscheinlichkeit:** NIEDRIG (simple Changes)
- **Impact:** Production-Downtime
- **Mitigation:**
  - Dev-Environment Testing
  - Code Review
  - Staging Deployment first

**Risiko 3: IIIF Bug #2 ist komplexer als gedacht**
- **Wahrscheinlichkeit:** MITTEL
- **Impact:** 20-30h → 40-50h (Budget-Überschreitung)
- **Mitigation:**
  - Erst templates/stanzas.html lesen
  - Time-boxed Approach (max 30h)
  - Laura vorwarnen: "Das könnte länger dauern"

**Risiko 4: Keine Dev-Environment Zugang**
- **Wahrscheinlichkeit:** NIEDRIG
- **Impact:** Testing blockiert
- **Mitigation:** Im Meeting klären: "Wann kriegen wir Zugang?"

---

### Business-Risiken

**Risiko 1: Laura genehmigt gar nichts**
- **Wahrscheinlichkeit:** NIEDRIG
- **Impact:** 12-19h Vorbereitung = Sunk Cost
- **Mitigation:** Akzeptabel (Vorbereitung war nötig für seriöses Angebot)

**Risiko 2: Budget zu hoch**
- **Wahrscheinlichkeit:** MITTEL
- **Impact:** Projekt fällt weg
- **Mitigation:**
  - Szenario A ist NUR 2.500€ (sehr niedrig)
  - "Pay per Bug" anbieten (Bug #1: 900€, Bug #3: 600€ einzeln buchbar)

**Risiko 3: Timeline zu kurz**
- **Wahrscheinlichkeit:** NIEDRIG (Juni 2026 Deadline!)
- **Impact:** Stress, Quality-Issues
- **Mitigation:** Timeline ist realistisch (2-5 Wochen, Deadline in 8 Monaten)

---

## Empfehlung: Konkreter Action Plan

### JETZT (28. Okt - 2./10. Nov):

1. **E-Mail an Laura schicken** (TODAY!)
   - Anhang: MEETING_BRIEF.md
   - Anhang: KONKRETE_BUGS_GEFUNDEN.md
   - Text: "Habe 3 Bugs gefunden, ~10k€ für alle. Meeting: Demonstrieren + Budget besprechen"

2. **Dev-Environment aufsetzen** (1-2h)
   ```bash
   git clone https://github.com/chnm/lasfera
   poetry install
   docker-compose up -d  # PostgreSQL
   python manage.py migrate
   python manage.py runserver
   ```

3. **Bug-Fixes VORBEREITEN** (12-19h)
   - 3 Branches erstellen
   - Code schreiben
   - Lokal testen
   - Screenshots machen

4. **Meeting-Demo vorbereiten** (2h)
   - Screen-Share Script
   - Before/After Screenshots
   - Kosten-Breakdown pro Bug

**TOTAL VOR MEETING:** 15-23h (Vorbereitung, kein Deployment)

---

### IM MEETING (3./11. Nov):

1. **Laura demonstriert Bugs** (ihre Perspektive)
2. **Christopher zeigt Fixes** (Code + Kosten)
3. **Budget-Entscheidung** (A: 2.5k, B: 6.2k, C: 7.4k)
4. **Timeline-Entscheidung** (Start: Mitte November?)

---

### NACH MEETING (ab 12. Nov):

**FALLS genehmigt:**
- Deployment-Zugang klären
- Pull Requests erstellen
- Code Review
- Deploy → Test → Invoice

**FALLS NICHT genehmigt:**
- Freundlich bleiben
- Vielleicht später (Post-Launch Issues)
- Vorbereitung war trotzdem wertvoll (Portfolio, Erfahrung)

---

## Warum NICHT sofort implementieren?

1. **Respekt für Client:** Laura muss Bugs bestätigen
2. **Budget-Sicherheit:** Erst Genehmigung, dann Arbeit
3. **Risiko-Minimierung:** Demo zeigt dass Fixes funktionieren
4. **Professionell:** Vorbereitung zeigt Kompetenz, verhindert Überraschungen

---

## Zusammenfassung

**Was können wir JETZT umsetzen?**
- ✅ Dev-Environment aufsetzen
- ✅ Bug-Fixes VORBEREITEN (Code schreiben, nicht deployen)
- ✅ Meeting-Demo vorbereiten
- ✅ E-Mail an Laura schicken

**Was kommt NACH Meeting?**
- ⏳ Deployment (FALLS genehmigt)
- ⏳ IIIF Integration (FALLS gewünscht)
- ⏳ Gazetteer (FALLS kaputt)

**Was ist READY TO GO?**
- Bug #1 Fix (Urb1) - Code schreiben: 4-6h
- Bug #3 Fix (page_number) - Code schreiben: 3-5h
- Silent Exceptions - Code schreiben: 2-3h

**Was braucht mehr Info?**
- Bug #2 (IIIF) - Laura-Input nötig
- Gazetteer - Erst verifizieren ob kaputt

---

**NEXT STEP:** E-Mail an Laura schicken, Meeting bestätigen, Dev-Environment aufsetzen

**CRITICAL:** Keine Production-Deployments ohne Laura's Bestätigung!
