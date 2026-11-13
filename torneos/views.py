from rest_framework import viewsets
from .models import Liga, Equipo, Jugador, Partido
from .serializers import (
    LigaSerializer, EquipoSerializer, JugadorSerializer, PartidoSerializer,
)


class LigaViewSet(viewsets.ModelViewSet):
    queryset = Liga.objects.all()
    serializer_class = LigaSerializer


class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer

    def get_queryset(self):
        queryset = Equipo.objects.select_related("liga")
        liga = self.request.query_params.get("liga")
        if liga:
            queryset = queryset.filter(liga_id=liga)
        return queryset


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