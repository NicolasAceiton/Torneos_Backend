from django.contrib import admin
from .models import Liga, Equipo, Jugador, Partido

admin.site.register(Liga)
admin.site.register(Equipo)
admin.site.register(Jugador)
admin.site.register(Partido)