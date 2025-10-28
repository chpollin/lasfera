# La Sfera - DH Craft Technical Analysis

**Date:** 28. Oktober 2025
**Contact:** Laura Morreale (lmorreale3@gmail.com)
**Meeting:** 3. oder 11. Nov 2025, 17:00 CET
**Timeline:** bis Juni 2026 (~7 Monate)

---

## Executive Summary

**Assessment: 7/10** - Solides DH-Projekt, machbar mit klarer Scope-Definition

**Empfehlung:** ✅ Annehmen mit Bedingungen (Proof-of-Concept, Milestone-Zahlung)

---

## Tech Stack

| Component | Version | Status |
|-----------|---------|--------|
| Python | 3.11+ | ✅ |
| Django | 5.0.2 | ✅ |
| Wagtail | 6.2.1 | ✅ |
| Mirador | 4.0.0-alpha.2 | ⚠️ ALPHA! |
| PostgreSQL | (unspecified) | ✅ |
| Tailwind | 3.8.0 | ✅ |
| Node.js | 20.14.0 | ✅ |

---

## Kritische Befunde

### 🔴 Risiken

1. **Mirador Alpha-Version** - Upgrade zu Stable nötig (Breaking Changes?)
2. **Keine Tests** - Nur 63-Byte Placeholder-Tests, manuelles Testing erforderlich
3. **Komplexe Datenmodelle** - 33KB models.py mit hierarchischem Line-Code-System
4. **Gazetteer-Bugs undokumentiert** - Keine Issues im Repo, Details von Laura erforderlich
5. **GMU-Probleme unklar** - Könnte Legacy-Code oder Infra-Issues bedeuten

### ✅ Stärken

- Solide Django/Wagtail-Architektur
- Docker + Poetry Setup vorhanden
- Pre-commit Hooks konfiguriert
- IIIF Canvas-Generation bereits implementiert
- Geopy-Integration für Geographic Data

---

## Core Apps

- `manuscript/` - Hauptfunktionalität (Line Codes, Folios, Stanzas, Variants)
- `textannotation/` - ProseMirror-basierte Annotations
- `gallery/` - Wagtail Image Gallery mit Theme-Filtering
- `pages/` - Wagtail CMS
- `accounts/` - Django Allauth Authentication

---

## Kritische Meeting-Fragen

### IIIF-Integration
- [ ] Welche Features fehlen konkret?
- [ ] Mirador 4 Stable-Upgrade erforderlich?
- [ ] IIIF Manifest-Generation Teil der Aufgabe?

### Gazetteer
- [ ] Konkrete Bug-Beschreibungen?
- [ ] Location Models, Templates oder Geopy-Problem?
- [ ] Screenshots/Error Messages?

### Scope
- [ ] Vollständige priorisierte Task-Liste?
- [ ] Must-Have vs. Nice-to-Have?
- [ ] Bereits Task-Tracking (GitHub Issues)?

### Export & Hosting
- [ ] Ziel-Provider (AWS/DO/Hetzner)?
- [ ] Wer managed Server nach Export?
- [ ] CI/CD Pipeline gewünscht?
- [ ] Domain & SSL vorhanden?

### Budget & Timeline
- [ ] Hourly Rate oder Fixed Price?
- [ ] Milestone-Zahlungen möglich?
- [ ] Launch-Deadline flexibel?

### Team
- [ ] Technischer Ansprechpartner bei RRCHNM?
- [ ] Frühere Developer-Dokumentation?
- [ ] Zugang zu Dev-Environment & DB-Dump?

---

## Zeitschätzung (vorläufig)

| Task | Hours |
|------|-------|
| IIIF-Integration (Mirador Upgrade) | 20-40h |
| Gazetteer-Bugs | 10-30h |
| Export & Hosting-Setup | 15-25h |
| Testing & Documentation | 10-15h |
| Buffer (20%) | ~15h |
| **TOTAL** | **60-130h** |

**Bei 20h/Woche: 3-7 Wochen Entwicklungszeit**

---

## Pricing-Empfehlung

**Hybrid-Modell (empfohlen):**
- Fixed Price für definierte Tasks
- Hourly Rate für zusätzliche Features
- Milestone-basierte Zahlungen

---

## Bedingungen für Zusage

1. ✅ Detaillierte Task-Liste mit Prioritäten
2. ✅ Proof-of-Concept Phase (5-10h bezahlt)
3. ✅ Zugang zu Dev-Environment & DB-Dump
4. ✅ Klare Scope-Definition & Acceptance Criteria
5. ✅ Dokumentation von früheren Entwicklern

---

## Nächste Schritte

1. Meeting wahrnehmen (3. oder 11. Nov)
2. Live-Demo aktuelles System
3. Gazetteer-Bugs demonstrieren lassen
4. Task-Liste & GitHub Issues erstellen
5. Proof-of-Concept vereinbaren (1-2 Tage)
6. Detailliertes Angebot mit Milestones

---

## Code-Quality Notes

**Positiv:**
- Poetry Dependency Management
- Docker/docker-compose ready
- django-environ für Config
- Pre-commit Hooks

**Verbesserungspotenzial:**
- Test-Coverage fehlt komplett
- Keine Type Hints
- Dokumentation ausbaufähig

---

## Repository

- GitHub: https://github.com/chnm/lasfera
- Live Dev: https://dev.lasfera.rrchnm.org/
- DB Schema: https://dbdocs.io/hepplerj/lasfera

---

**Gesamteinschätzung:** Interessantes, machbares Projekt für DH Craft. Timeline realistisch bei klarem Scope. Risiken managebar mit ordentlicher Planung und Proof-of-Concept.
