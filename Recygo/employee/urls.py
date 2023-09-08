from django.urls import path 
from employee import views

app_name = "employee"

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/<oid>/', views.notification_detail, name='notification_detail'),
    path("subscribed_plans/", views.subscribed_plans, name="subscribed_plans"),
    path("subscribed_plan_detail/<oid>/", views.subscribed_plan_detail, name="subscribed_plan_detail"),
    path("collected_waste/", views.collected_waste, name="collected_waste"),
    path("collected_waste/<oid>/", views.collected_waste_detail, name="collected_waste_detail"),
    path("settings/", views.settings, name="settings"),


]