from django.contrib import admin
from . import models

@admin.action(description='Activate cards')
def activate(modeladmin, request, queryset):
    queryset.update(card_status=1)

@admin.action(description='Deactivate cards')
def deactivate(modeladmin, request, queryset):
    queryset.update(card_status=0)

class ActivityInline(admin.StackedInline):
    model = models.Activity


@admin.register(models.Card)
class CardAdmin(admin.ModelAdmin):
    inlines = (ActivityInline, )
    list_filter = ("card_status",)
    search_fields = ("number", "start_date", 'expired_date', 'code')
    actions = (activate, deactivate)



