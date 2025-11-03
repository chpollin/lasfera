# La Sfera - IMMEDIATE Next Steps

**Datum:** 3. November 2025
**Status:** READY TO START
**Lokales Docker:** ✅ Läuft bereits
**Meeting mit Laura:** Noch ausstehend

---

## JETZT SOFORT (Nächste 3-5 Stunden)

Du hast lokales Docker laufen und willst HEUTE anfangen zu implementieren.
Hier ist EXAKT was du tun solltest:

---

## STEP 1: GitHub Issues Research (1h)

### 1.1 Repository aktualisieren
```bash
cd C:\Users\Chrisi\Documents\GitHub\Cloned\lasfera
git checkout main
git pull origin main
```

### 1.2 Issues lesen und dokumentieren

**Öffne GitHub Issues:**
- https://github.com/chnm/lasfera/issues/74 (Variant Data Model)
- https://github.com/chnm/lasfera/issues/76 (Variant Import)
- https://github.com/chnm/lasfera/issues/73 (Variant Display)
- https://github.com/chnm/lasfera/issues/65 (Gallery Docs)
- https://github.com/chnm/lasfera/issues/60 (Crowdsourcing)
- https://github.com/chnm/lasfera/issues/51 (User Roles)
- https://github.com/chnm/lasfera/issues/22 (import_export)
- https://github.com/chnm/lasfera/issues/56 (Historic Base Map)

**Für jedes Issue dokumentieren in `knowledge/03_bugs/github_issues_inventory.md`:**
- Status (Open/Closed)
- Summary (3-5 Sätze)
- Acceptance Criteria
- Technical Details (Files affected)
- Current Status (What's done, what's remaining)
- Effort Update (Original estimate still valid?)

**Deliverable:** Ausgefüllte `github_issues_inventory.md`

---

## STEP 2: Live-Site Investigation (2h)

### 2.1 Gazetteer Testing

**URL:** https://lasfera.rrchnm.org/toponyms

**Test Cases:**
```
TEST A2: Broken Links in Gazetteer
─────────────────────────────────────────
1. Open https://lasfera.rrchnm.org/toponyms
2. Wait for map to load
3. Click on a map marker
4. Popup opens → Click link in popup
5. EXPECTED: Opens toponym detail page
6. ACTUAL: [Document your findings]
7. Screenshot: [Save to knowledge/screenshots/]

Browser Console Check:
- Open DevTools (F12)
- Any JavaScript errors?
- Screenshot errors if present
```

```
TEST A3: Popup Format Issue
─────────────────────────────────────────
1. Same map as above
2. Hover/Click multiple markers
3. EXPECTED: Shows toponym name, description, link
4. ACTUAL: Shows "No name available" (according to Task Analysis)
5. Screenshot: [Save multiple popups]
6. Note which fields are missing
```

### 2.2 Introduction Page Check

```
TEST A1: Introduction Page Exists?
─────────────────────────────────────────
1. Try URL: https://lasfera.rrchnm.org/introduction/
2. RESULT: [Exists / 404 Not Found / Redirects]
3. If exists: Screenshot current state
4. Check navigation bar: Is "Introduction" link visible?
5. Screenshot: Navigation bar
```

### 2.3 Manuscript List Check

```
TEST C1: Manuscript List Page
─────────────────────────────────────────
1. Try URL: https://lasfera.rrchnm.org/manuscripts/
2. RESULT: [Exists / 404 / Shows something else]
3. Expected: List of 160 manuscripts
4. Actual: [Document]
5. Screenshot
6. Check navbar: Should be link but "disappeared" (Task Analysis)
```

### 2.4 Create Evidence Folder

```bash
mkdir knowledge/screenshots
mkdir knowledge/screenshots/gazetteer
mkdir knowledge/screenshots/navigation
mkdir knowledge/screenshots/manuscripts
```

**Save all screenshots with descriptive names:**
- `gazetteer_map_popup_issue.png`
- `gazetteer_broken_link_example.png`
- `navbar_missing_introduction.png`
- `manuscripts_404_error.png`

**Deliverable:** Investigation findings document + screenshots

---

## STEP 3: Lokales Testing (Optional, 1h)

### 3.1 Lokales Setup verifizieren

```bash
cd C:\Users\Chrisi\Documents\GitHub\Cloned\lasfera

# Check Docker is running
docker ps

# Check database
docker exec -it lasfera_db_1 psql -U lasfera -c "\dt"

# Check Django
python manage.py check

# Run dev server
python manage.py runserver
```

### 3.2 Lokale Tests (Same as Live-Site)

- Navigate to http://localhost:8000/toponyms
- Test same scenarios as Step 2
- Compare: Does local behave differently than live?

**Deliverable:** Notes on local vs. live differences

---

## STEP 4: Code-Vorbereitung für Bug-Fixes (1-2h)

### 4.1 Branch erstellen für Bug #1

```bash
git checkout -b fix/urb1-hardcoding
```

### 4.2 Code-Locations identifizieren

```bash
# Finde alle Urb1 Hardcodes
grep -rn "Urb1" manuscript/views.py

# Expected:
# manuscript/views.py:489
# manuscript/views.py:492
# manuscript/views.py:498
# manuscript/views.py:537
# manuscript/views.py:694
```

### 4.3 Refactoring vorbereiten (NOCH NICHT committen!)

**Datei:** `config/settings.py`
```python
# Add this at the end
DEFAULT_MANUSCRIPT_SIGLUM = "Urb1"  # Fallback manuscript for IIIF viewer
```

**Datei:** `manuscript/views.py`
```python
# At top, add import
from django.conf import settings

# In mirador_view() - Line 489
try:
    manuscript = SingleManuscript.objects.get(id=manuscript_id)
except SingleManuscript.DoesNotExist:
    logger.warning(f"Manuscript {manuscript_id} not found, using default")
    manuscript = SingleManuscript.objects.filter(
        siglum=settings.DEFAULT_MANUSCRIPT_SIGLUM
    ).first()
    if not manuscript:
        raise Http404("No manuscripts available")
```

**Deliverable:** Code changes PREPARED but NOT committed

---

## STEP 5: Meeting-Vorbereitung (2h)

### 5.1 Presentation erstellen

**Tool:** PowerPoint / Google Slides / Markdown Slides

**Struktur:**
```
SLIDE 1: Agenda
- Task Prioritization
- Data Dependencies
- GitHub Issues
- Budget & Timeline

SLIDE 2: The Scope Discovery
- Started with: 3 Bugs (3.510€)
- Discovered: 53 Tasks (59.250€)
- Factor: 17x difference!

SLIDE 3: Phase 1 - Quick Wins
- 8 Tasks
- 6.300€
- 4 weeks
- LOW RISK

SLIDE 4: Phase 2 - IIIF Integration
- Bug #2 (20-30h!)
- 12.750€
- 4-6 weeks
- MEDIUM RISK

SLIDE 5: Phase 3 - Backend/DB
- 10 Tasks
- 35.100€
- 10-15 weeks
- HIGH RISK (Data Dependencies!)

SLIDE 6: Recommended Strategy
- START: Phase 1 (6.300€)
- REVIEW: After 4 weeks
- DECIDE: Continue or stop?

SLIDE 7: Budget Comparison
[Table from IMPLEMENTATION_EXECUTIVE_SUMMARY.md]

SLIDE 8: Questions for Laura
[List from IMPLEMENTATION_ROADMAP.md Section 10]

SLIDE 9: Next Steps
- Approve Phase 1
- Start Sprint 1 (Week of Nov 10)
- First Review: Dec 6
```

### 5.2 Demo-Script vorbereiten

**Datei:** `knowledge/04_meetings/demo_script.md`
```markdown
# Demo Script for Laura Meeting

## Part 1: Live-Site Demonstration (10 min)

### Demo A: Gazetteer Issues
1. Screen-share https://lasfera.rrchnm.org/toponyms
2. Show map rendering
3. Click marker → Show popup issue
4. Click link → Show broken link (if applicable)
5. Ask Laura: "Is this how it should look?"

### Demo B: Bug #1 (Urb1 Hardcoding)
1. Show manuscript/views.py:489 in code
2. Explain: "Falls back to Urb1 when manuscript not found"
3. Ask: "Is this intentional or bug?"

### Demo C: Bug #3 (page_number)
1. Try URL: /manuscripts/1/mirador/42/
2. Show: Opens at page 1, ignores "42"
3. Ask: "Do you need deep-linking to specific pages?"

## Part 2: Task Prioritization (20 min)
[Present 5 Scenarios with costs]

## Part 3: Q&A (15 min)
[Open questions]
```

### 5.3 Agenda-Email an Laura schicken

**Template:**
```
Subject: La Sfera Implementation - Meeting Preparation

Hi Laura,

I've completed a detailed analysis of the Task Analysis Report and have prepared an implementation roadmap.

Key Findings:
- 53 tasks identified (vs. original 3 bugs)
- Budget range: 3.510€ (minimal) to 59.250€ (full scope)
- Recommended approach: Phase 1 (6.300€, 4 weeks)

For our meeting, I'd like to:
1. Demonstrate current issues on live site (10 min)
2. Present phased implementation plan (20 min)
3. Clarify data dependencies and priorities (15 min)

Attached:
- Implementation Roadmap (full document)
- Executive Summary (2 pages)
- Questions for discussion

Could you please review before we meet?

Looking forward to discussing!

Best,
Christopher
```

**Attachments:**
- IMPLEMENTATION_ROADMAP.md
- IMPLEMENTATION_EXECUTIVE_SUMMARY.md

**Deliverable:** Email sent, meeting confirmed

---

## STEP 6: Knowledge Base Update (30 min)

### 6.1 Verify all files created

```bash
# Check if all new KB files exist
ls -la knowledge/IMPLEMENTATION_ROADMAP.md
ls -la knowledge/IMPLEMENTATION_EXECUTIVE_SUMMARY.md
ls -la knowledge/NEXT_STEPS_IMMEDIATE.md
ls -la knowledge/07_implementation/task_tracking.md
ls -la knowledge/03_bugs/github_issues_inventory.md
```

### 6.2 Update task_tracking.md

Mark Sprint 0 tasks as started:
```markdown
## SPRINT 0: Pre-Work & Meeting (Nov 3-10, 2025)

### Tasks

#### Task 0.1: GitHub Issues Research
**Status:** IN PROGRESS (started Nov 3)
**Progress:** [X] 5/8 issues read

#### Task 0.2: Live-Site Investigation
**Status:** IN PROGRESS (started Nov 3)
**Progress:** [X] Gazetteer tested, [ ] Others pending

#### Task 0.3: Meeting Preparation
**Status:** IN PROGRESS
**Progress:** [X] Presentation created, [ ] Email sent
```

### 6.3 Create TODAY.md (Daily Log)

```bash
echo "# Daily Log - November 3, 2025" > knowledge/TODAY.md
```

**Inhalt:**
```markdown
# Daily Log - November 3, 2025

## What I did today:

### Morning (9:00-12:00)
- [X] Analyzed Task Analysis and Status Report
- [X] Created Implementation Roadmap (15k words!)
- [X] Created Task Tracking System
- [X] Created GitHub Issues Inventory template

### Afternoon (13:00-18:00)
- [ ] Read GitHub Issues #74, #76, #73 (in progress)
- [ ] Live-Site testing (gazetteer)
- [ ] Prepare meeting presentation
- [ ] Send email to Laura

## Discoveries:
- Task Analysis reveals 53 tasks vs. 3 bugs!
- Full scope is 17x larger than original estimate
- Many tasks blocked by data dependencies

## Blockers:
- None (pre-work phase, no blockers)

## Tomorrow:
- [ ] Finish GitHub Issues reading
- [ ] Complete live-site investigation
- [ ] Finalize meeting presentation
- [ ] Review with team (if applicable)

## Time Tracking:
- Implementation Planning: 3h
- Documentation: 2h
- Total: 5h (billable? TBD)
```

---

## SUMMARY: Was du die nächsten 5h machst

```
HOUR 1: GitHub Issues
├─ Read 8 issues on GitHub
├─ Document findings in github_issues_inventory.md
└─ Note any surprises or blockers

HOUR 2-3: Live-Site Testing
├─ Test Gazetteer (Task A2, A3)
├─ Test Introduction Page (Task A1)
├─ Test Manuscript List (Task C1)
├─ Screenshot everything
└─ Document findings

HOUR 4: Meeting Prep
├─ Create presentation slides
├─ Write demo script
├─ Draft email to Laura
└─ Prepare questions

HOUR 5: Wrap-Up
├─ Update task_tracking.md
├─ Create daily log
├─ Send email to Laura
└─ Review progress
```

---

## Deliverables (End of Day)

Nach 5 Stunden solltest du haben:

- [X] `knowledge/03_bugs/github_issues_inventory.md` (ausgefüllt)
- [X] `knowledge/screenshots/` (Ordner mit 5-10 Screenshots)
- [X] `knowledge/04_meetings/demo_script.md`
- [X] `knowledge/04_meetings/meeting_presentation.pdf` oder .pptx
- [X] `knowledge/07_implementation/task_tracking.md` (updated)
- [X] `knowledge/TODAY.md` (Daily Log)
- [X] Email an Laura (gesendet)

---

## Was du NICHT tun solltest (heute)

❌ **NICHT:** Code committen und pushen
- Grund: Kein Approval von Laura

❌ **NICHT:** Pull Requests erstellen
- Grund: Noch nicht abgesprochen

❌ **NICHT:** Production-Deployment
- Grund: NIEMALS ohne Client-Approval

❌ **NICHT:** Große Refactorings starten
- Grund: Erst nach Meeting

✅ **STATTDESSEN:** Vorbereitung, Investigation, Documentation

---

## Nach dem Meeting (nur wenn approved)

**Wenn Laura Phase 1 genehmigt:**

### Day 1 (Post-Meeting):
```bash
# Create feature branches
git checkout -b fix/urb1-hardcoding
git checkout main
git checkout -b fix/mirador-page-number
git checkout main
git checkout -b feature/introduction-nav
git checkout main
git checkout -b docs/gallery-images
```

### Day 2-5: Sprint 1 Implementation
- Implement Bug #1 fix
- Implement Bug #3 fix
- Add Introduction button
- Write Gallery docs

### Day 6-10: Sprint 2 Implementation
- Fix Gazetteer links
- Improve Popups
- Revive Manuscript List

### Day 11: Sprint Review
- Demo to Laura on dev.lasfera.rrchnm.org
- Gather feedback
- Plan Sprint 3 (if continuing)

---

## Contact & Questions

**Stuck? Unsicher?**

**Option 1:** Check Knowledge Vault
- `knowledge/README.md` - Übersicht
- `knowledge/IMPLEMENTATION_ROADMAP.md` - Full Plan
- `knowledge/02_technical/tech_stack.md` - System Info

**Option 2:** Note in Daily Log
- Add to "Blockers" section
- Ask Laura in meeting

**Option 3:** Search Codebase
```bash
# Find examples
grep -rn "similar_code" .

# Check git history
git log --all --grep="keyword"
```

---

## Success Criteria (End of Pre-Work Phase)

✅ **GitHub Issues:** All 8 issues read and documented
✅ **Live-Site:** All 4 test scenarios completed
✅ **Screenshots:** 5-10 evidence screenshots saved
✅ **Meeting:** Presentation prepared, email sent
✅ **Knowledge Base:** All documents up-to-date
✅ **Code:** Bug-fix branches created (but not committed!)

**Dann:** Ready for Meeting mit Laura

---

## Time Tracking

```
Sprint 0 Pre-Work Estimate: 3-5h
├─ GitHub Issues: 1h
├─ Live-Site Testing: 2h
├─ Meeting Prep: 2h
└─ Documentation: 0.5h

Actual: [TBD - track in task_tracking.md]
```

**Billable?** TBD - Depends on contract (pre-work often non-billable)

---

## Ready to Start?

**GO TO:** Task 0.1 (GitHub Issues Research)
**TOOL:** Browser + `knowledge/03_bugs/github_issues_inventory.md`
**TIME:** 1 hour
**OUTPUT:** Documented findings for 8 issues

**Los geht's! 🚀**

---

**Created:** November 3, 2025
**For:** Christopher Pollin / DH Craft
**Next Review:** After Meeting with Laura
