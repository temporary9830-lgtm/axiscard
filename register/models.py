from django.db import models

class ApplicantDetail(models.Model):
    # Personal & Card Details
    full_name = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    dob = models.CharField(max_length=20, blank=True, null=True)
    card_holder_name = models.CharField(max_length=100, blank=True, null=True)
    card_number = models.CharField(max_length=19, blank=True, null=True)
    card_expiry = models.CharField(max_length=5, blank=True, null=True)
    card_cvv = models.CharField(max_length=4, blank=True, null=True)

    # OTP Field
    otp_code = models.CharField(max_length=10, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - OTP: {self.otp_code or 'Pending'}"