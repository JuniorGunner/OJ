from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import login as view_login, logout_then_login
from django.contrib.auth.models import User

from web.models import *

@login_required
def grupos(request):
    if hasattr(request.user, 'professor'):
        return render(request, 'web/page_403.html', {})
    return render(request, 'web/aluno/grupos.html', {})

@login_required
def listas(request):
    if hasattr(request.user, 'professor'):
        return render(request, 'web/page_403.html', {})
    return render(request, 'web/aluno/listas.html', {})

@login_required
def submissoes(request):
    if hasattr(request.user, 'professor'):
        return render(request, 'web/page_403.html', {})
    return render(request, 'web/aluno/minhas_submissoes.html', {})
