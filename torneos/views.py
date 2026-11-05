from datetime import date
 
from django.db import transaction
from django.db.models import Q
from rest_framework import viewsets, status


from .models import Liga, Equipo, Jugador, Partido
from .serializers import (
    LigaSerializer, LigaDetalleSerializer,
    EquipoSerializer, EquipoDetalleSerializer,
    JugadorSerializer,
    PartidoSerializer,
)
 
def _es_id(valor):
    return valor is not None and valor.isdigit()
 
 
def recalcular_tabla(liga):
    equipos = {e.pk: e for e in liga.equipos.all()}
    for e in equipos.values():
        e.pj = e.pg = e.pe = e.pp = e.puntos = 0
 
    finalizados = Partido.objects.filter(
        liga=liga,
        estado='FIN',
        goles_local__isnull=False,
        goles_visitante__isnull=False,
    )
 
    for p in finalizados:
        local = equipos.get(p.equipo_local_id)
        visita = equipos.get(p.equipo_visitante_id)
        if local is None or visita is None:
            continue
 
        local.pj += 1
        visita.pj += 1
 
        if p.goles_local > p.goles_visitante:
            local.pg += 1
            local.puntos += 3
            visita.pp += 1
        elif p.goles_local < p.goles_visitante:
            visita.pg += 1
            visita.puntos += 3
            local.pp += 1
        else:
            local.pe += 1
            visita.pe += 1
            local.puntos += 1
            visita.puntos += 1
 
    Equipo.objects.bulk_update(equipos.values(), ['pj', 'pg', 'pe', 'pp', 'puntos'])