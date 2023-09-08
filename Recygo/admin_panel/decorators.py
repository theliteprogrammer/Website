from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser != True:
            messages.warning(request, "You are un-authorised to access the this page")
            return redirect('/') 

        return view_func(request, *args, **kwargs)

    return wrapper
