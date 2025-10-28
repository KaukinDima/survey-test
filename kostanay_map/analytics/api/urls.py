from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegionViewSet, CityViewSet, SurveyWaveViewSet, SurveyViewSet,
    QuestionViewSet, MetricViewSet, DataPointViewSet, ChoroplethView,
    QuestionGroupedViewSet,
)

router = DefaultRouter()
router.register(r"regions", RegionViewSet, basename="region")
router.register(r"cities", CityViewSet, basename="city")
router.register(r"waves", SurveyWaveViewSet, basename="wave")
router.register(r"surveys", SurveyViewSet, basename="survey")
router.register(r"questions", QuestionViewSet, basename="question")
router.register(r"metrics", MetricViewSet, basename="metric")
router.register(r"datapoints", DataPointViewSet, basename="datapoint")
router.register(r"questions/grouped", QuestionGroupedViewSet, basename="question-grouped")


urlpatterns = [
    path("", include(router.urls)),
    path("choropleth", ChoroplethView.as_view(), name="choropleth"),
]
