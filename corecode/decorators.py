from django.shortcuts import redirect,HttpResponse,HttpResponseRedirect
from django.urls import reverse
import uuid
from .models import *


def login_check_decorator(fun):
    def login_check(request, *args, **kwargs):
        if 'user' in request.session:
            return fun(request, *args, **kwargs)
        else:
            return redirect(f"/user_login?next={request.path}")

    return login_check


def is_login(fun):
    def login_check(request, *args, **kwargs):
        if 'user' in request.session:
            return redirect("index")
        else:
            return fun(request, *args, **kwargs)

    return login_check
