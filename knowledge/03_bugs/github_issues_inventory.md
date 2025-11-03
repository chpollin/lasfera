# La Sfera - GitHub Issues Inventory

**Repository:** https://github.com/chnm/lasfera
**Datum:** 3. November 2025
**Status:** PRE-RESEARCH (Issues noch nicht gelesen)

---

## ZWECK

Dieses Dokument trackt alle GitHub Issues die im Task Analysis Report erwähnt wurden.
Diese Issues müssen gelesen werden um vollständigen Kontext für Implementation zu bekommen.

---

## ISSUES REFERENCED IN TASK ANALYSIS

### Issue #22: Incorporate import_export for Datasets
**Source:** Project 3 (Extensible Edition), MEDIUM Priority
**Status:** [TBD - Issue noch nicht gelesen]
**Related Tasks:** Task L4 (8-12h estimated)

**Description (from Task Analysis):**
- Django-import-export integration
- CSV upload functionality for datasets
- Possibly alternative to custom management commands

**TO RESEARCH:**
- [ ] Read full issue description
- [ ] Check if still open or closed
- [ ] Identify acceptance criteria
- [ ] Check for existing implementation attempts
- [ ] Estimate effort required
- [ ] Decide: Priority vs. custom import commands?

**Notes:** [TBD after reading]

---

### Issue #51: Design User Roles for Contributions
**Source:** Project 3 (Extensible Edition), MEDIUM Priority
**Status:** [TBD]
**Related Tasks:** Task L2 (15-25h estimated)
**Dependencies:** Depends on Issue #60 (Crowdsourcing)

**Description (from Task Analysis):**
- User authentication/authorization design
- Role-based access control (RBAC)
- Contribution workflow permissions

**TO RESEARCH:**
- [ ] Read full issue
- [ ] Check if design document exists
- [ ] Identify roles needed (e.g., Admin, Editor, Contributor, Viewer)
- [ ] Check Django auth integration requirements
- [ ] Estimate implementation effort

**Notes:** [TBD]

---

### Issue #56: Add Historic Base Map to Gazetteer
**Source:** Project 6 (Geospatial Interface), LOW Priority
**Status:** BLOCKED (according to Task Analysis)
**Related Tasks:** Task K1 (5-10h if unblocked)

**Description (from Task Analysis):**
- Historic base map layer for Leaflet
- Currently blocked for unknown reason

**TO RESEARCH:**
- [ ] Read full issue
- [ ] Identify blocker reason (data unavailable? copyright? technical?)
- [ ] Check if blocker still valid
- [ ] Identify potential historic map sources (e.g., David Rumsey Collection, Old Maps Online)
- [ ] Estimate effort if unblocked

**Notes:** [TBD]

---

### Issue #60: Design Crowdsourcing Component
**Source:** Project 3 (Extensible Edition), MEDIUM Priority
**Status:** DESIGN PHASE
**Related Tasks:** Task L1 (20-40h estimated)

**Description (from Task Analysis):**
- Crowdsourced transcription/annotation system
- User contribution workflow
- Quality control mechanism

**TO RESEARCH:**
- [ ] Read full issue
- [ ] Check if design mockups exist
- [ ] Identify similar systems (e.g., FromThePage, Zooniverse patterns)
- [ ] Determine scope: Transcription only? Annotations? Both?
- [ ] Estimate full implementation effort

**Questions for Laura:**
- Is this in scope for current contract?
- Or post-launch feature?

**Notes:** [TBD]

---

### Issue #65: Write Documentation for Adding Gallery Images
**Source:** Project 2 (Limited Images), MEDIUM/HIGH Priority, Due: Oct 17, 2025 (overdue)
**Status:** [TBD]
**Related Tasks:** Task D1 (2-3h)

**Description (from Task Analysis):**
- Documentation task
- How to add new IIIF images to gallery

**TO RESEARCH:**
- [ ] Read full issue
- [ ] Check if partial documentation exists
- [ ] Identify target audience (developers? Laura's team? both?)
- [ ] Check current gallery functionality in code
- [ ] Draft documentation outline

**Notes:** [TBD]

---

### Issue #73: Finalize Design for Textual Variant Display
**Source:** Project 1 (Textual Variants), MEDIUM/HIGH Priority
**Status:** [TBD]
**Related Tasks:** Task F3 (8-15h)
**Dependencies:** Depends on Issue #74 (Data Model)

**Description (from Task Analysis):**
- UI/UX design for displaying textual variants
- Layout options: inline, side-by-side, tabbed?
- Highlighting differences between variants

**TO RESEARCH:**
- [ ] Read full issue
- [ ] Check for design mockups/wireframes
- [ ] Identify similar digital editions for inspiration (e.g., Digital Dante, Petrarchive)
- [ ] Check current template structure
- [ ] Estimate template/CSS work required

**Questions for Laura:**
- Do you have design preferences?
- Can you show examples from other editions you like?

**Notes:** [TBD]

---

### Issue #74: Revise Textual Variant Data Model
**Source:** Project 1 (Textual Variants), MEDIUM/HIGH Priority
**Status:** [TBD]
**Related Tasks:** Task F1 (8-15h)
**Owner (original):** Jason Heppler

**Description (from Task Analysis):**
- Current StanzaVariant model needs revision
- Unclear what's wrong with current model

**TO RESEARCH:**
- [ ] Read full issue description
- [ ] Review current manuscript/models.py StanzaVariant class
- [ ] Identify proposed changes
- [ ] Check for migration risks
- [ ] Estimate refactoring effort
- [ ] Check if existing data needs migration

**CRITICAL:** This blocks Issue #76 (importing) and Issue #73 (display)

**Questions for Laura/Jason:**
- What's the problem with current model?
- Do you have revised model specification?

**Notes:** [TBD]

---

### Issue #76: Handle Data Importing for Textual Variants
**Source:** Project 1 (Textual Variants), MEDIUM/HIGH Priority
**Status:** [TBD]
**Related Tasks:** Task F2 (10-20h)
**Dependencies:** BLOCKED BY Issue #74

**Description (from Task Analysis):**
- Import script for textual variant dataset
- Laura Ingallinella's RAs are creating data (Fall 2025/Winter 2026)
- Due: Feb 28, 2026

**TO RESEARCH:**
- [ ] Read full issue
- [ ] Check data format (CSV? Excel? JSON?)
- [ ] Identify validation requirements
- [ ] Review existing import commands in manuscript/management/commands/
- [ ] Draft import command structure

**Questions for Laura Ingallinella:**
- What format is your data in?
- Can you provide sample data?

**Notes:** [TBD]

---

## ISSUE CATEGORIES

### HIGH PRIORITY (Read First)
- Issue #74: Variant Data Model (blocks F1, F2, F3)
- Issue #73: Variant Display Design (blocks F3)
- Issue #76: Variant Import (blocks F2)
- Issue #65: Gallery Documentation (Task D1 ready to start)

### MEDIUM PRIORITY (Read if time permits)
- Issue #60: Crowdsourcing (determine if in scope)
- Issue #51: User Roles (depends on #60)
- Issue #22: import_export (alternative to custom commands)

### LOW PRIORITY (Read if relevant)
- Issue #56: Historic Base Map (blocked, low priority)

---

## RESEARCH TASKS (Sprint 0)

### Task 0.1.1: Clone/Update Repository
```bash
cd C:\Users\Chrisi\Documents\GitHub\Cloned\lasfera
git pull origin main
```

### Task 0.1.2: Read High Priority Issues (Estimated: 30-45 min)
- [ ] Issue #74 - Take detailed notes
- [ ] Issue #73 - Screenshot any mockups
- [ ] Issue #76 - Note data format requirements
- [ ] Issue #65 - Check existing docs

### Task 0.1.3: Read Medium Priority Issues (Estimated: 20-30 min)
- [ ] Issue #60 - Determine scope relevance
- [ ] Issue #51 - Note dependencies
- [ ] Issue #22 - Evaluate vs. custom commands

### Task 0.1.4: Document Findings (Estimated: 15-20 min)
- [ ] Fill in "Notes" sections above
- [ ] Update effort estimates if needed
- [ ] Add to "Questions for Laura" in meeting prep
- [ ] Update task_tracking.md with any new insights

**Total Estimated Time for Issue Research:** 1-1.5h

---

## ISSUE READING TEMPLATE

(Use this template when reading each issue)

### Issue #[NUMBER]: [TITLE]

**URL:** https://github.com/chnm/lasfera/issues/[NUMBER]
**Status:** [Open/Closed]
**Opened:** [Date]
**Last Updated:** [Date]
**Assigned:** [Person]
**Labels:** [Labels]

**Summary:**
[3-5 sentence summary of the issue]

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
- [...]

**Technical Details:**
- Files affected: [List]
- Dependencies: [List]
- Risks: [List]

**Comments Summary:**
- [Key points from discussion]

**Current Status:**
[What's been done, what's remaining]

**Implementation Notes:**
[Developer notes for implementation]

**Questions for Meeting:**
- [ ] Question 1
- [ ] Question 2

**Effort Estimate Update:**
- Original: [X]h
- Updated: [Y]h
- Justification: [Reason]

---

## FINDINGS SUMMARY

(Fill after reading all issues)

### Issues That Are Blockers:
- [TBD]

### Issues That Can Start Immediately:
- [TBD]

### Issues That Need Laura's Input:
- [TBD]

### Issues That Are Out of Scope:
- [TBD]

### Updated Effort Estimates:
- [TBD]

---

**Last Updated:** November 3, 2025
**Next Update:** After Sprint 0 Task 0.1 completion
**Owner:** Christopher Pollin / DH Craft
