# La Sfera - Vollständige Bug & Task-Analyse

**Erstellt:** 28. Oktober 2025
**Analysiert von:** DH Craft (Christopher Pollin)
**Für:** Laura Morreale, RRCHNM/GMU

---

## Executive Summary

**Repository-Status:** ✅ Solide Grundstruktur, produktionsreif mit bekannten Schwachstellen

**Identifizierte Issues:**
- **8 offene GitHub Issues** (Feature Requests + Enhancements)
- **2 kritische Code-TODOs** im Core-Bereich
- **Mirador Alpha-Version** benötigt Upgrade
- **Gazetteer funktioniert**, aber Performance-Optimierung möglich
- **IIIF-Integration teilweise implementiert**, aber nicht vollständig integriert

**Geschätzter Gesamtaufwand:** 90-150 Stunden (abhängig von Priorisierung)

**Kritischer Pfad für Launch:**
1. Mirador Stable-Upgrade (KRITISCH)
2. Textual Variants Frontend (HOCH)
3. Gazetteer Performance-Optimierung (MITTEL)
4. Testing & Documentation (MITTEL)

---

## 1. GitHub Issues (Offen)

### Feature Requests / Enhancements

#### **#76 - Revise textual variant data model**
- **Status:** Open
- **Label:** `database`, `feature`
- **Beschreibung:** Datenmodell für Textual Variants überarbeiten
- **Priorität:** **HOCH**
- **Betroffene Files:**
  - `manuscript/models.py` (StanzaVariant Model)
  - `manuscript/admin.py`
  - Migrations
- **Details aus Code:**
  - TODO in models.py:378: "Ability to have variation in lines"
  - Aktuell: Variants nur auf Stanza-Ebene
  - Gewünscht: Line-by-line variations
- **Aufwand:** 15-25 Stunden
  - Datenmodell-Redesign: 5h
  - Migration schreiben: 3h
  - Admin-Interface anpassen: 4h
  - Testing & Validation: 3-5h
  - Daten-Migration (falls nötig): 5-8h

---

#### **#74 - Finalize design for textual variant front-end display**
- **Status:** Open
- **Label:** `website`, `feature`
- **Beschreibung:** Frontend-Design für Textual Variants fertigstellen
- **Priorität:** **HOCH**
- **Betroffene Files:**
  - `templates/stanzas.html`
  - `templates/manuscript_single.html`
  - `static/js/variant_annotations.js`
  - `manuscript/views.py` (stanzas view)
- **Aufwand:** 20-30 Stunden
  - UI/UX Design Review: 4h
  - Template-Implementation: 8-12h
  - JavaScript Interaktivität: 6-10h
  - Responsive Design: 2-4h
  - Testing: 4h

---

#### **#73 - Write up documentation on adding gallery images**
- **Status:** Open
- **Label:** `documentation`
- **Beschreibung:** Dokumentation für Gallery-Image-Upload erstellen
- **Priorität:** NIEDRIG
- **Betroffene Files:**
  - Neue Datei: `docs/gallery_management.md`
  - `gallery/models.py` (bereits implementiert)
  - `gallery/admin.py`
- **Aufwand:** 3-5 Stunden
  - Dokumentation schreiben: 2-3h
  - Screenshots erstellen: 1h
  - Review: 1h

---

#### **#65 - Design crowdsourcing component for translations/transcriptions**
- **Status:** Open
- **Label:** `feature`, `outcome`
- **Beschreibung:** Crowdsourcing-Feature für Übersetzungen/Transkriptionen
- **Priorität:** NIEDRIG (Nice-to-have für v1.0)
- **Aufwand:** 40-60 Stunden (Major Feature)
  - Konzept & Design: 8h
  - User Permission System: 12-15h
  - Frontend Forms: 10-15h
  - Review/Approval Workflow: 10-15h
  - Testing: 8-10h
- **Empfehlung:** Post-Launch Feature (Phase 2)

---

#### **#60 - Add historic base map to the gazetteer interface**
- **Status:** Open (1 comment)
- **Label:** `feature`, `outcome`
- **Beschreibung:** Historische Basiskarte für Gazetteer hinzufügen
- **Priorität:** MITTEL
- **Betroffene Files:**
  - `templates/gazetteer/gazetteer_index.html` (Leaflet Map)
  - `templates/gazetteer/gazetteer_single.html`
- **Details:**
  - Aktuell: OpenStreetMap (modern)
  - Gewünscht: Historic map layer (z.B. David Rumsey Map Collection)
- **Aufwand:** 8-12 Stunden
  - Historic Map Tiles recherchieren: 2h
  - Leaflet Layer Switcher implementieren: 4-6h
  - Testing & Performance: 2-4h

---

#### **#56 - Design user roles for manuscript contributions**
- **Status:** Open
- **Label:** `database`, `django`
- **Beschreibung:** User-Rollen für Manuskript-Beiträge designen
- **Priorität:** MITTEL (abhängig von #65)
- **Aufwand:** 12-18 Stunden
  - Django Groups/Permissions Design: 4h
  - Models anpassen: 4-6h
  - Admin-Interface: 3-5h
  - Testing: 3-5h

---

#### **#51 - Incorporate import_export for downloadable datasets**
- **Status:** Open
- **Label:** `django`, `feature`, `outcome`
- **Beschreibung:** Django import_export für downloadbare Datasets integrieren
- **Priorität:** NIEDRIG
- **Status im Code:** ✅ **BEREITS IMPLEMENTIERT!**
  - `manuscript/resources.py` existiert bereits (LocationResource, LocationAliasResource, etc.)
  - `manuscript/admin.py` verwendet ImportExportModelAdmin
  - pyproject.toml: django-import-export = "^4.0.3"
- **Fehlende Teile:**
  - Frontend Download-Buttons für User (nicht nur Admin)
  - Export-Views für Public Access
- **Aufwand:** 4-6 Stunden (nur Frontend-Integration)
  - Export-Views erstellen: 2-3h
  - Templates/Buttons hinzufügen: 1-2h
  - Testing: 1h

---

#### **#22 - [Titel unbekannt]**
- **Status:** Open (seit Apr 10, 2024 - ältestes Issue!)
- **Priorität:** Unklar (Details benötigt)
- **Action:** Im Meeting klären

---

## 2. Code-TODOs (Kritische Findings)

### **TODO #1: Line-based Textual Variations**
- **File:** `manuscript/models.py:378`
- **Code:**
  ```python
  # TODO: Ability to have variation in lines
  ```
- **Context:** StanzaVariant Model
- **Priorität:** HOCH (verknüpft mit Issue #76)
- **Problem:** Aktuell können Variants nur auf Stanza-Ebene erfasst werden, nicht line-by-line
- **Impact:** Limitiert wissenschaftliche Präzision der Edition

### **TODO #2: Line Code Dropdown**
- **File:** `manuscript/models.py:620`
- **Code:**
  ```python
  # TODO: Convert these ranges to a dropdown of available line codes
  ```
- **Context:** Admin Interface für Line Code Ranges
- **Priorität:** MITTEL (UX Improvement)
- **Aufwand:** 3-5 Stunden
  - Custom Admin Widget: 2-3h
  - JavaScript für Dropdown: 1h
  - Testing: 1h

---

## 3. IIIF-Integration - Detailanalyse

### **Aktueller Stand:**

**✅ Implementiert:**
- Mirador Viewer in `templates/manuscript/mirador.html`
- Canvas ID Generation: `manuscript/utils.py:get_canvas_id_for_folio()`
- Manifest Caching: `manuscript/views.py:get_manifest_data()` (24h Cache)
- IIIF URL Fields in Models:
  - `SingleManuscript.iiif_url`
  - `LineCode.associated_iiif_url`
- Mirador View Route: `/mirador/<manuscript_id>/<page_number>/`

**⚠️ KRITISCH - Mirador Alpha-Version:**
- **package.json:** `"mirador": "^4.0.0-alpha.2"`
- **Problem:** Alpha-Version in Produktion ist riskant
- **Lösung:** Upgrade zu Mirador 4.0 Stable (oder Mirador 3.x falls Kompatibilität)
- **Risiko:** Breaking Changes beim Upgrade

**❌ Fehlende Features:**

1. **Canvas ID nicht übergeben an Mirador**
   - `mirador.html:19` übergibt nur `manifest_url`, NICHT `canvas_id`
   - View berechnet canvas_id nicht
   - **Impact:** Viewer startet immer bei Seite 1, nicht bei gewünschtem Folio

2. **IIIF-Integration in Stanza-View fehlt**
   - `templates/stanzas.html` hat keinen IIIF-Viewer
   - Line Codes könnten direkt zu Folio-Bildern linken

3. **Mirador View unvollständig**
   - `manuscript/views.py:485` - `mirador_view()` ignoriert `page_number` Parameter
   - Fallback zu "Urb1" manuscript ist hardcoded

4. **Fehlende IIIF Presentation API v3 Unterstützung**
   - Code verwendet v2 API (`sequences[0].canvases`)
   - Mirador 4 unterstützt v3, aber Code ist v2-only

### **Empfohlene IIIF-Tasks:**

#### **Task I-1: Mirador Upgrade zu Stable** ⚠️ KRITISCH
- **Priorität:** KRITISCH (Blocker für Production)
- **Files:**
  - `package.json`
  - `templates/manuscript/mirador.html`
- **Aufwand:** 10-15 Stunden
  - Mirador 4.0 Stable installieren: 1h
  - Breaking Changes identifizieren: 3-4h
  - Config-Migration: 3-5h
  - Testing mit allen Manuscripts: 3-5h

#### **Task I-2: Canvas ID korrekt übergeben**
- **Priorität:** HOCH
- **Files:**
  - `manuscript/views.py:mirador_view()`
  - `manuscript/utils.py`
  - `templates/manuscript/mirador.html`
- **Aufwand:** 5-8 Stunden
  - Canvas ID Lookup implementieren: 2-3h
  - View anpassen: 1-2h
  - Template-Variable übergeben: 1h
  - Testing: 2h

#### **Task I-3: IIIF in Stanza-View integrieren**
- **Priorität:** MITTEL-HOCH
- **Files:**
  - `templates/stanzas.html`
  - `manuscript/views.py:stanzas()`
- **Aufwand:** 8-12 Stunden
  - Folio zu Line Code Mapping: 3-4h
  - Mirador Embedding in Stanza View: 3-5h
  - Responsive Layout: 2-3h

#### **Task I-4: IIIF Presentation API v3 Migration**
- **Priorität:** MITTEL (abhängig von Mirador-Version)
- **Files:**
  - `manuscript/utils.py`
  - `manuscript/views.py`
- **Aufwand:** 6-10 Stunden
  - v3 API Parsing: 3-5h
  - Backward Compatibility: 2-3h
  - Testing: 2h

---

## 4. Gazetteer - Detailanalyse

### **Aktueller Stand:**

**✅ Implementiert & Funktionsfähig:**
- Location & LocationAlias Models
- Leaflet Map mit OpenStreetMap
- Marker Clustering
- Fuzzy Search (HTMX)
- Hover Effects (Map ↔ List)
- Detail-Seiten mit Variants, Line Codes, Coordinates
- REST API Endpoints (`/api/toponyms/`)
- Slug-basierte URLs

**Code-Qualität:** ✅ Gut
- Saubere Trennung Models/Views/Templates
- Prefetch-related für Performance
- Serializers für API

### **Potenzielle Bugs/Issues:**

#### **Bug G-1: Marker Cluster Performance**
- **File:** `templates/gazetteer/gazetteer_index.html:63`
- **Problem:** Alle Toponyms werden auf einmal geladen (keine Pagination)
- **Impact:** Bei vielen Locations (>500) könnte Performance leiden
- **Priorität:** NIEDRIG (aktuell wahrscheinlich unkritisch)
- **Aufwand:** 4-6 Stunden (Lazy Loading implementieren)

#### **Bug G-2: Empty Coordinates nicht gefiltert**
- **File:** `gazetteer_index.html:70-72`
- **Code:** Frontend filtert `null` Coordinates, aber Query tut es nicht
- **Priorität:** NIEDRIG (funktioniert, aber ineffizient)
- **Aufwand:** 1-2 Stunden
  - Filter in View hinzufügen: 30min
  - Testing: 30min

#### **Bug G-3: Hardcoded Manuscript Link**
- **File:** `gazetteer_single.html:67`
- **Code:** `href="/manuscripts/Urb1/stanzas/#{{ line_code.line_code }}"`
- **Problem:** Hardcoded "Urb1" - sollte dynamisch sein
- **Priorität:** MITTEL
- **Aufwand:** 2-3 Stunden

#### **Bug G-4: Slug-Generation bei Special Characters**
- **File:** `manuscript/views.py:871-873`
- **Problem:** `slugify()` könnte bei non-ASCII Zeichen Probleme haben (italienische Namen)
- **Test:** "città" → "citta" vs "città"
- **Priorität:** NIEDRIG
- **Aufwand:** 2-3 Stunden (Unicode-safe slugify)

### **Enhancements:**

#### **Enhancement G-5: Historic Map Layer** (siehe Issue #60)

#### **Enhancement G-6: Export Gazetteer Data**
- **Priorität:** NIEDRIG
- **Feature:** CSV/JSON Download aller Toponyms
- **Aufwand:** 3-4 Stunden (mit django-import-export)

---

## 5. Testing & Quality Assurance

### **Aktueller Test-Status:** ⚠️ KRITISCH

**Problem:** Nur Placeholder-Tests vorhanden
- `manuscript/tests.py`: 63 Bytes (leer)
- `gallery/tests.py`: 63 Bytes (leer)
- `textannotation/tests.py`: 63 Bytes (leer)

**Impact:** Jede Code-Änderung muss manuell getestet werden → erhöhter Zeitaufwand

### **Empfohlene Test-Suite:**

#### **Task T-1: Core Model Tests**
- **Priorität:** HOCH
- **Files:**
  - `manuscript/tests/test_models.py` (neu)
  - `manuscript/tests/test_line_codes.py` (neu)
- **Aufwand:** 12-18 Stunden
  - Line Code Parsing Tests: 4-6h
  - Folio-Stanza Mapping Tests: 4-6h
  - Location/Alias Tests: 4-6h

#### **Task T-2: View/Integration Tests**
- **Priorität:** MITTEL
- **Files:**
  - `manuscript/tests/test_views.py` (neu)
  - `manuscript/tests/test_api.py` (neu)
- **Aufwand:** 10-15 Stunden

#### **Task T-3: Frontend/JavaScript Tests**
- **Priorität:** NIEDRIG
- **Tools:** Jest oder Playwright
- **Aufwand:** 15-20 Stunden

---

## 6. Deployment & Hosting-Export

### **Aktueller Stand:**
- Docker + docker-compose konfiguriert
- Jinja2 Template für dynamic docker-compose
- Django settings via Environment Variables

### **Tasks für Host-Migration:**

#### **Task D-1: Deployment-Dokumentation**
- **Priorität:** HOCH
- **Aufwand:** 4-6 Stunden
  - Step-by-step Deployment Guide: 3h
  - Environment Variables dokumentieren: 1h
  - Troubleshooting Section: 1-2h

#### **Task D-2: CI/CD Pipeline**
- **Priorität:** MITTEL
- **Tool:** GitHub Actions (bereits `.github/` vorhanden)
- **Aufwand:** 8-12 Stunden
  - Automated Testing: 4-6h
  - Deployment Workflow: 3-5h
  - Rollback-Mechanismus: 1-2h

#### **Task D-3: Database Migration Script**
- **Priorität:** HOCH
- **Aufwand:** 4-6 Stunden
  - Backup-Strategie: 2h
  - Migration-Script: 2-3h
  - Rollback-Plan: 1h

#### **Task D-4: Media Files Transfer**
- **Priorität:** MITTEL
- **Aufwand:** 2-4 Stunden
  - rsync/S3 Setup: 1-2h
  - Testing: 1-2h

---

## 7. Priorisierte Gesamt-Task-Liste

### **PHASE 1: Kritische Bugs & Launch-Blocker (35-55h)**

- [ ] **[KRITISCH]** I-1: Mirador Upgrade zu Stable - `15h`
  - Files: `package.json`, `templates/manuscript/mirador.html`
  - Blocker für Production-Launch

- [ ] **[HOCH]** #76: Revise textual variant data model - `15-25h`
  - Files: `manuscript/models.py`, Migrations
  - Core-Feature für wissenschaftliche Edition

- [ ] **[HOCH]** I-2: Canvas ID korrekt übergeben - `5-8h`
  - Files: `manuscript/views.py`, `manuscript/utils.py`
  - IIIF-Viewer funktioniert nicht ohne

- [ ] **[HOCH]** #74: Finalize textual variant frontend - `20-30h`
  - Files: `templates/stanzas.html`, `static/js/variant_annotations.js`
  - User-facing critical feature

**Phase 1 Gesamt:** 55-78 Stunden

---

### **PHASE 2: Performance & UX (20-35h)**

- [ ] **[MITTEL]** G-3: Fix hardcoded manuscript link - `2-3h`
  - Files: `templates/gazetteer/gazetteer_single.html`

- [ ] **[MITTEL]** I-3: IIIF in Stanza-View integrieren - `8-12h`
  - Files: `templates/stanzas.html`, `manuscript/views.py`

- [ ] **[MITTEL]** #60: Historic base map für Gazetteer - `8-12h`
  - Files: `templates/gazetteer/*.html`

- [ ] **[MITTEL]** TODO #2: Line Code Dropdown - `3-5h`
  - Files: `manuscript/admin.py`

- [ ] **[MITTEL]** T-1: Core Model Tests schreiben - `12-18h`
  - Files: `manuscript/tests/` (neu)

**Phase 2 Gesamt:** 33-50 Stunden

---

### **PHASE 3: Deployment & Documentation (15-25h)**

- [ ] **[HOCH]** D-1: Deployment-Dokumentation - `4-6h`
- [ ] **[HOCH]** D-3: Database Migration Script - `4-6h`
- [ ] **[MITTEL]** D-2: CI/CD Pipeline - `8-12h`
- [ ] **[MITTEL]** D-4: Media Files Transfer - `2-4h`
- [ ] **[NIEDRIG]** #73: Gallery-Dokumentation - `3-5h`

**Phase 3 Gesamt:** 21-33 Stunden

---

### **PHASE 4: Nice-to-Have / Post-Launch (20-30h)**

- [ ] **[NIEDRIG]** #51: Import/Export Frontend - `4-6h`
- [ ] **[NIEDRIG]** I-4: IIIF API v3 Migration - `6-10h`
- [ ] **[NIEDRIG]** G-4: Unicode-safe slugify - `2-3h`
- [ ] **[NIEDRIG]** G-6: Gazetteer Export Feature - `3-4h`
- [ ] **[NIEDRIG]** T-2: View Tests - `10-15h`

**Phase 4 Gesamt:** 25-38 Stunden

---

## 8. Gesamtaufwand & Timeline

### **Minimal Viable Product (MVP) für Launch:**
**Phase 1 + ausgewählte Phase 2 Tasks**
- **Aufwand:** 70-100 Stunden
- **Timeline bei 20h/Woche:** 3,5-5 Wochen
- **Empfohlen bis:** Mitte Dezember 2025

### **Full Production-Ready:**
**Phase 1 + 2 + 3**
- **Aufwand:** 110-160 Stunden
- **Timeline bei 20h/Woche:** 5,5-8 Wochen
- **Empfohlen bis:** Ende Januar 2026

### **Complete Feature Set:**
**Alle Phasen**
- **Aufwand:** 135-200 Stunden
- **Timeline bei 20h/Woche:** 7-10 Wochen
- **Deadline:** Juni 2026 ✅ **Machbar!**

---

## 9. Risiken & Abhängigkeiten

### **Technische Risiken:**

1. **Mirador Upgrade (Kritisch)**
   - Breaking Changes könnten mehr Arbeit erfordern als geschätzt
   - **Mitigation:** 2-Tage Proof-of-Concept vor Commitment

2. **Datenmodell-Migration (#76)**
   - Bestehende Daten müssen migriert werden
   - **Mitigation:** Backup-Strategie, Rollback-Plan

3. **Fehlende Tests**
   - Regression-Risiko bei jeder Änderung
   - **Mitigation:** Manuelle Test-Checkliste, schrittweise Test-Coverage aufbauen

### **Projekt-Risiken:**

1. **Issue #22 unklar**
   - Ältestes offenes Issue, Details fehlen
   - **Mitigation:** Im Meeting klären

2. **GMU-Infrastruktur-Probleme**
   - Unbekannt, könnte zusätzliche Arbeit bedeuten
   - **Mitigation:** Detaillierte Bestandsaufnahme im Meeting

---

## 10. Empfehlungen für DH Craft

### **Vor Vertragsunterzeichnung:**

1. ✅ **Proof-of-Concept: Mirador Upgrade (1-2 Tage bezahlt)**
   - Identifiziert größten Risikofaktor
   - Realistische Aufwandsschätzung

2. ✅ **Meeting-Punkte klären:**
   - Issue #22 Details
   - Welche Phase ist Minimum für Launch?
   - GMU-Infrastruktur-Probleme?
   - Budget & Zahlungsmodalitäten

3. ✅ **Zugang anfordern:**
   - Dev-Environment
   - Database-Dump für lokale Entwicklung
   - Admin-Account auf dev.lasfera.rrchnm.org

4. ✅ **Scope definieren:**
   - MVP (Phase 1) vs. Full (Phase 1+2+3)?
   - Phase 4 optional/post-launch?

### **Pricing-Empfehlung:**

**Hybrid-Modell:**
- **Phase 1 (Kritisch):** Fixed Price - basierend auf 70h × Rate
  - Planungssicherheit für beide Seiten
  - Klare Deliverables

- **Phase 2+3:** Milestone-basiert oder Hourly
  - Flexibilität bei Scope-Changes
  - Pay-per-delivered-feature

- **Phase 4:** Optional Post-Launch Support (Hourly)

### **Vertrag sollte enthalten:**

- Klare Definition von "Done" pro Phase
- Acceptance Criteria
- Change Request Prozess
- Zahlungsplan (z.B. 30% Start, 40% nach Phase 1, 30% nach Launch)
- Intellectual Property Rechte (Code → RRCHNM)
- Support-Period nach Launch (z.B. 4 Wochen Bug-Fixes included)

---

## 11. Meeting-Agenda (Priorität)

### **Kritische Punkte (Must-Discuss):**

1. **Issue #22** - Was ist das? Noch relevant?
2. **MVP-Definition** - Welche Features sind Must-Have für Launch?
3. **Budget** - Wie viel ist verfügbar? Passt zu unserer Schätzung?
4. **Timeline** - Wann muss was fertig sein? Flexible Milestones?
5. **GMU-Probleme** - Was genau läuft schief? Zugang zu bisheriger Dev-Dokumentation?
6. **Testing** - Wer macht User Acceptance Testing? Staging-Environment?

### **Technische Diskussion:**

7. **Mirador Upgrade** - Proof-of-Concept vereinbaren?
8. **Textual Variants** - Wie soll das finale Design aussehen? Mockups?
9. **Gazetteer Bugs** - Welche konkreten Probleme gibt es? Screenshots?
10. **Historic Map** - Welche Karten-Source gewünscht?

### **Organisatorisches:**

11. **Kommunikation** - Email, Slack, GitHub Issues?
12. **Code Review** - Wer reviewed? Approval-Prozess?
13. **Deployment** - Wann ist Host-Migration geplant? Wer managed danach?

---

## 12. Nächste Schritte

### **Vor Meeting (bis 3./11. Nov):**
- [x] Code-Analyse abgeschlossen
- [x] Task-Liste erstellt
- [x] Aufwandsschätzungen berechnet
- [ ] Proof-of-Concept-Plan für Mirador vorbereiten
- [ ] Fragen-Katalog finalisieren

### **Im Meeting:**
- [ ] Issue #22 klären
- [ ] MVP-Scope definieren
- [ ] Budget besprechen
- [ ] Proof-of-Concept vereinbaren
- [ ] Zugang zu Dev-Environment anfragen

### **Nach Meeting:**
- [ ] Proof-of-Concept durchführen (2 Tage)
- [ ] Detailliertes Angebot erstellen
- [ ] Vertrag ausarbeiten
- [ ] Kick-off bei Zusage

---

## Anhang: Technische Referenzen

### **Wichtige Files:**

**Gazetteer:**
- Models: `manuscript/models.py:782` (Location), `manuscript/models.py:894` (LocationAlias)
- Views: `manuscript/views.py:919` (toponyms), `manuscript/views.py:876` (toponym_by_slug)
- Templates: `templates/gazetteer/gazetteer_index.html`, `templates/gazetteer/gazetteer_single.html`
- API: `manuscript/serializers.py:6` (ToponymSerializer), `manuscript/views.py:1060` (ToponymViewSet)

**IIIF:**
- Mirador: `templates/manuscript/mirador.html`
- Utils: `manuscript/utils.py:10` (get_manifest), `manuscript/utils.py:20` (get_canvas_id_for_folio)
- Views: `manuscript/views.py:40` (get_manifest_data), `manuscript/views.py:485` (mirador_view)
- URLs: `manuscript/urls.py:29-33`

**Textual Variants:**
- Models: `manuscript/models.py:370` (StanzaVariant)
- Templates: `templates/stanzas.html`, `templates/manage_stanza_variations.html`
- JavaScript: `static/js/variant_annotations.js`

### **Datenbank-Schema:**
- Dokumentation: https://dbdocs.io/hepplerj/lasfera
- Migrations: `manuscript/migrations/` (104 Migrations!)

### **Dependencies:**
- Django: 5.0.2
- Wagtail: 6.2.1
- Mirador: 4.0.0-alpha.2 ⚠️
- django-import-export: 4.0.3
- Python: 3.11+

---

**Ende der Analyse**

**Kontakt für Rückfragen:**
Christopher Pollin, DH Craft
christopher.pollin@dhcraft.org
