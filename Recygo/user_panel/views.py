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

from user_panel.forms import WasteItemForm
from core.models import WasteItem, WastePlan, WasteOrder, Notification
from addon.models import Company, BasicAddon



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
def dashboard(request):
    order = WasteOrder.objects.filter(user=request.user, payment_status="paid")
    collected_waste = WasteOrder.objects.filter(user=request.user, payment_status="paid", collected_status="Collected")
    noti = Notification.objects.filter(user=request.user, is_read=False)
    total_amount = WasteOrder.objects.filter(user=request.user, payment_status="paid").aggregate(total_amount=Sum("price"))['total_amount']

    output = (
       WasteOrder.objects
        .filter(user=request.user, payment_status="paid")
        .annotate(
            month=ExtractMonth("date")
        )
        .values("month")
        .annotate(
            total=Sum(
                F("price"),
                output_field=FloatField()
            )
        )
        .order_by("month")
    )
    monthNumber=[]
    amountTotal=[]
    for d in output:
        monthNumber.append(calendar.month_name[d['month']])
        amountTotal.append(d['total'])

    context = {
        "order":order,
        "collected_waste":collected_waste,
        "total_amount":total_amount,
        "amountTotal":amountTotal,
        "monthNumber":monthNumber,
        "noti":noti,
    }
    return render(request, "dashboard/dashboard.html", context)

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
    return render(request, "dashboard/notifications.html", context)

@login_required
def notification_detail(request, oid):
    noti = Notification.objects.get(user=request.user, oid=oid)
    noti.is_read = True 
    noti.save()
    context = {
        "noti":noti
    }
    return render(request, "dashboard/notification_detail.html", context)


@login_required
def mark_noti_as_seen(request, oid):
    noti = Notification.objects.get(user=request.user, oid=oid)
    noti.is_read = True 
    noti.save()
    return redirect("dashboard:notifications")

@login_required
def waste_plans(request):
    waste_plans = WastePlan.objects.filter(active=True)
    
    context = {
        "waste_plans":waste_plans
    }
    return render(request, "dashboard/waste_plans.html", context)

@login_required
def waste_order_details(request, slug):
    waste_plan = WastePlan.objects.get(slug=slug, active=True)
    user = request.user
    price = waste_plan.price 

    if request.method == "POST":
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        waste_order = WasteOrder.objects.create(
            user=user,
            waste_plan=waste_plan,
            price=price,
            payment_status="initiated",
            address=address,
            phone=phone,
            active=True
        )

        messages.success(request, "Waste Order Created, Checkout Now!")
        return redirect("dashboard:waste_checkout", waste_order.oid)
    
    context = {
        "waste_plan":waste_plan
    }
    return render(request, "dashboard/waste_order_details.html", context)

@login_required
def waste_checkout(request, oid):
    order = WasteOrder.objects.get(oid=oid, active=True)

    context = {
        "order":order
    }
    return render(request, "dashboard/waste_checkout.html", context)


@csrf_exempt
def create_checkout_session(request, id):
    request_data = json.loads(request.body)
    order = get_object_or_404(WasteOrder, oid=id)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        customer_email = order.email,
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                    'name': order.full_name,
                    },
                    
                    'unit_amount': int(order.total * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('dashboard:success')) + "?session_id={CHECKOUT_SESSION_ID}&success_key=payment_successfull",
        cancel_url=request.build_absolute_uri(reverse('dashboard:failed'))+ "?session_id={CHECKOUT_SESSION_ID}",
    )

    order.payment_status = "processing"
    order.stripe_payment_intent = checkout_session['id']
    order.save()

    print("checkout_session ==============", checkout_session)
    return JsonResponse({'sessionId': checkout_session.id})


@login_required
def payment_success(request, oid, *args, **kwargs):
    success_id = request.GET.get('Success_id')
    order_total = request.GET.get('Order_total')

    # if success_id and order_total: 
    success_id = success_id.rstrip('/')
    order_total = order_total.rstrip('/')
    order = WasteOrder.objects.get(oid=oid, success_id=success_id)
    
    if order.price == Decimal(order_total):
        if order.payment_status == "initiated": # initiated
            order.payment_status = "paid"
            order.pickup_status = "processing"
            order.save()

            Notification.objects.create(
                user=order.waste_plan.user,
                waste_plan=order.waste_plan,
                order=order,
                type="New Subscriber",
            )
            
            company = Company.objects.all().first()
            basic_addon = BasicAddon.objects.all().first()

            if basic_addon.send_email_notifications == True:

                # Customer Email
                merge_data = {
                    'company': company, 
                    'order': order, 
                }
                subject = f"Order Placed Successfully. ID {order.oid}"
                text_body = render_to_string("email/payment_success.txt", merge_data)
                html_body = render_to_string("email/payment_success.html", merge_data)
                msg = EmailMultiAlternatives(
                    subject=subject, from_email=settings.FROM_EMAIL,
                    to=[order.user.email], body=text_body
                )
                msg.attach_alternative(html_body, "text/html")
                msg.send()


                # Admin Email
                merge_data = {
                    'company': company, 
                    'order': order, 
                }
                subject = f"Order Placed Successfully. ID {order.oid}"
                text_body = render_to_string("email/admin_new_plan.txt", merge_data)
                html_body = render_to_string("email/admin_new_plan.html", merge_data)
                msg = EmailMultiAlternatives(
                    subject=subject, from_email=settings.FROM_EMAIL,
                    to=[settings.FROM_EMAIL], body=text_body
                )
                msg.attach_alternative(html_body, "text/html")
                msg.send()

        elif order.payment_status == "paid":
            messages.success(request, f'Your Order have been recieved.')
            return redirect("dashboard:dashboard")
        else:
            messages.success(request, 'Opps... Internal Server Error; please try again later')
            return redirect("dashboard:dashboard")
    else:
        messages.error(request, "Error: Payment Manipulation Detected, This payment have been cancelled")
        order.payment_status = "failed"
        order.save()
        return redirect("/")
    # else:
    #     messages.error(request, "Error: Payment Manipulation Detected, This payment have been cancelled")
    #     order.payment_status = "failed"
    #     order.save()
    #     return redirect("/")
    
    context = {
        "order": order, 
    }
    return render(request, "dashboard/payment_success.html", context) 

@login_required
def payment_failed(request, oid):
    order = WasteOrder.objects.get(oid=oid, active=True)
    context = {
            "order":order
        }
    return render(request, "dashboard/payment_failed.html", context) 

@login_required
def invoices(request):
    orders = WasteOrder.objects.filter(active=True, user=request.user, payment_status="paid")
    query = request.GET.get("oid")
    if query:
        orders = WasteOrder.objects.filter(active=True, user=request.user, oid=query)
    if query == "paid":
        orders = WasteOrder.objects.filter(active=True, user=request.user, payment_status="paid")
    if query == "unpaid":
        orders = WasteOrder.objects.filter(active=True, user=request.user, payment_status="initiated")
    if query == None or query == "":
        orders = WasteOrder.objects.filter(active=True, user=request.user, payment_status="paid")

    print("query =======", query)
    context = {
        "orders":orders
    }
    return render(request, "dashboard/invoices.html", context)


@login_required
def history(request):
    orders = WasteOrder.objects.filter(user=request.user)
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
        orders = WasteOrder.objects.filter(user=request.user)

    print("query =======", query)
    context = {
        "orders":orders
    }
    return render(request, "dashboard/history.html", context)


@login_required
def history_detail(request, oid):
    order = WasteOrder.objects.get(oid=oid, active=True)

    context = {
        "order":order
    }
    return render(request, "dashboard/history_detail.html", context)


@login_required
def spending(request):
    one_month_ago = datetime.today() - timedelta(days=28)
    monthly_earning = WasteOrder.objects.filter(active=True, user=request.user, payment_status="paid", date__gte=one_month_ago).aggregate(amount=models.Sum('price'))
    total_amount = WasteOrder.objects.filter(user=request.user, payment_status="paid").aggregate(total_amount=Sum("price"))['total_amount']
    
    output = (
        WasteOrder.objects
            .filter(active=True, user=request.user, payment_status="paid")
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
        "monthly_earning":monthly_earning,
        "output":output,
        "total_amount":total_amount,
    }
    return render(request, "dashboard/spending.html", context)

@login_required
def invoice(request, oid):
    order = WasteOrder.objects.get(oid=oid, active=True)

    context = {
        "order":order
    }
    return render(request, "dashboard/invoice.html", context)