# La Sfera Static Site MVP

## 🎉 SUCCESS! Der MVP ist fertig!

**Development Server läuft auf:** http://localhost:8080/

## Was ist das?

Dies ist ein **Minimum Viable Product (MVP)** für die Migration von La Sfera von Django/PostgreSQL zu einer statischen Site.

### Was funktioniert bereits:

✅ **YAML → JSON Datenkonvertierung**
- 2 Manuskripte (Urb1, Cam)
- 3 Stanzas mit italienischem Text
- 3 englische Übersetzungen
- 1 Location (Florence)

✅ **Statische HTML-Generierung mit 11ty**
- Homepage mit Übersicht
- Manuskript-Listenseite
- Stanza-Ansicht mit Übersetzungen
- Responsive Design

✅ **Live Development Server**
- Auto-Reload bei Änderungen
- Lokaler Test-Server

## Verzeichnisstruktur

```
static-mvp/
├── data/                    # Quelldaten (YAML)
│   ├── manuscripts/
│   │   ├── Urb1.yaml
│   │   └── Cam.yaml
│   ├── stanzas/
│   │   ├── 01.01.01.yaml
│   │   ├── 01.01.02.yaml
│   │   └── 01.01.03.yaml
│   ├── translations/
│   │   └── 01.01.01.yaml (etc.)
│   └── locations/
│       └── florence.yaml
│
├── src/                     # Templates & Assets
│   ├── _data/              # Generierte JSON-Dateien
│   ├── _includes/          # Layout-Templates
│   │   └── layout.njk
│   ├── index.njk           # Homepage
│   ├── manuscripts/
│   │   └── index.njk
│   └── stanzas/
│       └── index.njk
│
├── scripts/
│   └── build-data.js       # YAML → JSON Konverter
│
├── public/                  # Generierte HTML-Dateien
│   ├── index.html
│   ├── manuscripts/
│   └── stanzas/
│
├── .eleventy.js            # 11ty Konfiguration
└── package.json
```

## Verwendung

### Installation

```bash
npm install
```

### Development Server starten

```bash
npm run dev
```

Öffne dann: http://localhost:8080/

### Production Build

```bash
npm run build
```

Output wird in `public/` generiert.

## Arbeitsablauf

### 1. Daten bearbeiten

Bearbeite YAML-Dateien in `data/`:

```yaml
# data/stanzas/01.01.04.yaml
line_code: "01.01.04"
manuscript: "Urb1"
language: "it"
text: |
  Deine neue Strophe hier...
```

### 2. Neu builden

```bash
npm run build:data  # Konvertiert YAML → JSON
npm run build:11ty  # Generiert HTML
```

Oder alles zusammen:

```bash
npm run build
```

### 3. Live Preview

Der Dev-Server (`npm run dev`) macht das automatisch bei Dateiänderungen!

## Architektur-Konzept

```
YAML (Git)  →  Build Script  →  JSON  →  11ty  →  HTML (GitHub Pages)
    ↓              ↓              ↓       ↓         ↓
 Version      Konverter      Daten   Generator   Output
 Control                    Format   Engine
```

## Nächste Schritte

### Für vollständige Migration:

1. **Datenexport aus Django:**
   - Script schreiben: Django DB → YAML
   - Alle 6 Manuskripte exportieren
   - ~2.000-5.000 Stanzas exportieren
   - Alle Annotations, Folios, Locations

2. **Features hinzufügen:**
   - IIIF Mirador Viewer Integration
   - Client-side Search (Fuse.js)
   - Leaflet-Karte für Gazetteer
   - Annotation-Display

3. **GitHub Actions Setup:**
   - Auto-Build bei Git Push
   - Deploy zu GitHub Pages
   - Issue-to-PR Workflow für neue Annotationen

4. **Styling:**
   - Tailwind CSS Integration
   - Design vom aktuellen Django-Site übernehmen

5. **Testing:**
   - Performance Tests
   - Cross-Browser Tests
   - Mobile Responsive Tests

## Technologie-Stack

- **11ty (Eleventy)** - Static Site Generator
- **Nunjucks** - Template Engine (ähnlich Django Templates)
- **js-yaml** - YAML Parser
- **Node.js** - Build Environment

## Vorteile dieser Architektur

### ✅ Kostenlos
- GitHub Pages: €0/Monat
- Keine Datenbank-Kosten
- Nur Domain: ~€10-15/Jahr

### ✅ Schneller
- Statisches HTML = instant load
- CDN-Distribution
- Keine DB-Queries

### ✅ Sicherer
- Keine SQL Injection
- Keine Server-Side Vulnerabilities
- Minimale Attack Surface

### ✅ Wartbar
- Alle Daten in Git
- Version Control für alles
- Rollback = git revert

### ✅ Nachhaltig
- Überlebt Projekt-Ende
- Keine Hosting-Abhängigkeit
- Langzeit-Archivierung in Git

## Performance

Aktueller MVP:
- **Build Zeit:** ~0.05 Sekunden (3 Seiten)
- **Page Size:** ~3.2 KB (minimales HTML)
- **Load Zeit:** <100ms

Mit vollständigen Daten (~2.000 Stanzas):
- **Build Zeit:** ~2-5 Sekunden erwartet
- **Total Size:** <50 MB
- **Load Zeit:** <1 Sekunde

## Support

Bei Fragen siehe:
- `docs/static-site-migration/` - Vollständige Migrations-Dokumentation (211K)
- `.eleventy.js` - 11ty-Konfiguration
- `scripts/build-data.js` - Build-Script Logik

---

**Status:** ✅ MVP FUNKTIONIERT!
**Nächster Schritt:** Django-Datenexport implementieren
**Erstellt:** 2025-11-04
