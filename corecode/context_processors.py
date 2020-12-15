from .models import *
from django.shortcuts import redirect


def site_defaults(request):
    contexts ={

    }
    if request.session.get('user'):
        u_id = uuid.UUID(request.session.get('user'))
        u = user.objects.get(user_id=u_id)
        contexts = {
                "user": u,
            }
    return contexts
