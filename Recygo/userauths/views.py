from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.auth import logout
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse


import urllib.parse
from datetime import timedelta
import shortuuid

from addon.models import Company, EarningPoints, BasicAddon
from addon.models import NewsLetter
from userauths.models import Profile, User
from userauths.forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm, EmailUpdateForm

# Create your views here.

def Register(request, *args, **kwargs):
    try:
        addon = BasicAddon.objects.all().first()
    except:
        addon = None
    if request.user.is_authenticated:
        messages.warning(request, f"Hey {request.user.username}, you are already logged in")
        return redirect('core:home')   

    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('email')
            full_name = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # Generate and save otp
            uuid_key = shortuuid.uuid()
            otp = uuid_key[:7]

            # Send Email OTP 
            if addon:
                if addon.send_email_notifications == True:
                    company = Company.objects.all().first()
                    merge_data = {
                        'company': company,
                        'full_name':full_name, 
                        'otp':otp, 
                    }
                    subject = f"Welcome to {company.name}, Verify Your Account Now."
                    text_body = render_to_string("email/message_otp.txt", merge_data)
                    html_body = render_to_string("email/message_otp.html", merge_data)
                    
                    msg = EmailMultiAlternatives(
                        subject=subject, from_email=settings.FROM_EMAIL,
                        to=[username], body=text_body
                    )
                    msg.attach_alternative(html_body, "text/html")
                    msg.send()
            else:
                print("No Addon")
                

            user = authenticate(username=username, password=password)
            login(request, user)

            NewsLetter.objects.create(email=username)
            messages.success(request, f"Hi {request.user.username}, your account was created successfully.")
            request.user.otp = otp
            request.user.save()

            profile = Profile.objects.get(user=request.user)
            profile.full_name = form.cleaned_data.get("username")
            profile.save()

            request.user.otp = otp
            request.user.save()

            next_url = request.GET.get("next", 'dashboard:dashboard')
            return redirect(next_url)
    else:
        form = UserRegisterForm()
    context = {'form':form}
    return render(request, 'userauths/sign-up.html', context)


def loginView(request):

    # if request.user.is_authenticated:
    #     return redirect('core:dashboard')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are Logged In")
                # return HttpResponseRedirect(request.GET['next'])
                next_url = request.GET.get("next", 'dashboard:dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Username or password does not exit.')
        
        except:
            messages.error(request, 'User does not exist')

    return HttpResponseRedirect("/")


def loginViewTemp(request):
    # messages.success(request, f"Login for better experience.")
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('core:home')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are Logged In")
                # return redirect()
                next_url = request.GET.get("next", 'dashboard:dashboard')
                return redirect(next_url)
                
            else:
                messages.error(request, 'Username or password does not exit.')
        
        except:
            messages.error(request, 'User does not exist')

    return render(request, "userauths/sign-in.html")



def logoutView(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect("userauths:sign-in")


@login_required
def settings(request):
    if request.method == "POST":
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)

        if p_form.is_valid() and u_form.is_valid():
            p_form.save()
            u_form.save()
            messages.success(request, "Profile Updated Successfull")
            return redirect('dashboard:settings')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)

    context = {
        'p_form': p_form,
        'u_form': u_form,
    }
    return render(request, 'dashboard/settings.html', context)

