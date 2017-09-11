# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
        ),
        migrations.CreateModel(
            name='Exercicio',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('titulo', models.CharField(max_length=60, verbose_name='Título')),
                ('codigo', models.CharField(max_length=10, verbose_name='Código', unique=True)),
                ('descricao', models.TextField(max_length=800, verbose_name='Descrição')),
                ('lim_codigo_fonte', models.IntegerField(verbose_name='Limite de Código fonte', blank=True, null=True)),
                ('lim_tempo_s', models.IntegerField(verbose_name='Limite de Tempo (s)')),
                ('lim_memoria_k', models.IntegerField(verbose_name='Limite de Memória (KB)')),
                ('lim_saida_k', models.IntegerField(verbose_name='Limite de Saída (KB)', blank=True, null=True)),
                ('inativo', models.BooleanField(verbose_name='Inativo', default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('nome', models.CharField(max_length=60, verbose_name='Nome')),
                ('inativo', models.BooleanField(verbose_name='Inativo', default=False)),
                ('alunos', models.ManyToManyField(verbose_name='Alunos', to='web.Aluno')),
            ],
        ),
        migrations.CreateModel(
            name='Lista',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('titulo', models.CharField(max_length=60, verbose_name='Título')),
                ('ver', models.BooleanField(verbose_name='Ver', default=True)),
                ('submeter', models.BooleanField(verbose_name='Submeter', default=True)),
                ('hora_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data/Hora Criação')),
                ('prazo', models.DateTimeField(verbose_name='Prazo', blank=True, null=True)),
                ('inativo', models.BooleanField(verbose_name='Inativo', default=False)),
                ('exercicios', models.ManyToManyField(verbose_name='Exercícios', to='web.Exercicio')),
                ('grupo', models.ForeignKey(verbose_name='Grupo', to='web.Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('titulo', models.CharField(max_length=60, verbose_name='Título')),
                ('grupo', models.ForeignKey(verbose_name='Grupo', to='web.Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
        ),
        migrations.CreateModel(
            name='Submissao',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('status', models.IntegerField(verbose_name='Status da Submissão', blank=True, null=True)),
                ('hora_submissao', models.DateTimeField(auto_now_add=True, verbose_name='Data/Hora da Submissão')),
                ('aluno', models.ForeignKey(verbose_name='Aluno', to='web.Aluno')),
                ('exercicio', models.ForeignKey(verbose_name='Exercício', to='web.Exercicio')),
                ('lista', models.ForeignKey(verbose_name='Lista', to='web.Lista')),
            ],
        ),
        migrations.AddField(
            model_name='grupo',
            name='professor',
            field=models.ForeignKey(verbose_name='Professor', to='web.Professor'),
        ),
        migrations.AddField(
            model_name='exercicio',
            name='professor',
            field=models.ForeignKey(verbose_name='Professor', to='web.Professor'),
        ),
    ]
