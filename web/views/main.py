from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import login as view_login, logout_then_login
from django.contrib.auth.models import User
from django.db.models import Count

from web.models import *

@login_required
def home(request):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/aluno/home.html', {})
    elif hasattr(request.user, 'professor'):
        listas = Lista.objects.filter(grupo__professor = request.user.professor, inativo = False)[:5]
        grupos = Grupo.objects.filter(professor = request.user.professor, inativo = False)\
        .annotate(qtd_alunos = Count('alunos'))[:5]
        exercicios = Exercicio.objects.filter(professor = request.user.professor, inativo = False)[:5]

        return render(request, 'web/professor/home.html', {
            'listas': listas,
            'grupos': grupos,
            'exercicios': exercicios
        })
    return redirect(logout_then_login)

def error404(request):
    return render(request,'web/page_404.html')
