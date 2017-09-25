from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.views import login as view_login, logout_then_login
from django.contrib.auth.models import User
from django.db.models import Count
from django.core.files.storage import FileSystemStorage

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from django.utils import timezone
import datetime
# import pytz

import urllib.parse
import json

from OJL3 import judges

from web.models import *

import operator

@login_required
def grupos(request):
    if hasattr(request.user, 'professor'):
        return render(request, 'web/page_403.html', {})

    grupos = Grupo.objects.filter(inativo = False)\
    .order_by('nome').annotate(qtd_alunos = Count('alunos'))\
    .filter(alunos = request.user.aluno)

    return render(request, 'web/aluno/grupos.html', {'grupos': grupos})

@login_required
def grupo(request, id):
    if hasattr(request.user, 'professor'):
        return render(request, 'web/page_403.html', {})

    grupo = get_object_or_404(Grupo, id = id, inativo = False)

    if not request.user.aluno in grupo.alunos.all():
        return render(request, 'web/page_403.html', {})

    listas = Lista.objects.filter(grupo = grupo, inativo = False)

    return render(request, 'web/aluno/grupo.html', {'grupo': grupo, 'listas': listas})

@login_required
def listas(request):
    if hasattr(request.user, 'professor'):
        return render(request, 'web/page_403.html', {})

    listas = Lista.objects.filter(grupo__alunos = request.user.aluno,
    inativo = False, submeter = True).order_by('titulo')

    return render(request, 'web/aluno/listas.html', {'listas': listas})

@login_required
def lista(request, id):
    if hasattr(request.user, 'professor'):
        return render(request, 'web/page_403.html', {})

    lista = get_object_or_404(Lista, id = id, inativo = False, submeter = True)

    if not request.user.aluno in lista.grupo.alunos.all():
        return render(request, 'web/page_403.html', {})

    exercicios_sub = []
    exercicios = Exercicio.objects.filter(lista = lista)
    for exercicio in exercicios:
        submissoes = Submissao.objects.filter(lista = lista, aluno = request.user.aluno,
        exercicio = exercicio).order_by('hora_submissao')
        exercicio_sub = {'exercicio': exercicio}

        tentativas = 0
        for submissao in submissoes:
            tentativas += 1
            if submissao.status == 1:
                exercicio_sub['status'] = True
                break

        exercicio_sub['tentativas'] = tentativas
        exercicios_sub.append(exercicio_sub)

    # print(exercicios_sub)

    # submissoes = Submissao.objects.filter()

    alunos = []

    alunos_lista = Aluno.objects.filter(grupo__lista = lista)

    for aluno in alunos_lista:
        exercicios_aluno = []
        qtd_resolvida = 0
        total_tentativas = 0
        for exercicio in exercicios:

            submissoes = Submissao.objects.filter(lista = lista, aluno = aluno,
            exercicio = exercicio).order_by('hora_submissao')
            exercicio_aluno = {'exercicio': exercicio}

            tentativas = 0
            for submissao in submissoes:
                tentativas += 1
                if submissao.status == 1:
                    exercicio_aluno['status'] = True
                    qtd_resolvida += 1
                    break

            exercicio_aluno['tentativas'] = tentativas
            exercicios_aluno.append(exercicio_aluno)
            total_tentativas += tentativas

        alunos.append({
            'aluno': aluno,
            'exercicios_aluno': exercicios_aluno,
            'qtd_resolvida': qtd_resolvida,
            'nome': aluno.user.get_full_name(),
            'total_tentativas': total_tentativas
        })

        alunos.sort(key = operator.itemgetter('nome'))
        alunos.sort(key = operator.itemgetter('total_tentativas'))
        alunos.sort(key = operator.itemgetter('qtd_resolvida'), reverse = True)

    return render(request, 'web/aluno/lista.html', {
        'lista': lista,
        'alunos': alunos,
        'exercicios_sub': exercicios_sub
    })

@login_required
def exercicio_lista(request, lista, id):
    if hasattr(request.user, 'professor'):
        return render(request, 'web/page_403.html', {})

    lista = get_object_or_404(Lista, id = lista, inativo = False, submeter = True)
    exercicio = get_object_or_404(Exercicio, id = id, inativo = False)

    if not exercicio in lista.exercicios.all():
        return render(request, 'web/page_403.html', {})

    if not request.user.aluno in lista.grupo.alunos.all():
        return render(request, 'web/page_403.html', {})

    exemplos = {}

    with open(os.path.join(exercicio.caminho(), 'in/sample/1.txt'), 'r') as f:
        exemplos['entrada'] = f.read().splitlines()
    with open(os.path.join(exercicio.caminho(), 'out/sample/1.txt'), 'r') as f:
        exemplos['saida'] = f.read().splitlines()

    # utc = pytz.UTC
    # print(utc.localize(lista.prazo.replace(tzinfo=utc)))

    pode_submeter = timezone.now() < lista.prazo

    exercicio_sub = 0

    submissoes = Submissao.objects.filter(lista = lista, aluno = request.user.aluno,
    exercicio = exercicio).order_by('hora_submissao')

    for submissao in submissoes:
        if submissao.status == 1:
            exercicio_sub = submissao.id
            break

    return render(request, 'web/aluno/exercicio.html', {
        'exercicio': exercicio,
        'exemplos': exemplos,
        'lista': lista,
        'pode_submeter': pode_submeter,
        'exercicio_sub': exercicio_sub
    })

@login_required
def resposta_exercicio(request, lista, id):
    if hasattr(request.user, 'professor'):
        return render(request, 'web/page_403.html', {})

    lista = get_object_or_404(Lista, id = lista, inativo = False, submeter = True)
    exercicio = get_object_or_404(Exercicio, id = id, inativo = False)

    if not exercicio in lista.exercicios.all():
        return render(request, 'web/page_403.html', {})

    if not request.user.aluno in lista.grupo.alunos.all():
        return render(request, 'web/page_403.html', {})

    if timezone.now() < lista.prazo:
        return render(request, 'web/page_403.html', {})

    codigo = ''

    with open(os.path.join(exercicio.caminho(), 'solucao', 'solucao.py'), 'r') as f:
        codigo = f.read()

    return render(request, 'web/aluno/resposta.html',
    {
        'exercicio': exercicio,
        'lista': lista,
        'codigo': codigo
    })

@login_required
def submeter_exercicio(request, lista, id):
    if hasattr(request.user, 'professor'):
        return render(request, 'web/page_403.html', {})

    lista = get_object_or_404(Lista, id = lista, inativo = False, submeter = True)
    exercicio = get_object_or_404(Exercicio, id = id, inativo = False)

    if not exercicio in lista.exercicios.all():
        return render(request, 'web/page_403.html', {})

    if not request.user.aluno in lista.grupo.alunos.all():
        return render(request, 'web/page_403.html', {})

    if lista.prazo < timezone.now():
        return render(request, 'web/page_404.html', {})

    return render(request, 'web/aluno/submeter.html', {'exercicio': exercicio, 'lista': lista})

@login_required
def submissao_codigo(request, listaid, id):
    if hasattr(request.user, 'professor'):
        return render(request, 'web/page_403.html', {})

    lista = get_object_or_404(Lista, id = listaid, inativo = False, submeter = True)
    exercicio = get_object_or_404(Exercicio, id = id, inativo = False)

    if not exercicio in lista.exercicios.all():
        return render(request, 'web/page_403.html', {})

    if not request.user.aluno in lista.grupo.alunos.all():
        return render(request, 'web/page_403.html', {})

    if lista.prazo < timezone.now():
        return render(request, 'web/page_404.html', {})

    if request.method == 'POST':
        mensagem = ''
        erro = True

        if request.POST['tipo_submissao'] == 'arquivo' and not 'arquivo-codigo' in request.FILES:
            mensagem = 'Arquivo não submetido.'

            messages.add_message(request, messages.ERROR, mensagem)

            return HttpResponseRedirect(reverse('web.views.aluno.confirmacao_submissao'))

        submissao = Submissao(
            exercicio = exercicio,
            lista = lista,
            aluno = request.user.aluno,
            status = Submissao.STATUS['AGUARDANDO']
        )

        submissao.save()

        arquivo = None

        caminho_arquivo = submissao.caminho()

        if not os.path.exists(caminho_arquivo):
            os.makedirs(caminho_arquivo, mode=0o770)

        if request.POST['tipo_submissao'] == 'arquivo':
            arquivo = request.FILES['arquivo-codigo']

            fs = FileSystemStorage(location = caminho_arquivo)
            fs.save(str(submissao.id) + '.py', arquivo)
        elif request.POST['tipo_submissao'] == 'editor':
            codigo = request.POST['editor_codigo']

            with open(os.path.join(caminho_arquivo, str(submissao.id) + '.py'), 'w') as f:
                f.writelines(codigo)
                f.close()

        (status, resultado) = judges.send_to_IOCJ(
            prob_path = submissao.exercicio.caminho(),
            submission_code = str(submissao.id),
            lang = 'python3',
            source_path = os.path.join(caminho_arquivo, str(submissao.id) + '.py'),
            overwrite_prison_cell = True
        )

        count_AC = 0
        count_WA = 0
        count_TLE = 0
        count_NZEC = 0
        count_outros = 0

        for resultado in resultado.items():
            res = resultado[1].popitem(last = False)[1]

            if res == 'AC':
                count_AC += 1
            elif res == 'WA':
                count_WA += 1
            elif res == 'TLE':
                count_TLE += 1
            elif res == 'NZEC':
                count_NZEC += 1
            else:
                count_outros += 1

        if count_outros > 0:
            submissao.status = Submissao.STATUS['OUTRO']
        elif count_NZEC > 0:
            submissao.status = Submissao.STATUS['NZEC']
        elif count_TLE > 0:
            submissao.status = Submissao.STATUS['TLE']
        elif count_WA > 0:
            submissao.status = Submissao.STATUS['WA']
        elif count_AC > 0:
            submissao.status = Submissao.STATUS['AC']
            erro = False

        mensagem = Submissao.STATUS_STR[submissao.status]

        submissao.save()

        if erro:
            messages.add_message(request, messages.ERROR, mensagem)
        else:
            messages.add_message(request, messages.SUCCESS, mensagem)

        return HttpResponseRedirect(reverse('web.views.aluno.confirmacao_submissao'))
    else:
        mensagem = 'Nenhum código submetido.'
        messages.add_message(request, messages.ERROR, mensagem)

    return HttpResponseRedirect(reverse('web.views.aluno.confirmacao_submissao'))

@login_required
def confirmacao_submissao(request):
    msgs = messages.get_messages(request)

    if not msgs:
        return render(request, 'web/page_404.html', {})

    mensagem = None
    for msg in msgs:
        mensagem = msg
        break

    return render(request, 'web/aluno/confirmacao_submissao.html', {
        'mensagem': mensagem
    })

@login_required
def tutor(request):
    if hasattr(request.user, 'professor'):
        return render(request, 'web/page_403.html', {})

    mensagem = ''
    codigo_url = ''

    if request.method == 'POST':
        codigo = ''

        if request.POST['tipo_submissao'] == 'arquivo':
            if 'arquivo-codigo' in request.FILES:
                arquivo = request.FILES['arquivo-codigo']

                codigo = {'code': arquivo.read()}
                codigo_url = urllib.parse.urlencode(codigo)
            else:
                mensagem = 'Arquivo não submetido.'
        elif request.POST['tipo_submissao'] == 'editor':
            codigo = {'code': request.POST['editor_codigo']}
            codigo_url = urllib.parse.urlencode(codigo)
    else:
        mensagem = 'Nenhum código submetido.'

    return render(request, 'web/aluno/tutor.html', {'codigo': codigo_url, 'mensagem': mensagem})

@login_required
def submissoes(request):
    if hasattr(request.user, 'professor'):
        return render(request, 'web/page_403.html', {})

    submissoes = Submissao.objects.filter(aluno = request.user.aluno,
    lista__inativo = False).order_by('-hora_submissao')

    return render(request, 'web/aluno/minhas_submissoes.html', {'submissoes': submissoes})

@login_required
def submissao(request, id):
    if hasattr(request.user, 'professor'):
        return render(request, 'web/page_403.html', {})

    submissao = get_object_or_404(Submissao, id = id, lista__inativo = False, aluno = request.user.aluno)

    codigo = ''

    with open(os.path.join(submissao.caminho(), str(submissao.id) + '.py'), 'r') as f:
        codigo = f.read()

    return render(request, 'web/aluno/submissao.html',{'submissao': submissao, 'codigo': codigo})
