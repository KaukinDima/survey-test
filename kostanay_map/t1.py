from analytics.models import Region, City, Survey, SurveyWave, Question, AnswerOption, DataPoint, Metric
from decimal import Decimal

# --- Получаем город и регион ---
city = City.objects.get(slug="arkalyk-ga")
region = city.region

# --- Создаем волну ---
wave, _ = SurveyWave.objects.get_or_create(
    code="2025Q3",
    defaults={"label": "III квартал 2025"}
)

# --- Создаем опрос ---
survey, _ = Survey.objects.get_or_create(
    title="Источники информации",
)

# --- Создаем вопрос ---
question, _ = Question.objects.get_or_create(
    survey=survey,
    code="Q1",
    text="Скажите, через какие источники информации вы узнаёте о событиях происходящих в регионе?"
)

# --- Создаем метрику ---
metric, _ = Metric.objects.get_or_create(
    code="media_source_share",
    defaults={"name": "Доля источников информации", "unit": "percent"}
)

# --- Создаем варианты ответов и данные ---
options = {
    "Телевидение": Decimal("58.4"),
    "Интернет-СМИ": Decimal("67.2"),
    "Печатные СМИ": Decimal("21.5"),
    "Социальные сети": Decimal("74.0"),
    "Мессенджеры": Decimal("69.8"),
}

for label, value in options.items():
    option, _ = AnswerOption.objects.get_or_create(
        question=question,
        label=label,
    )
    DataPoint.objects.update_or_create(
        wave=wave,
        city=city,
        question=question,
        option=option,
        metric=metric,
        defaults={"value": value}
    )

print("✅ Тестовые данные для Аркалыка успешно созданы.")
