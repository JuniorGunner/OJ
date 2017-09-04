from django.contrib import admin
from web.models import *

# Register your models here.
# class AlunoAdmin(admin.ModelAdmin):
#     model = Aluno
#
# class ProfessorAdmin(admin.ModelAdmin):
#     model = Professor

admin.site.register(Aluno)
admin.site.register(Professor)
