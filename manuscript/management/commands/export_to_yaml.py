"""
Export La Sfera data from Django database to YAML files
Django Management Command

Usage:
    python manage.py export_to_yaml
    or
    docker-compose exec app python manage.py export_to_yaml
"""

from django.core.management.base import BaseCommand
from manuscript.models import (
    SingleManuscript, Stanza, StanzaTranslated, Folio,
    Location, LocationAlias, Library
)
from textannotation.models import TextAnnotation
import yaml
from pathlib import Path
from datetime import datetime


class Command(BaseCommand):
    help = 'Export La Sfera data to YAML files for static site'

    def add_arguments(self, parser):
        parser.add_argument(
            '--output',
            type=str,
            default='static-mvp/data',
            help='Output directory for YAML files'
        )

    def handle(self, *args, **options):
        output_base = Path(options['output'])
        output_base.mkdir(parents=True, exist_ok=True)

        self.stdout.write("=" * 60)
        self.stdout.write("La Sfera Data Export: Django → YAML")
        self.stdout.write("=" * 60)

        stats = {}
        stats['manuscripts'] = self.export_manuscripts(output_base)
        stats['stanzas'] = self.export_stanzas(output_base)
        stats['translations'] = self.export_translations(output_base)
        stats['folios'] = self.export_folios(output_base)
        stats['locations'] = self.export_locations(output_base)
        stats['annotations'] = self.export_annotations(output_base)

        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("EXPORT SUMMARY"))
        self.stdout.write("=" * 60)
        for key, value in stats.items():
            self.stdout.write(f"{key:20} {value:>6} files")
        self.stdout.write("=" * 60)
        self.stdout.write(
            self.style.SUCCESS(f"\n✅ Export complete! Files written to: {output_base.absolute()}")
        )

    def to_yaml_safe(self, value):
        """Convert value to YAML-safe format"""
        if value is None:
            return None
        if isinstance(value, datetime):
            return value.isoformat()
        return value

    def export_manuscripts(self, output_base):
        """Export all manuscripts to YAML"""
        output_dir = output_base / 'manuscripts'
        output_dir.mkdir(parents=True, exist_ok=True)

        manuscripts = SingleManuscript.objects.select_related('library').all()
        count = 0

        self.stdout.write(f"\nExporting manuscripts...")

        for ms in manuscripts:
            data = {
                'siglum': ms.siglum,
                'shelfmark': ms.shelfmark or '',
            }

            # Library info
            if ms.library:
                data['library'] = ms.library.library
                data['library_city'] = ms.library.city

            # Digital resources
            if ms.iiif_url:
                data['iiif_url'] = ms.iiif_url
            if ms.digitized_url:
                data['digitized_url'] = ms.digitized_url
            if ms.gazetteer_url:
                data['gazetteer_url'] = ms.gazetteer_url
            if ms.purl_url:
                data['purl_url'] = ms.purl_url

            # Description
            if ms.provenance:
                data['description'] = str(ms.provenance)

            # Status
            data['lost'] = ms.manuscript_lost
            data['destroyed'] = ms.manuscript_destroyed

            # Codex info
            try:
                codex = ms.codex_set.first()
                if codex:
                    codex_data = {}
                    if codex.support:
                        codex_data['support'] = codex.support
                    if codex.binding:
                        codex_data['binding'] = codex.binding
                    if codex.height and codex.width:
                        codex_data['dimensions'] = f"{codex.height} × {codex.width} mm"
                    if codex.folia:
                        codex_data['folios'] = codex.folia
                    if codex.date:
                        codex_data['date'] = codex.date
                    if codex.lines_per_page:
                        codex_data['lines_per_page'] = codex.lines_per_page

                    if codex_data:
                        data['codex'] = codex_data
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  Warning: Could not export codex for {ms.siglum}: {e}"))

            # Text decoration
            try:
                decoration = ms.textdecoration_set.first()
                if decoration:
                    dec_data = {}
                    if decoration.text_script:
                        dec_data['text_script'] = decoration.text_script
                    if decoration.illumination:
                        dec_data['illuminated'] = True
                    if decoration.white_vine_work:
                        dec_data['decorated'] = True
                    if decoration.maps:
                        dec_data['has_maps'] = True
                    if decoration.diagrams:
                        dec_data['has_diagrams'] = True

                    if dec_data:
                        data['text_decoration'] = dec_data
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  Warning: Could not export decoration for {ms.siglum}: {e}"))

            # Editorial status
            try:
                status = ms.editorialstatus_set.first()
                if status:
                    status_data = {}
                    if status.editorial_priority:
                        status_data['priority'] = status.editorial_priority
                    status_data['collated'] = status.collated
                    if status.access:
                        status_data['access'] = status.access

                    if status_data:
                        data['editorial_status'] = status_data
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"  Warning: Could not export status for {ms.siglum}: {e}"))

            # Metadata
            if hasattr(ms, 'created_at') and ms.created_at:
                data['created_at'] = self.to_yaml_safe(ms.created_at)
            if hasattr(ms, 'updated_at') and ms.updated_at:
                data['updated_at'] = self.to_yaml_safe(ms.updated_at)

            # Write YAML file
            filename = f"{ms.siglum}.yaml"
            filepath = output_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

            count += 1
            self.stdout.write(f"  ✓ {filename}")

        self.stdout.write(self.style.SUCCESS(f"✓ Exported {count} manuscripts"))
        return count

    def export_stanzas(self, output_base):
        """Export all Italian stanzas to YAML"""
        output_dir = output_base / 'stanzas'
        output_dir.mkdir(parents=True, exist_ok=True)

        stanzas = Stanza.objects.filter(language='it').prefetch_related('folios', 'folios__manuscript').order_by('stanza_line_code_starts')
        count = 0

        self.stdout.write(f"\nExporting stanzas...")

        for i, stanza in enumerate(stanzas, 1):
            line_code = stanza.stanza_line_code_starts

            if not line_code:
                self.stdout.write(self.style.WARNING(f"  ⚠ Skipping stanza without line_code (id={stanza.id})"))
                continue

            data = {
                'line_code': line_code,
                'language': stanza.language or 'it',
            }

            # Text
            if stanza.stanza_text:
                # Strip HTML if present
                text = str(stanza.stanza_text)
                # Basic HTML stripping (you might want to use BeautifulSoup for better results)
                import re
                text = re.sub(r'<[^>]+>', '', text)
                data['text'] = text.strip()

            # Manuscript - determine from folios
            first_folio = stanza.folios.first()
            if first_folio and first_folio.manuscript:
                data['manuscript'] = first_folio.manuscript.siglum
            else:
                data['manuscript'] = 'Unknown'

            # Notes
            if stanza.stanza_notes:
                notes = str(stanza.stanza_notes)
                notes = re.sub(r'<[^>]+>', '', notes)
                data['notes'] = notes.strip()

            # Folios
            folios = stanza.folios.all()
            if folios:
                data['folios'] = [
                    f"{f.manuscript.siglum}-{f.folio_number}"
                    for f in folios if f.manuscript
                ]

            # Metadata
            if hasattr(stanza, 'created_at') and stanza.created_at:
                data['created_at'] = self.to_yaml_safe(stanza.created_at)
            if hasattr(stanza, 'updated_at') and stanza.updated_at:
                data['updated_at'] = self.to_yaml_safe(stanza.updated_at)

            # Write YAML file
            filename = f"{line_code}.yaml"
            filepath = output_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

            count += 1
            if i % 100 == 0:
                self.stdout.write(f"  ... {i} processed")

        self.stdout.write(self.style.SUCCESS(f"✓ Exported {count} stanzas"))
        return count

    def export_translations(self, output_base):
        """Export all English translations to YAML"""
        output_dir = output_base / 'translations'
        output_dir.mkdir(parents=True, exist_ok=True)

        translations = StanzaTranslated.objects.filter(language='en').order_by('stanza_line_code_starts')
        count = 0

        self.stdout.write(f"\nExporting translations...")

        for i, trans in enumerate(translations, 1):
            line_code = trans.stanza_line_code_starts

            if not line_code:
                self.stdout.write(self.style.WARNING(f"  ⚠ Skipping translation without line_code (id={trans.id})"))
                continue

            data = {
                'line_code': line_code,
                'language': trans.language or 'en',
            }

            # Translated text
            if trans.stanza_text:
                import re
                text = str(trans.stanza_text)
                text = re.sub(r'<[^>]+>', '', text)
                data['translated_text'] = text.strip()

            # Translator
            data['translator'] = "Laura Morreale"  # Based on project documentation

            # Notes
            if trans.stanza_notes:
                notes = str(trans.stanza_notes)
                notes = re.sub(r'<[^>]+>', '', notes)
                data['translation_notes'] = notes.strip()

            # Metadata
            if hasattr(trans, 'created_at') and trans.created_at:
                data['created_at'] = self.to_yaml_safe(trans.created_at)
            if hasattr(trans, 'updated_at') and trans.updated_at:
                data['updated_at'] = self.to_yaml_safe(trans.updated_at)

            # Write YAML file
            filename = f"{line_code}.yaml"
            filepath = output_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

            count += 1
            if i % 100 == 0:
                self.stdout.write(f"  ... {i} processed")

        self.stdout.write(self.style.SUCCESS(f"✓ Exported {count} translations"))
        return count

    def export_folios(self, output_base):
        """Export all folios to YAML"""
        output_dir = output_base / 'folios'
        output_dir.mkdir(parents=True, exist_ok=True)

        folios = Folio.objects.select_related('manuscript').all()
        count = 0

        self.stdout.write(f"\nExporting folios...")

        for folio in folios:
            if not folio.manuscript:
                continue

            slug = f"{folio.manuscript.siglum}-{folio.folio_number}"

            data = {
                'manuscript': folio.manuscript.siglum,
                'folio_number': folio.folio_number,
            }

            # Line code range
            if folio.line_code_range_start:
                data['stanza_line_code_starts'] = folio.line_code_range_start
            if folio.line_code_range_end:
                data['stanza_line_code_ends'] = folio.line_code_range_end

            # IIIF
            if folio.iiif_url:
                data['iiif_url'] = folio.iiif_url

            # Map info
            if folio.folio_includes_map:
                data['contains_map'] = folio.folio_includes_map in ['yes', 'yes_toponyms', 'yes_no_toponyms']

            # Notes
            if folio.folio_notes:
                import re
                notes = str(folio.folio_notes)
                notes = re.sub(r'<[^>]+>', '', notes)
                data['description'] = notes.strip()

            # Metadata
            if hasattr(folio, 'created_at') and folio.created_at:
                data['created_at'] = self.to_yaml_safe(folio.created_at)
            if hasattr(folio, 'updated_at') and folio.updated_at:
                data['updated_at'] = self.to_yaml_safe(folio.updated_at)

            # Write YAML file
            filename = f"{slug}.yaml"
            filepath = output_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

            count += 1

        self.stdout.write(self.style.SUCCESS(f"✓ Exported {count} folios"))
        return count

    def export_locations(self, output_base):
        """Export all locations to YAML"""
        output_dir = output_base / 'locations'
        output_dir.mkdir(parents=True, exist_ok=True)

        locations = Location.objects.all()
        count = 0

        self.stdout.write(f"\nExporting locations...")

        for loc in locations:
            # Create slug from name
            slug = loc.name.lower().replace(' ', '-').replace("'", '').replace(',', '')
            # Remove special characters
            import re
            slug = re.sub(r'[^a-z0-9-]', '', slug)

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
                text = str(loc.description)
                text = re.sub(r'<[^>]+>', '', text)
                data['description'] = text.strip()

            # Type
            if hasattr(loc, 'place_type') and loc.place_type:
                data['location_type'] = loc.place_type

            # Toponym type
            if loc.toponym_type:
                data['toponym_type'] = loc.toponym_type

            # Placename ID
            if loc.placename_id:
                data['placename_id'] = loc.placename_id

            # Authority files
            if loc.authority_file:
                data['authority_url'] = loc.authority_file

            # Metadata
            if hasattr(loc, 'created_at') and loc.created_at:
                data['created_at'] = self.to_yaml_safe(loc.created_at)
            if hasattr(loc, 'updated_at') and loc.updated_at:
                data['updated_at'] = self.to_yaml_safe(loc.updated_at)

            # Write YAML file
            filename = f"{slug}.yaml"
            filepath = output_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

            count += 1

        self.stdout.write(self.style.SUCCESS(f"✓ Exported {count} locations"))
        return count

    def export_annotations(self, output_base):
        """Export all annotations to YAML"""
        output_dir = output_base / 'annotations'
        output_dir.mkdir(parents=True, exist_ok=True)

        annotations = TextAnnotation.objects.all()
        count = 0

        self.stdout.write(f"\nExporting annotations...")

        for ann in annotations:
            # Generate ID
            ann_id = f"annotation-{ann.id}"

            data = {
                'id': ann_id,
                'annotation_type': ann.annotation_type or 'note',
            }

            # Selected text
            if ann.selected_text:
                data['selected_text'] = ann.selected_text

            # Annotation content
            if ann.annotation:
                import re
                text = str(ann.annotation)
                text = re.sub(r'<[^>]+>', '', text)
                data['annotation'] = text.strip()

            # Position data (ProseMirror format)
            if ann.from_pos:
                data['from_pos'] = ann.from_pos
            if ann.to_pos:
                data['to_pos'] = ann.to_pos

            # Try to get related stanza
            try:
                if ann.content_type and ann.object_id:
                    model_class = ann.content_type.model_class()
                    if model_class.__name__ in ['Stanza', 'StanzaTranslated']:
                        obj = model_class.objects.get(id=ann.object_id)
                        if hasattr(obj, 'stanza_line_code_starts'):
                            data['stanza_code'] = obj.stanza_line_code_starts
            except:
                pass

            # Metadata
            if hasattr(ann, 'created_at') and ann.created_at:
                data['created_at'] = self.to_yaml_safe(ann.created_at)
            if hasattr(ann, 'updated_at') and ann.updated_at:
                data['updated_at'] = self.to_yaml_safe(ann.updated_at)

            # Author (if we can determine it)
            data['author'] = "Unknown"  # Update this if you have user tracking

            # Write YAML file
            filename = f"{ann_id}.yaml"
            filepath = output_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)

            count += 1

        self.stdout.write(self.style.SUCCESS(f"✓ Exported {count} annotations"))
        return count
