from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import *
from django.http import QueryDict
from django.contrib import messages
from django.core.paginator import Paginator
from django.urls import reverse
from .forms import *
from .decorators import *
from django.forms import widgets
from django.views.generic.edit import UpdateView
from django.utils.decorators import method_decorator


# Create your views here.

@login_check_decorator
def user_logout(request):
    if 'user' in request.session:
        request.session.flush()
        return redirect('/')
    return redirect('/')


@is_login
def user_login(request):
    if request.POST:
        next_val_dict = QueryDict(request.META['QUERY_STRING'])
        next_val = next_val_dict.get('next') or '/'
        email = request.POST['email']
        u_password = request.POST['password']
        u = user.objects.filter(email=email, password=u_password)
        if u:
            if u[0].user_status == 'P':
                messages.add_message(request, messages.INFO, 'Plz Wait Until Admin Approved Your Request.')
                return HttpResponseRedirect(reverse('user_login'))
            elif u[0].user_status == 'A':
                request.session['user'] = str(u[0].user_id)
                request.session['user_name'] = u[0].name
                return redirect(next_val)
            if u[0].user_status == 'B':
                messages.add_message(request, messages.INFO, 'You Cannot Login Admin Block Your Account.')
                return HttpResponseRedirect(reverse('user_login'))
        else:
            messages.add_message(request, messages.INFO, 'User Name And Password Are Not Match.')
            return HttpResponseRedirect(reverse('user_login'))
    else:
        return render(request, 'login.html', {"name": "User"})


def index(request):
    return render(request, 'index.html')


def movies(request):
    return render(request, 'movies.html')


@is_login
def user_register(request):
    form = registerForm()
    if request.method == "POST":
        form = registerForm(request.POST)
        if form.is_valid():
            p1 = form.cleaned_data['password']
            p2 = form.cleaned_data['rPassword']
            numb = form.cleaned_data['phone']
            if p1 == p2:
                if numb.isdigit() and len(numb) > 10:
                    f = form.save(commit=False)
                    f.save()
                    return redirect("index")
                messages.add_message(request, messages.INFO, f'Plz Enter Valid Phone Number')
                return render(request, 'register.html', {'form': form})
            messages.add_message(request, messages.INFO, f'Password And Confirm Password Must Be Same')
    return render(request, 'register.html', {'form': form})


@method_decorator(login_check_decorator, name='dispatch')
class user_edit_profile(UpdateView):
    template_name = 'form.html'
    model = user
    fields = ['name', 'email', 'address', 'phone', 'password', 'gender']

    def get(self, request, *args, **kwargs):
        get = super().get(request, *args, **kwargs)
        u_id = uuid.UUID(self.request.session.get('user'))
        u = user.objects.get(user_id=u_id)
        if not u == self.object:
            return HttpResponseRedirect(reverse('index'))
        return get

    def get_form(self):
        '''add date picker in forms'''
        form = super(user_edit_profile, self).get_form()
        form.fields['phone'].widget = widgets.DateInput(
            attrs={'readonly': 'true'})
        return form

    def form_valid(self, form):
        u_id = uuid.UUID(self.request.session.get('user'))
        u = user.objects.get(user_id=u_id)
        if not (u.phone == form.cleaned_data['phone']):
            messages.warning(self.request, 'You Cannot Change Register Number')
            return super().form_invalid(form)
        else:
            self.request.session['user_name'] = form.cleaned_data['name']
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['model_name'] = 'Update User'
        return context_data
