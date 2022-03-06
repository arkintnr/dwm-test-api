import csv
from datetime import tzinfo

from dateutil.parser import parse
from typing import Any, Optional

from django.core.management.base import BaseCommand
from django.utils import timezone

from api.models import CovidData


class Command(BaseCommand):
    help = "Loads covid data from csv file"

    def add_arguments(self, parser) -> None:
        parser.add_argument("--file_path", type=str)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        try:
            file_path: str = options["file_path"]
            self.stdout.write(self.style.SUCCESS(file_path))
            with open(file_path, "r") as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    last_update_date = parse(row[4])
                    last_update_date = last_update_date.replace(tzinfo=timezone.utc)
                    CovidData.objects.get_or_create(
                        s_no=row[0],
                        observation_date=parse(row[1]),
                        state=row[2],
                        country=row[3],
                        last_update=last_update_date,
                        confirmed=int(float(row[5])),
                        deaths=int(float(row[6])),
                        recovered=int(float(row[7])),
                    )
                    self.stdout.write(self.style.SUCCESS(row))
            self.stdout.write(self.style.SUCCESS("Successfully loaded Covid 19 Data."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading csv file, {e}"))
