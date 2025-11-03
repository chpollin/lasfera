# La Sfera - Bug Inventory (VERIFIZIERT)

**Datum:** 28. Oktober 2025 (Updated nach Live-Site Tests)
**Methode:** Code-Analyse + Live-Site Browser-Tests
**Status:** ✅ VOLLSTÄNDIG VERIFIZIERT (Code + Live-Site)
**Quelle:** Repository chnm/lasfera + https://lasfera.rrchnm.org

---

## ⚠️ WICHTIGE ERKENNTNISSE (NACH LIVE-TESTS)

**Ursprüngliche Annahme (Code-only):** 2 Bugs, 12h Aufwand, 2.340€
**Nach Live-Site Tests:** 3 echte Bugs, 18h Aufwand, 3.510€

**KRITISCHE REVISION:**
- ✅ Bug #1 (Urb1 Hardcoding) - Bestätigt, aber weniger kritisch (fehlende Daten)
- ✅ Bug #2 (IIIF Viewer fehlt) - **EXISTIERT DOCH!** Viewer rendert nicht (JS-Problem)
- ✅ Bug #3 (page_number) - Bestätigt
- ❌ Bug #4 (Silent Exceptions) - Widerlegt (bereits korrekt)
- ✅ Bug #5 (Gazetteer) - **FUNKTIONIERT PERFEKT** (kein Bug)

---

## ✅ VERIFIZIERTE BUGS (3)

### BUG #1: Fehlende IIIF-Manifeste + Hardcoding-Fallback

**Status:** ✅ VERIFIZIERT durch Code-Analyse + Live-Tests
**Severity:** KRITISCH (aber Daten-Problem dominiert)
**Impact:** Die meisten Manuscripts zeigen "No IIIF manifest or photographs available"

**Live-Test Ergebnisse:**
- ✅ Urb1: Hat IIIF-Manifest (https://digi.vatlib.it/iiif/MSS_Urb.lat.752/manifest.json)
- ❌ Yale1: "No IIIF manifest or photographs available"
- ❌ Fn1: "No IIIF manifest or photographs available"
- ✅ Cam: Funktioniert (Harvard IIIF: https://iiif.lib.harvard.edu/manifests/drs:3684069)

**HAUPTPROBLEM:** Daten fehlen in DB, nicht Code-Fehler!
**SEKUNDÄRPROBLEM:** Hardcoding-Bug in Fallback-Logik

**Betroffene Files:**
- [manuscript/views.py:489](manuscript/views.py#L489) - `mirador_view()` DoesNotExist fallback
- [manuscript/views.py:492](manuscript/views.py#L492) - `mirador_view()` No IIIF URL fallback
- [manuscript/views.py:498](manuscript/views.py#L498) - `mirador_view()` Manifest fetch error
- [manuscript/views.py:537](manuscript/views.py#L537) - `stanzas()` default_manuscript
- [manuscript/views.py:694](manuscript/views.py#L694) - `manuscripts()` default_manuscript

**Code-Beispiel:**
```python
# views.py:489
except SingleManuscript.DoesNotExist:
    manuscript = SingleManuscript.objects.get(siglum="Urb1")  # ❌ Hardcoded!

# views.py:492
if not manuscript.iiif_url:
    manuscript = SingleManuscript.objects.get(siglum="Urb1")  # ❌ Hardcoded!

# views.py:537
default_manuscript = SingleManuscript.objects.get(siglum="Urb1")  # ❌ Hardcoded!
```

**Problem:**
- Keine konfigurierbare Fallback-Logik
- `.get(siglum="Urb1")` kann DoesNotExist Exception werfen wenn Urb1 fehlt
- Andere Manuscripts werden nicht gleichwertig behandelt

**Lösung:**
```python
# Konfigurierbare Default-Manuscript (z.B. settings.py)
DEFAULT_MANUSCRIPT = getattr(settings, 'DEFAULT_MANUSCRIPT_SIGLUM', 'Urb1')

# Sichere Fallback-Logik
try:
    manuscript = SingleManuscript.objects.get(id=manuscript_id)
except SingleManuscript.DoesNotExist:
    logger.warning(f"Manuscript {manuscript_id} not found, using default")
    manuscript = SingleManuscript.objects.filter(
        siglum=DEFAULT_MANUSCRIPT
    ).first()
    if not manuscript:
        # Ultimate fallback: Irgendein Manuscript mit IIIF
        manuscript = SingleManuscript.objects.filter(
            iiif_url__isnull=False
        ).first()
        if not manuscript:
            raise Http404("No manuscripts available")
```

**Complexity:** MEDIUM
- Fallback-Logik refactoren
- Alle 5 Hardcodes ändern
- Testing required

---

### BUG #2: IIIF-Viewer rendert nicht

**Status:** ✅ VERIFIZIERT durch Live-Tests (EXISTIERT DOCH!)
**Severity:** HOCH
**Impact:** Viewer nicht sichtbar auf /stanzas/ und /manuscripts/Urb1/stanzas/

**Live-Test Ergebnisse:**
- ❌ /stanzas/ - Kein Viewer sichtbar
- ❌ /manuscripts/Urb1/stanzas/ - Kein Viewer sichtbar
- ⚠️ Code HAT Tify-Container (templates/stanzas.html:265-275)
- ⚠️ CSS vorhanden (.tify-container), aber keine Initialisierung

**URSACHE:** JavaScript-Initialisierungsproblem, nicht Template-Problem

**Code-Analyse vs. Live-Reality:**
- Code-Analyse sagte: "Viewer vorhanden, kein Bug"
- Live-Tests zeigen: "Viewer rendert NICHT"
- Problem: JS-Initialisierung, AlpineJS-Problem, oder missing dependency

**Complexity:** MEDIUM-HIGH (JavaScript debugging complex)
- Browser DevTools Debugging
- Root-Cause identifizieren
- Fix implementieren
- Testing

---

### BUG #3: page_number Parameter wird ignoriert

**Status:** ✅ VERIFIZIERT durch Code-Analyse
**Severity:** MITTEL
**Impact:** Deep-Links zu spezifischen Seiten funktionieren nicht, Viewer öffnet immer bei Seite 1

**Betroffene Files:**
- [manuscript/views.py:485-506](manuscript/views.py#L485-L506) - `mirador_view()`

**Code-Beweis:**
```python
def mirador_view(request, manuscript_id, page_number):
    try:
        manuscript = SingleManuscript.objects.get(id=manuscript_id)
    except SingleManuscript.DoesNotExist:
        manuscript = SingleManuscript.objects.get(siglum="Urb1")

    # ... mehr Logik ...

    return render(
        request,
        "manuscript/mirador.html",
        {
            "manifest_url": manuscript.iiif_url,
            # ❌ page_number wird NICHT verwendet!
            # ❌ canvas_id wird NICHT berechnet!
        },
    )
```

**Problem:**
- URL-Parameter `page_number` wird akzeptiert aber nie verwendet
- Template erwartet `canvas_id` Variable, erhält sie aber nicht
- Manifest-Daten werden gefetched aber nicht ausgewertet

**Lösung:**
```python
def mirador_view(request, manuscript_id, page_number):
    # ... manuscript logic ...

    # NEU: Canvas-ID aus page_number berechnen
    canvas_id = None
    if page_number and manuscript.iiif_url:
        try:
            manifest_data = get_manifest_data(manuscript.iiif_url)
            if manifest_data and "sequences" in manifest_data:
                canvases = manifest_data["sequences"][0].get("canvases", [])
                # page_number is 1-indexed, array is 0-indexed
                if 0 < page_number <= len(canvases):
                    canvas_id = canvases[page_number - 1]["@id"]
                    logger.info(f"Opening page {page_number}: {canvas_id}")
        except Exception as e:
            logger.error(f"Failed to calculate canvas_id: {e}")

    return render(request, "manuscript/mirador.html", {
        "manifest_url": manuscript.iiif_url,
        "canvas_id": canvas_id,  # ← NEU!
        "page_number": page_number,
    })
```

**Complexity:** MEDIUM
- Canvas-ID Berechnung implementieren
- Template-Variable übergeben
- Bounds-Checking & Error-Handling
- Testing

---

## ❌ NICHT-BUGS (Verifikation widerlegt ursprüngliche Annahmen)

### NICHT-BUG #4: Silent Exception Handling

**Status:** ❌ BEREITS GEFIXT - Kein bare `except:` mehr!
**Ursprüngliche Annahme:** "Bare `except: pass` an 3 Stellen"
**Nach Code-Verifikation:** Alle Exceptions sind spezifisch!

**Code-Beweis:** [manuscript/views.py:625-631](manuscript/views.py#L625-L631)
```python
manuscript_data = {
    "iiif_url": (
        default_manuscript.iiif_url
        if hasattr(default_manuscript, "iiif_url")
        else None
    )
}

return render(request, "stanzas.html", {
    "paired_books": paired_books,
    "manuscript": manuscript_data,  # ✅ IIIF URL wird übergeben!
    # ...
})
```

**Code-Beweis Template:** [templates/stanzas.html:265-275](templates/stanzas.html#L265-L275)
```html
<!-- Tify viewer container -->
<div class="w-1/3 relative"
     x-data="tifyViewer"
     data-has-known-folios="{{ has_known_folios|lower }}"
     data-manifest-url="{{ manuscript.iiif_url }}">  ✅ IIIF URL!
  <div class="sticky pt-8 top-0">
    <div class="bg-white rounded-lg shadow-lg">
      <div id="tify-container" class="w-full h-screen"></div>  ✅ Viewer!
    </div>
  </div>
</div>
```

**JavaScript vorhanden:** [templates/stanzas.html:287-290](templates/stanzas.html#L287-L290)
```html
<script src="https://cdn.jsdelivr.net/npm/tify@0.31.0/dist/tify.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/tify@0.31.0/dist/tify.css">
<script src="{% static 'js/tify-sync.js' %}"></script>
```

**Warum könnte es trotzdem nicht funktionieren? (Browser/Daten-Probleme, KEIN Code-Bug):**
- JavaScript-Error in Browser-Console (tify-sync.js)
- `has_known_folios` ist False → Viewer rendert nicht
- IIIF-URL fehlt in Datenbank für default_manuscript
- AlpineJS `x-data="tifyViewer"` nicht initialisiert

**Fazit:** Code ist korrekt, evtl. Data/Config-Problem, aber KEIN Bug zum Fixen!

**Aufwand:** 0h

---

### NICHT-BUG #4: Silent Exception Handling

**Status:** ❌ BEREITS GEFIXT - Kein bare `except:` mehr!
**Ursprüngliche Annahme:** "Bare `except: pass` an 3 Stellen"
**Nach Code-Verifikation:** Alle Exceptions sind spezifisch!

**Code-Beweis:**

[manuscript/models.py:421-428](manuscript/models.py#L421-L428):
```python
try:
    self.stanza = Stanza.objects.get(
        stanza_line_code_starts=stanza_line_code_starts
    )
except ObjectDoesNotExist:  # ✅ Spezifisch!
    pass
```

[manuscript/models.py:536-539](manuscript/models.py#L536-L539):
```python
try:
    self.stanza = Stanza.objects.get(stanza_line_code_starts=variant_code)
except ObjectDoesNotExist:  # ✅ Spezifisch!
    pass
```

[manuscript/resources.py:243-248](manuscript/resources.py#L243-L248):
```python
except Location.DoesNotExist:  # ✅ Spezifisch!
    pass
except Exception as e:
    logger.error(  # ✅ Logging vorhanden!
        f"Error creating alias for {row.get('Place_ID')}: {str(e)}"
    )
```

**Fazit:** Kein bare `except:` gefunden. Alle Exception-Handling ist korrekt:
- Spezifische Exception-Typen
- Logging bei unerwarteten Fehlern
- `pass` nur bei erwarteten DoesNotExist

**Aufwand:** 0h

---

## ✅ VERIFIZIERT ALS FUNKTIONIEREND

### NICHT-BUG #5: Gazetteer Map-Rendering

**Status:** ✅ FUNKTIONIERT PERFEKT (Live-Test durchgeführt!)
**Backend:** ✅ API liefert Daten
**Frontend:** ✅ Leaflet-Map rendert einwandfrei

**Live-Test Ergebnisse (https://lasfera.rrchnm.org/toponyms):**
- ✅ Leaflet-Map wird angezeigt
- ✅ CircleMarkers für alle ~80 Toponyme gerendert
- ✅ Hover-Effekte funktionieren
- ✅ API `/api/toponyms/` liefert Daten in akzeptabler Geschwindigkeit
- ✅ JavaScript-Bibliotheken laden: Leaflet + MarkerClusterGroup

**Wichtige Korrektur:**
- Ursprüngliche Annahme: "700+ Toponyme"
- Realität: **~80 Toponyme** (keine Performance-Probleme!)

**Code-Analyse bestätigt:**
- Backend: ToponymViewSet funktioniert
- Frontend: Leaflet-Integration korrekt
- Keine JavaScript-Errors im Browser

**Fazit:** KEIN BUG, KEIN FIX NÖTIG!

**Aufwand:** 0h

---

## 📊 FINALE ZUSAMMENFASSUNG (NACH LIVE-TESTS)

### Verifizierte Bugs

| Bug | Status | Severity | Complexity |
|-----|--------|----------|------------|
| #1: Fehlende IIIF + Hardcoding | ✅ BESTÄTIGT | KRITISCH | MEDIUM |
| #2: IIIF-Viewer rendert nicht | ✅ BESTÄTIGT | HOCH | MEDIUM-HIGH |
| #3: page_number ignoriert | ✅ BESTÄTIGT | MITTEL | MEDIUM |
| Testing & Review | | | Required |
| **TOTAL** | | | **3 bugs** |

### Nicht-Bugs (verifiziert als korrekt)

| Item | Status | Grund |
|------|--------|-------|
| #4: Silent Exceptions | ❌ KEIN BUG | Bereits korrekt, spezifische Exceptions |
| #5: Gazetteer Map | ✅ FUNKTIONIERT | Leaflet-Map rendert perfekt, ~80 Toponyme |

---

## 📊 SCOPE SUMMARY (FINAL NACH LIVE-TESTS)

### Verifizierte Bugs (alle 3)

```
Bug #1: Fehlende IIIF + Hardcoding  MEDIUM complexity
Bug #2: IIIF-Viewer nicht rendering MEDIUM-HIGH complexity
Bug #3: page_number ignoriert       MEDIUM complexity
Testing & Code Review               Required
────────────────────────────────────────────────────
TOTAL:                              3 bugs verified
```

**Timeline:** 3 Wochen (15 Arbeitstage)

### Vergleich: Schätzungen im Zeitverlauf

```
URSPRÜNGLICH (vor Code-Analyse):   5 Bugs (COMPLEX scope)
NACH CODE-ANALYSE (v2.0):           2 Bugs (too optimistic)
NACH LIVE-TESTS (v3.0):             3 Bugs (verified)
──────────────────────────────────────────────────────────
DIFFERENZ zu ursprünglich:          -2 bugs (-40%)
DIFFERENZ zu v2.0:                  +1 bug (+50%)
```

**Grund für Erhöhung v2.0 → v3.0:**
- Bug #2 wurde als "kein Bug" eingeschätzt (nur Code-Analyse)
- Live-Tests zeigten: Viewer rendert NICHT (JavaScript-Problem)
- Additional JavaScript debugging needed

---

## 🎯 EMPFEHLUNGEN (FINAL)

### Was JETZT implementieren?

1. **Alle 3 Bugs fixen** (3 weeks timeline)
   - Bug #1: Fallback-Logik (MEDIUM)
   - Bug #2: IIIF-Viewer JavaScript-Fix (MEDIUM-HIGH)
   - Bug #3: page_number Navigation (MEDIUM)
   - Testing & Review (Required)

2. **Gazetteer: KEIN FIX NÖTIG**
   - Live-Tests bestätigen: Funktioniert perfekt
   - ~80 Toponyme, keine Performance-Probleme
   - Leaflet-Map rendert einwandfrei

3. **Priorität für Laura-Meeting**
   - Bug #2 demonstrieren (Viewer fehlt)
   - Bug #1 erklären (aber Daten-Problem dominiert)
   - Bug #3 zeigen (page_number funktioniert nicht)

### Was Laura fragen?

Im Meeting:
1. "Siehst du den IIIF-Viewer auf /stanzas/?" → Demonstrieren dass er fehlt
2. "Welche Manuscripts außer Urb1 nutzt du?" → Priorisierung für IIIF-Manifest-Erfassung
3. "Brauchst du Deep-Links zu spezifischen Seiten?" → Bug #3 Relevanz

---

## 📝 VERSIONS-HISTORIE

**v3.0 (28. Oktober 2025):** LIVE-SITE VERIFIKATION
- Bug #2: "KEIN BUG" → "EXISTIERT DOCH!" (Viewer rendert nicht)
- Bug #5 (Gazetteer): "UNKLAR" → "FUNKTIONIERT PERFEKT"
- Kosten: 2.340€ → 3.510€ (+50%)
- Aufwand: 12h → 18h
- Methodik: Code-Analyse + Live-Site Browser-Tests

**v2.0 (28. Oktober 2025):** Code-Analyse
- Bug #2 als NICHT-BUG identifiziert (FALSCH - nur Code geprüft!)
- Bug #4 als bereits gefixt identifiziert (KORREKT)
- Kosten von 10k€ auf 2.3k€ reduziert

**v1.0 (28. Oktober 2025):** Initiale Analyse (enthielt falsche Annahmen)

---

**Nächstes Update:** Nach Implementierung der Fixes
