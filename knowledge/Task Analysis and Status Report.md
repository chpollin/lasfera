# La Sfera Project: Task Analysis and Status Report (2025-11-03)
*Based on Meeting Notes from Mapping Mobile Musicians (M³GIM) and Project Documentation*

## Document Metadata
- Source Document Date: Last updated Sep 30, 2025
- Meeting Date: November 3, 2025
- Project URL: https://lasfera.rrchnm.org/
- Documentation: https://docs.google.com/document/d/1W6L4d5v96FbpQPcMZ22kY_WKTF7xi3ShvZ0kmOmFxq8/
- Target Completion: Before May 2026

## Executive Summary
Digital edition project featuring Italian/English transcriptions, annotations, IIIF image integration, textual variations, and gazetteer functionality. Currently addressing 9 sub-projects with varying completion rates (0-50%).

## Project Status Overview

| Project | Description | Lead | Priority (Original) | Progress |
|---------|------------|------|-------------------|----------|
| 1 | Textual variant display/database | Laura Ingallinella | medium/high | 25% |
| 2 | Limited images | [Unassigned: "Person"] | medium/high | 25% |
| 3 | Extensible edition | Laura Morreale | medium | 0% |
| 4 | Structural tweaks | Jason Heppler | high | 0% |
| 5 | Content updates | [Unassigned: "Person"] | high | 0% |
| 6 | Geospatial interface | Carrie Benes | high | 50% |
| 7 | WHG integration | Carrie Benes | medium | 0% |
| 8 | Back-end | Amanda G Madden | medium/high | 0% |
| 9 | Full Image Gallery | [Unassigned: "Person"] | low | 0% |

## Tasks by Original Priority Classification

### HIGH PRIORITY TASKS (Document-Specified)

#### Project 4: Structural Tweaks
- [ ] Add "Introduction" button to main navigation bar - Due: Oct 17, 2025 (Jason Heppler)
- [ ] Reassign sferaproject.org to RRCHNM site - Due: Dec 31, 2025 (Jason Heppler)

#### Project 5: Content Updates
*Note: Collaborators CEB & LKM mentioned*
- [ ] Build & fill Introduction page (student-focused) - Due: Oct 31, 2025 (Laura Morreale)
- [ ] Improve landing page text - Due: Oct 31, 2025 (Laura Morreale)
- [ ] Incorporate revised "Page by page text" - Due: Oct 31, 2025 (Laura Morreale, Carrie)
- [ ] Update About page team members - Due: Oct 31, 2025 (Laura Morreale, Carrie)
- [ ] Refine text annotations with toponym links [marked "LINKY"] - Due: Oct 31, 2025 (Laura Morreale)

#### Project 6: Geospatial Interface
- [ ] Create "final" toponym dataset - No date specified (Carrie Benes)
- [ ] Fix broken links in gazetteer landing page map - No date specified
- [ ] Improve popup format (current shows "No name available") - No date specified
- [ ] Add bidirectional links between toponyms and pages [marked "LINKY"] - Due: Dec 31, 2025 (Carrie Benes)

#### Within Project 2: Limited Images
- [ ] Add MSS to IIIF integration on edition interface - Due: Feb 13, 2026 (Jason Heppler) - *IN PROGRESS*

#### Within Project 8: Back-end
- [x] Write README intro - Completed Oct 10, 2025 (Jason Heppler)

### MEDIUM/HIGH PRIORITY TASKS

#### Project 1: Textual Variants
- [ ] Fill out textual variant dataset - Due: Feb 28, 2026 (Laura Ingallinella) - *IN PROGRESS: RAs working Fall 2025/Winter 2026*
- [ ] Revise textual variant data model (Issue #74) - No date (Jason Heppler)
- [ ] Handle data importing for textual variants (Issue #76) - No date (Jason Heppler)
- [ ] Finalize design for textual variant display (Issue #73) - No date (Jason Heppler)

#### Project 2: Limited Images
- [ ] Write documentation for adding gallery images (Issue #65) - Due: Oct 17, 2025 (Jason Heppler)

### MEDIUM PRIORITY TASKS

#### Project 3: Extensible Edition
- [ ] Design crowdsourcing component (Issue #60) - No date specified
- [ ] Design user roles for contributions (Issue #51) - No date specified
- [ ] Design flowchart for manuscript placement - No date specified
- [ ] Incorporate import_export for datasets (Issue #22) - No date specified

#### Project 5: Content Updates (Medium items)
- [ ] Revive manuscript list page - No date (*Note: "Previously shown by Jason, disappeared"*)
- [ ] Create "Teach with La sfera" materials - Due: Jan 31, 2026 (Laura Morreale)
- [ ] Choose DRM-free images for gallery - Due: Mar 31, 2026

#### Project 6: Geospatial Interface (Medium items)
- [ ] Decide on variant display criteria - No date specified

#### Project 7: WHG Integration
- [ ] Create WHG data model - Due: Mar 31, 2026 (Carrie Benes) - *IN PROGRESS*
- [ ] Create toponym dataset in WHG format - Due: Mar 31, 2026 (Carrie Benes) - *IN PROGRESS*
- [ ] Create La sfera collection in WHG - Due: Mar 31, 2026 (Carrie Benes)
- [ ] Add WHG links to toponym pages - Due: Mar 31, 2026 [marked "Not-SH"]

#### Project 8: Back-end (Medium items)
- [ ] Write white paper/DHQ article - No date (Amanda G Madden) - *IN PROGRESS: Can start mid-October*

### LOW PRIORITY TASKS

#### Project 2: Limited Images
- [ ] Incorporate DMCA takedown note - No date specified

#### Project 6: Geospatial Interface
- [ ] Add historic base map to gazetteer (Issue #56) - Status: BLOCKED

#### Project 9: Full Image Gallery
- [ ] Establish copyright-clear manuscripts - Status: BLOCKED
- [ ] Incorporate DMCA takedown note - Status: BLOCKED
- [ ] Export images from Tropy and upload - Status: BLOCKED

## Issues Identified in Meeting Notes

### Technical Questions
1. Hosting/Deployment: "github eniarbeitne --> aber wie kommt es in das system" [How does content get into the system?]
2. Goal: "ziel eine funktionieren" [Goal: a functioning system before May 2026]

### Gazetteer Issues
- "Names are problematic" - specifics not detailed
- Each toponym has a detail page (functioning)
- Links to gazetteer need database addition

### Missing Features
- Manuscript list: 160 manuscripts total, information not available in current interface
- List should be in navbar but currently missing
- "List of significant variants, listed by folia number" - structure exists but needs implementation

### Data Management
- New data not ingested as manuscript pages
- Need workflow for crowdsourcing transcriptions

## Unclear Items Requiring Clarification

1. "Person" assignments: Multiple tasks have generic "Person" as owner
2. "Not-SH" notation: Meaning unclear (Project 7)
3. "LINKY" notation: Appears twice, purpose unclear
4. CEB & LKM: Abbreviations in Project 5 notes need clarification
5. Original project site: Status and update requirements not specified

## Critical Path Summary

### Immediate (Overdue or Due Soon)
- Oct 17, 2025: Navigation button, documentation
- Oct 31, 2025: All content updates (5 tasks)
- Dec 31, 2025: Domain transfer, toponym linking

### Q1 2026
- Jan 31, 2026: Teaching materials
- Feb 13, 2026: IIIF integration
- Feb 28, 2026: Textual variant dataset

### Q2 2026
- Mar 31, 2026: WHG integration, image selection
- May 2026: Project completion target

## Risk Assessment
- High Risk: Projects 3, 4, 5, 7, 9 at 0% completion
- Blocked Tasks: Historic base map, all Project 9 tasks
- Unassigned Ownership: Multiple "Person" assignments need clarification
- Deployment Pipeline: Unclear process for content integration