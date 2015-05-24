from django.contrib import admin

from models import Actividad, Usuario, Actividad_User, Variablescss, Comentario, Comments

# Register your models here.

admin.site.register(Actividad)
admin.site.register(Actividad_User)
admin.site.register(Usuario)
admin.site.register(Variablescss)
admin.site.register(Comentario)
admin.site.register(Comments)

