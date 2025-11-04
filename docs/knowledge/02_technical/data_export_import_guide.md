# 📦 La Sfera Datenexport - Anleitung

## Schritt-für-Schritt: Echte Daten aus Django exportieren

### ✅ Voraussetzungen

- Docker Desktop installiert ✅
- Docker Desktop **läuft** (muss gestartet sein!)
- Dieses Repository geklont ✅

---

## 🚀 Export-Prozess

### **Schritt 1: Docker Desktop starten**

1. **Docker Desktop öffnen** (Windows-App)
2. Warten bis Docker vollständig gestartet ist (grünes Symbol)
3. Prüfen, ob Docker läuft:

```bash
docker ps
```

Sollte KEINE Fehlermeldung geben.

---

### **Schritt 2: Django + PostgreSQL Container starten**

```bash
# Im lasfera-Hauptverzeichnis:
docker-compose up -d
```

Das startet:
- PostgreSQL Datenbank (Port 5432)
- Django App (Port 8000)

**Warten bis beide Container laufen:**

```bash
docker-compose ps
```

Sollte zeigen:
```
lasfera-app-1   running
lasfera-db-1    running
```

---

### **Schritt 3: Datenexport ausführen**

**OPTION A: Export direkt im Container ausführen (EMPFOHLEN)**

```bash
docker-compose exec app python manage.py export_to_yaml
```

Das exportiert ALLE Daten nach `static-mvp/data/`:
- Manuscripts → `static-mvp/data/manuscripts/`
- Stanzas → `static-mvp/data/stanzas/`
- Translations → `static-mvp/data/translations/`
- Folios → `static-mvp/data/folios/`
- Locations → `static-mvp/data/locations/`
- Annotations → `static-mvp/data/annotations/`

**OPTION B: Mit benutzerdefiniertem Output-Verzeichnis**

```bash
docker-compose exec app python manage.py export_to_yaml --output /app/exported-data
```

---

### **Schritt 4: Export prüfen**

```bash
# Anzahl exportierter Dateien prüfen:
ls -l static-mvp/data/manuscripts/ | wc -l
ls -l static-mvp/data/stanzas/ | wc -l
ls -l static-mvp/data/translations/ | wc -l
```

**Erwartete Werte (ca.):**
- Manuscripts: 6 Dateien
- Stanzas: 2.000-5.000 Dateien
- Translations: 2.000-5.000 Dateien
- Folios: 200-500 Dateien
- Locations: 300-800 Dateien
- Annotations: Variable Anzahl

---

### **Schritt 5: Beispiel-Dateien ansehen**

```bash
# Zeige ein exportiertes Manuskript:
cat static-mvp/data/manuscripts/Urb1.yaml

# Zeige eine exportierte Strophe:
cat static-mvp/data/stanzas/01.01.01.yaml

# Zeige eine Übersetzung:
cat static-mvp/data/translations/01.01.01.yaml
```

---

### **Schritt 6: Statische Site mit echten Daten builden**

```bash
cd static-mvp

# Daten konvertieren (YAML → JSON)
npm run build:data

# HTML generieren
npm run build:11ty

# ODER alles zusammen:
npm run build
```

---

### **Schritt 7: Ergebnis ansehen**

```bash
cd static-mvp
npm run dev
```

Öffne: **http://localhost:8080/**

Jetzt siehst du die ECHTEN Daten aus der Datenbank!

---

## 🐛 Problemlösung

### Docker Desktop startet nicht

- **Lösung:** Docker Desktop neu installieren
- Prüfe Windows-Version (braucht Windows 10/11 Pro oder WSL2)

### "Error: No such container"

```bash
# Container existieren nicht - erstelle sie:
docker-compose up -d --build
```

### "Database connection failed"

```bash
# Warte bis DB gesund ist:
docker-compose logs db

# Sollte zeigen: "database system is ready to accept connections"
```

### Export-Script findet Models nicht

```bash
# Stelle sicher, dass du im Container ausführst:
docker-compose exec app python manage.py export_to_yaml

# NICHT direkt auf Host:
# python manage.py export_to_yaml  ← FALSCH (braucht alle Dependencies)
```

### PyYAML fehlt

Im Docker-Container sollte PyYAML bereits installiert sein (via Poetry).
Falls nicht:

```bash
docker-compose exec app poetry add PyYAML
```

---

## 📊 Export-Statistik

Nach dem Export solltest du sehen:

```
==============================================================
EXPORT SUMMARY
==============================================================
manuscripts                  6 files
stanzas                   XXXX files
translations              XXXX files
folios                     XXX files
locations                  XXX files
annotations                XXX files
==============================================================

✅ Export complete! Files written to: /app/static-mvp/data
```

---

## 🔄 Re-Export (bei geänderten Daten)

Wenn sich Daten in der Django-DB geändert haben:

```bash
# 1. Alte YAML-Dateien löschen (optional)
rm -rf static-mvp/data/*

# 2. Neu exportieren
docker-compose exec app python manage.py export_to_yaml

# 3. Neu builden
cd static-mvp
npm run build
```

---

## 📁 Dateistruktur nach Export

```
static-mvp/data/
├── manuscripts/
│   ├── Urb1.yaml
│   ├── Cam.yaml
│   ├── Yale3.yaml
│   ├── Laur2.yaml
│   ├── Laur3.yaml
│   └── Laur6.yaml
│
├── stanzas/
│   ├── 01.01.01.yaml
│   ├── 01.01.02.yaml
│   ├── 01.01.03.yaml
│   └── ... (tausende Dateien)
│
├── translations/
│   ├── 01.01.01.yaml
│   ├── 01.01.02.yaml
│   └── ...
│
├── folios/
│   ├── Urb1-1r.yaml
│   ├── Urb1-1v.yaml
│   └── ...
│
├── locations/
│   ├── florence.yaml
│   ├── jerusalem.yaml
│   └── ...
│
└── annotations/
    ├── annotation-1.yaml
    ├── annotation-2.yaml
    └── ...
```

---

## ✅ Checkliste

- [ ] Docker Desktop gestartet
- [ ] `docker-compose up -d` ausgeführt
- [ ] Container laufen (`docker-compose ps`)
- [ ] Export ausgeführt (`docker-compose exec app python manage.py export_to_yaml`)
- [ ] Dateien vorhanden (`ls static-mvp/data/manuscripts/`)
- [ ] Build erfolgreich (`cd static-mvp && npm run build`)
- [ ] Dev-Server läuft (`npm run dev`)
- [ ] Seite im Browser geöffnet (http://localhost:8080/)
- [ ] Echte Daten werden angezeigt! 🎉

---

## 🎯 Nächste Schritte nach erfolgreichem Export

1. **Validierung:** Prüfe, ob alle Daten korrekt exportiert wurden
2. **Vergleich:** Vergleiche ein paar Stanzas zwischen Django-Site und Static-Site
3. **Features:** Füge IIIF Viewer, Suche, Karten hinzu
4. **Styling:** Übernehme Design vom Django-Template
5. **GitHub:** Pushe zu GitHub für automatisches Deployment

---

**Fragen? Probleme?**
Siehe [README.md](static-mvp/README.md) im static-mvp Verzeichnis für weitere Infos.
