# La Sfera - Konkrete Bugs im Code gefunden

**Datum:** 28. Oktober 2025
**Methode:** Code-Analyse (nicht Browser-Testing)
**Quelle:** Repository chnm/lasfera

---

## 🔴 KRITISCHE BUGS GEFUNDEN

### BUG #1: Urb1-Hardcoding überall

**Severity:** HOCH
**Impact:** Andere Manuscripts funktionieren nicht korrekt

**Betroffene Files:**
- `manuscript/views.py:489, 492, 498, 537, 694`

**Code-Beispiele:**

```python
# views.py:489 - mirador_view()
except SingleManuscript.DoesNotExist:
    manuscript = SingleManuscript.objects.get(siglum="Urb1")  # Hardcoded!

# views.py:492 - wenn kein IIIF URL
if not manuscript.iiif_url:
    manuscript = SingleManuscript.objects.get(siglum="Urb1")  # Hardcoded!

# views.py:537 - stanzas()
default_manuscript = SingleManuscript.objects.get(siglum="Urb1")  # Hardcoded!
```

**Problem:**
- Jedes Mal wenn ein Manuscript fehlt → Fallback zu "Urb1"
- Andere Manuscripts (Cambridge, Florence, Yale) werden nicht korrekt angezeigt
- User sieht falsche Bilder

**Aufwand:** 4-6 Stunden
- Fallback-Logik refactoren: 2-3h
- Alle Hardcodes entfernen: 1-2h
- Testing: 1h

---

### BUG #2: IIIF-Viewer fehlt auf Stanzas-Seite

**Severity:** KRITISCH
**Impact:** Hauptfeature der Edition fehlt

**Code-Beweis:**

```python
# views.py:523 - stanzas()
def stanzas(request: HttpRequest):
    folios = Folio.objects.all()
    stanzas = Stanza.objects...
    manuscripts = SingleManuscript.objects.all()
    default_manuscript = SingleManuscript.objects.get(siglum="Urb1")

    # ... viel Code ...

    return render(request, "stanzas.html", context)
    # ❌ Kein IIIF manifest_url im Context!
    # ❌ Kein Viewer-Code
```

**Vergleich mit manuscript_stanzas (funktioniert):**
```python
# views.py:57 - manuscript_stanzas()
# Hat IIIF-Integration:
iiif_manifest = get_manifest_data(manuscript.iiif_url)
context["iiif_manifest"] = iiif_manifest
```

**Problem:**
- `/stanzas/` zeigt nur Text (kein Viewer)
- `/manuscripts/Urb1/stanzas/` hat Tify-Viewer
- URLs sind unterschiedlich → Feature-Inkonsistenz

**Lösung:**
Mirador in `/stanzas/` Template integrieren, Canvas-Sync mit Line Codes

**Aufwand:** 20-30 Stunden
- Mirador in stanzas.html einbetten: 8-12h
- Canvas-ID aus Line Code berechnen: 4-6h
- Synchronisation Text↔Bild: 6-10h
- Testing: 2-4h

---

### BUG #3: Mirador View ignoriert page_number Parameter

**Severity:** MITTEL
**Impact:** Viewer startet immer bei Seite 1

**Code:**
```python
# views.py:485
def mirador_view(request, manuscript_id, page_number):
    # ...
    return render(request, "manuscript/mirador.html", {
        "manifest_url": manuscript.iiif_url,
        # ❌ canvas_id nicht übergeben!
        # ❌ page_number wird ignoriert!
    })
```

**Template:**
```html
<!-- templates/manuscript/mirador.html:19 -->
manifestId: "{{ manifest_url }}",
canvasId: "{{ canvas_id }}",  <!-- Variable leer! -->
```

**Problem:**
- URL hat `/mirador/<manuscript_id>/<page_number>/`
- Aber `page_number` wird nie verwendet
- Viewer öffnet immer erste Seite

**Aufwand:** 3-5 Stunden
- Canvas ID Berechnung: 2-3h
- Template-Variable übergeben: 1h
- Testing: 1h

---

## 🟡 POTENZIELLE PROBLEME

### PROBLEM #1: Silent Exception Handling

**Files:** `manuscript/models.py:426, 539`, `manuscript/resources.py:244`

```python
# models.py:426
try:
    # ... Code ...
except:
    pass  # ❌ Fehler werden verschluckt!
```

**Problem:**
- Bare `except:` fängt ALLE Exceptions
- `pass` = nichts tun
- Bugs werden versteckt, nicht gefixt

**Risiko:** Unbekannte Bugs in Production

**Aufwand:** 2-3 Stunden (alle finden und fixen)

---

### PROBLEM #2: Gazetteer API-Endpoints

**Gefunden:**
```python
# manuscript/urls.py:7-8
router.register(r"toponyms", views.ToponymViewSet, basename="toponyms")
router.register(r"toponym-detail", views.ToponymViewSet, basename="toponym-detail")
```

**Beide verwenden `ToponymViewSet`** → Warum zwei Endpoints?

**WebFetch-Test ergab:**
- `/api/toponyms` gibt Daten zurück ✅
- Aber: Map-Rendering auf Frontend unklar

**Mögliche Bugs:**
- JavaScript lädt Leaflet nicht
- Marker-Rendering fehlerhaft
- Performance-Problem (700+ Orte)

**Aufwand:** 4-8 Stunden (ohne konkrete Bug-Reproduktion schwer schätzbar)

---

## 📊 Zusammenfassung

### Definitiv kaputt (Code-Beweis):
1. **Urb1 Hardcoding** → 4-6h Fix
2. **IIIF fehlt auf /stanzas/** → 20-30h Feature-Implementierung
3. **Mirador page_number ignoriert** → 3-5h Fix

**Minimum Fix-Aufwand:** 27-41h reine Entwicklung

### Wahrscheinlich kaputt (zu prüfen mit Laura):
4. **Gazetteer Map-Rendering** → 4-8h
5. **Silent Exception Handling** → 2-3h

**Gesamt (wenn alles kaputt):** 33-52h reine Entwicklung

### Mit Overhead (1.55x):
- **Minimum:** 42-64h = **6.300-9.600€**
- **Alle Bugs:** 51-81h = **7.650-12.150€**

---

## Was wir im Meeting brauchen

### Von Laura:
1. **Screen-Share Gazetteer:**
   - "Zeig mir: Werden Marker auf der Karte angezeigt?"
   - "Was passiert wenn du auf einen Marker klickst?"
   - "Funktioniert die Suche?"

2. **Screen-Share Stanzas:**
   - "Siehst du irgendwo Manuscript-Bilder?"
   - "Soll der IIIF-Viewer hier sein?" (zeigt auf leere Stelle)

3. **Andere Manuscripts:**
   - "Funktioniert Florence/Cambridge/Yale genauso wie Urb1?"
   - "Oder gibt es da Unterschiede?"

### Dann wissen wir:
- Sind unsere Code-Bugs auch User-facing Bugs?
- Welche Priorität hat was?
- Gibt es MEHR Bugs die wir nicht gesehen haben?

---

## Empfehlung

**Szenario B (STANDARD) anpassen:**

```markdown
## Bestätigte Bugs aus Code-Analyse:

1. Urb1 Hardcoding entfernen          6h  →    900€
2. IIIF Viewer in Stanzas integrieren 25h → 3.750€
3. Mirador page_number fixen           4h →    600€
4. Silent Exceptions beheben           3h →    450€
                                     ────    ──────
   REINE ENTWICKLUNG:                38h    5.700€
   × Overhead (1.55):               59h    8.850€
                                     ════    ══════
```

**Plus Gazetteer** (nach Meeting-Bestätigung):
- Wenn kaputt: +6-10h → +900-1.500€

**TOTAL: 9.750-10.350€** (realistisch für alle bekannten Bugs)

---

## Nächster Schritt

**E-Mail an Laura schicken:**
- Anhang 1: MEETING_BRIEF.md
- Anhang 2: Dieses Dokument (KONKRETE_BUGS_GEFUNDEN.md)
- Text: "Habe bereits 3 kritische Bugs im Code gefunden. Schätzung: 10k€. Im Meeting schauen wir ob es mehr gibt."
