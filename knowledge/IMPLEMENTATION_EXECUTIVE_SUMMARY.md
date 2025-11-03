# La Sfera Implementation - Executive Summary

**Datum:** 3. November 2025
**Projekt:** La Sfera Digital Edition
**Client:** Laura Morreale, RRCHNM
**Developer:** Christopher Pollin, DH Craft

---

## TL;DR - Was du wissen musst

**URSPRÜNGLICHE ANNAHME:** 3 Bugs fixen, 3.510€
**TATSÄCHLICHES SCOPE:** 53 Tasks identifiziert, 35.700€ - 59.250€

**Das ist 10-17x mehr als ursprünglich gedacht!**

---

## Die Situation

### Was wir dachten (Bug-Only Analysis):
- 3 verifizierte Bugs in der Codebase
- 18 Stunden Entwicklung
- 3.510€ Kosten
- 3 Wochen Timeline

### Was das Task Analysis Document zeigt:
- **53 identifizierte Tasks** aus Meeting Notes
- **238-395 Stunden** Entwicklung (Full Scope)
- **35.700€ - 59.250€** Kosten
- **20-30 Wochen** Timeline

---

## Task Breakdown (53 Tasks total)

### SOFORT umsetzbar (8 Tasks):
- Navigation Fixes (Introduction Button, Links)
- Bug-Fixes (Urb1 Hardcoding, page_number)
- Gazetteer UI Improvements (Popups, Links)
- Documentation (Gallery Images)
- **Aufwand:** 20-27h
- **Kosten:** 4.650€ - 6.300€

### Braucht Backend/DB (12 Tasks):
- IIIF Viewer Integration (Bug #2 - 20-30h!)
- Textual Variant System (Data Model, Import, Display)
- Toponym Bidirectional Links
- WHG Integration (World Historical Gazetteer)
- **Aufwand:** 89-151h
- **Kosten:** 20.700€ - 35.100€

### Braucht Content von Laura/Carrie (18 Tasks):
- Introduction Page Content
- Page-by-Page Text Updates
- Textual Variant Dataset (Laura Ingallinella, due Feb 28, 2026)
- Final Toponym Dataset (Carrie Benes)
- **Developer Support:** 10-20h
- **Kosten:** 2.250€ - 4.650€

### Blocked/Low Priority (15 Tasks):
- Historic Base Map (blocked)
- Full Image Gallery (blocked - rights clearance)
- Crowdsourcing Component (design phase)
- User Roles System (future feature)

---

## Empfohlene Strategie: PHASENWEISE

### Phase 1: Quick Wins (SOFORT startbar)
**Was:** 8 Tasks ohne Dependencies
**Aufwand:** 31-42h (mit Overhead)
**Kosten:** 4.650€ - 6.300€
**Timeline:** 3-4 Wochen
**Risiko:** NIEDRIG

**Enthält:**
- Alle 3 Bugs aus Bug Inventory
- Navigation Improvements
- Gazetteer UI Fixes
- Manuscript List Revival
- Documentation

**Nicht enthält:**
- IIIF Viewer (das ist Phase 2)

---

### Phase 2: IIIF Integration (KOMPLEX)
**Was:** IIIF Viewer auf /stanzas/ (Bug #2)
**Aufwand:** 54-85h (mit Overhead)
**Kosten:** 8.100€ - 12.750€
**Timeline:** 4-6 Wochen
**Risiko:** MITTEL (JavaScript-Debugging)

**Nur starten wenn:**
- Laura bestätigt dass Feature gewünscht
- Phase 1 erfolgreich abgeschlossen
- Budget vorhanden

---

### Phase 3: Backend Integration (GRÖßTE KOMPONENTE)
**Was:** Textual Variants, Toponym Links, WHG
**Aufwand:** 138-234h (mit Overhead)
**Kosten:** 20.700€ - 35.100€
**Timeline:** 10-15 Wochen
**Risiko:** HOCH (Data Dependencies!)

**BLOCKED BY:**
- Carrie's final toponym dataset (kein Lieferdatum)
- Laura I's variant data (Feb 28, 2026)
- GitHub Issue #74 Clarification (Data Model)

**Kann NICHT starten ohne Daten!**

---

### Phase 4: Content Support
**Was:** Developer-Support für Content-Team
**Aufwand:** 15-31h (nur wenn Content geliefert)
**Kosten:** 2.250€ - 4.650€
**Timeline:** Abhängig von Laura/Carrie

---

## Budget-Szenarien im Vergleich

| Szenario | Scope | Kosten | Timeline | Risk |
|----------|-------|--------|----------|------|
| **BUG-ONLY** | 3 Bugs | 3.510€ | 3 Wochen | ✅ LOW |
| **PHASE 1** | 8 Quick Wins | 6.300€ | 4 Wochen | ✅ LOW |
| **PHASE 1+2** | + IIIF | 19.050€ | 10 Wochen | ⚠️ MEDIUM |
| **PHASE 1+2+3** | + Backend | 54.150€ | 25 Wochen | ❌ HIGH |
| **FULL SCOPE** | Alle 4 Phasen | 59.250€ | 30 Wochen | ❌ VERY HIGH |

---

## EMPFEHLUNG

### Was JETZT tun?

**OPTION A: Conservative (EMPFOHLEN)**
```
START: Bug-Only (3.510€, 3 Wochen)
→ Alle 3 Bugs gefixt
→ DANN Laura entscheidet: Weitermachen oder stoppen?
```

**OPTION B: Ambitious**
```
START: Phase 1 Quick Wins (6.300€, 4 Wochen)
→ 8 Tasks statt nur 3 Bugs
→ Mehr Value, aber auch mehr Aufwand
→ DANN Review und Phase 2 Entscheidung
```

**OPTION C: Full Commitment (NICHT empfohlen)**
```
START: Full Scope (59.250€, 30 Wochen)
→ ZU VIELE Unbekannte
→ Daten-Dependencies unklar
→ Hohes Risiko ohne Proof-of-Concept
```

---

## Kritische Dependencies

### 1. GitHub Issues (MUST READ vor Start)
**8 referenzierte Issues:**
- #74: Variant Data Model (blocks F1, F2, F3)
- #76: Variant Import (blocks F2)
- #73: Variant Display (blocks F3)
- #65: Gallery Docs (ready to start)
- #60: Crowdsourcing (scope clarification needed)
- #51: User Roles (depends on #60)
- #22: import_export (priority decision)
- #56: Historic Base Map (blocked)

**Action:** Read ALL issues in Sprint 0 (1h)

---

### 2. Data Delivery (BLOCKING Phase 3)
**Needed from:**
- **Carrie Benes:** Final toponym dataset (no date specified!)
- **Laura Ingallinella:** Textual variant data (due Feb 28, 2026)

**Risk:** Phase 3 kann NICHT starten ohne diese Daten!

---

### 3. Design Decisions (BLOCKING mehrere Tasks)
**Laura must decide:**
- IIIF Viewer Layout (Side-by-side? Tabs?)
- Textual Variant Display (Inline? Side-by-side?)
- Gazetteer Popup Format (Which fields to show?)
- Crowdsourcing in Scope? (Or post-launch?)

**Action:** Prepare mockups/examples for Meeting

---

## Next Steps (Konkret)

### PRE-MEETING (JETZT - 3-5h):

**1. GitHub Issues lesen (1h)**
```bash
cd C:\Users\Chrisi\Documents\GitHub\Cloned\lasfera
git pull
# Read Issues #22, #51, #56, #60, #65, #73, #74, #76
# Document in knowledge/03_bugs/github_issues_inventory.md
```

**2. Live-Site Investigation (2h)**
- Test Gazetteer links (Task A2)
- Inspect popup format (Task A3)
- Check if /introduction/ exists (Task A1)
- Check /manuscripts/ for list (Task C1)
- Screenshot findings

**3. Meeting Prep (2h)**
- Create presentation with 5 Scenarios
- Prepare questions (see IMPLEMENTATION_ROADMAP.md Section 10)
- Send agenda to Laura

---

### MEETING (45-60 min):

**Agenda:**
1. **Task Prioritization (20 min)**
   - Present Phase 1-4 breakdown
   - Laura chooses scenario (A-E)

2. **Data Dependencies (15 min)**
   - Carrie's timeline?
   - Laura I's timeline?
   - Content delivery schedule?

3. **GitHub Issues Review (10 min)**
   - Clarify #74, #73, #60
   - Show design examples

4. **Budget & Timeline (10 min)**
   - Agree on scenario
   - Payment milestones
   - Start date

---

### POST-MEETING (IF APPROVED):

**Sprint 1 (Week 1-2): Bug Fixes**
- Task B1: Urb1 Hardcoding (4h)
- Task B2: page_number Fix (4h)
- Task A1: Introduction Button (1-2h)
- Task D1: Gallery Docs (2-3h)
→ Pull Request #1

**Sprint 2 (Week 3-4): Gazetteer + Manuscript List**
- Task A2: Fix Links (2-3h)
- Task A3: Improve Popups (2-4h)
- Task C1: Manuscript List (3-5h)
→ Pull Request #2

**Sprint 3+ (IF APPROVED):**
- Task E1: IIIF Viewer (20-30h)
- Then Phase 3 tasks (when data ready)

---

## Risk Assessment

### HIGH RISK (Could Delay/Block Project):

**1. Data Delivery Delays**
- **Impact:** Phase 3 blockiert (35k€ scope)
- **Mitigation:** Work on Phase 1+2 while waiting

**2. IIIF Complexity Underestimated**
- **Impact:** 20-30h → 40-50h (Budget-Überschreitung)
- **Mitigation:** Time-box to 30h, then re-scope

**3. GitHub Issues Hide Major Requirements**
- **Impact:** Mehr Arbeit als geschätzt
- **Mitigation:** Read ALL issues before committing

### MEDIUM RISK:

**4. Content Team Availability**
- **Impact:** Slow review cycles
- **Mitigation:** 48h SLA agreement

**5. Wagtail CMS vs. Static Templates**
- **Impact:** Content updates komplexer
- **Mitigation:** Check early in Sprint 1

### LOW RISK:

**6. Deployment Access**
- **Impact:** Testing delayed
- **Mitigation:** Local dev works fine

---

## Key Learnings (from Knowledge Vault)

### Lektion 1: Code-Analyse ≠ Live-Site
Bug #2 wurde als "nicht existent" eingestuft (Code-Analyse), aber Live-Tests zeigten: Viewer rendert NICHT (JavaScript-Problem).
**Impact:** +8h, +1.200€

### Lektion 2: Meeting Notes >> Bug-Liste
v1.0-v3.0: 3 Bugs (3.510€)
v4.0 Task Analysis: 53 Tasks (59.250€)
**Faktor:** 17x Unterschied!

### Lektion 3: Data Dependencies blockieren
Phase 3 braucht Carrie's + Laura I's Daten (Feb 2026).
Developer kann NICHT vorarbeiten!

---

## Entscheidungs-Matrix

**WAS LAURA FRAGEN MUSS:**

### Budget-Frage:
- [ ] 3.510€ (Bug-Only) - Minimal
- [ ] 6.300€ (Phase 1) - Quick Wins
- [ ] 19.050€ (Phase 1+2) - Mit IIIF
- [ ] 54.150€ (Phase 1+2+3) - Full Backend
- [ ] 59.250€ (All Phases) - Complete

### Timeline-Frage:
- [ ] Juni 2026 Deadline hard oder soft?
- [ ] Milestones zwischen jetzt und Juni?

### Scope-Frage:
- [ ] IIIF Viewer MUST-HAVE oder NICE-TO-HAVE?
- [ ] Textual Variants MUST-HAVE (for launch)?
- [ ] Crowdsourcing in Scope (Project 3)?

### Data-Frage:
- [ ] Wann liefert Carrie finale Toponyme?
- [ ] Wann liefert Laura I Variants? (Feb confirmed?)

---

## Success Criteria

### Phase 1 Success:
- [ ] Alle 3 Bugs gefixt
- [ ] Introduction Button added
- [ ] Gazetteer UI improved
- [ ] Manuscript List restored
- [ ] Documentation written
- [ ] Laura can test on dev.lasfera.rrchnm.org
- [ ] Zero JavaScript errors in console

### Phase 2 Success:
- [ ] IIIF Viewer renders on /stanzas/
- [ ] Canvas sync with text works
- [ ] Cross-browser tested (Chrome, Firefox, Safari)
- [ ] Performance acceptable (< 3s load)

### Phase 3 Success:
- [ ] Textual variants display correctly
- [ ] Toponym links bidirectional
- [ ] WHG integration working
- [ ] Data imported successfully

---

## Was ist NICHT included (in allen Szenarien)

- ❌ Neue Features (außer gelistete)
- ❌ Mirador Alpha → Stable Upgrade
- ❌ Django/Wagtail Dependency Updates
- ❌ Comprehensive Test Suite (nur Task-spezifische Tests)
- ❌ CI/CD Pipeline
- ❌ Hosting Migration
- ❌ Content Creation (Laura's Team)
- ❌ IIIF Manifeste erstellen
- ❌ Historic Base Map (blocked)
- ❌ Full Image Gallery (blocked)

---

## Zahlungsmodalitäten (Vorschlag)

### Option 1: Milestone-basiert (EMPFOHLEN)
```
Phase 1 Start:          50% (3.150€)
Phase 1 Complete:       50% (3.150€)
─────────────────────────────────
Phase 1 Total:               6.300€

IF Phase 2 approved:
Phase 2 Start:          50% (6.375€)
Phase 2 Complete:       50% (6.375€)
─────────────────────────────────
Phase 2 Total:              12.750€

[etc.]
```

### Option 2: Time & Materials
```
Monatliche Abrechnung nach Stunden
Stundennachweis per Toggl
150€/h
```

---

## Timeline Overview

```
NOVEMBER 2025
─────────────────────────────────────────
Week 1 (Nov 3-9):   Pre-Work, Meeting
Week 2 (Nov 10-16): Sprint 1 Start (if approved)
Week 3 (Nov 17-23): Sprint 1 Continue
Week 4 (Nov 24-30): Sprint 2 Start

DECEMBER 2025
─────────────────────────────────────────
Week 1-2:           Sprint 2 Complete
                    → Phase 1 DONE (6.300€)

Week 3-4:           Sprint 3 (IIIF) - if approved
                    → Phase 2 START

JANUARY - MARCH 2026
─────────────────────────────────────────
                    Phase 2 + 3 (if approved)
                    Waiting for Data Delivery

APRIL - MAY 2026
─────────────────────────────────────────
                    Final Testing
                    UAT with Laura
                    Deployment

JUNE 2026
─────────────────────────────────────────
                    LAUNCH (Deadline)
```

---

## Contacts & Resources

**Client:**
- Laura Morreale: lmorreale3@gmail.com
- Carrie Benes (Geospatial)
- Laura Ingallinella (Textual Variants)
- Jason Heppler (Original Developer, RRCHNM)

**Developer:**
- Christopher Pollin: christopher.pollin@dhcraft.org

**Resources:**
- Live Site: https://lasfera.rrchnm.org/
- Dev Site: https://dev.lasfera.rrchnm.org/
- GitHub: https://github.com/chnm/lasfera
- DB Docs: https://dbdocs.io/hepplerj/lasfera

**Documentation:**
- [Full Implementation Roadmap](IMPLEMENTATION_ROADMAP.md)
- [Task Tracking](07_implementation/task_tracking.md)
- [Bug Inventory](03_bugs/bug_inventory.md)
- [Cost Estimate](05_deliverables/cost_estimate.md)

---

## FINAL RECOMMENDATION

**START WITH:** Phase 1 (6.300€, 4 weeks)

**WARUM:**
✅ LOW RISK (keine Data-Dependencies)
✅ HIGH VALUE (8 Tasks statt 3 Bugs)
✅ FAST DELIVERY (4 Wochen)
✅ PROOF-OF-CONCEPT (Laura kann Qualität beurteilen)
✅ FLEXIBEL (Kann nach Phase 1 stoppen oder weitermachen)

**DANN:**
→ Sprint Review nach 4 Wochen
→ Laura entscheidet: Phase 2? Phase 3? Stop?
→ Iterativ statt Big Bang

**AVOID:**
❌ Full Scope Commitment (59k€) ohne Proof
❌ Phase 3 Start ohne Daten
❌ IIIF Integration ohne Laura's Bestätigung

---

**Version:** 1.0
**Erstellt:** 3. November 2025
**Basis:** IMPLEMENTATION_ROADMAP.md + Task Analysis Report
**Für:** Meeting mit Laura Morreale
