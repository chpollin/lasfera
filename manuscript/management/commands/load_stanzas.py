import logging
import re

from django.core.management.base import BaseCommand

from manuscript.models import SingleManuscript, Stanza

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Import poem data from a plain text file"

    def add_arguments(self, parser):
        parser.add_argument(
            "--filepath", type=str, help="filepath of the plain text file to load"
        )

    def handle(self, *args, **options):
        file_path = options.get("filepath")

        with open(file_path, "r", encoding="utf-8-sig") as file:
            content = file.read()

        self.import_poem(content)

    def import_poem(self, content):
        manuscript = SingleManuscript.objects.get(siglum="TEST")
        book_pattern = re.compile(r"^\s*LIBRO (\d+)", re.MULTILINE)
        stanza_pattern = re.compile(
            r"^(\d+)\.\s*(.*?)(?=\n\d+\.|\Z)", re.DOTALL | re.MULTILINE
        )

        book_matches = book_pattern.split(content)
        if book_matches[0] == "":
            book_matches = book_matches[1:]

        for i in range(0, len(book_matches), 2):
            book_number = int(
                book_matches[i]
            )  # Extract book number from "LIBRO X" string
            book_text = book_matches[
                i + 1
            ].strip()  # Get the corresponding book content

            stanza_matches = stanza_pattern.findall(book_text)

            for stanza_number, stanza_text in stanza_matches:
                stanza_number = int(stanza_number)
                stanza_text = stanza_text.strip()

                stanza_lines = stanza_text.split("\n")

                for line_number, line_text in enumerate(stanza_lines, start=1):
                    line_code = (
                        f"{book_number:02d}.{stanza_number:02d}.{line_number:02d}"
                    )
                    # print(f"Line code: {line_code}, Line text: {line_text}")

                    Stanza.objects.create(
                        stanza_line_code_starts=line_code,
                        stanza_text=line_text,
                        related_manuscript=manuscript,
                    )

        self.stdout.write(self.style.SUCCESS("Successfully imported the stanzas"))
