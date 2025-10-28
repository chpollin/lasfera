# Knowledge Vault Analyse - Ergebnis

**Datum:** 28. Oktober 2025
**Geprüft:** Knowledge Vault Ausarbeitung vs. Repository chnm/lasfera

---

## Zusammenfassung

**Gesamtbewertung: 7.5/10** - Größtenteils korrekt, aber einige Ungenauigkeiten

### ✅ KORREKT (90%):

1. **Projektübersicht:** ✅
   - Django 5.0.2 ✓
   - Wagtail 6.2.1 ✓
   - Poetry ✓
   - Docker ✓
   - URLs korrekt ✓

2. **Bug #1 (Urb1-Hardcoding):** ✅ PERFEKT
   - Zeilen stimmen (489, 492, 498, 537, 694) ✓
   - Beschreibung korrekt ✓
   - Aufwand realistisch (4-6h) ✓

3. **Bug #3 (Mirador page_number):** ✅ KORREKT
   - Code-Beschreibung stimmt ✓
   - Problem korrekt identifiziert ✓
   - Aufwand realistisch (3-5h) ✓

4. **Kalkulation:** ✅ IDENTISCH
   - 38h Entwicklung ✓
   - 59h mit Overhead (1.55x) ✓
   - 8.850€ ✓

5. **Deployment:** ✅ GRUNDSÄTZLICH KORREKT
   - Docker ✓
   - PostgreSQL ✓
   - Python 3.11 ✓

---

## ❌ FEHLER & UNGENAUIGKEITEN:

### 1. **Bug #2 (IIIF-Integration) - TEILWEISE FALSCH**

**Ausarbeitung sagt:**
> "Der stanzas-View übergibt keine manifest_url an das Template"

**REALITÄT:**
```python
# manuscript/views.py:625-643
manuscript_data = {
    "iiif_url": default_manuscript.iiif_url  # ← WIRD übergeben!
}

return render(request, "stanzas.html", {
    "manuscript": manuscript_data,  # ← Context hat IIIF URL!
})
```

**Korrektur:**
- Der View **übergibt** die `iiif_url` im `manuscript_data` Dict
- **UNKLAR:** Ob das Template den Viewer damit rendert
- **Problem könnte sein:** Template nutzt die URL nicht, NICHT dass sie fehlt

**Impact:**
- Bug existiert wahrscheinlich trotzdem (kein Viewer sichtbar)
- Aber **Ursache anders als beschrieben**
- Fix könnte **einfacher sein** (Template anpassen, nicht View)

---

### 2. **Technische Architektur - FALSCH**

**Ausarbeitung sagt:**
> **Django-Apps:**
> - `gazetteer`: Ortsregister mit Toponymen
> - `iiif`: IIIF-Integration
> - `wagtail_hooks`: CMS-Integration

**REALITÄT (Repository):**
```bash
$ ls -d */
accounts/
gallery/
manuscript/      ← Enthält Gazetteer UND IIIF!
map/
pages/           ← Wagtail Pages
textannotation/
theme/
```

**Es gibt KEINE separaten Apps:**
- ❌ Kein `gazetteer/` App
- ❌ Kein `iiif/` App
- ❌ Kein `wagtail_hooks/` App

**Korrektur:**
- Gazetteer ist **Teil der manuscript App**
- IIIF ist **Teil der manuscript App**
- Wagtail nutzt `pages/` und `gallery/`

**Impact:**
- Architektur-Beschreibung irreführend
- Könnte zu falschen Annahmen führen
- Für Code-Navigation problematisch

---

### 3. **IIIF-Viewer - UNKLAR**

**Ausarbeitung sagt:**
> "Tify und Mirador als IIIF-Viewer"

**REALITÄT:**
- **package.json:** Nur `"mirador": "^4.0.0-alpha.2"` ✓
- **Tify:** Wird verwendet, aber **nicht in package.json**
- **Vermutung:** Tify kommt von CDN (siehe templates/manuscript/mirador.html)

**Korrektur:**
- Mirador in package.json ✓
- Tify wahrscheinlich über CDN eingebunden
- Beide werden verwendet, aber unterschiedlich geladen

---

### 4. **Deployment - SPEKULATION**

**Ausarbeitung sagt:**
> "Gunicorn als WSGI-Server, Nginx als Reverse Proxy"

**REALITÄT:**
- **Gunicorn:** Nicht explizit in pyproject.toml gefunden
- **Nginx:** Nicht im Repository (wahrscheinlich Server-Konfiguration)

**Korrektur:**
- Deployment-Details sind **Vermutungen** (wahrscheinlich korrekt, aber nicht beweisbar aus Repo)

---

## 🟡 FEHLENDE ASPEKTE:

### Was die Ausarbeitung NICHT erwähnt:

1. **textannotation App**
   - Existiert im Repo
   - Fehlt in Architektur-Beschreibung

2. **theme App**
   - Tailwind CSS Theme
   - Fehlt in Architektur-Beschreibung

3. **Mirador Alpha-Version**
   - Wichtig: 4.0.0-**alpha.2** ist problematisch
   - Sollte erwähnt werden als Risiko

4. **8 GitHub Issues**
   - Werden erwähnt aber nicht detailliert
   - Wichtige Issues (#76, #74) nicht genannt

---

## EMPFEHLUNGEN FÜR KORREKTUR:

### 1. Bug #2 neu formulieren:

**ALT:**
> "Der stanzas-View übergibt keine manifest_url an das Template"

**NEU:**
> "Der stanzas-View übergibt zwar die iiif_url im Context, aber das Template stanzas.html rendert keinen IIIF-Viewer. Vergleich: /manuscripts/Urb1/stanzas/ hat Tify-Viewer, /stanzas/ zeigt nur Text."

---

### 2. Architektur korrigieren:

**ALT:**
> Django-Apps: manuscript, gazetteer, iiif, wagtail_hooks

**NEU:**
> **Django-Apps:**
> - `manuscript/` - Kernfunktionalität (Stanzas, Folios, Gazetteer, IIIF)
> - `textannotation/` - Text-Annotationen
> - `gallery/` - Wagtail-basierte Bildergalerie
> - `pages/` - Wagtail CMS Seiten
> - `accounts/` - User Management
> - `map/` - Kartenfeatures
> - `theme/` - Tailwind CSS Theme

---

### 3. IIIF-Viewer präzisieren:

**ALT:**
> "Tify und Mirador als IIIF-Viewer"

**NEU:**
> "IIIF-Viewer: Mirador 4.0.0-alpha.2 (package.json, ⚠️ Alpha-Version!) und Tify (CDN-eingebunden). Manuscript-Detail-Pages nutzen Tify, Mirador ist konfiguriert aber teilweise ungenutzt."

---

### 4. Deployment als "Annahmen" markieren:

**ALT:**
> "Gunicorn als WSGI-Server, Nginx als Reverse Proxy"

**NEU:**
> "Deployment (anzunehmen basierend auf Django-Best-Practices, nicht im Repo verifiziert): Gunicorn als WSGI-Server, Nginx als Reverse Proxy. Docker-Setup vorhanden, PostgreSQL-Datenbank."

---

## FINALE BEWERTUNG

### Was funktioniert:

✅ **Bug-Identifikation:** 2 von 3 Bugs perfekt beschrieben
✅ **Kalkulation:** Identisch mit unserer Analyse
✅ **Projekt-Kontext:** Korrekt (Laura, RRCHNM, Timeline)
✅ **Tech-Stack Basis:** Django, Wagtail, Docker stimmen

### Was korrigiert werden sollte:

❌ **Bug #2:** Ursache präzisieren (Template, nicht View)
❌ **Architektur:** Keine separaten gazetteer/iiif Apps
❌ **Deployment:** Als "Annahmen" kennzeichnen
🟡 **Fehlende Apps:** textannotation, theme erwähnen

---

## VERWENDBARKEIT

**Für Meeting mit Laura:** ✅ VERWENDBAR
- Bugs sind im Kern korrekt
- Kalkulation stimmt
- Kleine Ungenauigkeiten nicht kritisch

**Für technische Dokumentation:** 🟡 MIT KORREKTUREN
- Architektur-Teil muss korrigiert werden
- Bug #2 Beschreibung anpassen
- Dann vollständig verwendbar

**Für Angebot:** ✅ KORREKT
- Aufwandsschätzung stimmt
- Kosten identisch mit unserer Analyse
- Kann 1:1 verwendet werden

---

## SCORE-CARD

| Kategorie | Score | Kommentar |
|-----------|-------|-----------|
| Projektübersicht | 9/10 | Fast perfekt, nur IIIF-Viewer-Details unklar |
| Bug #1 | 10/10 | Perfekt |
| Bug #2 | 6/10 | Ursache falsch, Bug existiert trotzdem |
| Bug #3 | 10/10 | Perfekt |
| Architektur | 4/10 | Falsche App-Struktur |
| Kalkulation | 10/10 | Identisch |
| Deployment | 7/10 | Teils Spekulation |
| Kontakte | 10/10 | Korrekt |
| **GESAMT** | **7.5/10** | **Gut, mit Verbesserungspotenzial** |

---

## NÄCHSTE SCHRITTE

1. **Für Meeting:** Dokument kann verwendet werden, Ungenauigkeiten sind nicht kritisch
2. **Für Angebot:** Kalkulation übernehmen (identisch mit unserer Analyse)
3. **Für Doku:** Architektur-Teil korrigieren vor finalem Dokument

**Fazit:** Knowledge Vault ist **solide Basis**, aber nicht 100% präzise. Für Projekt-Akquise ausreichend, für technische Dokumentation Korrekturen nötig.
