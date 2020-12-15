from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.http import QueryDict
from corecode.models import *
from .models import *
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from .decorators import *


# Create your views here.
@login_check_decorator
def admin_logout(request):
    if 'admin' in request.session:
        request.session.flush()
        return redirect('/')
    return redirect('/')


@is_login
def admin_login(request):
    if request.POST:
        next_val_dict = QueryDict(request.META['QUERY_STRING'])
        next_val = next_val_dict.get('next') or 'admin_dashboard'
        u_email = request.POST['email']
        u_password = request.POST['password']
        u = site_admin.objects.filter(email=u_email, password=u_password)
        if u:
            request.session['admin'] = str(u[0].admin_id)
            request.session['admin_name'] = u[0].name
            return redirect(next_val)
        else:
            messages.add_message(request, messages.INFO, 'User Name And Password Are Not Match')
    return render(request, 'site_admin/admin_login.html', {"name": "Admin"})

@login_check_decorator
def admin_dashboard(request):
    return render(request, 'site_admin/index.html', )

@login_check_decorator
def admin_manage_users(request):
    if request.method == 'POST':
        user_id = request.POST['u_id']
        user_status = request.POST['u_status']
        u = user.objects.get(user_id=uuid.UUID(user_id))
        if user_status == 'Delete':
            u = user.objects.get(user_id=uuid.UUID(user_id))
            u.delete()
            messages.add_message(request, messages.SUCCESS, f'{u.name}  Is Successfully Deleted')
            return HttpResponseRedirect(reverse("admin_manage_users"))
        elif user_status == 'Approved':
            u.user_status = "A"
            u.save(update_fields=['user_status'])
            return HttpResponseRedirect(reverse('admin_manage_users'))
        elif user_status == 'Pending':
            u.user_status = "P"
            u.save(update_fields=['user_status'])
            return HttpResponseRedirect(reverse('admin_manage_users'))
        elif user_status == 'Blocked':
            u.user_status = "B"
            u.save(update_fields=['user_status'])
            return HttpResponseRedirect(reverse('admin_manage_users'))
    else:
        users = user.objects.filter().order_by('-reg_date')
        p = Paginator(users, 5)
        page_no = request.GET.get('page') or 1
        pages = p.page(page_no)
        return render(request, 'site_admin/user/users.html', {'page_obj': pages})

@login_check_decorator
def admin_search_users(request):
    if request.method == 'POST':
        users = user.objects.filter(name__contains=request.POST['search_id'].lower()).order_by('-reg_date')
    p = Paginator(users, 5)
    page_no = request.GET.get('page') or 1
    pages = p.page(page_no)
    return render(request, 'site_admin/user/users.html', {'page_obj': pages})
