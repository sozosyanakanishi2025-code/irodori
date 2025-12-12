from django.contrib import admin
from .models import Customer, Activity, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = ("company_name", "contact_name", "email", "user", "created_at")

    list_filter = ("user", "tags", "created_at")

    search_fields = ("company_name", "contact_name", "email")

    fieldsets = (
        ("基本情報", {
            "fields": ("company_name", "contact_name", "email", "phone")
        }),
        ("担当・タグ", {
            "fields": ("user", "tags")
        }),
    )

    filter_horizontal = ("tags",)

    readonly_fields = ("created_at", "updated_at")


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("customer", "activity_date", "status", "created_at")
    list_filter = ("status", "activity_date", "customer__user")
    search_fields = ("customer__company_name", "note")

    date_hierarchy = "activity_date"

    fields = ("customer", "activity_date", "status", "note")

    raw_id_fields = ("customer",)
