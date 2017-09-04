from django.conf.urls import include, url
from django.contrib.auth.views import login as view_login, logout_then_login
from web.views import main, aluno, professor

urlpatterns = [
    # home
    url(r'^$', main.home, name="web-home"),

    # aluno
    url(r'^grupos_aluno/$', aluno.grupos, name="web-grupos-aluno"),
    url(r'^listas_aluno/$', aluno.listas, name="web-listas-aluno"),
    url(r'^submissoes_aluno/$', aluno.submissoes, name="web-submissoes-aluno"),

    # professor
    url(r'^grupos_professor/$', professor.grupos, name="web-grupos-professor"),
    url(r'^criar_grupo/$', professor.criar_grupo, name="web-criar-grupo-professor"),
    url(r'^listas_professor/$', professor.listas, name="web-listas-professor"),
    url(r'^criar_lista/$', professor.criar_lista, name="web-criar-lista-professor"),
    url(r'^exercicios_professor/$', professor.exercicios, name="web-exercicios-professor"),
    url(r'^criar_exercicio/$', professor.criar_exercicio, name="web-criar-exercicio-professor"),

    # login
	url(r'^login/$', view_login, {'template_name': 'web/check_login.html'}, name='web-login'),
    url(r'^logout/$', logout_then_login, {'login_url': '/login'}, name="web-logout"),
]
