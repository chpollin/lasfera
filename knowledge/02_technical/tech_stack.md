# Tech Stack - La Sfera Digital Edition

**Letzte Aktualisierung:** 28. Oktober 2025
**Quelle:** Repository-Analyse, pyproject.toml, package.json

---

## Backend

### Python & Django

**Python:** 3.11+ (pyproject.toml:10)
**Django:** 5.0.2 (pyproject.toml:11)

**Dependency Management:**
- Poetry (pyproject.toml vorhanden)
- `poetry install` für Setup
- `poetry shell` für Virtual Environment

### Django-Apps (Installed Apps)

**Core Django:**
- django.contrib.admin
- django.contrib.auth
- django.contrib.contenttypes
- django.contrib.sessions
- django.contrib.staticfiles
- django.contrib.messages

**Custom Apps:**
- `accounts` - User Management
- `manuscript` - Kernfunktionalität (Stanzas, Folios, Gazetteer, IIIF)
- `textannotation` - Text-Annotationen
- `map` - Kartenfeatures
- `pages` - Wagtail CMS Seiten
- `gallery` - Wagtail Bildgalerie
- `theme` - Tailwind CSS Theme

**Third-Party:**
- wagtail - CMS (6.2.1)
- allauth - Authentication (0.61.1)
- rest_framework - API (3.15.2)
- admin_interface - Enhanced Admin (0.28.5)
- prose - Rich Text (2.0.0)
- tailwind - CSS Framework (3.8.0)
- import_export - Data Management (4.0.3)

---

## Database

**System:** PostgreSQL
**Host:** Konfigurierbar via Environment Variables
**Default:** localhost:5432
**Database Name:** lasfera
**User:** lasfera

**ORM:** Django ORM
**Migrations:** Django Migrations (104 migrations in manuscript app)

**Schema-Dokumentation:** https://dbdocs.io/hepplerj/lasfera

---

## Frontend

### CSS Framework

**Tailwind CSS:** 3.8.0
**App:** `theme/` (Django-Tailwind Integration)
**Development:** `python manage.py tailwind start`
**Build:** Automatic via django-tailwind

### JavaScript Libraries

**Mirador:** 4.0.0-alpha.2 (package.json:31)
- ⚠️ ALPHA-Version (Production-Risiko!)
- IIIF-Viewer für Manuscripts
- Installed via npm

**Tify:** Verwendet, aber NICHT in package.json
- Vermutlich CDN-Einbindung
- Auf `/manuscripts/Urb1/stanzas/` im Einsatz
- Zu verifizieren: `grep -r "tify" templates/`

**Leaflet.js:** Für Gazetteer-Karte (anzunehmen)
- Marker Clustering
- OpenStreetMap Integration
- Zu verifizieren in Templates

### Node.js

**Version:** 20.14.0 (via Volta, package.json:5)
**npm:** 9.6.3
**Volta:** Node.js Version Manager

---

## Data Processing

**pandas:** 2.2.1 - Data manipulation
**numpy:** 1.26.4 - Numerical computing
**openpyxl:** 3.1.2 - Excel file handling
**BeautifulSoup4:** 4.12.3 - HTML parsing

---

## Geographic Features

**geopy:** 2.4.1
- Geocoding service
- Coordinate handling
- Used for Gazetteer/Toponyms

---

## Rich Text Editors

**Multiple installed (historical reasons?):**
- django-prose: 2.0.0
- django-prose-editor: 0.3.4
- django-tinymce: 4.0.0
- django-ckeditor: 6.7.1

→ Zu klären: Welcher wird aktiv genutzt?

---

## Image Processing

**Pillow:** 10.2.0
- Image uploads
- Thumbnail generation
- Gallery features

---

## API & Web

**djangorestframework:** 3.15.2
- REST API endpoints
- ToponymViewSet für Gazetteer
- Serializers für JSON responses

**requests:** Für IIIF-Manifest-Fetching
- Cache-Implementation in views.py
- 24h Cache-Timeout

---

## Development Tools

### Code Quality

**Pre-commit Hooks:** .pre-commit-config.yaml vorhanden
**Pylint-Django:** 2.5.5
**Black:** Auto-formatting (anzunehmen)
**isort:** Import sorting (anzunehmen)

### Admin Enhancement

**django-admin-interface:** 0.28.5
- Customizable Admin-UI
- Theming

**django-nested-admin:** 4.0.2
- Nested inline editing

---

## Deployment

### Docker

**Dockerfile:** Vorhanden (Python 3.11 base)
**docker-compose.yml:** Vorhanden
- Service: web (Django app)
- Service: db (PostgreSQL)

**Environment Variables:**
- django-environ: 0.11.2
- .env.example als Template

### Static Files

**STATIC_ROOT:** /staticfiles
**STATIC_URL:** /static/
**MEDIA_ROOT:** /media
**MEDIA_URL:** /media/

**Collection:** `python manage.py collectstatic`

---

## IIIF Integration

### Manifest Handling

**External Manifests:** z.B. Vatican Library
- URL: https://digi.vatlib.it/iiif/MSS_Urb.lat.752/manifest.json
- Cached in Django cache (24h)
- Function: `get_manifest_data()` in views.py

### Viewers

**Mirador 4.0.0-alpha.2:**
- Template: templates/manuscript/mirador.html
- Konfiguration: JavaScript-basiert
- Problem: Alpha-Version in Production

**Tify:**
- Einbindung unklar (CDN?)
- Funktioniert auf manuscript detail pages
- Zu verifizieren: Source

---

## Testing

**Framework:** Django TestCase (Standard)
**Status:** Minimal (nur Placeholder-Tests gefunden)
**Test Files:**
- manuscript/tests.py: 63 Bytes
- gallery/tests.py: 63 Bytes
- textannotation/tests.py: 63 Bytes

**Empfehlung:** Test-Suite aufbauen

---

## Logging

**Django Logging:** Konfiguriert in settings.py
**Level:** DEBUG (Development), INFO+ (Production anzunehmen)
**Handler:** Console

---

## Security

**Authentication:** Django Allauth
**CSRF Protection:** Enabled
**X-Frame-Options:** SAMEORIGIN
**SECRET_KEY:** Via environment variable

---

## Performance

**Database Connection Pooling:** TBD
**Caching:** Django Cache Framework
- IIIF Manifests: 24h
- To verify: Other cache usage

**Prefetch/Select Related:** Verwendet in views.py
- `prefetch_related("annotations")`
- `select_related` für Foreign Keys

---

## Versions-Management

**Git:** https://github.com/chnm/lasfera
**Branches:** main (anzunehmen)
**CI/CD:** GitHub Actions (anzunehmen, .github/ vorhanden)

---

## Known Issues

⚠️ **Mirador Alpha-Version** - Production-Risiko
⚠️ **Keine Test-Coverage** - Regression-Gefahr
⚠️ **Multiple Rich-Text-Editors** - Overhead?
❓ **Tify-Quelle unklar** - CDN-Abhängigkeit?

---

## Upgrade-Pfad (empfohlen)

1. **Mirador Alpha → Stable** (KRITISCH)
2. **Test-Suite aufbauen** (HOCH)
3. **Dependency Audit** (MITTEL)
4. **Performance Profiling** (NIEDRIG)

---

**Version:** 1.0
**Nächstes Update:** Nach Deployment-Zugang
