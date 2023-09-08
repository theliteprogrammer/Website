from django.urls import path 
from user_panel import views
from userauths.views import settings

app_name = "dashboard"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('waste_plans/', views.waste_plans, name='waste_plans'),
    path('notifications/', views.notifications, name='notifications'),
    path('notification/<oid>/', views.notification_detail, name='notification_detail'),
    path('mark_noti_as_seen/<oid>/', views.mark_noti_as_seen, name='mark_noti_as_seen'),
    path('waste_order_details/<slug:slug>/', views.waste_order_details, name='waste_order_details'),
    path('waste_checkout/<oid>/', views.waste_checkout, name='waste_checkout'),
    path('payment-completed/<oid>/', views.payment_success, name='payment_success'),
    path('payment_failed/<oid>/', views.payment_failed, name='payment_failed'),
    path('spending-tracker/', views.spending, name='spending'),
    path('history/', views.history, name='history'),
    path('history/<oid>/', views.history_detail, name='history_detail'),
    path('invoices/', views.invoices, name='invoices'),
    path('invoice/<oid>/', views.invoice, name='invoice'),
    path('invoice/<oid>/', views.invoice, name='invoice'),
    path('settings/', settings, name='settings'),
]