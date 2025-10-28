# La Sfera Digital Edition - Projektübersicht

**Letzte Aktualisierung:** 28. Oktober 2025

---

## Projekt-Kontext

### Was ist La Sfera?

Ein florentinisches Lehrgedicht (ca. 1430) von Goro Dati über:
- Kosmologie und Himmelskunde
- Navigation und Seefahrt
- Geografie des Mittelmeerraums
- Naturphänomene

**Wissenschaftlicher Wert:** Erste kritische digitale Edition (bisher nur mid-19th-century Print-Edition). Parallel erscheint eine englische Übersetzung bei Italica Press (Fall 2025).

---

## Projektgeschichte

**2023-2024:** NEH-gefördertes Projekt bei RRCHNM (GMU)
- 1,5 Jahre Entwicklung
- Zu 90% fertiggestellt
- **Problem:** NEH-Förderung endete vorzeitig
- **Problem:** GMU kann nicht weiterentwickeln (interne Probleme)

**Oktober 2025:** Neustart
- Laura Morreale hat neue Finanzierung gesichert
- Suche nach externem Entwickler
- DH Craft als Partner identifiziert

---

## Team & Kontakte

### Wissenschaftliches Team

**Projektleitung:**
- **Laura K. Morreale**
- E-Mail: lmorreale3@gmail.com
- Affiliation: Harvard University / Princeton University
- Rolle: Principal Investigator, Content-Verantwortung

**Wissenschaftliches Team:**
- **Carrie Beneš** - Mitarbeiterin
- **Laura Ingallinella** - Mitarbeiterin

### Institution

**RRCHNM (Roy Rosenzweig Center for History and New Media)**
- George Mason University, USA
- Website: https://rrchnm.org/
- Renommiertes DH-Zentrum seit 1994
- Projekte: Zotero, Omeka, viele digitale Editionen

### Entwicklung

**DH Craft - Digital Humanities Craft OG**
- **Christopher Pollin**
- E-Mail: christopher.pollin@dhcraft.org
- Rolle: Technische Entwicklung, Bug-Fixes, IIIF-Integration
- Standort: Österreich

---

## Projektziele

### Hauptziele (bis Juni 2026)

1. **Gazetteer-Bugs beheben**
   - Karte funktional machen
   - Performance optimieren
   - Verlinkung mit Edition sicherstellen

2. **IIIF-Integration vervollständigen**
   - Viewer auf `/stanzas/` Seite
   - Synchronisation Text ↔ Bilder
   - Canvas-Navigation korrigieren

3. **Weitere Bugs fixen** (siehe Bug-Inventory)
   - Urb1-Hardcoding entfernen
   - Silent Exceptions beheben
   - Code-Quality verbessern

4. **Optional: Hosting-Export**
   - Export zu neuem Host (falls gewünscht)
   - Dokumentation für Betrieb

---

## Timeline

**Projektstart:** Mitte November 2025 (nach Vertragsunterzeichnung)
**Deadline:** Ende akademisches Jahr 2025/26 (Juni 2026)
**Entwicklungszeit:** 6-8 Wochen (bei Vollzeit-Äquivalent)
**Puffer:** 4-5 Monate bis Deadline

### Phasen

**Phase 1 (2 Wochen):** Kritische Bugs
- Urb1-Hardcoding entfernen
- Mirador page_number fixen
- Silent Exceptions beheben

**Phase 2 (3-4 Wochen):** IIIF-Integration
- Mirador in Stanzas-View
- Canvas-Synchronisation
- Testing mit allen Manuscripts

**Phase 3 (1-2 Wochen):** Gazetteer & Polish
- Gazetteer-Bugs fixen
- Performance-Optimierung
- User Acceptance Testing

**Phase 4 (Optional):** Hosting-Export
- Server-Migration
- Deployment-Dokumentation
- Post-Launch Support

---

## Budget & Kalkulation

**Stundensatz:** 150€
**Overhead-Faktor:** 1.55 (55% für Einarbeitung, Kommunikation, Testing, Puffer)

### Szenarien

**Best Case:** 40h × 150€ = **6.000€**
- Nur kritische Bugs
- Templates sind fast fertig
- Keine Überraschungen

**Realistic Case:** 54h × 150€ = **8.100€**
- Alle bekannten Bugs
- IIIF-Integration vollständig
- Gazetteer funktionsfähig

**Worst Case:** 67h × 150€ = **10.050€**
- Zusätzliche unbekannte Bugs
- Komplexe IIIF-Probleme
- Gazetteer-Refactoring nötig

**Empfohlenes Szenario:** Realistic Case (~8.000€)

---

## Erfolgskriterien

### Must-Have (für Launch)

- [ ] Alle Manuscripts (nicht nur Urb1) funktionieren
- [ ] IIIF-Viewer zeigt Bilder auf `/stanzas/`
- [ ] Gazetteer-Karte rendert Marker
- [ ] Keine JavaScript-Errors in Console
- [ ] Page-Navigation in Mirador funktioniert

### Nice-to-Have

- [ ] Performance-Optimierung
- [ ] Test-Coverage verbessert
- [ ] Deployment-Dokumentation
- [ ] CI/CD Pipeline

### Launch-Ready Definition

"Website funktioniert ohne kritische Bugs, alle Hauptfeatures (Edition, Gazetteer, IIIF-Viewer) sind für Nutzer verwendbar."

---

## Kommunikation

**Primärkanal:** E-Mail
**Meetings:** Zoom, wöchentlich oder bei Bedarf
**Bug-Tracking:** GitHub Issues (nach Setup)
**Code-Review:** Pull Requests auf GitHub

**Response-Zeit-Erwartung:**
- Kunde → Entwickler: 24-48h
- Entwickler → Kunde: 24h (Blocker sofort)

---

## Risiken & Mitigation

### Technische Risiken

**Risiko:** IIIF-Manifeste externer Institutionen ändern sich
**Mitigation:** Lokale Manifest-Kopien als Backup

**Risiko:** Mehr Bugs als identifiziert
**Mitigation:** Puffer (20%) eingerechnet, Milestone-Zahlung

**Risiko:** Gazetteer-Performance-Problem
**Mitigation:** Pagination/Clustering wenn nötig

### Organisatorische Risiken

**Risiko:** Langsame Review-Zyklen
**Mitigation:** SLA vereinbaren (48h Response)

**Risiko:** Scope Creep
**Mitigation:** Change Request Prozess, klare Abgrenzung

**Risiko:** Server-Zugang verzögert sich
**Mitigation:** Lokale Entwicklung parallel möglich

---

## Nächste Schritte

### Vor Vertragsunterzeichnung

- [ ] Meeting am 3. oder 11. November 2025
- [ ] Laura demonstriert Bugs
- [ ] Budget final bestätigt
- [ ] Finales Angebot erstellt

### Nach Vertragsunterzeichnung

- [ ] SSH-Zugang zu Servern
- [ ] GitHub Collaborator-Zugang
- [ ] Kick-off Call
- [ ] Entwicklung Start

### Erste Woche

- [ ] Lokale Entwicklungsumgebung aufsetzen
- [ ] Bug #1 (Urb1) fixen
- [ ] Bug #3 (page_number) fixen
- [ ] First Review mit Laura

---

## Referenzen

- **Live-Site:** https://lasfera.rrchnm.org/
- **Dev-Site:** https://dev.lasfera.rrchnm.org/
- **Repository:** https://github.com/chnm/lasfera
- **Projekt-Website:** https://sites.google.com/ncf.edu/sfera-project/home
- **DB-Doku:** https://dbdocs.io/hepplerj/lasfera

---

**Version:** 2.0
**Nächstes Update:** Nach Meeting mit Laura
