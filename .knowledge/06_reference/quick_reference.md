# Quick Reference - La Sfera

**Schnellzugriff auf wichtigste Informationen**

---

## URLs

```
Production:   https://lasfera.rrchnm.org/
Development:  https://dev.lasfera.rrchnm.org/
Repository:   https://github.com/chnm/lasfera
DB Schema:    https://dbdocs.io/hepplerj/lasfera
Project Site: https://sites.google.com/ncf.edu/sfera-project/home
```

---

## Kontakte

```
Laura Morreale:    lmorreale3@gmail.com (Project Lead)
Christopher:       christopher.pollin@dhcraft.org (Developer)
RRCHNM:           rrchnm@gmu.edu (Institution)
```

**Zeitzone:** EST (UTC-5) = 6h hinter CET
**Meeting-Zeit:** 17:00 CET = 11:00 EST

---

## Die 3 Haupt-Bugs

```
#1  Urb1-Hardcoding         manuscript/views.py:489,492,498,537,694    4-6h
#2  IIIF-Viewer fehlt       templates/stanzas.html                      20-30h
#3  page_number ignoriert   manuscript/views.py:485, mirador.html:19    3-5h
```

**Total:** 27-41h rein × 1.55 Overhead = 42-64h = **6.300-9.600€**

---

## Tech Stack (Essentials)

```
Backend:   Django 5.0.2, Wagtail 6.2.1, Python 3.11
Database:  PostgreSQL
Frontend:  Tailwind CSS, Mirador 4.0.0-alpha.2
Tools:     Poetry, Docker, npm
```

---

## Django Apps

```
manuscript/        Kern (Stanzas, Folios, Gazetteer, IIIF)
gallery/           Wagtail Bildgalerie
pages/             Wagtail CMS
textannotation/    Text-Annotationen
accounts/          Users
map/               Karten
theme/             Tailwind CSS
```

---

## Wichtige Commands

```bash
# Setup
poetry install
poetry shell
python manage.py migrate

# Development
python manage.py runserver
python manage.py tailwind start

# Testing
python manage.py test

# Data
python manage.py loaddata fixture_name
```

---

## Code Locations

```
Urb1 Hardcodes:     grep -n "Urb1" manuscript/views.py
IIIF Views:         manuscript/views.py:40,485,523
Gazetteer API:      manuscript/views.py:1060 (ToponymViewSet)
Templates:          templates/stanzas.html
                    templates/manuscript/mirador.html
                    templates/gazetteer/*.html
```

---

## API Endpoints

```
/api/toponyms/              List all places with coordinates
/api/toponym-detail/        Same ViewSet
/manuscripts/<siglum>/      Manuscript detail
/stanzas/                   Main edition view
/mirador/<id>/<page>/       IIIF Viewer (broken)
```

---

## Environment Variables

```
DJANGO_SECRET_KEY
DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS
DEBUG (default: False)
DJANGO_ALLOWED_HOSTS
DJANGO_CSRF_TRUSTED_ORIGINS
```

See: `.env.example`

---

## Git Workflow

```bash
# Branches
git checkout -b feature/fix-urb1-hardcoding
git add .
git commit -m "fix: Remove Urb1 hardcoding in views"
git push origin feature/fix-urb1-hardcoding

# PR
gh pr create --title "Fix Urb1 hardcoding" --body "..."
```

---

## Testing Checklist

```
□ Gazetteer map renders
□ Markers appear (~80 items)
□ Click on marker works
□ Search toponyms works
□ IIIF viewer on /stanzas/
□ Mirador page navigation
□ Florence/Cambridge/Yale manuscripts work
□ No JavaScript errors in console
□ No 404s in Network tab
```

---

## Deployment

```bash
# Docker
docker-compose up --build

# Collect static
python manage.py collectstatic --noinput

# Migrate
python manage.py migrate
```

---

## Troubleshooting

```
Problem: Mirador doesn't load
Check:   Browser console for errors
         IIIF manifest URL accessible?
         CORS headers correct?

Problem: Gazetteer empty
Check:   /api/toponyms/ returns data?
         Leaflet.js loaded?
         JavaScript errors?

Problem: Wrong manuscript shown
Likely:  Urb1 hardcoding fallback
Fix:     Bug #1
```

---

## File Sizes

```
manuscript/views.py     39KB   (largest, most complex)
manuscript/models.py    34KB   (data models)
manuscript/resources.py 20KB   (import/export)
```

---

## Data Models (Key)

```python
SingleManuscript   siglum, iiif_url
Stanza             stanza_line_code_starts/ends, related_folio
Folio              folio_number, manuscript, get_canvas_id()
Location           placename_id, latitude, longitude
LocationAlias      placename_alias, manuscripts
```

---

## IIIF Manifest Example

```
Vatican Urb.lat.752:
https://digi.vatlib.it/iiif/MSS_Urb.lat.752/manifest.json

Cached: 24h in Django cache
Function: get_manifest_data() in views.py:40
```

---

## Line Code Format

```
Format:  BB.SS.LL
Example: 01.02.15
Meaning: Book 1, Stanza 2, Line 15

Validation: validate_line_number_code() in models.py:19
Parsing:    parse_line_code() in models.py:34
Numeric:    line_code_to_numeric() in models.py:53
```

---

## Meeting Prep

```
1. Laura shares screen
2. Demo Gazetteer bugs
3. Demo IIIF missing
4. Demo other manuscripts
5. Discuss budget (~10k€)
6. Agree on timeline
7. Next: Write proposal
```

---

## Next Steps

```
□ Meeting 3. or 11. Nov, 17:00 CET
□ Laura shows bugs
□ Finalize cost estimate
□ Write proposal
□ Get approval
□ Start development mid-Nov
```

---

## Budget Scenarios

```
Best Case:    40h × 150€ =  6.000€   (only critical)
Realistic:    54h × 150€ =  8.100€   (all bugs)
Worst Case:   67h × 150€ = 10.050€   (+ extras)
```

Overhead: 1.55x (includes testing, communication, buffer)

---

## Important Dates

```
Oct 28, 2025:  Initial contact
Nov 3/11:      Meeting with Laura
Nov ~15:       Development start (estimated)
Jun 2026:      Deadline (comfortable!)
```

---

## Knowledge Vault Structure

```
.knowledge/
├── 01_project/       overview.md, contacts.md
├── 02_technical/     tech_stack.md, repository_structure.md
├── 03_bugs/          bug_inventory.md
├── 04_meetings/      2025-11-03_preparation.md, demo_questions.md
├── 05_deliverables/  cost_estimate.md, proposal.md
└── 06_reference/     this file!
```

---

**Version:** 1.0
**Keep this open during meetings!**
