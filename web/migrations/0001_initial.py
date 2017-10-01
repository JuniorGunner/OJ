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
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('ra', models.CharField(max_length=10, unique=True, verbose_name='RA')),
                ('user', models.OneToOneField(verbose_name='Usuário', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Exercicio',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('titulo', models.CharField(max_length=60, verbose_name='Título')),
                ('descricao', models.TextField(max_length=800, verbose_name='Descrição')),
                ('lim_tempo_s', models.IntegerField(verbose_name='Limite de Tempo (s)')),
                ('inativo', models.BooleanField(verbose_name='Inativo', default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('nome', models.CharField(max_length=60, verbose_name='Nome')),
                ('inativo', models.BooleanField(verbose_name='Inativo', default=False)),
                ('alunos', models.ManyToManyField(to='web.Aluno', verbose_name='Alunos')),
            ],
        ),
        migrations.CreateModel(
            name='Lista',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('titulo', models.CharField(max_length=60, verbose_name='Título')),
                ('submeter', models.BooleanField(verbose_name='Submeter', default=True)),
                ('hora_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data/Hora Criação')),
                ('prazo', models.DateTimeField(null=True, blank=True, verbose_name='Prazo')),
                ('inativo', models.BooleanField(verbose_name='Inativo', default=False)),
                ('exercicios', models.ManyToManyField(to='web.Exercicio', verbose_name='Exercícios')),
                ('grupo', models.ForeignKey(to='web.Grupo', verbose_name='Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('titulo', models.CharField(max_length=60, verbose_name='Título')),
                ('hora_criacao', models.DateTimeField(auto_now_add=True, verbose_name='Data/Hora Criação')),
                ('grupo', models.ForeignKey(to='web.Grupo', verbose_name='Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('user', models.OneToOneField(verbose_name='Usuário', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submissao',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('status', models.IntegerField(null=True, blank=True, verbose_name='Status da Submissão')),
                ('hora_submissao', models.DateTimeField(auto_now_add=True, verbose_name='Data/Hora da Submissão')),
                ('aluno', models.ForeignKey(to='web.Aluno', verbose_name='Aluno')),
                ('exercicio', models.ForeignKey(to='web.Exercicio', verbose_name='Exercício')),
                ('lista', models.ForeignKey(to='web.Lista', verbose_name='Lista')),
            ],
        ),
        migrations.AddField(
            model_name='grupo',
            name='professor',
            field=models.ForeignKey(to='web.Professor', verbose_name='Professor'),
        ),
        migrations.AddField(
            model_name='exercicio',
            name='professor',
            field=models.ForeignKey(to='web.Professor', verbose_name='Professor'),
        ),
    ]
