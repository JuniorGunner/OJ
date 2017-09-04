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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('user', models.OneToOneField(verbose_name='Usuário', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Exercicio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('titulo', models.CharField(verbose_name='titulo', max_length=60)),
                ('codigo', models.CharField(verbose_name='codigo', max_length=10)),
                ('descricao', models.TextField(verbose_name='descricao', max_length=800)),
                ('lim_codigo_fonte', models.IntegerField()),
                ('lim_tempo_s', models.IntegerField()),
                ('lim_memoria_k', models.IntegerField()),
                ('lim_saida_k', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Exercicio_Lista',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('caminho_solucao', models.CharField(verbose_name='titulo', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('nome', models.CharField(verbose_name='nome', max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo_Aluno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('fk_aluno', models.ForeignKey(verbose_name='Aluno', to='web.Aluno')),
                ('fk_grupo', models.ForeignKey(verbose_name='Grupo', to='web.Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='Lista',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('titulo', models.CharField(verbose_name='titulo', max_length=60)),
                ('ver', models.BooleanField()),
                ('submeter', models.BooleanField()),
                ('hora_criacao', models.DateTimeField()),
                ('prazo', models.DateTimeField()),
                ('fk_grupo', models.ForeignKey(verbose_name='Grupo', to='web.Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('titulo', models.CharField(verbose_name='titulo', max_length=60)),
                ('fk_grupo', models.ForeignKey(verbose_name='Grupo', to='web.Grupo')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('user', models.OneToOneField(verbose_name='Usuário', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Submissao',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('status', models.IntegerField()),
                ('hora_submissao', models.DateTimeField()),
                ('caminho', models.CharField(verbose_name='titulo', max_length=300)),
                ('fk_aluno', models.ForeignKey(verbose_name='Aluno', to='web.Aluno')),
                ('fk_exercicio_lista', models.ForeignKey(verbose_name='Exercicio_Lista', to='web.Exercicio_Lista')),
            ],
        ),
        migrations.AddField(
            model_name='grupo',
            name='fk_prof',
            field=models.ForeignKey(verbose_name='Professor', to='web.Professor'),
        ),
        migrations.AddField(
            model_name='exercicio_lista',
            name='fk_lista',
            field=models.ForeignKey(verbose_name='Lista', to='web.Lista'),
        ),
        migrations.AddField(
            model_name='exercicio_lista',
            name='idexe',
            field=models.ForeignKey(verbose_name='Exercicio', to='web.Exercicio'),
        ),
        migrations.AddField(
            model_name='exercicio',
            name='fk_professor',
            field=models.ForeignKey(verbose_name='Professor', to='web.Professor'),
        ),
    ]
