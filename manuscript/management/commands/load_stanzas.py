from django.core.management.base import BaseCommand

from manuscript.models import Stanza


class Command(BaseCommand):
    help = "Insert stanzas from a text file"

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path", type=str, help="The path to the file that contains the stanzas"
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        with open(file_path, "r", encoding="utf-8") as file:
            line_counter = 0
            for line in file:
                line = line.strip()
                if line.startswith("[RUBRIC]") or line.isdigit():
                    continue
                if line != "":
                    line_counter += 1
                    line_number = f"01.02.{line_counter:02d}"
                    stanza = Stanza(line=line, line_number=line_number)
                    stanza.save()
                else:
                    line_counter = 0
