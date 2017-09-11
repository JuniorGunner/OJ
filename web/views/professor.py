from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.views import login as view_login, logout_then_login
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Count

import datetime

import os
import json

from web.models import *

@login_required
def excluir_grupo(request, id):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    grupo = get_object_or_404(Grupo, id = id, inativo = False)

    if grupo.professor != request.user.professor:
        return render(request, 'web/page_403.html', {})

    grupo.inativo = True
    grupo.save()

    return redirect('web.views.professor.grupos')

@login_required
def grupos(request):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    grupos = Grupo.objects.filter(professor = request.user.professor, inativo = False)\
    .order_by('nome').annotate(qtd_alunos = Count('alunos'))

    return render(request, 'web/professor/grupos.html', {'grupos': grupos})

@login_required
def criar_grupo(request):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    alunos = Aluno.objects.all()

    mensagem = ''

    if request.method == 'POST' and 'table_records' in request.POST:
        # recupera campos da requisição
        nome = request.POST['nome']
        alunos_grupo = request.POST.getlist('table_records')

        grupo = Grupo(nome = nome, professor = request.user.professor)
        grupo.save()

        for aluno in alunos_grupo:
            try:
                aluno_grupo = User.objects.get(pk = aluno)
            except:
                pass

            grupo.alunos.add(aluno_grupo.aluno)

        grupo.save()

        mensagem = 'Grupo adicionado com sucesso.'
    elif request.method == 'POST' and not 'table_records' in request.POST:
        mensagem = 'Você deve selecionar ao menos um aluno.'


    return render(request, 'web/professor/criar_grupo.html',
    {'alunos':  alunos, 'mensagem': mensagem})

@login_required
def grupo(request, id):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    grupo = get_object_or_404(Grupo, id = id, inativo = False)

    if grupo.professor != request.user.professor:
        return render(request, 'web/page_403.html', {})

    return render(request, 'web/professor/grupo.html', {'grupo': grupo})

@login_required
def perfil_aluno(request, id):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    aluno = get_object_or_404(Aluno, id = id)

    return render(request, 'web/professor/perfil_aluno.html', {'aluno': aluno})

@login_required
def listas(request):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    listas = Lista.objects.filter(grupo__professor = request.user.professor, inativo = False)\
    .order_by('titulo')

    return render(request, 'web/professor/listas.html', {'listas': listas})

@login_required
def criar_lista(request):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    exercicios = Exercicio.objects.filter(professor = request.user.professor, inativo = False)
    grupos = Grupo.objects.filter(professor = request.user.professor, inativo = False)

    mensagem = ''

    if request.method == 'POST' and 'table_records' in request.POST:
        # recupera campos da requisição

        try:
            titulo = request.POST['titulo']
            grupo =  Grupo.objects.get(pk = request.POST['grupo'], inativo = False)
            ver = True if 'ver' in request.POST else False
            submeter = True if 'submeter' in request.POST else False
            exercicios_lista = request.POST.getlist('table_records')
            prazo = datetime.datetime.strptime(request.POST['prazo'], "%d/%m/%Y %H:%M")

            lista = Lista(
                titulo = titulo,
                grupo = grupo,
                ver = ver,
                submeter = submeter,
                prazo = prazo
            )
            lista.save()

            for exercicio in exercicios_lista:
                try:
                    exercicio_lista = Exercicio.objects.get(pk = exercicio,
                    professor = request.user.professor, inativo = False)
                except:
                    pass

                lista.exercicios.add(exercicio_lista)

            lista.save()

            mensagem = 'Lista adicionada com sucesso.'
        except Grupo.DoesNotExist:
            mensagem = 'Grupo inexistente.'
    elif request.method == 'POST' and not 'table_records' in request.POST:
        mensagem = 'Você deve selecionar ao menos um exercício.'

    return render(request, 'web/professor/criar_lista.html', {
        'exercicios': exercicios,
        'grupos': grupos,
        'mensagem': mensagem
    })

@login_required
def lista(request, id):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    lista = get_object_or_404(Lista, id = id, inativo = False)

    if lista.grupo.professor != request.user.professor:
        return render(request, 'web/page_403.html', {})

    alunos = []

    alunos_lista = Aluno.objects.filter(grupo__lista = lista)

    for aluno in alunos_lista:
        alunos.append({
            'aluno': aluno,
            'submissoes': []
        })

    return render(request, 'web/professor/lista.html', {
        'lista': lista,
        'alunos': alunos
    })

@login_required
def exercicio(request, id):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    exercicio = get_object_or_404(Exercicio, id = id, inativo = False)

    if exercicio.professor != request.user.professor:
        return render(request, 'web/page_403.html', {})

    exemplos = {}

    with open(os.path.join(exercicio.caminho(), 'in/sample/1.txt'), 'r') as f:
        exemplos['entrada'] = f.read().splitlines()
    with open(os.path.join(exercicio.caminho(), 'out/sample/1.txt'), 'r') as f:
        exemplos['saida'] = f.read().splitlines()

    return render(request, 'web/professor/exercicio.html', {'exercicio': exercicio,
    'exemplos': exemplos})

@login_required
def excluir_exercicio(request, id):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    exercicio = get_object_or_404(Exercicio, id = id, inativo = False)

    if exercicio.professor != request.user.professor:
        return render(request, 'web/page_403.html', {})

    exercicio.inativo = True
    exercicio.save()

    return redirect('web.views.professor.exercicios')

@login_required
def exercicios(request):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    exercicios = Exercicio.objects.filter(professor = request.user.professor, inativo = False).order_by('codigo')

    return render(request, 'web/professor/exercicios.html', {'exercicios': exercicios})

@login_required
def criar_exercicio(request):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    mensagem = ''

    if request.method == 'POST' and request.FILES['arquivos-entrada'] and \
    request.FILES['arquivos-saida']:
        # recupera campos da requisição
        codigo = request.POST['codigo']
        exemplo_entrada = request.POST['entrada']
        exemplo_saida = request.POST['saida']
        tempo_lim = request.POST['tempo']
        tam_lim = request.POST['tamanho']
        titulo = request.POST['titulo']
        descricao = request.POST['descricao']

        try:
            exercicio = Exercicio.objects.get(codigo = codigo)

            if exercicio:
                mensagem = 'Já existe um exercício com esse código'
                return render(request, 'web/professor/criar_exercicio.html',
                {'mensagem': mensagem})
        except:
            pass



        prof_dir = os.path.join(settings.OJ_DATA_DIR, 'contests' , str(request.user.professor.id))

        # salva o exercício no bando
        e = Exercicio(
            titulo = titulo,
            codigo = codigo,
            descricao = descricao,
            professor = request.user.professor,
            lim_tempo_s = tempo_lim,
            lim_memoria_k = tam_lim
        )
        e.save()

        # cria diretório de exercícios do professor, caso não exista
        if not os.path.exists(prof_dir):
            os.makedirs(prof_dir)

        # cria diretório do problema
        prob_path = os.path.join(prof_dir, codigo)
        os.makedirs(prob_path)

        # cria diretório para arquivos de teste de entrada
        dir_in = os.path.join(prob_path, 'in')
        os.makedirs(dir_in)

        # cria diretório para arquivos de teste de saída
        dir_out = os.path.join(prob_path, 'out')
        os.makedirs(dir_out)

        # cria diretório para arquivos de exemplo de entrada
        dir_in_sample = os.path.join(dir_in, 'sample')
        os.makedirs(dir_in_sample)

        # cria diretório para arquivos de exemplo de saída
        dir_out_sample = os.path.join(dir_out, 'sample')
        os.makedirs(dir_out_sample)

        # cria o arquivo de exemplo de entrada
        with open(os.path.join(dir_in_sample, '1.txt'), 'w') as f:
            f.writelines(exemplo_entrada)
            f.close()

        # cria o arquivo de exemplo de saída
        with open(os.path.join(dir_out_sample, '1.txt'), 'w') as f:
            f.writelines(exemplo_saida)
            f.close()

        # recupera arquivos de upload de entrada e saida do exercicio
        arqs_entrada = request.FILES.getlist('arquivos-entrada')
        arqs_saida = request.FILES.getlist('arquivos-saida')

        # salva os arquivos de teste de entrada
        fs = FileSystemStorage(location = dir_in)
        for arq in arqs_entrada:
            fs.save(arq.name, arq)

        # salva os arquivos de teste de saída
        fs = FileSystemStorage(location = dir_out)
        for arq in arqs_saida:
            fs.save(arq.name, arq)

        # salva o JSON com dados de limite de tempo e tamanho
        with open(os.path.join(prob_path, 'data.json'), 'w') as f:
            f.writelines(json.dumps({'time_lim_s': int(tempo_lim),
            'mem_lim_k': int(tam_lim)}, indent = 4))
            f.close()

        mensagem = 'Exercício criado com sucesso'

    return render(request, 'web/professor/criar_exercicio.html',
    {'mensagem': mensagem})
