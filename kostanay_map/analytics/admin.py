from django.contrib import admin
from .models import (
    Region, City, SurveyWave, Survey, Question, AnswerOption, Metric, DataPoint, SavedView
)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "sort_order")
    search_fields = ("name", "slug")
    list_editable = ("sort_order",)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "region", "is_oblast", "sort_order")
    list_filter = ("region", "is_oblast")
    search_fields = ("name", "slug")
    list_editable = ("sort_order", "is_oblast")


class AnswerOptionInline(admin.TabularInline):
    model = AnswerOption
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("survey", "code", "short_text", "category", "sort_order")
    list_filter = ("survey", "category")
    search_fields = ("code", "text")
    list_editable = ("sort_order", "category")
    inlines = [AnswerOptionInline]

    def short_text(self, obj):
        return (obj.text or "")[:100]
    
@admin.register(AnswerOption)
class AnswerOptionAdmin(admin.ModelAdmin):
    search_fields = ("label", "code")

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ("title", "is_frontier")
    list_editable = ("is_frontier",)
    search_fields = ("title",)


@admin.register(SurveyWave)
class SurveyWaveAdmin(admin.ModelAdmin):
    list_display = ("code", "label", "starts_at", "ends_at", "is_locked")
    list_editable = ("label", "starts_at", "ends_at", "is_locked")
    search_fields = ("code", "label")
    actions = ["lock_waves", "unlock_waves"]

    @admin.action(description="Lock selected waves")
    def lock_waves(self, request, qs):
        qs.update(is_locked=True)

    @admin.action(description="Unlock selected waves")
    def unlock_waves(self, request, qs):
        qs.update(is_locked=False)


@admin.register(Metric)
class MetricAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "unit")
    list_editable = ("name", "unit")
    search_fields = ("code", "name")


@admin.register(DataPoint)
class DataPointAdmin(admin.ModelAdmin):
    list_display = ("wave", "who", "metric", "value", "question", "option")
    list_filter = ("wave", "metric", "question", "city__region")
    search_fields = ("city__name", "region__name", "metric__name", "question__text")
    list_editable = ("value",)
    autocomplete_fields = ("city", "region", "question", "option", "metric", "wave")

    def who(self, obj):
        return obj.city or obj.region


@admin.register(SavedView)
class SavedViewAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at")
    search_fields = ("name", "user__email")
