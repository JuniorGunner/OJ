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
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ra', models.CharField(max_length=10, verbose_name='RA', unique=True)),
                ('user', models.OneToOneField(verbose_name='Usuário', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Exercicio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=60, verbose_name='Título')),
                ('descricao', models.TextField(max_length=800, verbose_name='Descrição')),
                ('lim_tempo_s', models.IntegerField(verbose_name='Limite de Tempo (s)')),
                ('inativo', models.BooleanField(default=False, verbose_name='Inativo')),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=60, verbose_name='Nome')),
                ('inativo', models.BooleanField(default=False, verbose_name='Inativo')),
                ('alunos', models.ManyToManyField(verbose_name='Alunos', to='web.Aluno')),
            ],
        ),
        migrations.CreateModel(
            name='Lista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=60, verbose_name='Título')),
                ('submeter', models.BooleanField(default=True, verbose_name='Submeter')),
                ('hora_criacao', models.DateTimeField(verbose_name='Data/Hora Criação', auto_now_add=True)),
                ('prazo', models.DateTimeField(verbose_name='Prazo', null=True, blank=True)),
                ('inativo', models.BooleanField(default=False, verbose_name='Inativo')),
                ('exercicios', models.ManyToManyField(verbose_name='Exercícios', to='web.Exercicio')),
                ('grupo', models.ForeignKey(verbose_name='Grupo', to='web.Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=60, verbose_name='Título')),
                ('grupo', models.ForeignKey(verbose_name='Grupo', to='web.Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(verbose_name='Usuário', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submissao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(verbose_name='Status da Submissão', null=True, blank=True)),
                ('hora_submissao', models.DateTimeField(verbose_name='Data/Hora da Submissão', auto_now_add=True)),
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
