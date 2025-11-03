# La Sfera Digital Edition - Knowledge Vault v2

**Erstellt:** 28. Oktober 2025
**Aktualisiert:** 28. Oktober 2025
**Version:** 2.0
**Status:** Verifiziert gegen Repository

---

## Projektübersicht

Die La Sfera Digital Edition ist eine wissenschaftliche Online-Edition eines florentinischen Lehrgedichts (ca. 1430) über Geografie und Kosmologie. Das Projekt wurde vom Roy Rosenzweig Center for History and New Media (RRCHNM) der George Mason University zu 90% fertiggestellt, bevor die NEH-Förderung endete. Laura Morreale (Harvard/Princeton) hat neue Finanzierung für die Fertigstellung bis Juni 2026 gesichert.

**Technische Basis:** Django 5.0.2, Wagtail CMS 6.2.1, Poetry für Dependency Management, Docker für Deployment. Mirador 4.0.0-alpha.2 als npm-Dependency installiert. Tify-Viewer funktioniert auf Production, Einbindungsart noch zu verifizieren (vermutlich CDN oder Bundle).

**URLs:**
- Produktion: https://lasfera.rrchnm.org/
- Development: https://dev.lasfera.rrchnm.org/
- Repository: https://github.com/chnm/lasfera

---

## Verifizierte Projektstruktur

### Django-Apps (tatsächlich vorhanden)

**Kern-Apps:**
- `manuscript/` - HAUPT-APP: Enthält Manuskripte, Stanzas, Folios, Toponymen-API (Gazetteer-Funktionalität), IIIF-Integration, REST API ViewSets
- `textannotation/` - Annotationssystem für Textkommentare mit ProseMirror
- `gallery/` - Wagtail-basierte Bildgalerie mit Theme-Filtering
- `pages/` - Wagtail CMS-Seiten für statischen Content
- `map/` - Kartenfunktionalität (möglicherweise Gazetteer-Frontend, zu verifizieren)
- `accounts/` - User-Management und Authentication (Django Allauth)
- `theme/` - Tailwind CSS Konfiguration und Templates

**Wichtig:** Es gibt KEINE separaten Apps für `gazetteer`, `iiif` oder `wagtail_hooks`. Diese Funktionalität ist in `manuscript/` integriert.

### API-Endpoints [VERIFIZIERT]

**Gazetteer/Toponyms:**
- `/api/toponyms/` - ToponymViewSet in manuscript/urls.py:7
- `/api/toponym-detail/` - Gleicher ViewSet, manuscript/urls.py:8
- Beide Endpoints verwenden `manuscript.views.ToponymViewSet`
- Response: JSON mit ~80 Toponymen, Koordinaten, Aliases

**Edition:**
- `/manuscripts/<siglum>/` - Manuscript Detail View
- `/manuscripts/<siglum>/stanzas/` - Manuscript Stanzas with Tify Viewer
- `/stanzas/` - Main Edition View (BUG: kein Viewer)
- `/mirador/<manuscript_id>/<page_number>/` - Mirador Viewer (BUG: page_number ignoriert)

---

## Identifizierte Probleme

### Bug #1: Urb1-Hardcoding [VERIFIZIERT]

**Datei:** `manuscript/views.py`
**Zeilen:** 489, 492, 498, 537, 694
**Code-Snippet:**
```python
except SingleManuscript.DoesNotExist:
    manuscript = SingleManuscript.objects.get(siglum="Urb1")

if not manuscript.iiif_url:
    manuscript = SingleManuscript.objects.get(siglum="Urb1")
```

**Problem:** Bei fehlenden Manuskripten oder fehlender IIIF-URL wird hardcoded "Urb1" (Vatican Manuscript) als Fallback verwendet. Dies verhindert korrekte Darstellung der anderen Manuskripte (Cambridge, Florence, Yale).

**Impact:** User wählt "Florence" → sieht aber Urb1-Bilder

**Lösung:** Dynamische Fallback-Logik basierend auf verfügbaren IIIF-URLs implementieren. Wenn kein IIIF vorhanden: Fehlermeldung statt falsches Manuscript.

**Aufwand:** 4-6 Stunden
- Fallback-Logik refactoren: 2-3h
- Alle 5 Stellen ändern: 1-2h
- Testing mit allen Manuscripts: 1h

---

### Bug #2: IIIF-Viewer auf /stanzas/ [TEILWEISE VERIFIZIERT]

**Datei:** `manuscript/views.py:523-643` (stanzas view)
**Datei:** `templates/stanzas.html` (zu analysieren)

**Beobachtung:** Der stanzas-View übergibt `iiif_url` im manuscript_data Dictionary (Zeile 625-643):
```python
manuscript_data = {
    "iiif_url": (
        default_manuscript.iiif_url
        if hasattr(default_manuscript, "iiif_url")
        else None
    )
}
```

**Hypothese:** Template `stanzas.html` hat keine Viewer-Integration trotz vorhandener IIIF-URL im Context. Der View ist korrekt, das Problem liegt im Template.

**Vergleich:**
- `/stanzas/` - Nur Text (KEIN Viewer)
- `/manuscripts/Urb1/stanzas/` - Text + Tify Viewer (FUNKTIONIERT)

**Verifikation nötig:** `grep -i "tify\|mirador" templates/stanzas.html`

**Aufwand:**
- **Best Case:** 5-10h wenn nur Template-Fix (Viewer-Code aus manuscript_stanzas.html kopieren)
- **Worst Case:** 20-30h wenn komplette Integration nötig (Canvas-Sync, Line-Code-Linking)

---

### Bug #3: Mirador page_number ignoriert [VERIFIZIERT]

**Datei:** `manuscript/views.py:485-506` (mirador_view)
**Datei:** `templates/manuscript/mirador.html:19`

**Code:**
```python
def mirador_view(request, manuscript_id, page_number):
    # ... manuscript lookup ...
    return render(request, "manuscript/mirador.html", {
        "manifest_url": manuscript.iiif_url,
        # ❌ canvas_id wird nicht übergeben!
        # ❌ page_number wird nie verwendet!
    })
```

**Template:**
```html
manifestId: "{{ manifest_url }}",
canvasId: "{{ canvas_id }}",  <!-- Variable ist leer! -->
```

**Problem:** Die mirador_view akzeptiert einen page_number Parameter in der URL-Route, verwendet diesen aber nicht. Die canvas_id wird weder berechnet noch an das Template übergeben, wodurch der Viewer immer bei Seite 1 startet.

**Lösung:**
1. Canvas-ID aus page_number und Manifest-Struktur berechnen
2. Template-Variable `canvas_id` übergeben
3. Mirador mit canvas_id initialisieren

**Aufwand:** 3-5 Stunden
- Canvas-ID Berechnung: 2-3h (get_canvas_url_for_folio bereits vorhanden!)
- Template-Variable übergeben: 30min
- Testing: 1h

---

### Weitere Issues [VERIFIZIERT]

**Silent Exception Handling:**
- `manuscript/models.py:426, 539`
- `manuscript/resources.py:244`

**Code:**
```python
try:
    # ... Code ...
except:
    pass  # ❌ Fehler werden verschluckt!
```

**Problem:** Bare `except:` fängt ALLE Exceptions, `pass` bedeutet "nichts tun". Potenzielle Fehler werden verschluckt statt geloggt.

**Lösung:** Specific exceptions fangen, logging implementieren
```python
except SpecificError as e:
    logger.error(f"Error in X: {e}")
    # Handle or re-raise
```

**Aufwand:** 2-3 Stunden (alle 3 Stellen finden und fixen)

---

### Gazetteer-Status [UNBEKANNT - BROWSER-TEST NÖTIG]

**Backend:** ✅ ToponymViewSet liefert Daten über `/api/toponyms/`
- Response: JSON mit ~80 Locations
- Koordinaten vorhanden
- API funktioniert

**Frontend:** ❓ Unklar ob Leaflet/Mapbox korrekt rendert
- Template: `templates/gazetteer/gazetteer_index.html` hat Leaflet-Code
- JavaScript fetcht `/api/toponyms`
- Marker-Rendering: Zu verifizieren

**Mögliche Probleme:**
- Leaflet lädt nicht (CDN-Fehler?)
- Marker werden nicht gerendert (JavaScript-Error?)
- Performance-Problem bei 80+ Markern
- Hover-Effects kaputt

**Verifikation nötig:** Browser-Testing auf `https://lasfera.rrchnm.org/toponyms/`

**Aufwand:** 4-8 Stunden (abhängig von gefundenen Problemen)
- Wenn nur CSS/Minor: 4h
- Wenn JavaScript-Refactoring: 8h

---

## Technische Details

### Datenmodell (Kern-Konzepte)

**Hierarchisches Line-Code-System:**
- Format: `BB.SS.LL` (Book.Stanza.Line)
- Beispiel: `01.02.15` = Book 1, Stanza 2, Line 15
- Validation: `validate_line_number_code()` in models.py:19
- Parsing: `parse_line_code()` in models.py:34
- Numerische Konversion: `line_code_to_numeric()` in models.py:53

**SingleManuscript:**
- Felder: siglum, iiif_url, purl_url
- Beispiel: siglum="Urb1", iiif_url="https://digi.vatlib.it/iiif/..."

**Stanza:**
- Felder: stanza_line_code_starts, stanza_line_code_ends, related_folio
- Verknüpfung: ManyToMany zu Folios
- Annotations: Generic Relation

**Folio:**
- Felder: folio_number, manuscript, line_code_range_start/end
- Methode: `get_canvas_id()` für IIIF-Canvas-URL

**Location (Gazetteer):**
- Felder: placename_id, name, latitude, longitude
- Verknüpfung: LocationAlias für Namens-Varianten

**LocationAlias:**
- Felder: placename_alias, placename_modern, placename_standardized
- ManyToMany: manuscripts (welche MSS verwenden welchen Alias)

### IIIF-Implementation

**Installiert:** Mirador 4.0.0-alpha.2 über npm (package.json:31)
⚠️ **PROBLEM:** Alpha-Version in Production ist Risiko!

**In Verwendung:** Tify auf `/manuscripts/Urb1/stanzas/`
❓ **Integration unklar:** Nicht in package.json → vermutlich CDN
📝 **Verifikation nötig:** `grep -r "tify" --include="*.html" templates/`

**Manifeste:** Externe URLs, Beispiel:
```
https://digi.vatlib.it/iiif/MSS_Urb.lat.752/manifest.json
```

**Caching:** 24h in Django Cache via `get_manifest_data()` in views.py:40

**Canvas-ID-Generation:** `get_canvas_id_for_folio()` in utils.py:20

### Dependencies [VERIFIZIERT]

**Python (pyproject.toml):**
- Django 5.0.2
- Wagtail 6.2.1
- djangorestframework 3.15.2
- requests (für IIIF-Manifest-Fetching)
- Pillow 10.2.0
- psycopg2 2.9.9
- pandas 2.2.1, numpy 1.26.4 (Data Processing)
- geopy 2.4.1 (Geocoding)

**JavaScript (package.json):**
- Mirador 4.0.0-alpha.2
- Node.js 20.14.0 (via Volta)
- npm 9.6.3

**Deployment:**
- Docker (docker-compose.yml vorhanden)
- PostgreSQL (docker-compose service "db")

---

## Kalkulation

### Aufwandsschätzung (reine Entwicklung)

**Bestätigte Bugs:**
```
Bug #1 (Urb1-Hardcoding):       5h
Bug #2 (IIIF in stanzas):      8-25h   (Template-Fix bis volle Integration)
Bug #3 (page_number):           4h
Silent Exceptions:              3h
```

**Optionale Bugs:**
```
Gazetteer (falls kaputt):      6h
```

**Summen:**
- **Best Case:** 20h (alle Bugs minimal)
- **Realistic:** 27h (Bug #2 ist komplex)
- **Worst Case:** 43h (alles + Gazetteer)

### Overhead-Faktoren

**Breakdown:**
- Einarbeitung: +10% (lokale Setup, Code verstehen)
- Kommunikation/Meetings: +10% (wöchentliche Updates, Reviews)
- Testing/QA: +15% (manuell, keine Test-Suite)
- Unvorhergesehenes: +20% (unbekannte Bugs, IIIF-Komplexität)

**Gesamt-Faktor:** 1.55x (55% Overhead)

### Kostenberechnung (150€/h)

**Best Case:** 20h × 1.55 = 31h × 150€ = **4.650€**
- Nur kritische Bugs
- Template-Fixes ausreichend
- Gazetteer funktioniert

**Realistic Case:** 27h × 1.55 = 42h × 150€ = **6.300€**
- Bug #2 braucht mehr Arbeit
- Gazetteer hat kleinere Probleme
- Standard-Szenario

**Worst Case:** 43h × 1.55 = 67h × 150€ = **10.050€**
- Bug #2 volle Integration nötig
- Gazetteer-Refactoring
- Zusätzliche unbekannte Bugs

**Empfehlung:** Realistic Case (~6.000-8.000€) für Angebot

---

## Deployment und Testing

### Entwicklungsumgebung

**Docker-Setup:**
```bash
docker-compose up --build
```

**Services:**
- web: Django App (Port 8000)
- db: PostgreSQL (Port 5432)

**Poetry:**
```bash
poetry install
poetry shell
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Tailwind CSS:**
```bash
python manage.py tailwind start  # Development
python manage.py tailwind build  # Production
```

### Testing-Strategie

**Unit-Tests:** Django TestCase für Backend-Logik
⚠️ **Status:** Aktuell nur Placeholder-Tests (63 Bytes)
📝 **TODO:** Test-Suite aufbauen (nicht im Scope)

**Browser-Tests:** Manuelle Tests für IIIF-Viewer
- Chrome DevTools Console für JavaScript-Errors
- Network Tab für API-Calls
- Verschiedene Manuscripts testen

**API-Tests:** curl/Postman für `/api/toponyms/`
```bash
curl https://lasfera.rrchnm.org/api/toponyms/ | jq
```

**Performance:** Django Debug Toolbar für Query-Optimierung
- prefetch_related() für Annotations
- select_related() für Foreign Keys

### Deployment [ZU VERIFIZIEREN]

**Angenommen (Django-Standard):**
- Git-basiertes Deployment
- Gunicorn als WSGI-Server
- Nginx als Reverse Proxy
- Static Files via collectstatic

**Staging:** dev.lasfera.rrchnm.org
**Production:** lasfera.rrchnm.org

**Details zu klären:**
- SSH-Zugang zu Servern
- Deployment-Pipeline (manual/automatic)
- Rollback-Prozess
- Backup-Strategie

---

## Risiken und Abhängigkeiten

### Technische Risiken

**Risiko:** IIIF-Manifeste externer Institutionen könnten sich ändern
**Impact:** Viewer bricht
**Wahrscheinlichkeit:** Niedrig (stabile APIs)
**Mitigation:** Lokale Manifest-Kopien als Fallback, Error-Handling

**Risiko:** CORS-Policies könnten Manifest-Zugriff blockieren
**Impact:** Bilder laden nicht
**Wahrscheinlichkeit:** Niedrig (aktuell funktioniert es)
**Mitigation:** Proxy-Lösung via Django

**Risiko:** Gazetteer-Performance bei 700+ Toponymen
**Impact:** Langsame Karte, Browser friert ein
**Wahrscheinlichkeit:** Mittel
**Mitigation:** Pagination oder Marker Clustering

**Risiko:** Tify-Integration unklar (CDN-Abhängigkeit?)
**Impact:** Viewer bricht wenn CDN down
**Wahrscheinlichkeit:** Niedrig
**Mitigation:** Tify lokal hosten

**Risiko:** Mirador Alpha-Version instabil
**Impact:** Bugs, Breaking Changes
**Wahrscheinlichkeit:** Mittel
**Mitigation:** Upgrade zu Stable (außerhalb Scope)

### Organisatorische Abhängigkeiten

**Erforderlich vom Client:**
- SSH-Zugang zu Staging/Production-Servern
- Database-Dump für lokale Entwicklung
- Admin-Account für Content-Tests
- Technischer Ansprechpartner bei RRCHNM
- Laura's Team für Content-Verifikation
- Zeitnahe Reviews (48h SLA)

**Deployment-Pipeline:**
- Dokumentation fehlt im Repo
- Prozess zu klären im Kick-off
- Wer deployed? Automatisch oder manuell?

### Mitigation-Strategien

**Milestone-basierte Abrechnung:**
- 50% bei Start
- 50% bei Abnahme
- Ermöglicht Projektabbruch bei Blockern

**Lokale Entwicklung:**
- Vollständig möglich mit Docker
- Unabhängig von Server-Zugang
- Database-Dump reicht

**Kritische Bugs priorisiert:**
- Bug #1 (Urb1) zuerst
- Bug #3 (page_number) parallel
- Bug #2 (IIIF) zum Schluss (größter Scope)

**Klare Kommunikation:**
- Blocker sofort melden
- Wöchentliche Updates
- Change Requests schriftlich

---

## Projektorganisation

### Team

**Projektleitung:** Laura K. Morreale (lmorreale3@gmail.com)
- Harvard/Princeton
- Principal Investigator
- Budget-Verantwortung

**Wissenschaftliches Team:**
- Carrie Beneš
- Laura Ingallinella

**Entwicklung:** Christopher Pollin (christopher.pollin@dhcraft.org)
- Digital Humanities Craft OG
- Technische Umsetzung
- 150€/h

**Institution:** RRCHNM, George Mason University

### Timeline

**Projektstart:** Mitte November 2025 (nach Vertrag)
**Deadline:** Ende akademisches Jahr 2025/26 (Juni 2026)
**Puffer:** 4-5 Monate bis Deadline

**Phasen:**
1. **Kritische Bugs** (1-2 Wochen): Bug #1, #3, Silent Exceptions
2. **IIIF-Integration** (2-3 Wochen): Bug #2, Testing
3. **Gazetteer & Polish** (1 Woche): Falls nötig, QA
4. **Launch** (1 Woche): User Acceptance Testing, Deployment

### Budget

**Genehmigt (anzunehmen):** 8.000-10.000€
**Stundensatz:** 150€
**Zahlungsmodalität:** 50/50 (Start/Abnahme)

### Kommunikation

**Primär:** E-Mail
**Meetings:** Zoom, wöchentlich oder bei Bedarf (17:00 CET = 11:00 EST)
**Bug-Tracking:** GitHub Issues (nach Setup)
**Code-Review:** Pull Requests

**Response-Zeit:**
- Kunde → Entwickler: 24-48h
- Entwickler → Kunde: 24h (Blocker sofort)

---

## Offene Aktionen

**Vor Meeting (3./11. Nov):**
- [ ] Meeting-Termin bestätigen
- [ ] Laura bereitet Screen-Share vor
- [ ] Christopher: Demo-Fragen vorbereitet ✅

**Im Meeting:**
- [ ] Gazetteer live testen
- [ ] IIIF-Problem demonstrieren
- [ ] Andere Manuscripts testen
- [ ] Budget final bestätigen
- [ ] Timeline besprechen

**Nach Meeting:**
- [ ] `grep -r "tify\|mirador" templates/stanzas.html`
- [ ] Finales Angebot schreiben
- [ ] Vertrag ausarbeiten
- [ ] SSH-Zugang anfordern

**Nach Vertragsunterzeichnung:**
- [ ] Lokale Entwicklungsumgebung aufsetzen
- [ ] Database-Dump importieren
- [ ] Bug #1 fixen (Quick Win)
- [ ] First Review mit Laura

---

## Versions-Historie

**v2.0 (2025-10-28):**
- Projektstruktur gegen Repository verifiziert
- Bug #2 präzisiert (View übergibt Daten, Template nutzt sie nicht)
- Architektur korrigiert (keine separaten gazetteer/iiif Apps)
- Verifikations-Status eingeführt [VERIFIZIERT/ZU VERIFIZIEREN/UNBEKANNT]
- Deployment-Details als "anzunehmen" markiert
- Kalkulation an reale Bug-Komplexität angepasst

**v1.0 (2025-10-28):**
- Initiale Analyse basierend auf Repository-Review
- 3 Haupt-Bugs identifiziert
- Erste Aufwandsschätzung

---

**Nächstes Update:** Nach Meeting mit Laura (3. oder 11. Nov 2025)
**Maintainer:** Christopher Pollin, DH Craft
