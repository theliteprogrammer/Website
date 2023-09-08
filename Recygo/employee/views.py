from django.shortcuts import render, get_object_or_404 ,redirect
from django.views.decorators.csrf import csrf_exempt
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

from admin_panel.forms import CollectionStatusForm
from core.models import WasteItem, WastePlan, WasteOrder, Notification
from addon.models import Company, BasicAddon

from datetime import datetime as d
from datetime import datetime
import datetime
import pytz
import json
import stripe
import requests
from decimal import Decimal
from anymail.message import attach_inline_image_file
from paypal.standard.forms import PayPalPaymentsForm
import shortuuid
import calendar

from userauths.forms import ProfileUpdateForm, UserUpdateForm



@login_required
def dashboard(request):
    order = WasteOrder.objects.filter(collector__user=request.user, payment_status="paid", collected_status="Collected")
    noti = Notification.objects.filter(user=request.user, is_read=False)
    
    output = WasteOrder.objects.filter(collector__user=request.user, payment_status="paid", collected_status="Collected").annotate(month=ExtractMonth("date")).values("month").annotate(count=Count("id"),).order_by("month")
    
    monthNumber=[]
    collectedWastes=[]
    for d in output:
        monthNumber.append(calendar.month_name[d['month']])
        collectedWastes.append(d['count'])

    context = {
        "order":order,
        "noti":noti,
        "monthNumber":monthNumber,
        "collectedWastes":collectedWastes,
    }
    return render(request, "employee/dashboard.html", context)

@login_required
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
    return render(request, "employee/notifications.html", context)

@login_required
def notification_detail(request, oid):
    noti = Notification.objects.get(user=request.user, oid=oid)
    noti.is_read = True 
    noti.save()

    order = noti.order

    if request.method == "POST":
        form = CollectionStatusForm(request.POST, instance=noti.order)
        if form.is_valid():
            new_form = form.save()
            # subscriber notification
            Notification.objects.create(
                user=noti.order.user,
                waste_plan=noti.order.waste_plan,
                order=noti.order,
                type="Waste Collected",
            )
            # employee notification
            Notification.objects.create(
                user=new_form.waste_plan.user,
                waste_plan=noti.order.waste_plan,
                order=noti.order,
                type="Waste Collected",
            )
            messages.success(request, "Collected Status Updated")
            return redirect("employee:subscribed_plan_detail", noti.order.oid)
    else:
        form = CollectionStatusForm(instance=noti.order)

    context = {
        "noti":noti,
        "form":form,
    }
    return render(request, "employee/notification_detail.html", context)




@login_required
def subscribed_plans(request):
    query = request.GET.get("oid")
    if query:
        orders = WasteOrder.objects.filter(active=True, collector__user=request.user, oid=query)
    
    if query == "collected":
        orders = WasteOrder.objects.filter(active=True, collector__user=request.user, payment_status="paid", collected_status="Collected")
    if query == "uncollected":
        orders = WasteOrder.objects.filter(active=True, collector__user=request.user, payment_status="paid", collected_status="Not Collected")
    if query == None or query == "":
        orders = WasteOrder.objects.filter(active=True, collector__user=request.user, payment_status="paid")
    

    print("query =======", query)
    context = {
        "orders":orders
    }
    return render(request, "employee/subscribed_plans.html", context)


@login_required
def subscribed_plan_detail(request, oid):
    
    order = WasteOrder.objects.get(oid=oid, collector__user=request.user, active=True)
    
    if request.method == "POST":
        form = CollectionStatusForm(request.POST, instance=order)
        if form.is_valid():
            new_form = form.save()
            # subscriber notification
            Notification.objects.create(
                user=order.user,
                waste_plan=order.waste_plan,
                order=order,
                type="Waste Collected",
            )
            # employee notification
            Notification.objects.create(
                user=new_form.waste_plan.user,
                waste_plan=order.waste_plan,
                order=order,
                type="Waste Collected",
            )
            messages.success(request, "Collected Status Updated")
            return redirect("employee:subscribed_plan_detail", order.oid)
    else:
        form = CollectionStatusForm(instance=order)
    context = {
        "order":order,
        "form":form,
    }
    return render(request, "employee/subscribed_plan_detail.html", context)



@login_required
def collected_waste(request):
    query = request.GET.get("oid")
    if query:
        orders = WasteOrder.objects.filter(active=True, collector__user=request.user, oid=query)
    
    if query == "collected":
        orders = WasteOrder.objects.filter(active=True, collector__user=request.user, payment_status="paid", collected_status="Collected")
    if query == "uncollected":
        orders = WasteOrder.objects.filter(active=True, collector__user=request.user, payment_status="paid", collected_status="Not Collected")
    if query == None or query == "":
        orders = WasteOrder.objects.filter(active=True, collector__user=request.user, payment_status="paid")
    

    print("query =======", query)
    context = {
        "orders":orders
    }
    return render(request, "employee/collected_waste.html", context)


@login_required
def collected_waste_detail(request, oid):
    order = WasteOrder.objects.get(oid=oid, collector__user=request.user, active=True)

    context = {
        "order":order,
    }
    return render(request, "employee/collected_waste_detail.html", context)




@login_required
def settings(request):
    if request.method == "POST":
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, "Profile Updated Successfull")
            return redirect('employee:settings')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'p_form': p_form,
        'u_form': u_form,
    }
    return render(request, 'employee/settings.html', context)