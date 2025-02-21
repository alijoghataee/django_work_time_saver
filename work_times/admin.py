from django.contrib import admin
from django.utils.html import format_html

from work_times.models import Project, WorkTime


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "hex_color", "color_display",)
    list_editable = ("hex_color",)

    def color_display(self, obj):
        return format_html(
            '<div style="width: 30px; height: 30px; background-color: {}; border: 1px solid #000;"></div>',
            obj.hex_color
        )


@admin.register(WorkTime)
class WorkTimeAdmin(admin.ModelAdmin):
    list_display = ("id", "project", "start_time", "end_time", "worked_minutes")
