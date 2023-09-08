from django.conf import settings

from addon.models import BasicAddon, Company
from core.models import Notification

def default(request):

    try:
        basic_addon = BasicAddon.objects.all().first()
    except:
        basic_addon = None 

    try:
        company = Company.objects.all().first()
    except:
        company = None 

    try:
        ca = basic_addon.currency_abbreviation
        cs = basic_addon.currency_sign
    except:
        ca = "USD"
        cs = "$"
    
    try:
        noti_ = Notification.objects.filter(user=request.user, is_read=False)
    except:
        noti_ = None

    try:
        noti_admin = Notification.objects.filter(user=request.user, is_read=False)
    except:
        noti_admin = None

    try:
        noti_employee = Notification.objects.filter(user=request.user, is_read=False)
    except:
        noti_employee = None

    return {
        "noti_":noti_,
        "noti_admin":noti_admin,
        "noti_employee":noti_employee,
        "basic_addon":basic_addon,
        "company":company,
        "cs":cs,
        "ca":ca,
        "PAYPAL_CLIENT_ID": settings.PAYPAL_CLIENT_ID,
        "WEBSITE_URL": settings.WEBSITE_URL,
        "flutter_publick_key":settings.FLUTTERWAVE_PUBLIC,
    }