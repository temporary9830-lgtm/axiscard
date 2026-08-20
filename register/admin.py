from django.contrib import admin
from .models import ApplicantDetail

@admin.register(ApplicantDetail)
class ApplicantDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'card_number', 'otp_code', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'otp_code')