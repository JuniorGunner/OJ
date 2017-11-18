from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.views import login as view_login, logout_then_login
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Count
import shutil

from web.tasks import moss_task
from django.http import JsonResponse

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages

import datetime
from django.utils import timezone

import os
import json

from web.models import *

import operator

@login_required
def moss(request, lista_id, exercicio_id):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    lista = get_object_or_404(Lista, id = lista_id, inativo = False)

    if lista.grupo.professor != request.user.professor:
        return render(request, 'web/page_403.html', {})

    submissoes = []

    alunos_lista = Aluno.objects.filter(grupo__lista = lista)
    exercicio = lista.exercicios.filter(id = exercicio_id)

    for aluno in alunos_lista:
        submissoes_aluno = Submissao.objects.filter(lista = lista, aluno = aluno,
        exercicio = exercicio).order_by('hora_submissao')

        for submissao in submissoes_aluno:
            if submissao.status == 1:
                submissoes.append(submissao.id)
                break

    if len(submissoes) < 2:
        mensagem = 'Devem existir pelo menos duas submissões aceitas para a comparação.'
        messages.add_message(request, messages.WARNING, mensagem)
    else:
        moss_task.delay(submissoes)
        mensagem = 'Solicitação efetuada com sucesso.'
        messages.add_message(request, messages.SUCCESS, mensagem)

    return redirect('web.views.professor.lista', lista.id)

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
    .annotate(qtd_alunos = Count('alunos'))

    return render(request, 'web/professor/grupos.html', {'grupos': grupos})

@login_required
def criar_grupo(request):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    alunos = Aluno.objects.all()

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
        messages.add_message(request, messages.SUCCESS, mensagem)

        return HttpResponseRedirect(reverse('web.views.professor.criar_grupo'))
    elif request.method == 'POST' and not 'table_records' in request.POST:
        mensagem = 'Você deve selecionar ao menos um aluno.'
        messages.add_message(request, messages.WARNING, mensagem)


    return render(request, 'web/professor/criar_grupo.html', {'alunos':  alunos})

@login_required
def grupo(request, id):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    grupo = get_object_or_404(Grupo, id = id)

    if grupo.professor != request.user.professor:
        return render(request, 'web/page_403.html', {})

    listas = Lista.objects.filter(grupo = grupo, inativo = False)

    desempenho = {'resolvidos': 0, 'tentativas': 0, 'total_exercicios': 0, 'total_tentativas': 0}

    alunos_grupo = Aluno.objects.filter(grupo = grupo)

    for lista in listas:
        desempenho['total_exercicios'] += lista.exercicios.count()
        for aluno in alunos_grupo:
            for exercicio in lista.exercicios.all():
                submissoes = Submissao.objects.filter(lista = lista, aluno = aluno,
                exercicio = exercicio).order_by('hora_submissao')
                for submissao in submissoes:
                    desempenho['total_tentativas'] += 1
                    if submissao.status == 1:
                        desempenho['resolvidos'] += 1
                        break

    try:
        desempenho['resolvidos'] /= alunos_grupo.count()
        desempenho['tentativas'] = desempenho['total_tentativas'] / alunos_grupo.count()
    except:
        desempenho['resolvidos'] = 0
        desempenho['tentativas'] = 0

    materiais = Material.objects.filter(grupo = grupo)

    return render(request, 'web/professor/grupo.html',
    {
        'grupo': grupo,
        'listas': listas,
        'desempenho': desempenho,
        'materiais': materiais
    })

@login_required
def perfil_aluno(request, id):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    aluno = get_object_or_404(Aluno, id = id)

    return render(request, 'web/professor/perfil_aluno.html', {'aluno': aluno})

@login_required
def upload_material(request, id):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    grupo = get_object_or_404(Grupo, id = id)

    return render(request, 'web/professor/upload_material.html', {'grupo': grupo})

@login_required
def confirmacao_upload(request, id):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    grupo = get_object_or_404(Grupo, id = id)

    for arq in request.FILES:
        arquivos = request.FILES.getlist(arq)
        for arquivo in arquivos:
            material = Material(
                titulo = arquivo.name,
                grupo = grupo
            )

            material.save()

            caminho = material.caminho()
            os.makedirs(caminho)

            fs = FileSystemStorage(location = caminho)
            fs.save(arquivo.name, arquivo)

    return redirect('web.views.professor.grupo', id = id)

@login_required
def download(request, id):
    material = get_object_or_404(Material, id = id, grupo__inativo = False)

    if hasattr(request.user, 'professor'):
        if material.grupo.professor != request.user.professor:
            return render(request, 'web/page_403.html', {})
    elif hasattr(request.user, 'aluno'):
        if not request.user.aluno in material.grupo.alunos.all():
            return render(request, 'web/page_403.html', {})

    caminho = os.path.join(material.caminho(), material.titulo)

    with open(caminho, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/pdf")
        response['Content-Disposition'] = 'inline; filename=' + os.path.basename(caminho)
        return response

    return render(request, 'web/page_403.html', {})

@login_required
def excluir_material(request, id_grupo):
    if hasattr(request.user, 'aluno'):
        return JsonResponse({
            'sucesso': False,
            'mensagem': 'Acesso Negado.',
            'materiais': []
        })

    try:
        grupo = Grupo.objects.get(id = id_grupo, inativo = False)
    except Grupo.DoesNotExist:
        grupo = None

    if grupo:
        if grupo.professor != request.user.professor:
            return JsonResponse({
                'sucesso': False,
                'mensagem': 'Acesso Negado.',
                'materiais': []
            })

        materiais = request.POST.getlist('materiais[]')

        if not materiais:
            return JsonResponse({
                'sucesso': False,
                'mensagem': 'Nenhum arquivo selecionado.',
                'materiais': []
            })

        mensagem = 'Arquivos excluídos com sucesso.'
        del_mats = []

        for material in materiais:
            try:
                mat = Material.objects.get(id = int(material), grupo = grupo)
            except Material.DoesNotExist:
                mensagem = 'Um ou mais arquivos não puderam ser excluídos.'
                continue

            shutil.rmtree(mat.caminho())
            mat.delete()
            del_mats.append(material)

        return JsonResponse({
            'sucesso': True,
            'mensagem': mensagem,
            'materiais': del_mats
        })

    mensagem = 'Grupo não encontrado.'

    return JsonResponse({
        'sucesso': False,
        'mensagem': mensagem,
        'materiais': []
    })


@login_required
def listas(request):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    listas = Lista.objects.filter(grupo__professor = request.user.professor, inativo = False)

    return render(request, 'web/professor/listas.html', {'listas': listas})

@login_required
def criar_lista(request):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    exercicios = Exercicio.objects.filter(professor = request.user.professor, inativo = False)
    grupos = Grupo.objects.filter(professor = request.user.professor, inativo = False)

    if request.method == 'POST' and 'table_records' in request.POST:
        # recupera campos da requisição

        try:
            titulo = request.POST['titulo']
            grupo =  Grupo.objects.get(pk = request.POST['grupo'], inativo = False)
            # ver = True if 'ver' in request.POST else False
            submeter = True if 'submeter' in request.POST else False
            exercicios_lista = request.POST.getlist('table_records')
            prazo = datetime.datetime.strptime(request.POST['prazo'], "%d/%m/%Y %H:%M")

            lista = Lista(
                titulo = titulo,
                grupo = grupo,
                # ver = True,
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
            messages.add_message(request, messages.SUCCESS, mensagem)

        except Grupo.DoesNotExist:
            mensagem = 'Grupo inexistente.'
            messages.add_message(request, messages.ERROR, mensagem)

        return HttpResponseRedirect(reverse('web.views.professor.criar_lista'))
    elif request.method == 'POST' and not 'table_records' in request.POST:
        mensagem = 'Você deve selecionar ao menos um exercício.'
        messages.add_message(request, messages.WARNING, mensagem)

    return render(request, 'web/professor/criar_lista.html', {
        'exercicios': exercicios,
        'grupos': grupos
    })

@login_required
def lista(request, id):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    lista = get_object_or_404(Lista, id = id, inativo = False)

    if lista.grupo.professor != request.user.professor:
        return render(request, 'web/page_403.html', {})

    alunos = []

    msgs = messages.get_messages(request)

    mensagem = None
    for msg in msgs:
        mensagem = msg
        break

    alunos_lista = Aluno.objects.filter(grupo__lista = lista)

    desempenho = {
        'tentativas': 0,
        'resolvidos': 0,
        'total_tentativas': 0
    }

    for aluno in alunos_lista:
        exercicios_aluno = []
        qtd_resolvida = 0
        total_tentativas = 0
        for exercicio in lista.exercicios.all():

            submissoes = Submissao.objects.filter(lista = lista, aluno = aluno,
            exercicio = exercicio).order_by('hora_submissao')
            exercicio_aluno = {'exercicio': exercicio}

            tentativas = 0
            for submissao in submissoes:
                tentativas += 1
                if submissao.status == 1:
                    exercicio_aluno['status'] = True
                    exercicio_aluno['submissao_aceita'] = submissao.id
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

        desempenho['total_tentativas'] += total_tentativas
        desempenho['resolvidos'] += qtd_resolvida

    try:
        desempenho['tentativas'] = desempenho['total_tentativas'] / alunos_lista.count()
        desempenho['resolvidos'] /= alunos_lista.count()
    except:
        desempenho['tentativas'] = 0
        desempenho['resolvidos'] = 0

    return render(request, 'web/professor/lista.html', {
        'lista': lista,
        'alunos': alunos,
        'desempenho': desempenho,
        'mensagem': mensagem
    })

@login_required
def excluir_lista(request, id):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    lista = get_object_or_404(Lista, id = id, inativo = False)

    if lista.grupo.professor != request.user.professor:
        return render(request, 'web/page_403.html', {})

    if timezone.now() < lista.prazo:
        mensagem = 'Lista não pode ser excluída. Prazo em vigência.'
        messages.add_message(request, messages.ERROR, mensagem)
        return redirect('web.views.professor.lista', id = id)
    else:
        grupo.inativo = True
        grupo.save()

    return redirect('web.views.professor.listas')

@login_required
def submissoes_lista_aluno(request, lista_id, exercicio_id, aluno_id):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    submissoes = Submissao.objects.filter(lista = lista_id, exercicio = exercicio_id,
    aluno = aluno_id).order_by('-hora_submissao')

    if len(submissoes) > 0:
        if submissoes[0].lista.grupo.professor != request.user.professor:
            return render(request, 'web/page_403.html', {})

    return render(request, 'web/professor/submissoes_aluno.html', {'submissoes': submissoes})

@login_required
def submissao(request, id):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    submissao = get_object_or_404(Submissao, id = id, lista__grupo__professor = request.user.professor)

    codigo = ''

    with open(os.path.join(submissao.caminho(), str(submissao.id) + '.py'), 'r') as f:
        codigo = f.read()

    return render(request, 'web/professor/submissao.html', {'submissao': submissao, 'codigo': codigo})

@login_required
def habilita_submissao(request, listaid):
    if hasattr(request.user, 'aluno'):
        return JsonResponse({'habilitou': False})

    try:
        lista = Lista.objects.get(id = listaid, inativo = False)
    except Lista.DoesNotExist:
        lista = None

    # print(lista)

    if lista:
        if lista.grupo.professor != request.user.professor:
            return JsonResponse({'habilitou': False})

        lista.submeter = True
        lista.save()

        return JsonResponse({'habilitou': True})
    else:
        return JsonResponse({'habilitou': False})

@login_required
def exercicio(request, id):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    exercicio = get_object_or_404(Exercicio, id = id)

    if exercicio.professor != request.user.professor:
        return render(request, 'web/page_403.html', {})

    exemplos = {}

    with open(os.path.join(exercicio.caminho(), 'in/sample/1.txt'), 'r') as f:
        exemplos['entrada'] = f.read().splitlines()
    with open(os.path.join(exercicio.caminho(), 'out/sample/1.txt'), 'r') as f:
        exemplos['saida'] = f.read().splitlines()

    codigo = ''

    with open(os.path.join(exercicio.caminho(), 'solucao', 'solucao.py'), 'r') as f:
        codigo = f.read()

    return render(request, 'web/professor/exercicio.html', {'exercicio': exercicio,
    'exemplos': exemplos, 'codigo': codigo})

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

    exercicios = Exercicio.objects.filter(professor = request.user.professor, inativo = False)

    return render(request, 'web/professor/exercicios.html', {'exercicios': exercicios})

@login_required
def criar_exercicio(request):
    if hasattr(request.user, 'aluno'):
        return render(request, 'web/page_403.html', {})

    if request.method == 'POST' and request.FILES['arquivos-entrada'] and \
    request.FILES['arquivos-saida']:
        # recupera campos da requisição
        # codigo = request.POST['codigo']
        exemplo_entrada = request.POST['entrada']
        exemplo_saida = request.POST['saida']
        tempo_lim = request.POST['tempo']
        titulo = request.POST['titulo']
        descricao = request.POST['descricao']

        # try:
        #     exercicio = Exercicio.objects.get(codigo = codigo)
        #
        #     if exercicio:
        #         mensagem = 'Já existe um exercício com esse código'
        #         tipo_mensagem = -1
        #         return render(request, 'web/professor/criar_exercicio.html',
        #         {'mensagem': mensagem, 'tipo_mensagem': tipo_mensagem})
        # except:
        #     pass



        prof_dir = os.path.join(settings.OJ_DATA_DIR, 'contests' , str(request.user.professor.id))

        # salva o exercício no bando
        e = Exercicio(
            titulo = titulo,
            descricao = descricao,
            professor = request.user.professor,
            lim_tempo_s = tempo_lim,
            # codigo = codigo,
            # lim_memoria_k = 0
        )
        e.save()

        # cria diretório de exercícios do professor, caso não exista
        if not os.path.exists(prof_dir):
            os.makedirs(prof_dir)

        # cria diretório do problema
        prob_path = os.path.join(prof_dir, str(e.id))
        os.makedirs(prob_path)

        # cria diretório para arquivo da solução
        dir_solucao = os.path.join(prob_path, 'solucao')
        os.makedirs(dir_solucao)

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
        exemplo_entrada = exemplo_entrada.replace('\r\n', '\n')
        with open(os.path.join(dir_in_sample, '1.txt'), 'w') as f:
            f.writelines(exemplo_entrada + '\n')
            f.close()

        # cria o arquivo de exemplo de saída
        exemplo_saida = exemplo_saida.replace('\r\n', '\n')
        with open(os.path.join(dir_out_sample, '1.txt'), 'w') as f:
            f.writelines(exemplo_saida + '\n')
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

        # recupera arquivo de upload de solução do exercício
        arq_solucao = request.FILES['arquivo-solucao']

        # salva arquivo de solução do exercício
        fs = FileSystemStorage(location = dir_solucao)
        fs.save('solucao.py', arq_solucao)

        # salva o JSON com dados de limite de tempo e tamanho
        with open(os.path.join(prob_path, 'data.json'), 'w') as f:
            f.writelines(json.dumps({'time_lim_s': int(tempo_lim)}, indent = 4))
            f.close()

        mensagem = 'Exercício criado com sucesso'
        messages.add_message(request, messages.SUCCESS, mensagem)

        return HttpResponseRedirect(reverse('web.views.professor.criar_exercicio'))

    return render(request, 'web/professor/criar_exercicio.html', {})
