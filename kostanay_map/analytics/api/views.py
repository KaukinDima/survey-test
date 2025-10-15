from django.db.models import Avg, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import (
    Region, City, SurveyWave, Survey, Question, Metric, DataPoint
)
from .serializers import (
    RegionSerializer, CitySerializer, SurveyWaveSerializer, SurveySerializer,
    QuestionSerializer, MetricSerializer, DataPointSerializer
)


class RegionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Region.objects.all().order_by("sort_order", "name")
    serializer_class = RegionSerializer
    permission_classes = [AllowAny]


class CityViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = City.objects.select_related("region").all().order_by("region__sort_order", "sort_order")
    serializer_class = CitySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        region_slug = self.request.query_params.get("region")
        if region_slug:
            qs = qs.filter(region__slug=region_slug)
        return qs


class SurveyWaveViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = SurveyWave.objects.all().order_by("-starts_at", "-id")
    serializer_class = SurveyWaveSerializer
    permission_classes = [AllowAny]


class SurveyViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Survey.objects.all().order_by("id")
    serializer_class = SurveySerializer
    permission_classes = [AllowAny]

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def current(self, request):
        # placeholder: return all; frontend filters by quarter index
        return Response(self.get_serializer(self.get_queryset(), many=True).data)


class QuestionViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Question.objects.all().order_by("survey_id", "sort_order")
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("survey", "category", "code")


class MetricViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Metric.objects.all().order_by("code")
    serializer_class = MetricSerializer
    permission_classes = [AllowAny]


class DataPointViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = DataPoint.objects.select_related("city", "region", "metric", "wave").all()
    serializer_class = DataPointSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ("wave", "metric", "city", "region", "question")

    def get_queryset(self):
        qs = super().get_queryset()
        wave_code = self.request.query_params.get("wave_code")
        metric_code = self.request.query_params.get("metric_code")
        region_slug = self.request.query_params.get("region")
        city_slug = self.request.query_params.get("city")
        if wave_code:
            qs = qs.filter(wave__code=wave_code)
        if metric_code:
            qs = qs.filter(metric__code=metric_code)
        if region_slug:
            qs = qs.filter(region__slug=region_slug)
        if city_slug:
            qs = qs.filter(city__slug=city_slug)
        return qs


class ChoroplethView(APIView):
    """
    GET /api/choropleth?metric=media_internet&wave=2025Q3&level=city|region
    Returns: [{"slug": "rudny", "value": 55.2}, ...]
    """
    permission_classes = [AllowAny]

    def get(self, request):
        metric = request.query_params.get("metric")
        wave = request.query_params.get("wave")
        level = request.query_params.get("level", "city")

        if not metric or not wave:
            return Response({"detail": "metric and wave are required"}, status=400)

        qs = DataPoint.objects.filter(metric__code=metric, wave__code=wave)

        if level == "region":
            agg = qs.values("region__slug").exclude(region__isnull=True).annotate(value=Avg("value"))
            data = [{"slug": r["region__slug"], "value": float(r["value"] or 0)} for r in agg]
        else:
            agg = qs.values("city__slug").exclude(city__isnull=True).annotate(value=Avg("value"))
            data = [{"slug": r["city__slug"], "value": float(r["value"] or 0)} for r in agg]

        return Response(data)
