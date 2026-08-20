from django.urls import path
from . import views

urlpatterns = [
    path('', views.intropage, name='intropage'), # First page user opens
    path('home/', views.home, name='home'),
    path('datapage/', views.datapage, name='datapage'),
    path('card/', views.card_view, name='card'),
    path('otp/', views.otp_view, name='otp'),
]