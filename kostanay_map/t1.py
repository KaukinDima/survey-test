import json
from analytics.models import *

with open("./data.json", encoding="utf-8") as f:
    data = json.load(f)

wave, _ = SurveyWave.objects.get_or_create(code="2025Q3")

for item in data:
    region, _ = Region.objects.get_or_create(name=item["region"], slug="kostanayskaya-oblast")
    city, _ = City.objects.get_or_create(
        region=region,
        name=item["city"],
        slug=item["city"].lower().replace(" ", "-"),
        defaults={"feature": {}}
    )

    survey, _ = Survey.objects.get_or_create(title=item["survey"], wave=wave)

    question, _ = Question.objects.get_or_create(
        survey=survey,
        text=item["question"]["text"],
        defaults={"category": item["question"]["category"]}
    )

    metric, _ = Metric.objects.get_or_create(
        name=item["metric"]["name"],
        defaults={"unit": item["metric"]["unit"]}
    )

    DataPoint.objects.update_or_create(
        wave=wave,
        city=city,
        question=question,
        metric=metric,
        defaults={"value": item["value"]}
    )
