from django.contrib import admin
from arduino.models import *

# Register your models here.
admin.site.register(LocalModel)
admin.site.register(CategoriaModel)
admin.site.register(EquipamentoModel)
admin.site.register(ComentarioModel)
admin.site.register(UtilizacaoModel)
