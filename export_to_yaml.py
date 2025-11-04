#!/usr/bin/env python
"""
Export La Sfera data from Django database to YAML files
This script can run with minimal dependencies
"""

import os
import sys
import django
import yaml
from pathlib import Path
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Add minimal apps to avoid loading everything
os.environ['DJANGO_INSTALLED_APPS'] = 'manuscript,textannotation'

try:
    django.setup()
except Exception as e:
    print(f"Warning: Full Django setup failed: {e}")
    print("Attempting minimal setup...")

# Now import models
try:
    from manuscript.models import (
        SingleManuscript, Stanza, StanzaTranslated, Folio,
        Location, LocationAlias, Library, LineCode
    )
    from textannotation.models import TextAnnotation
    print("✓ Models imported successfully")
except ImportError as e:
    print(f"Error importing models: {e}")
    print("\nTrying direct database export instead...")
    sys.exit(1)

# Output directories
OUTPUT_BASE = Path('static-mvp/data')
OUTPUT_BASE.mkdir(parents=True, exist_ok=True)

def to_yaml_safe(value):
    """Convert value to YAML-safe format"""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.isoformat()
    if hasattr(value, '__dict__'):
        return str(value)
    return value

def export_manuscripts():
    """Export all manuscripts to YAML"""
    output_dir = OUTPUT_BASE / 'manuscripts'
    output_dir.mkdir(parents=True, exist_ok=True)

    manuscripts = SingleManuscript.objects.all()
    count = manuscripts.count()

    print(f"\nExporting {count} manuscripts...")

    for ms in manuscripts:
        data = {
            'siglum': ms.siglum,
            'shelfmark': ms.shelfmark or '',
            'library': ms.library.name if ms.library else '',
            'library_city': f"{ms.library.city}" if ms.library else '',
        }

        # Digital resources
        if ms.iiif_url:
            data['iiif_url'] = ms.iiif_url
        if ms.digitized_url:
            data['digitized_url'] = ms.digitized_url
        if ms.gazetteer_url:
            data['gazetteer_url'] = ms.gazetteer_url

        # Description
        if ms.provenance:
            data['description'] = str(ms.provenance)

        # Physical info
        data['lost'] = ms.manuscript_lost or False
        data['destroyed'] = ms.manuscript_destroyed or False

        # Codex info (if exists)
        try:
            codex = ms.codex_set.first()
            if codex:
                data['codex'] = {}
                if codex.support:
                    data['codex']['support'] = codex.support
                if codex.height and codex.width:
                    data['codex']['dimensions'] = f"{codex.height} × {codex.width} mm"
                if codex.folia:
                    data['codex']['folios'] = codex.folia
        except:
            pass

        # Text decoration
        try:
            decoration = ms.textdecoration_set.first()
            if decoration:
                data['text_decoration'] = {
                    'illuminated': bool(decoration.illumination),
                    'decorated': bool(decoration.white_vine_work),
                }
        except:
            pass

        # Editorial status
        try:
            status = ms.editorialstatus_set.first()
            if status:
                data['editorial_status'] = {
                    'priority': status.editorial_priority or 5,
                    'status': 'complete' if status.collated else 'in_progress'
                }
        except:
            pass

        # Metadata
        if hasattr(ms, 'created_at'):
            data['created_at'] = to_yaml_safe(ms.created_at)
        if hasattr(ms, 'updated_at'):
            data['updated_at'] = to_yaml_safe(ms.updated_at)

        # Write to file
        filename = f"{ms.siglum}.yaml"
        filepath = output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

        print(f"  ✓ {filename}")

    print(f"✓ Exported {count} manuscripts")
    return count

def export_stanzas():
    """Export all stanzas to YAML"""
    output_dir = OUTPUT_BASE / 'stanzas'
    output_dir.mkdir(parents=True, exist_ok=True)

    # Only export Italian stanzas
    stanzas = Stanza.objects.filter(language='it').order_by('stanza_line_code_starts')
    count = stanzas.count()

    print(f"\nExporting {count} stanzas...")

    for i, stanza in enumerate(stanzas, 1):
        line_code = stanza.stanza_line_code_starts

        if not line_code:
            print(f"  ⚠ Skipping stanza without line_code (id={stanza.id})")
            continue

        data = {
            'line_code': line_code,
            'language': stanza.language or 'it',
            'text': str(stanza.stanza_text) if stanza.stanza_text else '',
        }

        # Manuscript - try to determine from folios
        try:
            first_folio = stanza.folios.first()
            if first_folio and first_folio.related_manuscript:
                data['manuscript'] = first_folio.related_manuscript.siglum
            else:
                data['manuscript'] = 'Unknown'
        except:
            data['manuscript'] = 'Unknown'

        # Notes
        if stanza.stanza_notes:
            data['notes'] = str(stanza.stanza_notes)

        # Folios
        try:
            folios = stanza.folios.all()
            if folios:
                data['folios'] = [
                    f"{f.related_manuscript.siglum}-{f.folio_number}"
                    for f in folios if f.related_manuscript
                ]
        except:
            pass

        # Metadata
        if hasattr(stanza, 'created_at') and stanza.created_at:
            data['created_at'] = to_yaml_safe(stanza.created_at)
        if hasattr(stanza, 'updated_at') and stanza.updated_at:
            data['updated_at'] = to_yaml_safe(stanza.updated_at)

        # Write to file
        filename = f"{line_code}.yaml"
        filepath = output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

        if i % 100 == 0:
            print(f"  ... {i}/{count}")

    print(f"✓ Exported {count} stanzas")
    return count

def export_translations():
    """Export all translations to YAML"""
    output_dir = OUTPUT_BASE / 'translations'
    output_dir.mkdir(parents=True, exist_ok=True)

    translations = StanzaTranslated.objects.filter(language='en').order_by('stanza_line_code_starts')
    count = translations.count()

    print(f"\nExporting {count} translations...")

    for i, trans in enumerate(translations, 1):
        line_code = trans.stanza_line_code_starts

        if not line_code:
            print(f"  ⚠ Skipping translation without line_code (id={trans.id})")
            continue

        data = {
            'line_code': line_code,
            'language': trans.language or 'en',
            'translated_text': str(trans.stanza_text) if trans.stanza_text else '',
        }

        # Translator (if we have that info)
        data['translator'] = "Laura Morreale"  # Default based on project info

        # Translation notes
        if trans.stanza_notes:
            data['translation_notes'] = str(trans.stanza_notes)

        # Metadata
        if hasattr(trans, 'created_at') and trans.created_at:
            data['created_at'] = to_yaml_safe(trans.created_at)
        if hasattr(trans, 'updated_at') and trans.updated_at:
            data['updated_at'] = to_yaml_safe(trans.updated_at)

        # Write to file
        filename = f"{line_code}.yaml"
        filepath = output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

        if i % 100 == 0:
            print(f"  ... {i}/{count}")

    print(f"✓ Exported {count} translations")
    return count

def export_locations():
    """Export all locations to YAML"""
    output_dir = OUTPUT_BASE / 'locations'
    output_dir.mkdir(parents=True, exist_ok=True)

    locations = Location.objects.all()
    count = locations.count()

    print(f"\nExporting {count} locations...")

    for loc in locations:
        # Create slug from name
        slug = loc.slug if hasattr(loc, 'slug') and loc.slug else loc.name.lower().replace(' ', '-').replace("'", '')

        data = {
            'id': slug,
            'name': loc.name,
        }

        # Geographic coordinates
        if loc.latitude:
            data['latitude'] = float(loc.latitude)
        if loc.longitude:
            data['longitude'] = float(loc.longitude)
        if loc.modern_country:
            data['modern_country'] = loc.modern_country

        # Description
        if loc.description:
            data['description'] = str(loc.description)

        # Type
        if hasattr(loc, 'place_type') and loc.place_type:
            data['location_type'] = loc.place_type

        # Metadata
        if hasattr(loc, 'created_at') and loc.created_at:
            data['created_at'] = to_yaml_safe(loc.created_at)
        if hasattr(loc, 'updated_at') and loc.updated_at:
            data['updated_at'] = to_yaml_safe(loc.updated_at)

        # Write to file
        filename = f"{slug}.yaml"
        filepath = output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

        print(f"  ✓ {filename}")

    print(f"✓ Exported {count} locations")
    return count

def main():
    """Main export function"""
    print("=" * 60)
    print("La Sfera Data Export: Django → YAML")
    print("=" * 60)

    try:
        # Export all data types
        stats = {}
        stats['manuscripts'] = export_manuscripts()
        stats['stanzas'] = export_stanzas()
        stats['translations'] = export_translations()
        stats['locations'] = export_locations()

        # Summary
        print("\n" + "=" * 60)
        print("EXPORT SUMMARY")
        print("=" * 60)
        for key, value in stats.items():
            print(f"{key:20} {value:>6} files")
        print("=" * 60)
        print(f"\n✅ Export complete! Files written to: {OUTPUT_BASE.absolute()}")

    except Exception as e:
        print(f"\n❌ Export failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
