# La Sfera - Task Status Tracker

**Projekt:** La Sfera Digital Edition
**Start:** TBD (nach Meeting mit Laura)
**Methodik:** 2-Week Sprints
**Letzte Aktualisierung:** 3. November 2025

---

## SPRINT OVERVIEW

| Sprint | Dates | Focus | Tasks | Effort | Status |
|--------|-------|-------|-------|--------|--------|
| Sprint 0 | Nov 3-10 | Pre-Work & Meeting | 3 tasks | 3-5h | IN PLANNING |
| Sprint 1 | TBD | Quick Wins Phase 1A | 4 tasks | 11-13h | PENDING |
| Sprint 2 | TBD | Quick Wins Phase 1B | 3 tasks | 7-12h | PENDING |
| Sprint 3 | TBD | IIIF Integration | 1 task | 20-30h | PENDING APPROVAL |
| Sprint 4+ | TBD | Backend Integration | TBD | TBD | PENDING APPROVAL |

---

## SPRINT 0: Pre-Work & Meeting (Nov 3-10, 2025)

**Goal:** Prepare for Laura meeting, gather information, make decisions

### Tasks

#### Task 0.1: GitHub Issues Research
**Owner:** Christopher
**Effort Estimate:** 1h
**Status:** NOT STARTED
**Description:** Read and document GitHub Issues #22, #51, #56, #60, #65, #73, #74, #76

**Subtasks:**
- [ ] Clone/pull latest from https://github.com/chnm/lasfera
- [ ] Read Issue #74: Textual variant data model revision
- [ ] Read Issue #76: Textual variant data importing
- [ ] Read Issue #73: Textual variant display design
- [ ] Read Issue #65: Gallery image documentation
- [ ] Read Issue #60: Crowdsourcing component design
- [ ] Read Issue #56: Historic base map (blocked)
- [ ] Read Issue #51: User roles for contributions
- [ ] Read Issue #22: import_export integration
- [ ] Document findings in `knowledge/03_bugs/github_issues_inventory.md`

**Deliverable:** `knowledge/03_bugs/github_issues_inventory.md`

---

#### Task 0.2: Live-Site Investigation
**Owner:** Christopher
**Effort Estimate:** 2h
**Status:** NOT STARTED
**Description:** Test live site for Task A2, A3, A1, C1 status

**Testing Checklist:**
- [ ] Navigate to https://lasfera.rrchnm.org/toponyms
- [ ] Click on map markers - check if links work (Task A2)
- [ ] Inspect popup content - note current format (Task A3)
- [ ] Check if /introduction/ exists (Task A1)
- [ ] Try /manuscripts/ URL for manuscript list (Task C1)
- [ ] Screenshot findings
- [ ] Browser console - check JavaScript errors
- [ ] Test on Chrome, Firefox, Safari (if available)

**Deliverable:** Screenshots + findings notes for meeting

---

#### Task 0.3: Meeting Preparation
**Owner:** Christopher
**Effort Estimate:** 2h
**Status:** NOT STARTED
**Description:** Prepare meeting agenda, slides, questions

**Subtasks:**
- [ ] Create meeting agenda document
- [ ] Prepare scenario comparisons (A-E)
- [ ] List open questions (see IMPLEMENTATION_ROADMAP.md section 10)
- [ ] Create visual task breakdown (Phases 1-4)
- [ ] Prepare screen-share demo plan
- [ ] Send agenda to Laura 24h before meeting

**Deliverable:** Meeting agenda + presentation materials

---

### Sprint 0 Retrospective
**Date:** After meeting
**Outcome:** [TBD - fill after meeting]
**Approved Scenario:** [TBD]
**Approved Budget:** [TBD]
**Start Date for Sprint 1:** [TBD]

---

## SPRINT 1: Quick Wins Phase 1A (Week 1-2)

**Goal:** High-confidence bug fixes and navigation improvements
**Prerequisites:** Meeting completed, Scenario B or higher approved
**Estimated Effort:** 11-13h

### Tasks

#### Task B1: Remove Urb1 Hardcoding (Bug #1)
**Source:** Bug Inventory, HIGH Priority
**Owner:** [TBD]
**Effort Estimate:** 4h
**Status:** READY TO START
**Branch:** `fix/urb1-hardcoding`

**Subtasks:**
- [ ] Create branch from main
- [ ] Add DEFAULT_MANUSCRIPT setting to config/settings.py
- [ ] Refactor manuscript/views.py:489 (mirador_view DoesNotExist)
- [ ] Refactor manuscript/views.py:492 (mirador_view no IIIF URL)
- [ ] Refactor manuscript/views.py:498 (mirador_view manifest error)
- [ ] Refactor manuscript/views.py:537 (stanzas default_manuscript)
- [ ] Refactor manuscript/views.py:694 (manuscripts default_manuscript)
- [ ] Add logging for all fallback scenarios
- [ ] Write unit test for fallback logic
- [ ] Test with Urb1, Cambridge, Yale manuscripts
- [ ] Create Pull Request
- [ ] Code review

**Actual Effort:** [TBD]
**Completion Date:** [TBD]
**Notes:** [TBD]

---

#### Task B2: Fix page_number Parameter (Bug #3)
**Source:** Bug Inventory, MEDIUM Priority
**Owner:** [TBD]
**Effort Estimate:** 4h
**Status:** READY TO START
**Branch:** `fix/mirador-page-number`

**Subtasks:**
- [ ] Create branch from main
- [ ] Modify manuscript/views.py:485-506 (mirador_view)
- [ ] Add canvas_id calculation from page_number
- [ ] Use existing get_manifest_data() function
- [ ] Add bounds checking (page 1 to max pages)
- [ ] Add error handling for invalid page_number
- [ ] Update template context (add canvas_id, page_number)
- [ ] Test with /manuscripts/1/mirador/42/
- [ ] Verify canvas opens at correct page
- [ ] Create Pull Request
- [ ] Code review

**Actual Effort:** [TBD]
**Completion Date:** [TBD]
**Notes:** [TBD]

---

#### Task A1: Add Introduction Button to Navigation
**Source:** Project 4, HIGH Priority (overdue Oct 17)
**Owner:** [TBD]
**Effort Estimate:** 1-2h
**Status:** PENDING (check if content exists)
**Branch:** `feature/introduction-nav`

**Prerequisites:**
- [ ] Verify /introduction/ page exists (Wagtail CMS check)
- [ ] If not exists: Ask Laura for content or create placeholder

**Subtasks:**
- [ ] Locate navigation template (base.html or Wagtail menu)
- [ ] Add "Introduction" link
- [ ] Verify link works
- [ ] Check responsive design (mobile menu)
- [ ] Test cross-browser
- [ ] Create Pull Request

**Actual Effort:** [TBD]
**Completion Date:** [TBD]
**Notes:** [TBD]

---

#### Task D1: Write Gallery Image Documentation
**Source:** Project 2, MEDIUM/HIGH Priority (overdue Oct 17)
**Owner:** [TBD]
**Effort Estimate:** 2-3h
**Status:** READY TO START
**Branch:** `docs/gallery-images`

**Subtasks:**
- [ ] Research current gallery functionality (code review)
- [ ] Document IIIF manifest integration process
- [ ] Write step-by-step guide for adding new images
- [ ] Include example manifest URLs
- [ ] Document rights/DRM requirements
- [ ] Add troubleshooting section
- [ ] Create docs/gallery_images.md
- [ ] Update README.md with link to docs
- [ ] Create Pull Request

**Actual Effort:** [TBD]
**Completion Date:** [TBD]
**Notes:** [TBD]

---

### Sprint 1 Metrics
**Planned Effort:** 11-13h
**Actual Effort:** [TBD]
**Velocity:** [TBD] (Actual/Planned)
**Completed Tasks:** [TBD] / 4
**Blockers Encountered:** [TBD]

### Sprint 1 Retrospective
**Date:** [TBD]
**What went well:** [TBD]
**What to improve:** [TBD]
**Action items:** [TBD]

---

## SPRINT 2: Quick Wins Phase 1B (Week 3-4)

**Goal:** Gazetteer improvements and manuscript list revival
**Prerequisites:** Sprint 1 completed and reviewed
**Estimated Effort:** 7-12h

### Tasks

#### Task A2: Fix Broken Links in Gazetteer Map
**Source:** Project 6, HIGH Priority
**Owner:** [TBD]
**Effort Estimate:** 2-3h
**Status:** PENDING (needs investigation)
**Branch:** `fix/gazetteer-links`

**Investigation:**
- [ ] Reproduce broken link issue on live site
- [ ] Check Leaflet popup HTML generation
- [ ] Verify ToponymViewSet API returns correct URLs
- [ ] Check toponym.get_absolute_url() method

**Subtasks:**
- [ ] [TBD - after investigation]

**Actual Effort:** [TBD]
**Completion Date:** [TBD]
**Notes:** [TBD]

---

#### Task A3: Improve Gazetteer Popup Format
**Source:** Project 6, HIGH Priority
**Owner:** [TBD]
**Effort Estimate:** 2-4h
**Status:** PENDING (needs Laura input on design)
**Branch:** `feature/gazetteer-popup-format`

**Prerequisites:**
- [ ] Laura confirms which fields to show in popup
- [ ] Design approved

**Subtasks:**
- [ ] [TBD - after design approval]

**Actual Effort:** [TBD]
**Completion Date:** [TBD]
**Notes:** [TBD]

---

#### Task C1: Revive Manuscript List Page
**Source:** Project 5, MEDIUM Priority
**Owner:** [TBD]
**Effort Estimate:** 3-5h
**Status:** PENDING (needs git history research)
**Branch:** `feature/manuscript-list`

**Investigation:**
- [ ] Search git history for deleted manuscript_list files
- [ ] Check if route /manuscripts/ exists
- [ ] Verify SingleManuscript.objects.count() == 160

**Subtasks:**
- [ ] [TBD - after investigation]

**Actual Effort:** [TBD]
**Completion Date:** [TBD]
**Notes:** [TBD]

---

### Sprint 2 Metrics
**Planned Effort:** 7-12h
**Actual Effort:** [TBD]
**Velocity:** [TBD]
**Completed Tasks:** [TBD] / 3
**Blockers Encountered:** [TBD]

### Sprint 2 Retrospective
**Date:** [TBD]
**What went well:** [TBD]
**What to improve:** [TBD]
**Action items:** [TBD]

---

## SPRINT 3: IIIF Integration (Week 5-8) - PENDING APPROVAL

**Goal:** Fix IIIF Viewer rendering on /stanzas/
**Prerequisites:** Scenario C or higher approved by Laura
**Estimated Effort:** 20-30h

**Status:** AWAITING APPROVAL
**Approval Needed From:** Laura Morreale
**Budget Impact:** +7.950€ (vs. Scenario B)

### Tasks

#### Task E1: Add IIIF Viewer to /stanzas/ (Bug #2)
**Source:** Bug Inventory + Project 2, HIGH Priority
**Owner:** [TBD]
**Effort Estimate:** 20-30h
**Status:** PENDING APPROVAL
**Branch:** `fix/stanzas-iiif-viewer`

**Phases:**

**Phase 1: Investigation (3-5h)**
- [ ] Read templates/manuscript/stanzas.html line 265-290
- [ ] Check static/js/tify-sync.js exists and content
- [ ] Browser DevTools: Why Tify doesn't initialize?
- [ ] Check AlpineJS x-data="tifyViewer" definition
- [ ] Check has_known_folios variable propagation
- [ ] Check IIIF URL availability in template context

**Phase 2: Fix JavaScript (3-5h)**
- [ ] Fix Tify initialization errors
- [ ] Ensure Tify CDN loads correctly
- [ ] Debug tify-sync.js script
- [ ] Test basic viewer rendering

**Phase 3: Canvas Synchronization (8-12h)**
- [ ] Calculate canvas_id from stanza line_code
- [ ] Implement scroll-to-canvas on stanza click
- [ ] Implement stanza highlight on canvas change
- [ ] Test bidirectional sync

**Phase 4: Testing (3-5h)**
- [ ] Test with Urb1 manuscript
- [ ] Test with Cambridge manuscript
- [ ] Test with manuscripts without IIIF
- [ ] Cross-browser testing
- [ ] Performance profiling

**Phase 5: Polish (2-3h)**
- [ ] Code review
- [ ] Documentation
- [ ] Create Pull Request

**Actual Effort:** [TBD]
**Completion Date:** [TBD]
**Notes:** [TBD]

---

### Sprint 3 Metrics
**Planned Effort:** 20-30h
**Actual Effort:** [TBD]
**Velocity:** [TBD]
**Completed Tasks:** [TBD] / 1
**Blockers Encountered:** [TBD]

### Sprint 3 Retrospective
**Date:** [TBD]
**What went well:** [TBD]
**What to improve:** [TBD]
**Action items:** [TBD]

---

## SPRINT 4+: Backend Integration - PENDING APPROVAL

**Status:** AWAITING DATA & APPROVAL
**Prerequisites:**
- Carrie Benes delivers final toponym dataset
- Laura Ingallinella provides variant data samples
- Scenario D approved by Laura

**Estimated Tasks:**
- Task F4: Toponym bidirectional links (6-10h)
- Task F5: Annotation toponym links (8-15h)
- Task F1: Variant data model revision (8-15h)
- Task F2: Variant data importing (10-20h)
- Task F3: Variant display (8-15h)
- [More tasks TBD based on approval]

**Total Estimate:** 40-75h (minimum)
**Budget Impact:** +21.600€ - 39.750€

**Approval Status:** NOT APPROVED
**Data Status:** NOT DELIVERED

---

## BACKLOG (Not Scheduled)

### High Priority (Waiting for Dependencies)
- Task E2: MSS IIIF Integration (15-25h) - NEEDS CLARIFICATION
- Task H3: Import revised page-by-page text (2-3h) - NEEDS CONTENT
- Task I1: Import final toponym dataset (2-3h) - NEEDS DATA

### Medium Priority (Future Enhancements)
- Task B3: Logging enhancement (2-3h)
- Task C2: Update About page (1-2h) - NEEDS CONTENT
- Task I2: Variant display criteria implementation (3-5h) - NEEDS DECISION
- Task G1: WHG data model (10-15h) - IN PROGRESS (Carrie)
- Task G2: WHG export script (2-3h) - BLOCKED BY G1
- Task G3: WHG links in templates (2-3h) - BLOCKED BY G2

### Low Priority / Blocked
- Task K1: Historic base map (5-10h) - BLOCKED
- Task K2: Full image gallery (TBD) - BLOCKED
- Task L1: Crowdsourcing component (20-40h) - DESIGN PHASE
- Task L2: User roles (15-25h) - DESIGN PHASE
- Task L3: Manuscript placement flowchart (3-5h) - PLANNING
- Task L4: import_export integration (8-12h) - LOW PRIORITY

### Content Team Tasks (Not Developer Work)
- Task H1: Build Introduction page - Laura Morreale
- Task H2: Improve landing page text - Laura Morreale
- Task H4: Teaching materials - Laura Morreale
- Task H5: Fill variant dataset - Laura Ingallinella
- Task I3: Choose DRM-free images - Laura Morreale
- Task J1: Domain reassignment - Jason Heppler
- Task J2: White paper - Amanda G Madden

---

## OVERALL PROJECT METRICS

### Completion Status
**Phase 1 (Quick Wins):**
- Planned: 8 tasks
- Completed: 0 / 8
- In Progress: 0 / 8
- Blocked: 0 / 8

**Phase 2 (Backend/DB):**
- Planned: 10 tasks
- Completed: 0 / 10
- In Progress: 0 / 10
- Blocked: TBD

**Phase 3 (Content Support):**
- Planned: 5 developer-support tasks
- Completed: 0 / 5
- Waiting for content: 5 / 5

### Time Tracking
**Total Estimated (Approved Scope):** 0h (no approval yet)
**Total Actual:** 0h
**Variance:** 0h
**Budget Status:** 0€ / 0€ (no budget approved)

### Velocity Tracking
**Sprint 0:** [TBD] h/week
**Sprint 1:** [TBD] h/week
**Sprint 2:** [TBD] h/week
**Average Velocity:** [TBD] h/week

---

## BLOCKERS & DEPENDENCIES LOG

| Date | Blocker | Impact | Tasks Affected | Resolution | Status |
|------|---------|--------|----------------|------------|--------|
| Nov 3 | Meeting not yet held | Cannot start | ALL | Schedule meeting | OPEN |
| [TBD] | [Future blockers] | [TBD] | [TBD] | [TBD] | [TBD] |

---

## NOTES & LEARNINGS

### Date: Nov 3, 2025
**Note:** Pre-work phase started. Awaiting meeting with Laura for approval and prioritization.

### [Future dates]
[Add learnings, discoveries, important decisions here]

---

**Last Updated:** November 3, 2025
**Next Review:** After Sprint 0 completion (post-meeting)
**Owner:** Christopher Pollin / DH Craft
