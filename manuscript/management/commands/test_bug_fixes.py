"""
Django management command to test the bug fixes for La Sfera Digital Edition.

This command tests:
1. BUG #1: Urb1 hardcoding - verifies all manuscripts are accessible
2. BUG #2: page_number parameter - verifies Mirador canvas_id calculation

Usage:
    python manage.py test_bug_fixes
"""

from django.core.management.base import BaseCommand
from django.test import RequestFactory
from manuscript.models import SingleManuscript
from manuscript.views import mirador_view, manuscript_stanzas


class Command(BaseCommand):
    help = "Test the bug fixes for manuscript access and page navigation"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("\n=== Testing La Sfera Bug Fixes ===\n"))

        # Initialize request factory
        factory = RequestFactory()

        # Test 1: Verify all manuscripts exist in database
        self.stdout.write(self.style.NOTICE("TEST 1: Checking manuscript database entries..."))
        manuscripts = SingleManuscript.objects.all()

        self.stdout.write(f"Found {manuscripts.count()} manuscripts in database:")
        for ms in manuscripts:
            iiif_status = "✓ IIIF URL present" if ms.iiif_url else "✗ No IIIF URL"
            self.stdout.write(f"  - {ms.siglum}: {ms.library} ({iiif_status})")
            if ms.iiif_url:
                self.stdout.write(f"    URL: {ms.iiif_url[:80]}...")

        # Test 2: Test manuscript_stanzas view for each manuscript
        self.stdout.write(self.style.NOTICE("\nTEST 2: Testing manuscript_stanzas view for each manuscript..."))
        for ms in manuscripts:
            try:
                request = factory.get(f"/manuscripts/{ms.siglum}/stanzas/")
                response = manuscript_stanzas(request, ms.siglum)

                if response.status_code == 200:
                    self.stdout.write(self.style.SUCCESS(f"  ✓ {ms.siglum}: Status 200 OK"))
                else:
                    self.stdout.write(self.style.ERROR(f"  ✗ {ms.siglum}: Status {response.status_code}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ {ms.siglum}: Exception - {str(e)[:100]}"))

        # Test 3: Test mirador_view with page_number parameter
        self.stdout.write(self.style.NOTICE("\nTEST 3: Testing Mirador page_number parameter..."))

        # Get a manuscript with IIIF URL for testing
        test_manuscript = manuscripts.filter(iiif_url__isnull=False).exclude(iiif_url="").first()

        if test_manuscript:
            self.stdout.write(f"Using manuscript {test_manuscript.siglum} for page_number test")

            # Test without page_number
            try:
                request = factory.get(f"/mirador/{test_manuscript.id}/1/")
                response = mirador_view(request, str(test_manuscript.id), None)

                context_data = response.context_data if hasattr(response, "context_data") else {}
                canvas_id = context_data.get("canvas_id", "No canvas_id in context")

                self.stdout.write(f"  Without page_number: canvas_id = {canvas_id}")
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  ✗ Without page_number: Exception - {str(e)[:100]}"))

            # Test with page_number
            test_pages = [1, 5, 10]
            for page_num in test_pages:
                try:
                    request = factory.get(f"/mirador/{test_manuscript.id}/{page_num}/")
                    response = mirador_view(request, str(test_manuscript.id), str(page_num))

                    # Check if canvas_id is in context
                    context_data = response.context_data if hasattr(response, "context_data") else {}
                    canvas_id = context_data.get("canvas_id", None)

                    if canvas_id:
                        self.stdout.write(self.style.SUCCESS(f"  ✓ Page {page_num}: canvas_id = {canvas_id[:80]}..."))
                    else:
                        self.stdout.write(self.style.WARNING(f"  ⚠ Page {page_num}: No canvas_id resolved"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"  ✗ Page {page_num}: Exception - {str(e)[:100]}"))
        else:
            self.stdout.write(self.style.WARNING("  No manuscript with IIIF URL found for testing"))

        # Summary
        self.stdout.write(self.style.SUCCESS("\n=== Test Complete ===\n"))
        self.stdout.write("Expected results:")
        self.stdout.write("  1. All manuscripts should be listed")
        self.stdout.write("  2. manuscript_stanzas should return 200 for all manuscripts")
        self.stdout.write("  3. mirador_view should calculate canvas_id for page_number parameter")
