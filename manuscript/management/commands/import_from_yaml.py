"""
Import data from YAML files back into Django database.
This is the reverse operation of export_to_yaml.py
"""
import os
from pathlib import Path
import yaml
from django.core.management.base import BaseCommand
from django.db import transaction
from manuscript.models import (
    SingleManuscript,
    Library,
    Codex,
    Stanza,
    StanzaTranslated,
    Folio,
    Location,
    EditorialStatus,
    TextDecoration,
)
from textannotation.models import TextAnnotation


class Command(BaseCommand):
    help = 'Import data from YAML files into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--input',
            type=str,
            default='static-mvp/data',
            help='Input directory containing YAML files (default: static-mvp/data)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before import (WARNING: destructive!)'
        )

    def handle(self, *args, **options):
        input_dir = Path(options['input'])

        if not input_dir.exists():
            self.stderr.write(self.style.ERROR(f'Input directory not found: {input_dir}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Starting import from: {input_dir}'))

        if options['clear']:
            self.stdout.write(self.style.WARNING('⚠️  Clearing existing data...'))
            with transaction.atomic():
                TextAnnotation.objects.all().delete()
                Stanza.objects.all().delete()
                StanzaTranslated.objects.all().delete()
                Folio.objects.all().delete()
                SingleManuscript.objects.all().delete()
                Codex.objects.all().delete()
                Location.objects.all().delete()
                # Keep libraries as they are from fixtures
            self.stdout.write(self.style.SUCCESS('✅ Data cleared'))

        # Import order matters due to foreign key dependencies
        self.import_libraries(input_dir / 'manuscripts')
        self.import_locations(input_dir / 'locations')
        self.import_manuscripts(input_dir / 'manuscripts')
        self.import_folios(input_dir / 'folios')
        self.import_stanzas(input_dir / 'stanzas')
        self.import_translations(input_dir / 'translations')
        self.import_annotations(input_dir / 'annotations')

        self.stdout.write(self.style.SUCCESS('\n✅ Import complete!'))
        self.print_summary()

    def import_libraries(self, manuscripts_dir):
        """Extract and create libraries from manuscript files"""
        if not manuscripts_dir.exists():
            return

        self.stdout.write('\n📚 Importing libraries...')
        count = 0

        for yaml_file in manuscripts_dir.glob('*.yaml'):
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            library_name = data.get('library')
            if library_name:
                library, created = Library.objects.get_or_create(
                    library=library_name,
                    defaults={
                        'city': data.get('library_city', ''),
                    }
                )
                if created:
                    count += 1
                    self.stdout.write(f'  ✓ Created library: {library_name}')

        self.stdout.write(self.style.SUCCESS(f'✅ Imported {count} libraries'))

    def import_locations(self, locations_dir):
        """Import location data"""
        if not locations_dir.exists():
            self.stdout.write(self.style.WARNING('⚠️  No locations directory found'))
            return

        self.stdout.write('\n🗺️  Importing locations...')
        count = 0

        for yaml_file in locations_dir.glob('*.yaml'):
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            location, created = Location.objects.update_or_create(
                name=data.get('name', yaml_file.stem),
                defaults={
                    'modern_country': data.get('modern_country'),
                    'latitude': data.get('latitude'),
                    'longitude': data.get('longitude'),
                    'description': data.get('description', ''),
                }
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Imported {count} locations'))

    def import_manuscripts(self, manuscripts_dir):
        """Import manuscript data"""
        if not manuscripts_dir.exists():
            self.stdout.write(self.style.WARNING('⚠️  No manuscripts directory found'))
            return

        self.stdout.write('\n📜 Importing manuscripts...')
        count = 0

        for yaml_file in manuscripts_dir.glob('*.yaml'):
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            # Get or create library
            library = None
            if data.get('library'):
                library, _ = Library.objects.get_or_create(
                    library=data['library'],
                    defaults={'city': data.get('library_city', '')}
                )

            # Create manuscript
            # item_id must be unique integer - use hash of siglum
            item_id = abs(hash(data['siglum'])) % 1000000

            manuscript, created = SingleManuscript.objects.update_or_create(
                siglum=data['siglum'],
                defaults={
                    'shelfmark': data.get('shelfmark', ''),
                    'library': library,
                    'digitized_url': data.get('digitized_url'),
                    'iiif_url': data.get('iiif_url'),
                    'item_id': item_id,
                }
            )

            # Create editorial status (simplified - just basic fields)
            if data.get('editorial_status'):
                try:
                    EditorialStatus.objects.update_or_create(
                        manuscript=manuscript,
                        defaults={
                            'editorial_priority': data['editorial_status'].get('priority', 99),
                            'collated': data['editorial_status'].get('status') == 'complete',
                        }
                    )
                except Exception:
                    pass  # Skip if fields don't match

            # Create codex
            if data.get('codex'):
                Codex.objects.update_or_create(
                    related_manuscript=manuscript,
                    defaults={
                        'support': data['codex'].get('support'),
                        'folia': data['codex'].get('folios'),
                    }
                )

            # Create text decoration
            if data.get('text_decoration'):
                TextDecoration.objects.update_or_create(
                    manuscript=manuscript,
                    defaults={
                        'illumination': data['text_decoration'].get('illuminated', False),
                    }
                )

            count += 1
            self.stdout.write(f'  ✓ Imported manuscript: {data["siglum"]}')

        self.stdout.write(self.style.SUCCESS(f'✅ Imported {count} manuscripts'))

    def import_folios(self, folios_dir):
        """Import folio data"""
        if not folios_dir.exists():
            self.stdout.write(self.style.WARNING('⚠️  No folios directory found'))
            return

        self.stdout.write('\n📄 Importing folios...')
        count = 0

        for yaml_file in folios_dir.glob('*.yaml'):
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            # Extract manuscript siglum from folio_id (e.g., "Urb1-1r" -> "Urb1")
            folio_id = data['folio_id']
            manuscript_siglum = folio_id.split('-')[0]

            try:
                manuscript = SingleManuscript.objects.get(siglum=manuscript_siglum)

                Folio.objects.update_or_create(
                    folio_id=folio_id,
                    defaults={
                        'manuscript': manuscript,
                        'folio_number': data.get('folio_number', ''),
                        'iiif_manifest': data.get('iiif_manifest'),
                        'canvas_id': data.get('canvas_id'),
                    }
                )
                count += 1
            except SingleManuscript.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  ⚠️  Manuscript not found for folio: {folio_id}'))

        self.stdout.write(self.style.SUCCESS(f'✅ Imported {count} folios'))

    def import_stanzas(self, stanzas_dir):
        """Import stanza data"""
        if not stanzas_dir.exists():
            self.stdout.write(self.style.WARNING('⚠️  No stanzas directory found'))
            return

        self.stdout.write('\n📝 Importing stanzas...')
        count = 0

        for yaml_file in stanzas_dir.glob('*.yaml'):
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            try:
                stanza, created = Stanza.objects.update_or_create(
                    stanza_line_code_starts=data['line_code'],
                    defaults={
                        'stanza_text': data.get('text', ''),
                        'language': data.get('language', 'it'),
                    }
                )

                # Folios skipped - directory is empty
                # Will be linked later if folios are imported

                count += 1
                if count % 100 == 0:
                    self.stdout.write(f'  ... {count} stanzas imported')

            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ⚠️  Error importing stanza: {e}'))

        self.stdout.write(self.style.SUCCESS(f'✅ Imported {count} stanzas'))

    def import_translations(self, translations_dir):
        """Import translation data"""
        if not translations_dir.exists():
            self.stdout.write(self.style.WARNING('⚠️  No translations directory found'))
            return

        self.stdout.write('\n🌍 Importing translations...')
        count = 0

        for yaml_file in translations_dir.glob('*.yaml'):
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            line_code = data.get('line_code')
            language = data.get('language', 'en')

            if not line_code:
                continue

            # Find the original stanza
            try:
                base_stanza = Stanza.objects.filter(
                    stanza_line_code_starts=line_code
                ).first()

                if base_stanza:
                    StanzaTranslated.objects.update_or_create(
                        stanza=base_stanza,
                        language=language,
                        defaults={
                            'stanza_text': data.get('translated_text', ''),
                            'stanza_line_code_starts': line_code,
                        }
                    )
                    count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ⚠️  Error importing translation: {e}'))

        self.stdout.write(self.style.SUCCESS(f'✅ Imported {count} translations'))

    def import_annotations(self, annotations_dir):
        """Import annotation data"""
        if not annotations_dir.exists():
            self.stdout.write(self.style.WARNING('⚠️  No annotations directory found'))
            return

        self.stdout.write('\n📌 Importing annotations...')
        count = 0

        for yaml_file in annotations_dir.glob('*.yaml'):
            with open(yaml_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            try:
                TextAnnotation.objects.update_or_create(
                    annotation_id=data.get('annotation_id', yaml_file.stem),
                    defaults={
                        'quote': data.get('quote', ''),
                        'text': data.get('text', ''),
                        'ranges': data.get('ranges', []),
                    }
                )
                count += 1
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'  ⚠️  Error importing annotation: {e}'))

        self.stdout.write(self.style.SUCCESS(f'✅ Imported {count} annotations'))

    def print_summary(self):
        """Print import summary"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write('IMPORT SUMMARY')
        self.stdout.write('='*60)
        self.stdout.write(f'Libraries:     {Library.objects.count():>6}')
        self.stdout.write(f'Locations:     {Location.objects.count():>6}')
        self.stdout.write(f'Manuscripts:   {SingleManuscript.objects.count():>6}')
        self.stdout.write(f'Folios:        {Folio.objects.count():>6}')
        self.stdout.write(f'Stanzas:       {Stanza.objects.count():>6}')
        self.stdout.write(f'Translations:  {StanzaTranslated.objects.count():>6}')
        self.stdout.write(f'Annotations:   {TextAnnotation.objects.count():>6}')
        self.stdout.write('='*60)
