from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Region(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    feature = models.JSONField(blank=True, null=True)   # Region GeoJSON (optional; usually only City has it)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    feature = models.JSONField()  # GeoJSON string/dict expected by your Vue/Leaflet
    sort_order = models.IntegerField(default=0)
    is_oblast = models.BooleanField(default=False)  # e.g., "Костанайская область" outline

    class Meta:
        ordering = ["region__sort_order", "sort_order", "name"]
        unique_together = (("region", "name"),)

    def __str__(self):
        return f"{self.name}"


class SurveyWave(models.Model):
    """
    '2025Q3', '2025Q4', or month codes (e.g., '2025M07').
    """
    code = models.CharField(max_length=20, unique=True)
    label = models.CharField(max_length=120, blank=True, default="")
    starts_at = models.DateField(blank=True, null=True)
    ends_at = models.DateField(blank=True, null=True)
    is_locked = models.BooleanField(default=False)

    class Meta:
        ordering = ["-starts_at", "code"]

    def __str__(self):
        return self.label or self.code


class Survey(models.Model):
    """
    Your 'survey list' for Vue (is_frontier split).
    """
    title = models.CharField(max_length=255)
    is_frontier = models.BooleanField(default=False)  # corresponds to your surveyFrontier/surveyBase split
    wave = models.ForeignKey(SurveyWave, on_delete=models.CASCADE, related_name="surveys")

    def __str__(self):
        return self.title


class Question(models.Model):
    """
    A single question (belongs to a Survey).
    """
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    code = models.CharField(max_length=50, null=True, blank=True,)  # Q12, etc.
    text = models.TextField()
    category = models.CharField(max_length=50, blank=True, default="")  # 'media', 'wellbeing', ...
    sort_order = models.IntegerField(default=0)

    class Meta:
        unique_together = (("survey", "code"),)
        ordering = ["survey_id", "sort_order", "code"]

    def __str__(self):
        return f"{self.code} — {self.text[:80]}"


class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    code = models.CharField(max_length=50, null=True, blank=True, default="")
    label = models.CharField(max_length=255)
    sort_order = models.IntegerField(default=0)

    class Meta:
        ordering = ["question_id", "sort_order"]

    def __str__(self):
        return f"{self.label}"


class Metric(models.Model):
    """
    Generic metrics for DataPoint: percent|count|index
    Example codes: 'media_tv', 'media_internet', 'wellbeing_index'
    """
    code = models.CharField(max_length=80, null=True, blank=True,)
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=16, default="percent")  # percent|count|index

    def __str__(self):
        return self.name


class DataPoint(models.Model):
    """
    Normalized facts for any slice.
    Only one of region/city may be set (usually city).
    """
    wave = models.ForeignKey(SurveyWave, on_delete=models.CASCADE, related_name="datapoints")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True, related_name="datapoints")
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, related_name="datapoints")
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True, related_name="datapoints")
    option = models.ForeignKey(AnswerOption, on_delete=models.SET_NULL, null=True, blank=True, related_name="datapoints")
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name="datapoints")
    value = models.DecimalField(max_digits=10, decimal_places=2)
    extra = models.JSONField(blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["wave", "city", "region"]),
            models.Index(fields=["metric", "wave"]),
            models.Index(fields=["question", "option"]),
        ]
        unique_together = (
            ("wave", "region", "city", "question", "option", "metric"),
        )

    def __str__(self):
        who = self.city.slug if self.city_id else (self.region.slug if self.region_id else "-")
        return f"{self.wave.code}:{who}:{self.metric.code}={self.value}"


class SavedView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="saved_views")
    name = models.CharField(max_length=255)
    filters_json = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
