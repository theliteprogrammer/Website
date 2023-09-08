from django.urls import path 
from core import views

app_name = "core"

urlpatterns = [
    path('', views.index, name='home'),
    path('donation_checkout/<did>/', views.donation_checkout, name='donation_checkout'),
    path('payment-completed/<did>/', views.payment_success, name='payment_success'),
]