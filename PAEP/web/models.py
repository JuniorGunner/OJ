from django.db import models
from django.contrib.auth.models import User


class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name = 'Usuário')

class Professor(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, verbose_name = 'Usuário')

class Grupo(models.Model):
    nome = models.CharField('nome', max_length = 60)
    fk_prof = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Professor')

class Material(models.Model):
    titulo = models.CharField('titulo', max_length = 60)
    #caminho = models.CharField('nome', max_length = 300)
    fk_grupo = models.ForeignKey(Grupo, on_delete = models.CASCADE, verbose_name = 'Grupo')

class Grupo_Aluno(models.Model):
    fk_aluno = models.ForeignKey(Aluno, on_delete = models.CASCADE, verbose_name = 'Aluno')
    fk_grupo = models.ForeignKey(Grupo, on_delete = models.CASCADE, verbose_name = 'Grupo')

class Lista(models.Model):
    titulo = models.CharField('titulo', max_length = 60)
    ver = models.BooleanField()
    submeter = models.BooleanField()
    hora_criacao = models.DateTimeField()
    prazo = models.DateTimeField()
    #caminho = models.CharField('caminho', max_length = 300)
    fk_grupo = models.ForeignKey(Grupo, on_delete = models.CASCADE, verbose_name = 'Grupo')

class Exercicio(models.Model):
    titulo = models.CharField('titulo', max_length = 60)
    codigo = models.CharField('codigo', max_length = 10)
    descricao = models.TextField('descricao', max_length = 800)
    lim_codigo_fonte = models.IntegerField()
    lim_tempo_s = models.IntegerField()
    lim_memoria_k = models.IntegerField()
    lim_saida_k = models.IntegerField()
    fk_professor = models.ForeignKey(Professor, on_delete = models.CASCADE, verbose_name = 'Professor')
    #caminho = models.CharField('caminho', max_length = 300)


class Exercicio_Lista(models.Model):
    idexe = models.ForeignKey(Exercicio, on_delete = models.CASCADE, verbose_name = 'Exercicio')
    fk_lista = models.ForeignKey(Lista, on_delete = models.CASCADE, verbose_name = 'Lista')
    caminho_solucao = models.CharField('titulo', max_length = 300)

class Submissao(models.Model):
    status = models.IntegerField()
    hora_submissao = models.DateTimeField()
    fk_exercicio_lista = models.ForeignKey(Exercicio_Lista, on_delete = models.CASCADE, verbose_name = 'Exercicio_Lista')
    fk_aluno = models.ForeignKey(Aluno, on_delete = models.CASCADE, verbose_name = 'Aluno')
    caminho = models.CharField('titulo', max_length = 300)
