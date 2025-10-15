from rest_framework import serializers
from ..models import Region, City, SurveyWave, Survey, Question, AnswerOption, Metric, DataPoint


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ("id", "name", "slug", "feature", "sort_order")


class CitySerializer(serializers.ModelSerializer):
    region = RegionSerializer(read_only=True)

    class Meta:
        model = City
        fields = ("id", "name", "slug", "feature", "sort_order", "is_oblast", "region")


class SurveyWaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyWave
        fields = ("id", "code", "label", "starts_at", "ends_at", "is_locked")


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = ("id", "title", "is_frontier")


class AnswerOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerOption
        fields = ("id", "code", "label", "sort_order")


class QuestionSerializer(serializers.ModelSerializer):
    options = AnswerOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ("id", "survey", "code", "text", "category", "sort_order", "options")


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ("id", "code", "name", "unit")


class DataPointSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    region = RegionSerializer(read_only=True)
    metric = MetricSerializer(read_only=True)
    wave = SurveyWaveSerializer(read_only=True)

    class Meta:
        model = DataPoint
        fields = ("id", "wave", "region", "city", "question", "option", "metric", "value", "extra")
