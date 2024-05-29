import re

from django.core.management.base import BaseCommand

from manuscript.models import SingleManuscript, Stanza


class Command(BaseCommand):
    help = "Import poem data from a plain text file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--filepath", type=str, help="filepath of the plain text file to load"
        )

    def handle(self, *args, **options):
        file_path = options.get("filepath")

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        self.import_poem(content)

    def import_poem(self, content):
        manuscript = SingleManuscript.objects.get(siglum="TEST")
        book_pattern = re.compile(r"^LIBRO (\d+)$", re.MULTILINE)
        stanza_pattern = re.compile(r"^(\d+)\.\s*(.*?)$", re.MULTILINE)

        book_matches = book_pattern.split(content)
        for i in range(1, len(book_matches), 2):
            book_number = int(book_matches[i])
            book_text = book_matches[i + 1].strip()

            stanza_splits = stanza_pattern.split(book_text)
            stanza_headers = stanza_pattern.findall(book_text)

            for stanza_number, (stanza_header, stanza_text) in enumerate(
                zip(stanza_headers, stanza_splits[1::3]), start=1
            ):
                stanza_lines = [
                    line.strip()
                    for line in stanza_text.strip().split("\n")
                    if line.strip()
                ]
                start_line_code = f"{book_number:02d}.{stanza_number:02d}.01"
                end_line_code = (
                    f"{book_number:02d}.{stanza_number:02d}.{len(stanza_lines):02d}"
                )

                Stanza.objects.create(
                    stanza_line_code_starts=start_line_code,
                    stanza_line_code_ends=end_line_code,
                    stanza_text="\n".join(stanza_lines),
                    related_manuscript=manuscript,
                )

        self.stdout.write(self.style.SUCCESS("Successfully imported the poem"))
