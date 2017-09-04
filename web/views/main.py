from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import login as view_login, logout_then_login
from django.contrib.auth.models import User

from web.models import *

@login_required
def home(request):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/aluno/home.html', {})
    elif hasattr(request.user, 'professor'):
        return render(request, 'web/professor/home.html', {})
    return redirect(logout_then_login)
