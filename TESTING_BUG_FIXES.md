# Testing La Sfera Bug Fixes

**Date:** 28. Oktober 2025
**Bugs Fixed:** 2 critical bugs
**Files Modified:**
- `manuscript/views.py` (3 functions modified)
- `manuscript/management/commands/test_bug_fixes.py` (new test command)

---

## Overview of Fixes

### BUG #1: Urb1 Hardcoding (FIXED)
**Problem:** Three manuscripts (Cambridge, Florence, Yale) were inaccessible because the code always fell back to "Urb1" hardcoded manuscript.

**Fix Applied:** Replaced all 5 instances of hardcoded `SingleManuscript.objects.get(siglum="Urb1")` with intelligent fallback logic:
1. Try to find requested manuscript
2. Fall back to ANY manuscript with valid IIIF URL
3. Only use Urb1 as last resort if available

**Locations Fixed:**
- `manuscript/views.py:489-493` - mirador_view exception handler
- `manuscript/views.py:495-500` - mirador_view IIIF URL check
- `manuscript/views.py:505-508` - mirador_view request exception handler
- `manuscript/views.py:547-550` - stanzas view default manuscript
- `manuscript/views.py:707-710` - manuscripts view default manuscript

---

### BUG #2: page_number Parameter Ignored (FIXED)
**Problem:** URL structure accepted `page_number` parameter, but Mirador viewer always opened at page 1.

**Fix Applied:** Implemented canvas_id calculation in `mirador_view`:
1. Fetch IIIF manifest data
2. Convert page_number to 0-indexed canvas index
3. Extract canvas @id from manifest
4. Pass canvas_id to template for Mirador initialization

**Locations Fixed:**
- `manuscript/views.py:502-533` - Added canvas_id calculation logic
- Template already had canvas_id support at `templates/manuscript/mirador.html:19`

---

## Testing Methods

### Method 1: Automated Django Management Command

**Setup (one-time):**
```bash
# Activate virtual environment (if exists)
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Ensure Django is installed
pip install -r requirements.txt
```

**Run tests:**
```bash
python manage.py test_bug_fixes
```

**Expected Output:**
```
=== Testing La Sfera Bug Fixes ===

TEST 1: Checking manuscript database entries...
Found 4 manuscripts in database:
  - Urb1: Biblioteca Apostolica Vaticana (✓ IIIF URL present)
  - Cambridge: Fitzwilliam Museum, Cambridge (✓ IIIF URL present)
  - Florence: Biblioteca Nazionale Centrale (✓ IIIF URL present)
  - Yale3: Beinecke Rare Book and Manuscript Library (✓ IIIF URL present)

TEST 2: Testing manuscript_stanzas view for each manuscript...
  ✓ Urb1: Status 200 OK
  ✓ Cambridge: Status 200 OK
  ✓ Florence: Status 200 OK
  ✓ Yale3: Status 200 OK

TEST 3: Testing Mirador page_number parameter...
Using manuscript Urb1 for page_number test
  Without page_number: canvas_id = None
  ✓ Page 1: canvas_id = https://digi.vatlib.it/iiif/MSS_Urb.lat.1392.pt.A/canvas/p0001
  ✓ Page 5: canvas_id = https://digi.vatlib.it/iiif/MSS_Urb.lat.1392.pt.A/canvas/p0005
  ✓ Page 10: canvas_id = https://digi.vatlib.it/iiif/MSS_Urb.lat.1392.pt.A/canvas/p0010

=== Test Complete ===
```

---

### Method 2: Manual Browser Testing

**Prerequisites:**
1. Start Django development server: `python manage.py runserver`
2. Open browser to `http://localhost:8000`

#### Test BUG #1 Fix (Manuscript Access)

**Test all 4 manuscripts are accessible:**

1. **Vatican (Urb1):**
   - URL: `http://localhost:8000/manuscripts/Urb1/stanzas/`
   - Expected: ✓ Page loads with stanzas and IIIF viewer

2. **Cambridge:**
   - URL: `http://localhost:8000/manuscripts/Cambridge/stanzas/`
   - Expected: ✓ Page loads (previously would fail)

3. **Florence:**
   - URL: `http://localhost:8000/manuscripts/Florence/stanzas/`
   - Expected: ✓ Page loads (previously would fail)

4. **Yale (Yale3):**
   - URL: `http://localhost:8000/manuscripts/Yale3/stanzas/`
   - Expected: ✓ Page loads (previously would fail)

**Pass Criteria:** All 4 URLs return 200 status and display stanzas.

---

#### Test BUG #2 Fix (Page Navigation)

**Test Mirador opens at specified page:**

1. **Get manuscript ID:**
   ```bash
   python manage.py shell
   >>> from manuscript.models import SingleManuscript
   >>> ms = SingleManuscript.objects.get(siglum="Urb1")
   >>> print(ms.id)
   1  # (example ID)
   ```

2. **Test URLs with different page numbers:**
   - `http://localhost:8000/mirador/1/1/` → Opens at page 1 (first page)
   - `http://localhost:8000/mirador/1/10/` → Opens at page 10
   - `http://localhost:8000/mirador/1/50/` → Opens at page 50

3. **Visual verification:**
   - Check browser developer console for log: `Resolved page X to canvas_id: ...`
   - Verify Mirador viewer displays the correct page (check page counter in viewer)
   - Page number in URL should match visible page in viewer

**Pass Criteria:** Mirador viewer opens at the exact page specified in URL.

---

### Method 3: Code Inspection (No Server Required)

**Verify fixes by reading the code:**

1. **Check BUG #1 fixes:**
   ```bash
   # Search for remaining hardcoded "Urb1" references
   grep -n 'objects.get(siglum="Urb1")' manuscript/views.py
   ```
   - Expected: No results (all replaced with `.filter().first()`)

2. **Check BUG #2 fix:**
   ```bash
   # Verify canvas_id calculation exists
   grep -n "canvas_id" manuscript/views.py
   ```
   - Expected: Lines 503, 515, 531 show canvas_id logic

3. **Review changes:**
   ```bash
   git diff manuscript/views.py
   ```

---

## Quick Test Summary

| Test | Method | Pass Criteria | Status |
|------|--------|---------------|--------|
| Urb1 accessible | Browser: `/manuscripts/Urb1/stanzas/` | Page loads | ✓ |
| Cambridge accessible | Browser: `/manuscripts/Cambridge/stanzas/` | Page loads | ⏳ |
| Florence accessible | Browser: `/manuscripts/Florence/stanzas/` | Page loads | ⏳ |
| Yale accessible | Browser: `/manuscripts/Yale3/stanzas/` | Page loads | ⏳ |
| Page navigation | Browser: `/mirador/1/10/` | Opens at page 10 | ⏳ |
| Automated tests | Command: `python manage.py test_bug_fixes` | All tests pass | ⏳ |

---

## Notes for Laura (Project Lead)

**To test these fixes on the live site:**

1. Deploy the changes to staging/production server
2. Test each manuscript URL:
   - https://lasfera.rrchnm.org/manuscripts/Urb1/stanzas/
   - https://lasfera.rrchnm.org/manuscripts/Cambridge/stanzas/
   - https://lasfera.rrchnm.org/manuscripts/Florence/stanzas/
   - https://lasfera.rrchnm.org/manuscripts/Yale3/stanzas/

3. Test page navigation by adding a page number to any Mirador URL

**What you should see:**
- All manuscripts load successfully (no 404 or 500 errors)
- Mirador viewer opens at the correct page when page_number is specified

**Known limitations:**
- If a manuscript truly has no IIIF URL configured, it will still fail (but gracefully)
- Page numbers beyond the manuscript's length will fall back to page 1

---

## For Developers

**Running unit tests:**
```bash
python manage.py test manuscript.tests.test_views
```

**Checking logs:**
```bash
# Look for these log messages
tail -f logs/django.log | grep "Resolved page"
tail -f logs/django.log | grep "manuscript"
```

**Reverting changes (if needed):**
```bash
git checkout HEAD -- manuscript/views.py
```

---

**End of Testing Guide**
Generated with Claude Code
