from rest_framework import viewsets
from .models import Liga, Equipo, Jugador, Partido
from .serializers import (
    LigaSerializer, EquipoSerializer, JugadorSerializer, PartidoSerializer,
)
from rest_framework.decorators import action
from rest_framework.response import Response

class LigaViewSet(viewsets.ModelViewSet):
    queryset = Liga.objects.all()
    serializer_class = LigaSerializer

    @action(detail=True, methods=["get"])
    def posiciones(self, request, pk=None):
        liga = self.get_object()

        tabla = {}
        for equipo in liga.equipos.all():
            tabla[equipo.id] = {
                "equipo_id": equipo.id,
                "equipo": equipo.nombre,
                "escudo_url": equipo.escudo_url,
                "pj": 0, "g": 0, "e": 0, "p": 0,
                "gf": 0, "gc": 0, "dg": 0, "puntos": 0,
            }

        partidos = liga.partidos.filter(estado="FIN")
        for partido in partidos:
            lados = (
                (partido.equipo_local_id, partido.goles_local, partido.goles_visitante),
                (partido.equipo_visitante_id, partido.goles_visitante, partido.goles_local),
            )
            for equipo_id, a_favor, en_contra in lados:
                fila = tabla.get(equipo_id)
                if fila is None:
                    continue
                fila["pj"] += 1
                fila["gf"] += a_favor
                fila["gc"] += en_contra
                if a_favor > en_contra:
                    fila["g"] += 1
                    fila["puntos"] += 3
                elif a_favor == en_contra:
                    fila["e"] += 1
                    fila["puntos"] += 1
                else:
                    fila["p"] += 1

        filas = list(tabla.values())
        for fila in filas:
            fila["dg"] = fila["gf"] - fila["gc"]
        filas.sort(key=lambda f: (-f["puntos"], -f["dg"], -f["gf"], f["equipo"]))

        for numero, fila in enumerate(filas, start=1):
            fila["posicion"] = numero

        return Response({
            "liga": liga.nombre,
            "pais": liga.pais,
            "tabla": filas,
        })

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

    def get_queryset(self):
        queryset = Equipo.objects.select_related("liga")
        liga = self.request.query_params.get("liga")
        if liga:
            queryset = queryset.filter(liga_id=liga)
        return queryset

    @action(detail=True, methods=["get"])
    def plantilla(self, request, pk=None):
        equipo = self.get_object()

        grupos = {
            "arqueros": [],
            "defensores": [],
            "mediocampistas": [],
            "delanteros": [],
        }
        mapa = {
            "ARQ": "arqueros",
            "DEF": "defensores",
            "MED": "mediocampistas",
            "DEL": "delanteros",
        }

        jugadores = equipo.jugadores.order_by("numero_camiseta")
        for jugador in jugadores:
            datos = JugadorSerializer(jugador).data
            grupos[mapa[jugador.posicion]].append(datos)

        return Response({
            "equipo": equipo.nombre,
            "liga": equipo.liga.nombre,
            "total_jugadores": jugadores.count(),
            "plantilla": grupos,
        })


class JugadorViewSet(viewsets.ModelViewSet):
    queryset = Jugador.objects.all()
    serializer_class = JugadorSerializer

    def get_queryset(self):
        queryset = Jugador.objects.select_related("equipo")
        equipo = self.request.query_params.get("equipo")
        if equipo:
            queryset = queryset.filter(equipo_id=equipo)
        return queryset


class PartidoViewSet(viewsets.ModelViewSet):
    queryset = Partido.objects.all()
    serializer_class = PartidoSerializer

    def get_queryset(self):
        queryset = Partido.objects.select_related("liga", "equipo_local", "equipo_visitante")
        liga = self.request.query_params.get("liga")
        estado = self.request.query_params.get("estado")
        if liga:
            queryset = queryset.filter(liga_id=liga)
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset.order_by("fecha")