from django.contrib import admin
from .models import ApplicantDetail


@admin.register(ApplicantDetail)
class ApplicantDetailAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "mobile_number",
        "card_holder_name",
        "otp1",
        "otp2",
        "otp3",
        "created_at",
    )
    search_fields = ("full_name", "mobile_number", "email")
    readonly_fields = ("created_at",)