from celery.decorators import task
from celery.utils.log import get_task_logger

from django.contrib.auth.models import User
from django.conf import settings
from web.models import Submissao

import os
import subprocess

logger = get_task_logger(__name__)

@task(name="moss_task")
def moss_task(submissoes_ids):
    submissoes = Submissao.objects.filter(id__in = submissoes_ids)

    if submissoes.count() < 2:
        return "Quantidade de Submissão Insuficiente"

    professor = submissoes[0].lista.grupo.professor
    lista = submissoes[0].lista
    exercicio = submissoes[0].exercicio

    run_path = ['perl', settings.MOSS_PATH, '-l', 'python']
    arquivos = []

    for submissao in submissoes:
        arquivos.append(os.path.join(submissao.caminho(), str(submissao.id) + '.py'))

    run_path += arquivos

    sp = subprocess.Popen(run_path, stdout = subprocess.PIPE, stderr = subprocess.PIPE, universal_newlines = True)
    try:
        (out, err) = sp.communicate()
    except UnicodeDecodeError:
        sp.kill()
        return "Erro ao Executar Script MOSS"

    if err:
        return err

    url = [i for i in out.split('\n') if i][-1]
    assunto = u"PAEP [REQUISIÇÃO MOSS]"
    mensagem = u"Resultados do MOSS para:\n"
    mensagem += u'Lista "' + lista.titulo + u'" - Exercício "' + exercicio.titulo + '"\n\n'
    mensagem += url
    try:
        professor.user.email_user(subject = assunto, message = mensagem)
    except:
        return "Falha ao Enviar E-mail"

    return True
