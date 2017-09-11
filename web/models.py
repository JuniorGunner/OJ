from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import os

class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name = 'Usuário')

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name = 'Usuário')

class Grupo(models.Model):
    nome = models.CharField(max_length = 60, verbose_name = 'Nome')
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Professor')
    inativo = models.BooleanField(default = False, verbose_name = 'Inativo')
    alunos = models.ManyToManyField(Aluno, verbose_name = 'Alunos')

class Material(models.Model):
    titulo = models.CharField(max_length = 60, verbose_name = 'Título')
    grupo = models.ForeignKey(Grupo, on_delete = models.CASCADE, verbose_name = 'Grupo')

class Exercicio(models.Model):
    titulo = models.CharField( max_length = 60, verbose_name = 'Título')
    codigo = models.CharField(max_length = 10, unique = True, verbose_name = 'Código')
    descricao = models.TextField(max_length = 800, verbose_name = 'Descrição')
    lim_codigo_fonte = models.IntegerField(null = True, blank = True, verbose_name = 'Limite de Código fonte')
    lim_tempo_s = models.IntegerField(verbose_name = 'Limite de Tempo (s)')
    lim_memoria_k = models.IntegerField(verbose_name = 'Limite de Memória (KB)')
    lim_saida_k = models.IntegerField(null = True, blank = True, verbose_name = 'Limite de Saída (KB)')
    professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Professor')
    inativo = models.BooleanField(default = False, verbose_name = 'Inativo')

    def caminho(self):
        return os.path.join(settings.OJ_DATA_DIR, 'contests', str(self.professor.id), self.codigo)

class Lista(models.Model):
    titulo = models.CharField(max_length = 60, verbose_name = 'Título')
    ver = models.BooleanField(default = True, verbose_name = 'Ver')
    submeter = models.BooleanField(default = True, verbose_name = 'Submeter')
    hora_criacao = models.DateTimeField(auto_now_add = True, verbose_name = 'Data/Hora Criação')
    prazo = models.DateTimeField(null = True, blank = True, verbose_name = 'Prazo')
    grupo = models.ForeignKey(Grupo, on_delete = models.CASCADE, verbose_name = 'Grupo')
    inativo = models.BooleanField(default = False, verbose_name = 'Inativo')
    exercicios = models.ManyToManyField(Exercicio, verbose_name = 'Exercícios')

class Submissao(models.Model):
    status = models.IntegerField(blank = True, null = True, verbose_name = 'Status da Submissão')
    hora_submissao = models.DateTimeField(auto_now_add = True, verbose_name = 'Data/Hora da Submissão')
    exercicio = models.ForeignKey(Exercicio, on_delete = models.CASCADE, verbose_name = 'Exercício')
    lista = models.ForeignKey(Lista, on_delete = models.CASCADE, verbose_name = 'Lista')
    aluno = models.ForeignKey(Aluno, on_delete = models.CASCADE, verbose_name = 'Aluno')
