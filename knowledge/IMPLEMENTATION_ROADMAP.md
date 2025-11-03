# IMPLEMENTIERUNGSPLAN: La Sfera Task Analysis

**Datum:** 3. November 2025
**Basis:** Task Analysis and Status Report.md
**Status:** PRE-IMPLEMENTATION (Docker läuft lokal)
**Meeting mit Laura:** Ausstehend (3. oder 11. November)

---

## EXECUTIVE SUMMARY

**Gesamtübersicht:** 53 identifizierte Tasks aus Meeting Notes
- **SOFORT umsetzbar (Developer):** 8 Tasks (SIMPLE to MEDIUM complexity)
- **Braucht Backend/DB:** 12 Tasks (MEDIUM to COMPLEX)
- **Braucht Content von Laura/Carrie:** 18 Tasks (nicht Developer-Aufgabe)
- **BLOCKED/Low Priority:** 8 Tasks
- **Unklar/Need Clarification:** 7 Tasks

**EMPFEHLUNG:** Fokus auf HIGH PRIORITY Tasks mit klarer Machbarkeit

---

## 1. SOFORT UMSETZBAR (Ohne zusätzliche Daten)

### CATEGORY A: Navigation & UI Quick Wins (SIMPLE)

#### Task A1: Add "Introduction" Button to Navigation Bar
**Source:** Project 4, HIGH PRIORITY, Due: Oct 17, 2025 (überfällig)
**Owner:** Jason Heppler (originally)
**Files:** `templates/base.html` oder Wagtail Navigation Template
**Complexity:** SIMPLE
**Dependencies:** KEINE (Content-Seite sollte bereits existieren)

**Implementation:**
```html
<!-- In navigation template -->
<nav>
  <a href="/">Home</a>
  <a href="/introduction/">Introduction</a>  <!-- NEU -->
  <a href="/about/">About</a>
  <!-- ... -->
</nav>
```

**Status Check nötig:**
- [ ] Existiert `/introduction/` Seite bereits? (Wagtail CMS check)
- [ ] Wenn nicht: Placeholder-Seite erstellen

**DECISION NEEDED:** Laura fragen ob Content schon existiert

---

#### Task A2: Fix Broken Links in Gazetteer Landing Page Map
**Source:** Project 6, HIGH PRIORITY
**Files:** `templates/manuscript/toponyms.html`, `manuscript/views.py:952`
**Complexity:** SIMPLE (debugging + fix)

**Symptoms:**
- "Broken links" nicht spezifiziert
- Vermutlich: Links von Map-Popups zu Toponym-Detail-Pages

**Investigation needed:**
```python
# manuscript/views.py:952
def toponyms(request: HttpRequest):
    # Check link generation logic
    # Verify ToponymViewSet API returns correct URLs
```

**Template Check:**
```javascript
// Check Leaflet popup HTML generation
// Verify href="{{ toponym.get_absolute_url }}" oder ähnlich
```

**DECISION NEEDED:** Live-Site inspizieren, welche Links genau kaputt sind

---

#### Task A3: Improve Popup Format (Gazetteer Map)
**Source:** Project 6, HIGH PRIORITY
**Current Issue:** Shows "No name available"
**Files:**
- `templates/manuscript/toponyms.html` (Leaflet init)
- `manuscript/views.py:1093` (ToponymViewSet)
**Complexity:** SIMPLE

**Current Code Check:**
```python
# manuscript/serializers.py (?)
class ToponymSerializer(serializers.ModelSerializer):
    # Check which fields are exposed
    # Likely missing: name, description, related_stanzas_count
```

**Fix:**
```javascript
// Leaflet popup template
L.marker([lat, lng]).bindPopup(`
  <strong>${toponym.name || 'Unknown Location'}</strong><br>
  ${toponym.description || ''}<br>
  <a href="/toponyms/${toponym.placename_id}/">Details</a>
`);
```

**DECISION NEEDED:** Laura zeigen, welche Infos sie in Popups will

---

### CATEGORY B: Code Quality Fixes (bereits vorbereitet)

#### Task B1: Remove Urb1 Hardcoding (Bug #1)
**Source:** Bug Inventory (bereits identifiziert)
**Files:** `manuscript/views.py:489, 492, 498, 537, 694`
**Complexity:** MEDIUM
**Status:** BEREIT ZUM IMPLEMENTIEREN (Code prepared)

**Implementation:** Siehe `knowledge/03_bugs/bug_inventory.md`

**READY TO GO:** ✅ Ja, Branch `fix/urb1-hardcoding` kann erstellt werden

---

#### Task B2: Fix page_number Parameter (Bug #3)
**Source:** Bug Inventory
**Files:** `manuscript/views.py:485-506`
**Complexity:** MEDIUM
**Status:** BEREIT ZUM IMPLEMENTIEREN

**READY TO GO:** ✅ Ja, Branch `fix/mirador-page-number` kann erstellt werden

---

#### Task B3: Fix Silent Exceptions
**Source:** Bug Inventory (bereits als "fixed" verifiziert, aber Logging verbessern)
**Files:** `manuscript/models.py`, `manuscript/resources.py`
**Complexity:** SIMPLE
**Status:** OPTIONAL (Code ist bereits korrekt, aber Logging kann erweitert werden)

**Enhancement:**
```python
# Erweitere bestehende Exception-Handling mit mehr Context
logger.warning(
    f"Stanza not found for line_code {stanza_line_code_starts}, "
    f"manuscript: {self.manuscript.siglum}",
    extra={"manuscript_id": self.manuscript.id}
)
```

---

### CATEGORY C: Template/Content Improvements

#### Task C1: Revive Manuscript List Page
**Source:** Project 5, MEDIUM Priority
**Issue:** "Previously shown by Jason, disappeared"
**Potential Files:**
- `manuscript/views.py` (create/reactivate view)
- `manuscript/urls.py` (add route)
- `templates/manuscript/manuscript_list.html` (create/find)
**Complexity:** MEDIUM

**Investigation:**
```bash
# Check git history for deleted files
git log --all --full-history --diff-filter=D -- "**/*manuscript_list*"
git log --all --grep="manuscript list" --grep="160 manuscripts"
```

**Implementation:**
```python
# manuscript/views.py
def manuscript_list(request):
    manuscripts = SingleManuscript.objects.all().order_by('siglum')
    return render(request, 'manuscript/manuscript_list.html', {
        'manuscripts': manuscripts,
        'total_count': manuscripts.count()  # Should be 160
    })
```

**DECISION NEEDED:**
- [ ] Git History durchsuchen
- [ ] Laura fragen: "Wie sah die Liste aus?"

---

#### Task C2: Update About Page Team Members
**Source:** Project 5, HIGH PRIORITY, Due: Oct 31, 2025 (überfällig)
**Files:** Wagtail CMS-Seite oder `templates/about.html`
**Complexity:** SIMPLE (wenn Content bereitgestellt wird)

**BLOCKED BY:** Content von Laura/Carrie

**Implementation:**
- IF static template → Edit HTML
- IF Wagtail CMS → Laura muss selbst updaten (Developer nur bei Template-Problemen)

**DECISION NEEDED:** Laura fragen ob Wagtail-Zugang oder Template-Edit nötig

---

### CATEGORY D: Documentation Tasks

#### Task D1: Write Documentation for Adding Gallery Images
**Source:** Project 2, MEDIUM/HIGH Priority, Due: Oct 17, 2025
**Files:** Create `docs/gallery_images.md` or update README
**Complexity:** SIMPLE
**Owner:** Jason Heppler (originally)

**Content:**
```markdown
# Adding Gallery Images to La Sfera

## Prerequisites
- Images in IIIF format
- Rights-cleared (DRM-free)

## Steps
1. Upload image to IIIF server
2. Add manifest URL to database
3. Configure gallery display settings
4. Test rendering

## Examples
[...]
```

**READY TO GO:** ✅ Ja (Developer kann dokumentieren wie aktuelles System funktioniert)

---

### **PHASE 1 SUMMARY: Quick Wins**

| Task | Priority | Complexity | Dependencies | Status |
|------|----------|------------|--------------|--------|
| A1: Introduction Button | HIGH | SIMPLE | Content-Check | READY (if content exists) |
| A2: Fix Gazetteer Links | HIGH | SIMPLE | Live-Site Debug | NEEDS INVESTIGATION |
| A3: Improve Popups | HIGH | SIMPLE | Laura Input | NEEDS DESIGN |
| B1: Urb1 Hardcoding | HIGH | MEDIUM | NONE | ✅ READY |
| B2: page_number Fix | MED | MEDIUM | NONE | ✅ READY |
| B3: Logging Enhancement | LOW | SIMPLE | NONE | OPTIONAL |
| C1: Manuscript List | MED | MEDIUM | Git History | NEEDS INVESTIGATION |
| D1: Gallery Docs | MED | SIMPLE | NONE | ✅ READY |

**TOTAL PHASE 1:** 8 tasks (mix of SIMPLE and MEDIUM complexity)

---

## 2. BRAUCHT BACKEND/DB ÄNDERUNGEN

### CATEGORY E: IIIF Integration (COMPLEX)

#### Task E1: Add IIIF Viewer to /stanzas/ (Bug #2)
**Source:** Bug Inventory + Project 2
**Priority:** HIGH (In Progress Jason)
**Due:** Feb 13, 2026
**Files:**
- `templates/manuscript/stanzas.html`
- `manuscript/views.py:550` (stanzas view)
- `static/js/tify-sync.js`
**Complexity:** COMPLEX

**Current Status:** Viewer code exists but doesn't render (JavaScript issue)

**Sub-Tasks:**
1. Debug why Tify doesn't initialize
2. Fix JavaScript initialization
3. Add canvas synchronization with text
4. Test across different manuscripts
5. Performance optimization

**COMPLEXITY:** HIGH
- JavaScript debugging
- AlpineJS integration
- Canvas-ID calculation from Line Codes
- Cross-browser testing

**DECISION NEEDED:**
- [ ] Laura bestätigen dass Feature gewünscht
- [ ] Layout-Design abstimmen (Side-by-side wie manuscript_stanzas?)

---

#### Task E2: Add MSS to IIIF Integration on Edition Interface
**Source:** Project 2, HIGH Priority, Due: Feb 13, 2026
**Owner:** Jason Heppler (IN PROGRESS)
**Complexity:** COMPLEX

**Interpretation:** "MSS" = Multiple Manuscripts gleichzeitig?
**Possible Feature:** Compare view with multiple IIIF viewers side-by-side

**NEEDS CLARIFICATION:**
- [ ] Was bedeutet "MSS"? (Manuscripts?)
- [ ] Welches Interface? (Mirador? Stanzas?)
- [ ] Already in progress von Jason?

**DECISION NEEDED:** Laura/Jason fragen was gemeint ist

---

### CATEGORY F: Data Model & Database

#### Task F1: Revise Textual Variant Data Model (Issue #74)
**Source:** Project 1, MEDIUM/HIGH Priority
**Owner:** Jason Heppler
**Files:** `manuscript/models.py` (StanzaVariant model)
**Complexity:** MEDIUM

**Current Model:** (needs inspection)
```python
class StanzaVariant(models.Model):
    # Check current fields
    # Likely needs: manuscript, stanza, variation_type, text
```

**BLOCKED BY:**
- [ ] What's wrong with current model? (Check Issue #74 on GitHub)
- [ ] Laura Ingallinella input (RAs working on dataset)

**DECISION NEEDED:** GitHub Issue lesen, Laura fragen

---

#### Task F2: Handle Data Importing for Textual Variants (Issue #76)
**Source:** Project 1, MEDIUM/HIGH Priority
**Files:**
- `manuscript/resources.py` (import logic)
- `manuscript/management/commands/load_textual_variants.py` (create?)
**Complexity:** MEDIUM

**Requirements:**
- Import CSV/Excel with textual variants
- Validate data (stanza exists, manuscript exists)
- Handle duplicates
- Logging & error reporting

**Implementation:**
```python
# manuscript/management/commands/load_textual_variants.py
class Command(BaseCommand):
    def handle(self, *args, **options):
        # Read CSV
        # For each row:
        #   - Find stanza by line_code
        #   - Find manuscript by siglum
        #   - Create StanzaVariant
        #   - Handle errors
```

**BLOCKED BY:**
- [ ] Data model finalization (Task F1)
- [ ] Sample data from Laura Ingallinella

---

#### Task F3: Finalize Design for Textual Variant Display (Issue #73)
**Source:** Project 1, MEDIUM/HIGH Priority
**Files:**
- `templates/manuscript/stanza_detail.html` (?)
- CSS for variant highlighting
**Complexity:** MEDIUM

**Features:**
- Display variants inline or side-by-side
- Highlight differences
- Toggle between base text and variants
- Filter by manuscript

**DECISION NEEDED:**
- [ ] Design mockup von Laura
- [ ] GitHub Issue #73 checken

---

#### Task F4: Add Bidirectional Links (Toponyms ↔ Pages) [LINKY]
**Source:** Project 6, HIGH Priority, Due: Dec 31, 2025
**Owner:** Carrie Benes
**Files:**
- `manuscript/models.py` (ensure ManyToMany exists)
- `templates/manuscript/toponym_detail.html`
- `templates/manuscript/stanzas.html`
**Complexity:** MEDIUM

**Current Status:** Check if ManyToMany relationship exists
```python
# manuscript/models.py
class Stanza(models.Model):
    locations_mentioned = models.ManyToManyField(Location, ...)

class Location(models.Model):
    # Reverse relation: location.stanza_set.all()
```

**Implementation:**
```html
<!-- In toponym_detail.html -->
<h3>Mentioned in:</h3>
<ul>
  {% for stanza in toponym.stanza_set.all %}
    <li><a href="{{ stanza.get_absolute_url }}">{{ stanza.stanza_line_code }}</a></li>
  {% endfor %}
</ul>
```

**DECISION NEEDED:**
- [ ] Check current model relationships
- [ ] Verify data exists (Carrie's dataset)

---

#### Task F5: Refine Text Annotations with Toponym Links [LINKY]
**Source:** Project 5, HIGH Priority, Due: Oct 31, 2025
**Owner:** Laura Morreale
**Files:**
- `manuscript/models.py` (Annotation model?)
- `templates/manuscript/stanzas.html` (rendering)
**Complexity:** MEDIUM

**Feature:** Clickable toponyms in transcription text
**Example:**
```html
<p class="transcription">
  Passando per <a href="/toponyms/roma/" class="toponym-link">Roma</a>
  verso il mare...
</p>
```

**COMPLEXITY:**
- Text parsing/replacement (regex or NLP?)
- Database lookup (match text → Location)
- Avoid false positives ("Roma" could be "roman" adjective)

**BLOCKED BY:**
- [ ] Final toponym dataset (Carrie)
- [ ] Matching strategy (Laura input)

---

### CATEGORY G: WHG Integration (External System)

#### Task G1: Create WHG Data Model
**Source:** Project 7, MEDIUM Priority, Due: Mar 31, 2026
**Owner:** Carrie Benes (IN PROGRESS)
**Complexity:** MEDIUM (Backend Developer part)

**WHG:** World Historical Gazetteer (https://whgazetteer.org/)

**Requirements:**
- Export La Sfera toponyms to WHG format (JSON-LD)
- Link to WHG place IDs
- Store WHG URLs in database

**BLOCKED BY:** Carrie's work (she's creating data model)

**Developer Part:** Implement data export when model ready

---

#### Task G2: Create Toponym Dataset in WHG Format
**Source:** Project 7, MEDIUM Priority, Due: Mar 31, 2026
**Owner:** Carrie Benes (IN PROGRESS)
**Complexity:** SIMPLE (Developer part: implement export script)

**Implementation:**
```python
# manuscript/management/commands/export_to_whg.py
class Command(BaseCommand):
    def handle(self):
        # Query all Location objects
        # Convert to WHG JSON-LD format
        # Write to file for Carrie to upload
```

**BLOCKED BY:** Carrie's WHG model definition

---

#### Task G3: Add WHG Links to Toponym Pages [Not-SH]
**Source:** Project 7, MEDIUM Priority, Due: Mar 31, 2026
**Files:** `templates/manuscript/toponym_detail.html`
**Complexity:** SIMPLE

**Implementation:**
```html
<!-- In toponym_detail.html -->
{% if toponym.whg_url %}
  <a href="{{ toponym.whg_url }}" target="_blank">
    View in World Historical Gazetteer
  </a>
{% endif %}
```

**BLOCKED BY:**
- [ ] WHG URLs in database (Carrie's work)
- [ ] WHG collection created

---

### **PHASE 2 SUMMARY: Backend/DB Changes**

| Task | Priority | Complexity | Dependencies | Status |
|------|----------|------------|--------------|--------|
| E1: IIIF Viewer /stanzas/ | HIGH | COMPLEX | Laura approval | COMPLEX |
| E2: MSS IIIF Integration | HIGH | COMPLEX | Clarification | UNCLEAR |
| F1: Variant Data Model | MED/HIGH | MEDIUM | Issue #74, Laura | NEEDS REVIEW |
| F2: Variant Importing | MED/HIGH | MEDIUM | F1 done | BLOCKED |
| F3: Variant Display | MED/HIGH | MEDIUM | F1 done, Design | BLOCKED |
| F4: Toponym Links | HIGH | MEDIUM | Carrie dataset | DATA NEEDED |
| F5: Annotation Links | HIGH | MEDIUM | Carrie dataset | DATA NEEDED |
| G1: WHG Data Model | MED | MEDIUM | Carrie | IN PROGRESS |
| G2: WHG Export | MED | SIMPLE | G1 done | BLOCKED |
| G3: WHG Links | MED | SIMPLE | G2 done | BLOCKED |

**TOTAL PHASE 2:** 10 tasks (mostly MEDIUM to COMPLEX complexity)

**CRITICAL:** Viele Tasks blockiert durch Data/Design-Entscheidungen

---

## 3. BRAUCHT CONTENT VON LAURA/CARRIE (Nicht Developer-Tasks)

### CATEGORY H: Content Creation (Laura Morreale)

#### Task H1: Build & Fill Introduction Page
**Source:** Project 5, HIGH Priority, Due: Oct 31, 2025
**Owner:** Laura Morreale
**Deliverable:** Student-focused introduction content
**Developer Part:** NONE (Wagtail CMS entry)

**Developer Support (if needed):** Template adjustments (SIMPLE)

---

#### Task H2: Improve Landing Page Text
**Source:** Project 5, HIGH Priority, Due: Oct 31, 2025
**Owner:** Laura Morreale
**Developer Part:** NONE (Wagtail CMS)

---

#### Task H3: Incorporate Revised "Page by Page Text"
**Source:** Project 5, HIGH Priority, Due: Oct 31, 2025
**Owner:** Laura Morreale, Carrie
**Developer Part:** NONE (data import wenn CSV geliefert)

**IF Developer needed:** Import command schreiben (SIMPLE)

---

#### Task H4: Create "Teach with La sfera" Materials
**Source:** Project 5, MEDIUM Priority, Due: Jan 31, 2026
**Owner:** Laura Morreale
**Developer Part:** NONE (Content page)

---

#### Task H5: Fill Out Textual Variant Dataset
**Source:** Project 1, MEDIUM/HIGH Priority, Due: Feb 28, 2026
**Owner:** Laura Ingallinella (RAs working Fall 2025/Winter 2026)
**Developer Part:** Import script (Task F2)

---

### CATEGORY I: Geospatial Content (Carrie Beneš)

#### Task I1: Create "Final" Toponym Dataset
**Source:** Project 6, HIGH Priority
**Owner:** Carrie Benes
**Developer Part:** NONE (wait for dataset)

**Developer Task AFTER delivery:** Import script if format changes (SIMPLE)

---

#### Task I2: Decide on Variant Display Criteria
**Source:** Project 6, MEDIUM Priority
**Owner:** Carrie + Laura (Content decision)
**Developer Part:** Implement filter logic (SIMPLE) AFTER decision

---

#### Task I3: Choose DRM-free Images for Gallery
**Source:** Project 5, MEDIUM Priority, Due: Mar 31, 2026
**Developer Part:** NONE (Laura's rights clearance work)

---

### CATEGORY J: Infrastructure (Not Developer's Direct Work)

#### Task J1: Reassign sferaproject.org Domain
**Source:** Project 4, HIGH Priority, Due: Dec 31, 2025
**Owner:** Jason Heppler (RRCHNM sys admin)
**Developer Part:** NONE (DNS config)

---

#### Task J2: Write White Paper/DHQ Article
**Source:** Project 8, MEDIUM Priority
**Owner:** Amanda G Madden (IN PROGRESS, can start mid-October)
**Developer Part:** NONE (academic writing)

---

### **PHASE 3 SUMMARY: Content-Dependencies**

| Task | Owner | Developer Part | Status |
|------|-------|----------------|--------|
| H1-H5 | Laura Morreale | Minimal (SIMPLE tasks) | WAITING FOR CONTENT |
| I1-I3 | Carrie Benes | Import scripts (SIMPLE each) | WAITING FOR DATA |
| J1-J2 | RRCHNM/Amanda | NONE | NOT DEVELOPER |

**TOTAL Developer Support:** Multiple SIMPLE tasks (when content delivered)

---

## 4. BLOCKED / LOW PRIORITY

### CATEGORY K: Blocked Tasks

#### Task K1: Add Historic Base Map to Gazetteer (Issue #56)
**Source:** Project 6, LOW Priority
**Status:** BLOCKED (no details why)
**Complexity:** MEDIUM (if unblocked)

**Blocker:** Possibly map data unavailable or copyright issues

**DECISION NEEDED:** Laura klären warum blockiert

---

#### Task K2: Project 9 - Full Image Gallery (ALL BLOCKED)
**Source:** Project 9, LOW Priority
**Sub-Tasks:**
- Establish copyright-clear manuscripts (BLOCKED)
- Incorporate DMCA takedown note (BLOCKED)
- Export images from Tropy and upload (BLOCKED)

**Blocker:** Rights clearance

**Developer Part:** NONE until unblocked

---

### CATEGORY L: Extensible Edition (Future Features)

#### Task L1: Design Crowdsourcing Component (Issue #60)
**Source:** Project 3, MEDIUM Priority
**Complexity:** COMPLEX (LARGE feature)
**Status:** Design phase, no implementation yet

**DECISION NEEDED:** Laura confirm if wanted for launch

---

#### Task L2: Design User Roles for Contributions (Issue #51)
**Source:** Project 3, MEDIUM Priority
**Complexity:** COMPLEX
**Dependencies:** L1 (Crowdsourcing)

**DECISION NEEDED:** Post-launch feature?

---

#### Task L3: Design Flowchart for Manuscript Placement
**Source:** Project 3, MEDIUM Priority
**Complexity:** SIMPLE (design doc)
**Status:** Pre-implementation planning

---

#### Task L4: Incorporate import_export for Datasets (Issue #22)
**Source:** Project 3, MEDIUM Priority
**Complexity:** MEDIUM
**Feature:** Django-import-export integration for CSV uploads

**DECISION NEEDED:** Priority vs. custom import commands?

---

### **PHASE 4 SUMMARY: Blocked/Future**

| Category | Tasks | Complexity (if unblocked) | Status |
|----------|-------|---------------------------|--------|
| K: Blocked | 3 tasks | MEDIUM | WAIT FOR UNBLOCK |
| L: Future Features | 4 tasks | COMPLEX | DESIGN PHASE |

**NOT RECOMMENDED FOR IMMEDIATE WORK**

---

## 5. KNOWLEDGE BASE UPDATES NEEDED

### Files to CREATE:

#### KB1: `knowledge/04_meetings/2025-11-XX_meeting_notes.md`
**Purpose:** Document decisions from upcoming meeting
**Content:**
- Which tasks Laura approves
- Budget allocation
- Timeline agreement
- Content delivery schedule

---

#### KB2: `knowledge/07_implementation/task_tracking.md`
**Purpose:** Live task status tracking
**Format:**
```markdown
# Task Status Tracker

## Sprint 1 (Nov 11-22)
- [x] Task B1: Urb1 Hardcoding (4h actual)
- [ ] Task A1: Introduction Button (2h estimated)
- [IN PROGRESS] Task E1: IIIF Viewer debugging

## Sprint 2 (Nov 25 - Dec 6)
[...]
```

---

#### KB3: `knowledge/03_bugs/github_issues_inventory.md`
**Purpose:** Track referenced GitHub issues
**Content:**
- Issue #22: import_export
- Issue #51: User roles
- Issue #56: Historic base map
- Issue #60: Crowdsourcing
- Issue #65: Gallery docs
- Issue #73: Variant display
- Issue #74: Variant data model
- Issue #76: Variant import

**Action:** Clone/read these issues from GitHub

---

#### KB4: `knowledge/02_technical/api_documentation.md`
**Purpose:** Document existing APIs
**Content:**
- `/api/toponyms/` (ToponymViewSet)
- `/api/manuscripts/` (SingleManuscriptViewSet)
- `/api/annotations/` (if exists)

---

#### KB5: `knowledge/06_reference/wagtail_cms_guide.md`
**Purpose:** Document CMS usage for content updates
**For:** Laura's team to update pages without developer

---

### Files to UPDATE:

#### KB-U1: `knowledge/03_bugs/bug_inventory.md`
**Add:**
- Task A2: Gazetteer broken links
- Task A3: Popup format issue
- Cross-reference with Tasks E1, F4, F5

---

#### KB-U2: `knowledge/01_project/overview.md`
**Add:**
- Meeting notes section
- Task prioritization (Phase 1-4)
- Updated timeline with Sprints

---

#### KB-U3: `knowledge/05_deliverables/cost_estimate.md`
**Note:** Cost estimates removed for client confidentiality

---

#### KB-U4: `knowledge/README.md`
**Add:**
- Link to IMPLEMENTATION_ROADMAP.md
- Link to task_tracking.md
- Sprint structure explanation

---

## 6. EMPFOHLENE REIHENFOLGE (Step-by-Step)

### JETZT SOFORT (Vor Meeting): Pre-Work (3-5h)

#### Step 0.1: GitHub Issues lesen (1h)
```bash
# Clone repo wenn nicht vorhanden
git clone https://github.com/chnm/lasfera.git

# Browse Issues
# Read: #22, #51, #56, #60, #65, #73, #74, #76
# Document findings in KB3
```

---

#### Step 0.2: Live-Site Investigation (2h)
**Tasks:**
- [ ] Test Gazetteer links (Task A2)
- [ ] Inspect popup format (Task A3)
- [ ] Check if Introduction page exists (Task A1)
- [ ] Test Manuscript List URL (Task C1)
- [ ] Screenshot findings for meeting

---

#### Step 0.3: Knowledge Base Setup (1-2h)
- [ ] Create KB1-KB5 files
- [ ] Update KB-U1 to KB-U4
- [ ] Prepare meeting agenda with Task priorities

---

### MEETING (3. oder 11. Nov): Decision Time (45-60 min)

#### Agenda:

**1. Task Prioritization (20 min)**
Present:
- Phase 1: Quick Wins (8 tasks, 3.900€)
- Phase 2: Backend (10 tasks, 20.000€)
- Laura decides: Which phases for current budget?

**2. Data Dependencies (15 min)**
Confirm:
- [ ] Carrie's toponym dataset timeline
- [ ] Laura Ingallinella's variant data timeline
- [ ] Content delivery schedule (Introduction, About, etc.)

**3. GitHub Issues Review (10 min)**
Clarify:
- [ ] Issue #74: What's wrong with variant model?
- [ ] Issue #73: Show design mockup?
- [ ] Issue #60: Crowdsourcing in scope?

**4. Timeline & Budget (10 min)**
Agree:
- [ ] Start date
- [ ] Sprint structure (2-week sprints?)
- [ ] Payment milestones

---

### NACH MEETING: Implementation Starts

### SPRINT 1 (Woche 1-2): Quick Wins Phase 1A

**Focus:** High-confidence, low-dependency tasks

#### Week 1: Bug Fixes
- [ ] Day 1-2: Task B1 - Urb1 Hardcoding (4h)
- [ ] Day 2-3: Task B2 - page_number Fix (4h)
- [ ] Day 3-4: Task A1 - Introduction Button (1-2h)
- [ ] Day 4-5: Task D1 - Gallery Documentation (2-3h)

**Deliverable:** Pull Request #1 (Bug Fixes + Nav)

---

#### Week 2: Gazetteer Improvements
- [ ] Day 6-7: Task A2 - Fix Broken Links (2-3h)
- [ ] Day 7-8: Task A3 - Improve Popups (2-4h)
- [ ] Day 9-10: Task C1 - Revive Manuscript List (3-5h)

**Deliverable:** Pull Request #2 (Gazetteer + Manuscript List)

**SPRINT 1 TOTAL:** 18-25h
**Sprint Review:** Show Laura on dev.lasfera.rrchnm.org

---

### SPRINT 2 (Woche 3-4): IIIF Deep Dive (IF APPROVED)

**Focus:** Task E1 - IIIF Viewer in /stanzas/

#### Week 3: Investigation & Setup
- [ ] Day 11-12: Debug Tify initialization (3-5h)
- [ ] Day 12-13: Fix JavaScript errors (3-5h)
- [ ] Day 13-14: Test basic rendering (2-3h)

#### Week 4: Integration
- [ ] Day 15-16: Canvas sync with line codes (8-12h)
- [ ] Day 17-18: Cross-manuscript testing (3-5h)
- [ ] Day 19-20: Performance optimization (2-3h)

**Deliverable:** Pull Request #3 (IIIF Viewer)

**SPRINT 2 TOTAL:** 21-33h
**Sprint Review:** Full IIIF demo

---

### SPRINT 3 (Woche 5-6): Data Integration (IF DATA READY)

**Focus:** Tasks F4, F5 - Toponym Linking

**Prerequisites:**
- [ ] Carrie delivered final toponym dataset
- [ ] Bi-directional links data exists in DB

#### Week 5: Backend
- [ ] Task F4: Toponym ↔ Page links (6-10h)
- [ ] Task F5: Annotation link logic (8-15h)

#### Week 6: Testing & Polish
- [ ] Test all toponyms (2-3h)
- [ ] Fix edge cases (2-4h)
- [ ] Performance check (1-2h)

**Deliverable:** Pull Request #4 (Toponym Links)

**SPRINT 3 TOTAL:** 19-34h

---

### SPRINT 4+ (Woche 7+): Textual Variants (IF DATA READY)

**Focus:** Tasks F1, F2, F3

**Only if:**
- [ ] Laura Ingallinella provides sample data
- [ ] Issue #74 clarified
- [ ] Design approved

**Estimated:** 26-50h (separate planning needed)

---

## 7. RISK ASSESSMENT & DEPENDENCIES

### Critical Path Items:

**HIGH RISK - Could Delay Project:**

1. **Data Delivery Delays**
   - Carrie's toponym dataset (needed for F4, F5, I1)
   - Laura I's variant data (needed for F2, F3)
   - **Mitigation:** Work on Phase 1 tasks while waiting

2. **IIIF Complexity Underestimated**
   - Task E1 could be 20-30h → 40-50h
   - JavaScript debugging unpredictable
   - **Mitigation:** Time-box to 30h, then re-scope

3. **GitHub Issues Lack Context**
   - 8 referenced issues not fully understood
   - Could hide major requirements
   - **Mitigation:** Read ALL issues before committing

**MEDIUM RISK:**

4. **Wagtail CMS vs. Static Templates**
   - Unclear which content is CMS-managed
   - Could affect Task A1, C2, H1-H4
   - **Mitigation:** Check early in Sprint 1

5. **Content Team Availability**
   - Laura/Carrie might be busy (academic schedules)
   - Could delay approvals/reviews
   - **Mitigation:** 48h SLA agreement

**LOW RISK:**

6. **Deployment Access**
   - Might not have server access immediately
   - **Mitigation:** Local dev works, deploy later

---

## 8. IMPLEMENTATION SCENARIOS

### Scenario A: MINIMAL (Bug Fixes Only)
**Tasks:** B1, B2, B3 (from original bug inventory)
**Complexity:** Mix of SIMPLE and MEDIUM
**Timeline:** 2 weeks

---

### Scenario B: PHASE 1 (Quick Wins)
**Tasks:** A1, A2, A3, B1, B2, D1, C1
**Complexity:** 8 tasks (SIMPLE to MEDIUM)
**Timeline:** 3-4 weeks

---

### Scenario C: PHASE 1 + IIIF (High Priority)
**Tasks:** Scenario B + E1
**Complexity:** Adds COMPLEX IIIF integration
**Timeline:** 6-8 weeks

---

### Scenario D: PHASE 1 + 2 (Backend Integration)
**Tasks:** All A, B, C, D, E, F (excluding WHG)
**Complexity:** Multiple COMPLEX backend tasks
**Timeline:** 12-20 weeks (3-5 months)

---

### Scenario E: FULL SCOPE (All Non-Blocked Tasks)
**Tasks:** All A-L (excluding blocked K tasks)
**Complexity:** Full project scope with COMPLEX tasks
**Timeline:** 17-31 weeks (4-8 months)

---

### RECOMMENDATION:

**START WITH:** Scenario B (Phase 1 Quick Wins)
**RATIONALE:**
- Low risk (no data dependencies)
- High value (fixes 8 issues)
- Fast delivery (3-4 weeks)
- Builds trust for larger phases

**THEN DECIDE:** After Sprint 1 review, Laura can greenlight:
- Scenario C (add IIIF)
- Or Scenario D (full backend)

**AVOID:** Committing to Scenario E upfront (too much uncertainty)

---

## 9. NEXT STEPS CHECKLIST

### Pre-Meeting (JETZT):
- [ ] Read GitHub Issues #22, #51, #56, #60, #65, #73, #74, #76
- [ ] Live-Site investigation (Gazetteer, Introduction, Manuscript List)
- [ ] Create KB files (KB1-KB5)
- [ ] Update existing KB files (KB-U1 to KB-U4)
- [ ] Prepare meeting slides/agenda

**Deadline:** Before meeting (Nov 3 or 11)

---

### Meeting (Nov 3/11):
- [ ] Present Phase 1-4 breakdown
- [ ] Get Laura's priority ranking
- [ ] Clarify GitHub Issues
- [ ] Agree on Scenario (A-E)
- [ ] Set Sprint start date
- [ ] Request server access

---

### Post-Meeting (Same Day):
- [ ] Update `knowledge/04_meetings/2025-11-XX_meeting_notes.md`
- [ ] Update `knowledge/07_implementation/task_tracking.md` with approved tasks
- [ ] Send follow-up email with summary

---

### Sprint 1 Prep (Week before start):
- [ ] Setup local dev environment (if not already)
- [ ] Create Git branches for Phase 1 tasks
- [ ] Write test plans for each task
- [ ] Schedule Sprint Review with Laura

---

### Sprint 1 Execution (Week 1-2):
- [ ] Implement approved Phase 1 tasks
- [ ] Daily commits to feature branches
- [ ] Update task_tracking.md daily
- [ ] Create Pull Requests
- [ ] Sprint Review demo

---

## 10. OPEN QUESTIONS FOR LAURA (Meeting)

### HIGH PRIORITY QUESTIONS:

1. **Task Prioritization:**
   - "Which tasks are MUST-HAVE for launch vs. nice-to-have?"
   - "Is IIIF Viewer on /stanzas/ critical? (COMPLEX task)"

2. **Data Dependencies:**
   - "When will Carrie deliver final toponym dataset?"
   - "When will Laura Ingallinella's RAs finish variant data?"

3. **GitHub Issues:**
   - "Can you show me Issue #74? What's wrong with variant model?"
   - "Issue #73 - do you have a design mockup for variant display?"

4. **Content:**
   - "Is Introduction page content ready? (Task H1)"
   - "Can I get list of team members for About page? (Task C2)"

5. **Scope:**
   - "Which scenario fits your timeline and priorities? (A through E)"
   - "Prefer phased approach or full implementation?"

### MEDIUM PRIORITY QUESTIONS:

6. **Infrastructure:**
   - "When can I get SSH access to dev.lasfera.rrchnm.org?"
   - "GitHub collaborator access? (chnm/lasfera repo)"

7. **Testing:**
   - "Can you test on dev environment within 48h of deployment?"
   - "Do you have test users/scenarios prepared?"

8. **Timeline:**
   - "Absolute deadline? (June 2026 = end of academic year?)"
   - "Any milestones between now and then?"

### LOW PRIORITY QUESTIONS:

9. **Crowdsourcing:**
   - "Is Project 3 (Extensible Edition) in scope for this contract?"
   - "Or post-launch feature?"

10. **Hosting:**
    - "Will RRCHNM continue hosting or migrate elsewhere?"
    - "Do you need export/migration documentation?"

---

## SUMMARY

**Total Identified Tasks:** 53
- **SOFORT umsetzbar:** 8 tasks (SIMPLE to MEDIUM complexity)
- **Backend/DB:** 12 tasks (MEDIUM to COMPLEX)
- **Content-abhängig:** 18 tasks (Developer support needed)
- **Blocked/Future:** 15 tasks (nicht jetzt)

**RECOMMENDED START:** Phase 1 (Scenario B)
- 8 Quick Win tasks
- SIMPLE to MEDIUM complexity
- 3-4 Wochen
- LOW RISK, HIGH VALUE

**CRITICAL SUCCESS FACTORS:**
1. Meeting klärt Prioritäten
2. GitHub Issues werden gelesen
3. Data-Dependencies werden getracked
4. Iterative Sprints statt Big Bang

**NEXT IMMEDIATE ACTION:**
GitHub Issues lesen → Live-Site checken → Meeting Prep

---

**Version:** 1.0
**Nächstes Update:** Nach Meeting mit Laura
**Owner:** Christopher Pollin / DH Craft
