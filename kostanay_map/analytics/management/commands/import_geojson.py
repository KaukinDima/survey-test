import json
import os
from django.core.management.base import BaseCommand, CommandError
from analytics.models import Region, City


class Command(BaseCommand):
    help = "Import GeoJSON files from a folder. File name should be <slug>.geojson"

    def add_arguments(self, parser):
        parser.add_argument("folder", type=str, help="Path to folder with *.geojson")
        parser.add_argument("--region", type=str, help="Region slug for all cities", required=True)
        parser.add_argument("--oblast-slug", type=str, help="Slug for oblast outline file (optional)", default="kostanayskaya-oblast")

    def handle(self, *args, **opts):
        folder = opts["folder"]
        region_slug = opts["region"]
        oblast_slug = opts["oblast_slug"]

        if not os.path.isdir(folder):
            raise CommandError(f"Folder not found: {folder}")

        region, _ = Region.objects.get_or_create(slug=region_slug, defaults={"name": region_slug.replace("-", " ").title()})

        files = [f for f in os.listdir(folder) if f.endswith(".geojson")]
        created, updated = 0, 0

        for fname in files:
            slug = os.path.splitext(fname)[0]
            path = os.path.join(folder, fname)
            with open(path, "r", encoding="utf-8") as f:
                feature = json.load(f)

            defaults = {"name": slug.replace("-", " ").title(), "feature": feature, "is_oblast": (slug == oblast_slug)}
            obj, was_created = City.objects.update_or_create(slug=slug, defaults={**defaults, "region": region})
            if was_created: created += 1
            else: updated += 1

        self.stdout.write(self.style.SUCCESS(f"Cities imported: created={created}, updated={updated}"))
