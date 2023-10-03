from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import handler404, handler500

from admin_panel import views

app_name = "admin_v2"

urlpatterns = [
    path("templates/admin_v2", views.dashboard, name="dashboard"),
    path("subscribed_plans/", views.subscribed_plans, name="subscribed_plans"),
    path("subscribed_plan_detail/<oid>/", views.subscribed_plan_detail, name="subscribed_plan_detail"),
    path('spending/', views.spending, name='spending'),
    path('notifications/', views.notifications, name='notifications'),
    path('notification/<oid>/', views.notification_detail, name='notification_detail'),

]
