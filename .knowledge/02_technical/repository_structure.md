# Repository-Struktur - La Sfera

**Letzte Aktualisierung:** 28. Oktober 2025
**Quelle:** git ls-tree, find, Repository-Analyse

---

## Projekt-Root

```
lasfera/
├── .github/              GitHub Actions, CI/CD
├── accounts/             Django App: User Management
├── config/               Django Settings & URLs
├── gallery/              Django App: Wagtail Image Gallery
├── manuscript/           Django App: KERN-APP (Stanzas, IIIF, Gazetteer)
├── map/                  Django App: Map Features
├── pages/                Django App: Wagtail CMS Pages
├── static/               Static Assets (CSS, JS, Images)
├── templates/            Django Templates
├── textannotation/       Django App: Text Annotations
├── theme/                Tailwind CSS Theme App
├── docker-compose.yml    Docker Setup
├── Dockerfile           Container Definition
├── manage.py            Django Management Script
├── pyproject.toml       Poetry Dependencies
└── package.json         npm Dependencies
```

---

## Core Django Apps (Detail)

### manuscript/ (Kern-App)

```
manuscript/
├── admin.py             Admin Interface (13KB)
├── models.py            Data Models (34KB) - WICHTIG!
├── views.py             Views & API (39KB) - WICHTIG!
├── urls.py              URL Routes
├── serializers.py       REST API Serializers
├── resources.py         Import/Export (20KB)
├── utils.py             Helper Functions (IIIF)
├── management/          Management Commands
│   └── commands/
│       ├── load_aliases.py
│       ├── load_folio.py
│       ├── load_libraries.py
│       ├── load_line_codes.py
│       ├── load_manuscript.py
│       ├── load_stanzas.py
│       ├── load_stanzas_english.py
│       ├── load_toponyms.py
│       └── load_toponym_variants.py
├── migrations/          104 Migration Files
├── templatetags/        Custom Template Tags
└── fixtures/            Data Fixtures (JSON/SQL)
```

**Key Files:**
- **models.py:** LineCode, Stanza, Folio, SingleManuscript, Location, LocationAlias
- **views.py:** stanzas(), mirador_view(), ToponymViewSet, manuscript_stanzas()
- **utils.py:** get_canvas_id_for_folio(), get_manifest()

---

### templates/

```
templates/
├── base.html                      Base Template mit Navigation
├── index.html                     Homepage
├── stanzas.html                   Edition View (WICHTIG!)
├── manuscripts.html               Manuscript List
├── manuscript_single.html         Manuscript Detail
├── gazetteer/
│   ├── gazetteer_index.html      Gazetteer Main Page (Leaflet Map)
│   └── gazetteer_single.html     Toponym Detail Page
├── manuscript/
│   └── mirador.html              Mirador Viewer Template
├── pages/
│   ├── about_page.html
│   └── site_page.html
└── partials/
    └── navigation.html
```

**Templates für Bug-Fixing:**
- `stanzas.html` - Bug #2 (IIIF-Viewer fehlt)
- `manuscript/mirador.html` - Bug #3 (page_number ignoriert)
- `gazetteer/gazetteer_index.html` - Gazetteer-Status unklar

---

### static/

```
static/
├── css/
├── fonts/
├── images/
└── js/
    ├── annotations.js
    ├── main.js
    ├── manuscript.js
    ├── stanza.js
    ├── text_annotations.js
    ├── tify-sync.js           IIIF-Tify Integration
    └── variant_annotations.js
```

---

## Configuration Files

### Django

```
config/
├── __init__.py
├── settings.py         Main Settings (228 lines)
├── urls.py             Root URL Configuration
├── asgi.py             ASGI Server
└── wsgi.py             WSGI Server
```

**Key Settings:**
- INSTALLED_APPS: Line 41-80
- DATABASES: Line 125-134
- STATIC/MEDIA: Line 190-196
- WAGTAIL: Line 203-217

### Dependencies

```
pyproject.toml          Poetry Python Dependencies
package.json            npm JavaScript Dependencies
package-lock.json       npm Lock File
.env.example            Environment Variables Template
```

### Docker

```
Dockerfile              Python 3.11 + Volta setup
docker-compose.yml      Web + DB Services
docker-compose.yml.j2   Jinja2 Template for dynamic config
```

---

## Code Locations (Bug-Relevant)

### Bug #1: Urb1-Hardcoding

**File:** manuscript/views.py
**Lines:** 489, 492, 498, 537, 694
```python
manuscript = SingleManuscript.objects.get(siglum="Urb1")
```

### Bug #2: IIIF-Viewer fehlt

**File:** manuscript/views.py:523-643 (stanzas view)
**File:** templates/stanzas.html (Template zu prüfen)

### Bug #3: page_number ignoriert

**File:** manuscript/views.py:485-506 (mirador_view)
**File:** templates/manuscript/mirador.html:19

### Gazetteer

**Backend:**
- manuscript/views.py:ToponymViewSet (Line 1060)
- manuscript/serializers.py:ToponymSerializer (Line 6)
- manuscript/models.py:Location (Line 782), LocationAlias (Line 894)

**Frontend:**
- templates/gazetteer/gazetteer_index.html (Leaflet Map)
- templates/gazetteer/gazetteer_single.html (Detail Page)

---

## Data Files

### Fixtures

```
manuscript/fixtures/
├── *.json              Data Seeds
└── *.sql               Database Dumps (?)
```

### Migrations

```
manuscript/migrations/
├── 0001_initial.py
├── 0002_location_singlemanuscript_authority_file_and_more.py
├── ...
└── 0104_remove_stanza_related_folio_stanza_folios.py
```

**104 Migrations!** → Lange Entwicklungsgeschichte

---

## Git Structure

```
.git/
├── hooks/              Pre-commit Hooks
├── ...
```

**.gitignore:** Vorhanden, ignoriert:
- __pycache__/
- *.pyc
- .env
- /staticfiles/
- /media/

---

## Documentation

```
README.md               Quick Start Guide
DEVNOTES.rst           Development Documentation
CHANGELOG.rst          Version History (kurz)
CITATION.cff           Academic Citation Format
```

---

## Development Tools

```
.pre-commit-config.yaml    Code Quality Hooks
.pylintrc                  Pylint Configuration
Makefile                   Quality-of-life Commands
make_library_fixture.py    Data Fixture Generator
```

---

## Important Constants

**Line Code Format:** `BB.SS.LL` (Book.Stanza.Line)
- Example: `01.01.04` = Book 1, Stanza 1, Line 4
- Validation: models.py:19-31

**IIIF Manifest URLs:** External (Vatican, etc.)
- Cached 24h in Django cache
- Function: get_manifest_data() in views.py:40

**Gazetteer API:** `/api/toponyms/`
- Returns JSON with coordinates
- ~80+ locations

---

## File Sizes (Notable)

```
manuscript/views.py      39KB    Largest view file
manuscript/models.py     34KB    Complex data models
manuscript/resources.py  20KB    Import/Export logic
manuscript/admin.py      13KB    Admin customizations
```

---

## Next Steps für Code-Navigation

1. **Für Bug #1:** `grep -n "Urb1" manuscript/views.py`
2. **Für Bug #2:** `cat templates/stanzas.html | grep -i "tify\|mirador"`
3. **Für Bug #3:** `cat templates/manuscript/mirador.html`
4. **Für Gazetteer:** `cat templates/gazetteer/gazetteer_index.html | grep -i "leaflet"`

---

**Version:** 1.0
**Nächstes Update:** Nach Template-Analyse
