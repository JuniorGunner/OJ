from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import login as view_login, logout_then_login
from django.contrib.auth.models import User

from web.models import *

@login_required
def grupos(request):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})
    return render(request, 'web/professor/grupos.html', {})

@login_required
def criar_grupo(request):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})
    return render(request, 'web/professor/criar_grupo.html', {})

@login_required
def listas(request):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})
    return render(request, 'web/professor/listas.html', {})

@login_required
def criar_lista(request):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})
    return render(request, 'web/professor/criar_lista.html', {})

@login_required
def exercicios(request):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})
    return render(request, 'web/professor/exercicios.html', {})

@login_required
def criar_exercicio(request):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})
    return render(request, 'web/professor/criar_exercicio.html', {})
