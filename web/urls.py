from django.conf.urls import include, url
from django.contrib.auth.views import login as view_login, logout_then_login
from web.views import main, aluno, professor

urlpatterns = [
    # home
    url(r'^$', main.home, name="web-home"),

    # aluno
    url(r'^grupos_aluno/$', aluno.grupos, name="web-grupos-aluno"),
    url(r'^grupo_aluno/(?P<id>\d+)$', aluno.grupo, name="web-grupo-aluno"),
    url(r'^listas_aluno/$', aluno.listas, name="web-listas-aluno"),
    url(r'^lista_aluno/(?P<id>\d+)$', aluno.lista, name="web-lista-aluno"),
    url(r'^exercicio_lista_aluno/(?P<lista>\d+)/(?P<id>\d+)$', aluno.exercicio_lista, name="web-exercicio-lista-aluno"),
    url(r'^resposta_exercicio_aluno/(?P<lista>\d+)/(?P<id>\d+)$', aluno.resposta_exercicio, name="web-resposta-exercicio-aluno"),
    url(r'^submeter_exercicio_aluno/(?P<lista>\d+)/(?P<id>\d+)$', aluno.submeter_exercicio, name="web-exercicio-lista-aluno"),
    url(r'^submissao_codigo_aluno/(?P<listaid>\d+)/(?P<id>\d+)$', aluno.submissao_codigo, name="web-submissao-codigo-aluno"),
    url(r'^tutor/$', aluno.tutor, name="web-tutor-aluno"),
    url(r'^submissoes_aluno/$', aluno.submissoes, name="web-submissoes-aluno"),
    url(r'^submissao_aluno/(?P<id>\d+)$', aluno.submissao, name="web-submissao-aluno"),
    url(r'^confirmacao_submissao/$', aluno.confirmacao_submissao, name="web-confirmacao-submissao-aluno"),

    # professor
    url(r'^grupos_professor/$', professor.grupos, name="web-grupos-professor"),
    url(r'^excluir_grupo/(?P<id>\d+)$', professor.excluir_grupo, name="web-excluir-grupo-professor"),
    url(r'^criar_grupo/$', professor.criar_grupo, name="web-criar-grupo-professor"),
    url(r'^grupo_professor/(?P<id>\d+)$', professor.grupo, name="web-grupo-professor"),
    # url(r'^perfil_aluno/(?P<id>\d+)$', professor.perfil_aluno, name="web-perfil-aluno-professor"),
    url(r'^lista_professor/(?P<id>\d+)$', professor.lista, name="web-lista-professor"),
    url(r'^listas_professor/$', professor.listas, name="web-listas-professor"),
    url(r'^criar_lista/$', professor.criar_lista, name="web-criar-lista-professor"),
    url(r'^exercicios_professor/$', professor.exercicios, name="web-exercicios-professor"),
    url(r'^exercicio_professor/(?P<id>\d+)$', professor.exercicio, name="web-exercicio-professor"),
    url(r'^excluir_exercicio/(?P<id>\d+)$', professor.excluir_exercicio, name="web-excluir-exercicio-professor"),
    url(r'^criar_exercicio/$', professor.criar_exercicio, name="web-criar-exercicio-professor"),
    url(r'^habilita_submissao/(?P<listaid>\d+)$', professor.habilita_submissao, name="web-habilita-submissao-professor"),
    url(r'^submissao_exercicio_aluno/(?P<id>\d+)$', professor.submissao, name="web-submissao-professor"),
    url(r'^submissoes_lista_aluno/(?P<lista_id>\d+)/(?P<exercicio_id>\d+)/(?P<aluno_id>\d+)$', professor.submissoes_lista_aluno, name="web-submissoes-lista-aluno-professor"),

    # login
	url(r'^login/$', view_login, {'template_name': 'web/check_login.html'}, name='web-login'),
    url(r'^logout/$', logout_then_login, {'login_url': '/login'}, name="web-logout"),
]
