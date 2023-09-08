from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from core.models import Donation, Notification

def index(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        amount = request.POST.get("donation_amount")

        donation = Donation.objects.create(
            full_name=full_name,
            email=email,
            amount=amount,
            payment_status="initiated",
        )
        return redirect("core:donation_checkout", donation.did)
    
    return render(request, "core/index.html")

def donation_checkout(request, did):
    donation = Donation.objects.get(did=did)
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        amount = request.POST.get("donation_amount")

        donation = Donation.objects.create(
            full_name=full_name,
            email=email,
            amount=amount,
            payment_status="initiated",
        )
        return redirect("core:donation_checkout", donation.did)
    
    context = {
        "donation":donation
    }
    return render(request, "core/donation_checkout.html", context)


def payment_success(request, did, *args, **kwargs):
    success_id = request.GET.get('Success_id')
    order_total = request.GET.get('Order_total')

    # if success_id and order_total: 
    success_id = success_id.rstrip('/')
    order_total = order_total.rstrip('/')
    order = Donation.objects.get(did=did, success_id=success_id)
    
    if order.amount == Decimal(order_total):
        if order.payment_status == "initiated": # initiated
            order.payment_status = "paid"
            order.pickup_status = "processing"
            order.save()

        elif order.payment_status == "paid":
            messages.success(request, f'Your have been recieved successfully, thanks you.')
            return redirect("/")
        else:
            messages.success(request, 'Opps... Internal Server Error; please try again later')
            return redirect("/")
    else:
        messages.error(request, "Error: Payment Manipulation Detected, This payment have been cancelled")
        order.payment_status = "failed"
        order.save()
        return redirect("/")
    
    
    context = {
        "order": order, 
    }
    return render(request, "core/payment_success.html", context) 

@login_required
def payment_failed(request, oid):
    order = WasteOrder.objects.get(oid=oid, active=True)
    context = {
            "order":order
        }
    return render(request, "dashboard/payment_failed.html", context) 
