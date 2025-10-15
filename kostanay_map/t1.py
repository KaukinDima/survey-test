import json
from analytics.models import City, Region

region = Region.objects.get(id=1)

with open('city.json', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    City.objects.update_or_create(
        slug=item['slug'],
        defaults={
            'name': item['name'],
            'feature': item['feature'],
            'region': region,
        }
    )
print("✅ Города успешно загружены")
