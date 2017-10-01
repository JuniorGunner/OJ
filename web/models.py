from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import os

class Aluno(models.Model):
    ra = models.CharField(max_length = 10, unique = True, verbose_name = 'RA')
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name = 'Usuário')

    def __str__(self):
        return self.ra + ' - ' + self.user.get_full_name()

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name = 'Usuário')

    def __str__(self):
        return str(self.id) + ' - ' + self.user.get_full_name()

class Grupo(models.Model):
    nome = models.CharField(max_length = 60, verbose_name = 'Nome')
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Professor')
    inativo = models.BooleanField(default = False, verbose_name = 'Inativo')
    alunos = models.ManyToManyField(Aluno, verbose_name = 'Alunos')

class Material(models.Model):
    titulo = models.CharField(max_length = 60, verbose_name = 'Título')
    grupo = models.ForeignKey(Grupo, on_delete = models.CASCADE, verbose_name = 'Grupo')
    hora_criacao = models.DateTimeField(auto_now_add = True, verbose_name = 'Data/Hora Criação')

    def caminho(self):
        return os.path.join(settings.OJ_DATA_DIR, 'grupos', str(self.grupo.id), str(self.id))

class Exercicio(models.Model):
    titulo = models.CharField( max_length = 60, verbose_name = 'Título')
    descricao = models.TextField(max_length = 800, verbose_name = 'Descrição')
    lim_tempo_s = models.IntegerField(verbose_name = 'Limite de Tempo (s)')
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Professor')
    inativo = models.BooleanField(default = False, verbose_name = 'Inativo')
    # codigo = models.CharField(max_length = 10, unique = True, verbose_name = 'Código')
    # lim_codigo_fonte = models.IntegerField(null = True, blank = True, verbose_name = 'Limite de Código fonte')
    # lim_memoria_k = models.IntegerField(verbose_name = 'Limite de Memória (KB)')
    # lim_saida_k = models.IntegerField(null = True, blank = True, verbose_name = 'Limite de Saída (KB)')

    def caminho(self):
        return os.path.join(settings.OJ_DATA_DIR, 'contests', str(self.professor.id), str(self.id))

class Lista(models.Model):
    titulo = models.CharField(max_length = 60, verbose_name = 'Título')
    submeter = models.BooleanField(default = True, verbose_name = 'Submeter')
    hora_criacao = models.DateTimeField(auto_now_add = True, verbose_name = 'Data/Hora Criação')
    prazo = models.DateTimeField(null = True, blank = True, verbose_name = 'Prazo')
    grupo = models.ForeignKey(Grupo, on_delete = models.CASCADE, verbose_name = 'Grupo')
    inativo = models.BooleanField(default = False, verbose_name = 'Inativo')
    exercicios = models.ManyToManyField(Exercicio, verbose_name = 'Exercícios')
    # ver = models.BooleanField(default = True, verbose_name = 'Ver')

class Submissao(models.Model):
    status = models.IntegerField(blank = True, null = True, verbose_name = 'Status da Submissão')
    hora_submissao = models.DateTimeField(auto_now_add = True, verbose_name = 'Data/Hora da Submissão')
    exercicio = models.ForeignKey(Exercicio, on_delete = models.CASCADE, verbose_name = 'Exercício')
    lista = models.ForeignKey(Lista, on_delete = models.CASCADE, verbose_name = 'Lista')
    aluno = models.ForeignKey(Aluno, on_delete = models.CASCADE, verbose_name = 'Aluno')

    STATUS = {'AGUARDANDO': 0, 'AC': 1, 'WA': 2, 'TLE': 3, 'NZEC': 4, 'OUTRO': 5}
    STATUS_STR = ('Aguardando', 'Aceito', 'Resposta Errada', 'Tempo Limite Excedido', 'Erro em Tempo de Execução', 'Erro Desconhecido')

    def caminho(self):
        return os.path.join(settings.OJ_DATA_DIR, 'submissions', self.aluno.user.username)

    def status_str(self):
        return self.STATUS_STR[self.status]
