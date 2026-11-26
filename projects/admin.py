from django.contrib import admin

from .models import Project, Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "owner__email")
    list_select_related = ("owner",)
    autocomplete_fields = ("owner",)
    filter_horizontal = ("participants", "skills")
    readonly_fields = ("created_at",)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.participants.add(form.instance.owner)
