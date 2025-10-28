#!/usr/bin/env python3
"""
Quick verification script for La Sfera bug fixes.
Runs WITHOUT Django - just checks the code changes.
"""

import re
import sys

def check_file(filepath, checks):
    """Run checks on a file and return results."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return False, f"File not found: {filepath}"

    results = []
    all_passed = True

    for check_name, pattern, should_exist in checks:
        matches = re.findall(pattern, content, re.MULTILINE)
        found = len(matches) > 0

        if should_exist:
            passed = found
            status = "[PASS]" if passed else "[FAIL]"
            msg = f"{status} {check_name}: {'FOUND' if found else 'NOT FOUND'}"
            if found:
                msg += f" ({len(matches)} occurrences)"
        else:
            passed = not found
            status = "[PASS]" if passed else "[FAIL]"
            msg = f"{status} {check_name}: {'CORRECTLY REMOVED' if passed else f'STILL EXISTS ({len(matches)} occurrences)'}"

        results.append((passed, msg))
        all_passed = all_passed and passed

    return all_passed, results


def main():
    print("=" * 70)
    print("La Sfera Bug Fix Verification")
    print("=" * 70)
    print()

    # BUG #1: Check for removed hardcoded Urb1
    print("BUG #1: Urb1 Hardcoding Removal")
    print("-" * 70)

    bug1_checks = [
        ("No hardcoded .get(siglum=\"Urb1\")", r'objects\.get\(siglum="Urb1"\)', False),
        ("Uses .filter().first() pattern", r'objects\.filter\(siglum="Urb1"\)\.first\(\)', True),
        ("Has IIIF URL fallback logic", r'filter\(iiif_url__isnull=False\)', True),
    ]

    passed1, results1 = check_file('manuscript/views.py', bug1_checks)

    for _, msg in results1:
        print(f"  {msg}")

    print()

    # BUG #2: Check for page_number implementation
    print("BUG #2: page_number Parameter Implementation")
    print("-" * 70)

    bug2_checks = [
        ("canvas_id variable declared", r'canvas_id = None', True),
        ("page_number conversion logic", r'page_idx = int\(page_number\) - 1', True),
        ("Canvas extraction from manifest", r'canvas_id = canvases\[page_idx\]\["@id"\]', True),
        ("canvas_id passed to template", r'"canvas_id": canvas_id', True),
        ("Logging for resolved pages", r'logger\.info\(f"Resolved page', True),
    ]

    passed2, results2 = check_file('manuscript/views.py', bug2_checks)

    for _, msg in results2:
        print(f"  {msg}")

    print()

    # Check test files exist
    print("Test Infrastructure")
    print("-" * 70)

    import os
    test_files = [
        ('manuscript/management/commands/test_bug_fixes.py', 'Django test command'),
        ('TESTING_BUG_FIXES.md', 'Testing documentation'),
    ]

    all_files_exist = True
    for filepath, description in test_files:
        exists = os.path.exists(filepath)
        all_files_exist = all_files_exist and exists
        status = "[PASS]" if exists else "[FAIL]"
        print(f"  {status} {description}: {filepath}")

    print()
    print("=" * 70)

    # Summary
    if passed1 and passed2 and all_files_exist:
        print("RESULT: [PASS] ALL CHECKS PASSED")
        print()
        print("Code changes look correct! To verify runtime behavior:")
        print("  1. Install dependencies: poetry install")
        print("  2. Run Django test: python manage.py test_bug_fixes")
        print("  3. Or start dev server and test manually")
        return 0
    else:
        print("RESULT: [FAIL] SOME CHECKS FAILED")
        if not passed1:
            print("  - BUG #1 fixes may be incomplete")
        if not passed2:
            print("  - BUG #2 fixes may be incomplete")
        if not all_files_exist:
            print("  - Some test files are missing")
        return 1


if __name__ == '__main__':
    sys.exit(main())
