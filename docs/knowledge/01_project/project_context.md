# La Sfera Project Context

**Project Name:** La Sfera Digital Edition
**Client:** Roy Rosenzweig Center for History and New Media (RRCHNM)
**Developer:** Digital Humanities Craft OG
**Analysis Period:** October 27-28, 2025
**Meeting Scheduled:** November 3 or 11, 2025 at 17:00 CET

---

## What is La Sfera?

La Sfera is a digital edition of a 15th-century Italian geographical text about the known world at that time. The project presents manuscript variations across multiple historical sources with IIIF-based image viewing capabilities.

### Historical Context
- **Text:** Italian geographical/cosmological poem
- **Period:** 15th century
- **Content:** Description of the known world, cities, regions, cosmology
- **Format:** Hierarchical line code system (Book.Stanza.Line - e.g., "01.01.01")

### Digital Edition Features
- **Manuscript Comparison:** Side-by-side viewing of textual variants
- **IIIF Integration:** High-resolution manuscript images via Mirador viewer
- **Translation Support:** English translations alongside original Italian
- **Geographic Data:** Interactive map (Gazetteer) with ~80 toponyms
- **Scholarly Apparatus:** Annotations, editorial notes, references

---

## Client: RRCHNM

**Organization:** Roy Rosenzweig Center for History and New Media
**Institution:** George Mason University, Virginia, USA
**Website:** https://rrchnm.org

**Contact Person:**
- **Name:** Laura (Project Lead)
- **Role:** Coordinator for La Sfera Digital Edition
- **Communication:** Email (meeting request sent Oct 28, 2025)

**RRCHNM Expertise:**
- Digital humanities projects
- Historical databases
- Open-source scholarly tools
- Academic web publishing

---

## Project Timeline

### Historical Development
- **Repository Created:** Early 2024 (estimated)
- **Django Version:** 5.0.2 (released January 2024)
- **Live Site Launch:** 2024 (exact date unknown)
- **Current Status:** Production site live at https://lasfera.rrchnm.org

### Analysis & Fix Timeline

**October 27, 2025:**
- Initial code repository cloning
- First complete code review
- Database schema analysis

**October 28, 2025:**
- Live site testing on https://lasfera.rrchnm.org
- Bug verification through browser tests
- Cost estimation completed
- Email to Laura drafted
- Meeting request sent

**November 3 or 11, 2025 (Planned):**
- 45-minute meeting with Laura
- Bug demonstration (before/after)
- Budget discussion (€3.9k - €10.2k)
- Timeline agreement (2-5 weeks)
- Development credentials exchange

**Mid-November 2025 (IF Approved):**
- Development start
- Pull requests creation
- Staging deployment
- Laura testing

**Late November - Early December 2025 (IF Approved):**
- Production deployment
- Monitoring & bug fixes
- Final invoice

---

## Project Goals

### Original Goals (RRCHNM)
1. Provide open-access digital edition of historical text
2. Enable scholarly comparison of manuscript variants
3. Integrate high-quality IIIF manuscript images
4. Support multilingual access (Italian + English)
5. Present geographic context through interactive map

### Our Analysis Goals
1. Identify technical bugs preventing full functionality
2. Provide accurate cost estimates for fixes
3. Minimize development time through targeted fixes
4. Maintain backward compatibility with existing data
5. Ensure production-ready, tested code

---

## Scope of Our Work

### In Scope
✅ **Code Analysis:**
- Complete review of manuscript/views.py (700 lines)
- Database schema understanding (14 models)
- IIIF integration verification
- Live site behavior testing

✅ **Bug Fixes:**
- BUG #1: Urb1 hardcoding (5 locations)
- BUG #3: page_number parameter (1 function)
- Static code verification (8 automated checks)

✅ **Documentation:**
- Technical analysis reports
- Budget scenarios (3 options)
- Meeting preparation materials
- Testing guides

### Out of Scope
❌ **Data Work:**
- Adding missing IIIF manifests to database
- Contacting institutions for manifest URLs
- Data migration or bulk updates

❌ **Infrastructure:**
- Server configuration changes
- Docker setup modifications
- PostgreSQL tuning

❌ **Feature Development:**
- New functionality beyond bug fixes
- UI/UX improvements
- Performance optimizations (unless bug-related)

### Conditional Scope
⚠️ **BUG #2 Investigation:**
- JavaScript debugging (IF Laura prioritizes this)
- IIIF viewer integration on /stanzas/ page
- Estimated 18-20 hours additional work

---

## Stakeholders

### Primary Stakeholder
**Laura (RRCHNM Project Lead)**
- Decides on budget approval
- Prioritizes which bugs to fix
- Provides development credentials
- Tests deployed fixes
- Represents end-user needs

### Secondary Stakeholders
**RRCHNM Researchers:**
- Use the site for scholarly work
- Expect reliable manuscript access
- Need working IIIF viewer for image analysis

**General Public:**
- Open-access users
- History/geography enthusiasts
- Students researching medieval geography

### Developer (Us)
**Digital Humanities Craft OG:**
- Delivers bug-free code
- Maintains professional communication
- Provides accurate estimates
- Documents all work thoroughly

---

## Success Criteria

### For RRCHNM
✅ All 6 manuscripts accessible (not just Urb1)
✅ Page navigation works (direct links to specific pages)
✅ IIIF viewer displays manuscript images
✅ No 404/500 errors on critical pages
✅ Code is maintainable for future work

### For Us
✅ Meeting demonstrates clear value (bug fixes)
✅ Budget approved for at least minimum scope (€3.9k)
✅ Deployment completed within agreed timeline
✅ Laura satisfied with professionalism
✅ Invoice paid without issues
✅ Potential for future collaboration

---

## Risk Factors

### Technical Risks
⚠️ **BUG #2 (IIIF Viewer):**
- Root cause still unclear (JavaScript issue)
- May require extensive debugging (18-20h)
- Could uncover additional problems

⚠️ **Runtime Testing:**
- No production data available in repository (_data/ is gitignored)
- Requires Laura to provide PostgreSQL dump
- Testing may reveal issues not caught by static analysis

⚠️ **Deployment:**
- No access to production server yet
- Docker/Poetry configuration may differ from dev
- Potential for environment-specific bugs

### Business Risks
⚠️ **Budget Approval:**
- Laura may have limited funding
- €10.2k (Scenario B) might be too high
- May need to negotiate pay-per-bug approach

⚠️ **Timeline Pressure:**
- June 2026 deadline mentioned in GitHub issues
- Plenty of time, but dependencies could delay

⚠️ **Communication:**
- Meeting needs to clearly demonstrate value
- Laura must understand technical vs. data issues
- Misaligned expectations could derail project

---

## Current Project Status

### Live Site
**URL:** https://lasfera.rrchnm.org
**Status:** PRODUCTION, publicly accessible
**Verified Working:**
- ✅ Urb1 (Vatican manuscript)
- ✅ Cam (Harvard manuscript)
- ✅ Gazetteer map with ~80 toponyms
- ✅ API endpoints (/api/manuscripts/, /api/toponyms/)
- ✅ English translations display

**Verified NOT Working:**
- ❌ IIIF viewer on /stanzas/ (BUG #2)
- ❌ Page navigation in Mirador (BUG #3 - fixed in code)
- ⚠️ Yale3, Laur2, Laur3, Laur6 (unknown IIIF status)

### Codebase
**Repository:** https://github.com/chnm/lasfera
**Branch:** main
**Last Commit (at analysis):** c8f4641 (October 2024)
**Our Commits:** c0179f2, 12a84b1, 326ff20 (bug fixes)

**Technology Stack:**
- Django 5.0.2 (Python 3.11)
- PostgreSQL 16
- Wagtail 6.2.1 (CMS)
- Mirador 4.0.0-alpha.2 (IIIF viewer)
- Tailwind CSS 3.4.16

**Code Quality:**
- ✅ Follows Django best practices
- ✅ Uses ORM (no raw SQL)
- ✅ CSRF protection enabled
- ✅ Logging implemented
- ⚠️ Mirador using alpha version (not stable)

### Database
**Platform:** PostgreSQL 16
**Schema Documentation:** https://dbdocs.io/hepplerj/lasfera

**Key Models:**
- `SingleManuscript` (6 records expected)
- `Library` (52 records in fixtures)
- `Stanza` (thousands of stanzas)
- `StanzaTranslated` (English translations)
- `Folio` (manuscript pages)
- `Location` (~80 toponyms)

**Data Availability:**
- ❌ _data/ directory is gitignored (not in repo)
- ⏳ Need to request from Laura
- Options: PostgreSQL dump OR _data/ directory contents

---

## Meeting Preparation

### Pre-Meeting Deliverables
✅ **Email to Laura:**
- Subject: "La Sfera - Bug Analysis Complete + Meeting Request"
- Attachments: Meeting agenda, bug summary
- Sent: October 28, 2025

✅ **Meeting Materials:**
- 45-minute agenda (structured presentation)
- Bug demonstration script (before/after code)
- 3 budget scenarios (€3.9k / €10.2k / flexible)
- Timeline breakdown (2-5 weeks)

### Meeting Goals
1. **Demonstrate Value:** Show bugs are real and fixable
2. **Build Trust:** Professional presentation, accurate estimates
3. **Get Approval:** For at least minimum scope (€3.9k)
4. **Set Expectations:** Realistic timeline, clear deliverables
5. **Obtain Access:** Development credentials, production data

### Post-Meeting Success
✅ Laura confirms bugs are problems
✅ Budget scenario selected
✅ Timeline agreed upon
✅ Development credentials shared
✅ Next steps clear (contract, development start)

---

## Documentation Standards

### File Organization
```
docs/knowledge/
├── 01_project/         ← Project context, stakeholders, timeline
├── 02_technical/       ← System architecture, database, IIIF
├── 03_bugs/            ← Bug reports with code locations
├── 04_implementation/  ← Fixes applied, testing, deployment
└── 05_meeting/         ← Email, agenda, budget scenarios
```

### Writing Style
- **Technical Details:** Precise, with code examples and line numbers
- **Executive Summaries:** Concise, business-focused
- **Client Communication:** Professional, avoiding jargon
- **Internal Notes:** Detailed, includes reasoning and alternatives

---

## Lessons Learned

### What Worked Well
✅ **Methodical Approach:**
- Code analysis BEFORE live site testing
- Static verification BEFORE runtime testing
- Documentation WHILE coding (not after)

✅ **Realistic Estimates:**
- 1.55x overhead multiplier per task
- Contingency buffer (10-20%)
- Multiple budget scenarios for flexibility

✅ **Verification:**
- verify_fixes.py catches regressions
- Django test command for runtime checks
- Live site testing confirmed initial findings

### What Could Be Improved
⚠️ **Initial Assumptions:**
- First estimate: 700+ toponyms (WRONG - actually ~80)
- Timeline too optimistic (Week 1 deploy → realistic 3-4 weeks)
- Didn't account for waiting time (Laura's review, credentials)

⚠️ **Data Access:**
- Should have requested _data/ earlier
- Runtime testing blocked without production data
- Need backup plan for data-dependent testing

---

## Next Steps

### Immediate (Before Meeting)
- ✅ Email sent to Laura
- ⏳ Meeting confirmation from Laura
- ⏳ Practice demo presentation
- ⏳ Prepare screen-share setup

### Meeting (Nov 3 or 11)
- ⏳ Demonstrate bugs (20 min)
- ⏳ Discuss budget (15 min)
- ⏳ Agree on timeline (10 min)

### After Meeting (IF Approved)
- ⏳ Receive development credentials
- ⏳ Request production data (_data/ or SQL dump)
- ⏳ Run runtime tests
- ⏳ Create pull requests
- ⏳ Deploy to staging
- ⏳ Laura testing
- ⏳ Deploy to production
- ⏳ Send invoice

---

**Document Status:** Complete
**Last Updated:** November 4, 2025
**Next Review:** After Laura's meeting
