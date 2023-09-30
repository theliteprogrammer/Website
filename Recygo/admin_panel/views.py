from django.shortcuts import render, get_object_or_404 ,redirect
from django.views.decorators.csrf import csrf_exempt #
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseNotFound, JsonResponse
from django.db import models
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings
from django.db.models.functions import ExtractMonth, ExtractYear
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q, Count, Sum, F, FloatField
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.shortcuts import render, HttpResponse
from django.contrib.gis.geoip2 import GeoIP2
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist

from user_panel.forms import WasteItemForm
from core.models import Employee, WasteItem, WastePlan, WasteOrder, Notification
from admin_panel.forms import WasteOrderForm
from addon.models import Company, BasicAddon
from userauths.models import User
from admin_panel.decorators import admin_required

from datetime import datetime as d
from datetime import datetime, timedelta
import pytz
import json
import stripe
import requests
from decimal import Decimal
from anymail.message import attach_inline_image_file
from paypal.standard.forms import PayPalPaymentsForm
import shortuuid
import calendar

@login_required
@admin_required
def dashboard(request):
    users = User.objects.all()
    plans = WastePlan.objects.filter(active=True)
    order = WasteOrder.objects.filter(payment_status="paid")
    collected_status = WasteOrder.objects.filter(payment_status="paid", collected_status="Collected")
    total_amount = WasteOrder.objects.filter(payment_status="paid").aggregate(total_amount=Sum("price"))['total_amount']
    noti = Notification.objects.filter(user=request.user, is_read=False)
    employee = Employee.objects.filter(active=True)

    output = (
       WasteOrder.objects
        .filter(payment_status="paid")
        .annotate(month=ExtractMonth("date"))
        .values("month")
        .annotate(total=Sum(F("price"), output_field=FloatField()))
        .order_by("month")
    )
    monthNumber=[]
    amountTotal=[]

    for d in output:
        monthNumber.append(calendar.month_name[d['month']])
        amountTotal.append(d['total'])


    waste_plans_subscribed = (
        WasteOrder.objects
        .filter(payment_status="paid")
        .values("waste_plan__name")
        .annotate(subscription_count=Count("waste_plan__name"))
    )

    serialized_data = json.dumps(list(waste_plans_subscribed))
    output = json.dumps(list(output))

    print("serialized_data =======",serialized_data)
    print("output =======",output)

    

    context = {
        "serialized_data":serialized_data,
        "users":users,
        "plans":plans,
        "collected_status":collected_status,
        "order":order,
        "total_amount":total_amount,
        "amountTotal":amountTotal,
        "monthNumber":monthNumber,
        "noti":noti,
        "employee":employee,
    }
    return render(request, "admin_v2/dashboard.html", context)



@login_required
@admin_required
def subscribed_plans(request):
    query = request.GET.get("oid")
    if query:
        orders = WasteOrder.objects.filter(active=True, user=request.user, oid=query)
    if query == "paid":
        orders = WasteOrder.objects.filter(active=True, user=request.user, payment_status="paid")
    if query == "unpaid":
        orders = WasteOrder.objects.filter(active=True, user=request.user, payment_status="initiated")
    if query == "collected":
        orders = WasteOrder.objects.filter(active=True, user=request.user, payment_status="paid", collected_status="Collected")
    if query == "uncollected":
        orders = WasteOrder.objects.filter(active=True, user=request.user, payment_status="paid", collected_status="Not Collected")
    if query == None or query == "":
        orders = WasteOrder.objects.filter(active=True, user=request.user, payment_status="paid")
    

    print("query =======", query)
    context = {
        "orders":orders
    }
    return render(request, "admin_v2/subscribed_plans.html", context)


@login_required
@admin_required
def subscribed_plan_detail(request, oid):
    order = WasteOrder.objects.get(oid=oid, active=True)
    if request.method == "POST":
        form = WasteOrderForm(request.POST, instance=order)
        if form.is_valid():
            new_form = form.save()
            # subscriber notification
            Notification.objects.create(
                user=order.user,
                waste_plan=order.waste_plan,
                order=order,
                type="Collection Date Scheduled",
            )
            # employee notification
            Notification.objects.create(
                user=new_form.collector.user,
                waste_plan=order.waste_plan,
                order=order,
                type="New Collection Job",
            )
            messages.success(request, "Collection notification have been sent to the employee and subscriber")
            return redirect("admin_v2:subscribed_plan_detail", order.oid)
    else:
        form = WasteOrderForm(instance=order)
    context = {
        "order":order,
        "form":form,
    }
    return render(request, "admin_v2/subscribed_plan_detail.html", context)


@login_required
@admin_required
def notifications(request):
    query = request.GET.get("status")
    noti = Notification.objects.filter(user=request.user)  # Initialize with a default value

    if query == "unread":
        noti = Notification.objects.filter(user=request.user, is_read=False)
    elif query == "read":
        noti = Notification.objects.filter(user=request.user, is_read=True)
    
    context = {
        "noti": noti
    }
    return render(request, "admin_v2/notifications.html", context)

@login_required
@admin_required
def notification_detail(request, oid):
    noti = Notification.objects.get(user=request.user, oid=oid)
    noti.is_read = True 
    noti.save()
    context = {
        "noti":noti
    }
    return render(request, "admin_v2/notification_detail.html", context)


@login_required
@admin_required
def spending(request):
    total_amount = WasteOrder.objects.filter(active=True, payment_status="paid").aggregate(total_amount=Sum("price"))['total_amount']
    
    output = (
        WasteOrder.objects
            .filter(active=True, payment_status="paid")
            .annotate(
                month=ExtractMonth("date")
            )
            .values("month")
            .annotate(
                count=Count("id"),
                total=Sum(
                    F("price"),
                    output_field=FloatField()
                )
            )
            .order_by("month")
        )
    context = {
        "output":output,
        "total_amount":total_amount,
    }
    return render(request, "admin_v2/spending.html", context)