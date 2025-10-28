# La Sfera Digital Edition - Knowledge Vault

**Erstellt:** 28. Oktober 2025
**Projekt:** La Sfera Digital Edition Bug-Fixes & IIIF-Integration
**Client:** Laura Morreale (RRCHNM, George Mason University)
**Entwickler:** DH Craft - Christopher Pollin

---

## Ordnerstruktur

```
.knowledge/
├── 01_project/          Projektverwaltung & Kontext
├── 02_technical/        Technische Dokumentation
├── 03_bugs/             Bug-Reports & Fixes
├── 04_meetings/         Meeting-Protokolle & Vorbereitung
├── 05_deliverables/     Angebote, Verträge, Rechnungen
├── 06_reference/        Referenzmaterial & Recherche
└── 07_implementation/   Implementation Plan & Feasibility
```

---

## ⚠️ WICHTIGE ERKENNTNISSE (28. Okt 2025 - v3.0)

### 🚨 LIVE-SITE VERIFIKATION ABGESCHLOSSEN!

**Ursprüngliche Annahme (v1.0):** 5 Bugs, ~10.000€
**Nach Code-Analyse (v2.0):** 2 Bugs, ~2.340€ (-77%) ← ZU OPTIMISTISCH!
**Nach Live-Tests (v3.0):** **3 Bugs, ~3.510€** (-65% vs. Original)

### Kritische Korrektur v2.0 → v3.0:
- **Bug #2 existiert doch!** (Viewer rendert nicht, JavaScript-Problem)
- **Gazetteer funktioniert perfekt** (kein Fix nötig)
- **+1.170€ / +50%** gegenüber v2.0

**Siehe:** [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) für Details
**Siehe:** [VERIFICATION_REPORT.md](../VERIFICATION_REPORT.md) für Live-Test Ergebnisse

---

## Quick Start für neue Leser

**Wichtigste Dokumente zuerst lesen:**

1. **[EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md)** ⭐ - Übersicht & Haupterkenntnisse (v3.0)
2. **[VERIFICATION_REPORT.md](../VERIFICATION_REPORT.md)** ⭐⭐ - Vollständiger Verifikationsbericht mit Live-Tests
3. **[03_bugs/bug_inventory.md](03_bugs/bug_inventory.md)** - 3 verifizierte Bugs (v3.0)
4. **[05_deliverables/cost_estimate.md](05_deliverables/cost_estimate.md)** - 3.510€ (v3.0)

---

## Quick Links

### Projekt-Start
- [Projektübersicht](01_project/overview.md) - Kontext, Team, Timeline
- [Tech-Stack](02_technical/tech_stack.md) - Django, Wagtail, IIIF
- [Bug-Liste (LIVE-VERIFIED)](03_bugs/bug_inventory.md) - 3 echte Bugs gefunden (v3.0)

### Für Meeting (optional)
- [Meeting-Brief](04_meetings/2025-11-03_preparation.md) - Agenda
- [Demo-Fragen](04_meetings/demo_questions.md) - Laura zeigen lassen

### Für Entwicklung
- [Repository-Struktur](02_technical/repository_structure.md)
- [Implementation Plan](07_implementation/immediate_action_plan.md) - Was JETZT tun?
- [Feasibility Analysis](07_implementation/claude_code_feasibility.md) - Machbarkeits-Analyse

### Für Abrechnung
- [Kalkulation (v3.0 FINAL)](05_deliverables/cost_estimate.md) - 3.510€ (verifiziert via Live-Tests)

---

## Versions-Historie

**v3.0 (2025-10-28):** ✅ LIVE-SITE VERIFIKATION ABGESCHLOSSEN
- **KRITISCHE KORREKTUR:** Bug #2 existiert doch! (Viewer rendert nicht)
- Gazetteer funktioniert perfekt (kein Fix nötig)
- Bugs: 2 → 3 (+50%)
- Kosten: 2.340€ → 3.510€ (+50%)
- Methodik: Code-Analyse + Live-Site Browser-Tests
- VERIFICATION_REPORT.md erstellt (10.500 Wörter)

**v2.1 (2025-10-28):** CODE-VERIFIKATION (ZU OPTIMISTISCH!)
- Bugs von 5 auf 2 reduziert
- Bug #2 als "KEIN BUG" eingestuft (FALSCH - nur Code geprüft!)
- Kosten auf 2.340€ geschätzt (zu niedrig)

**v2.0 (2025-10-28):** Vollständiger Knowledge Vault mit strukturierter Ablage
**v1.0 (2025-10-28):** Initiale Analyse (enthielt falsche Annahmen)

---

## Verwendung

Jeder Ordner enthält spezifische Dokumente mit klaren Dateinamen.
Neue Erkenntnisse werden als neue Dateien oder Updates hinzugefügt.
Versions-Historie am Ende jedes Dokuments dokumentiert Änderungen.

**Bei Unsicherheiten:** Immer die v3.0 Dokumente verwenden (nach LIVE-SITE Verifikation)!

## Wichtige Lektion

**Code-Analyse allein reicht nicht!** v2.0 hatte Bug #2 als "nicht existent" eingestuft, weil Template-Code vorhanden war. Live-Browser-Tests zeigten: Viewer rendert trotzdem nicht (JavaScript-Problem). **Impact:** +8h, +1.200€.

**Fazit:** Immer Code-Analyse + Live-Site Tests kombinieren!
