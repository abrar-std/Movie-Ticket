from django.shortcuts import redirect,HttpResponse
from .models import *
from corecode.models import *


def login_check_decorator(fun):
    def login_check(request, *args, **kwargs):
        if 'admin' in request.session:
            return fun(request, *args, **kwargs)
        else:
            return redirect(f"/admin/?next={request.path}")

    return login_check


def is_login(fun):
    def login_check(request, *args, **kwargs):
        if 'admin' in request.session:
            return redirect("admin_dashboard")
        else:
            return fun(request, *args, **kwargs)

    return login_check
