from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LigaViewSet, EquipoViewSet, JugadorViewSet, PartidoViewSet

router = DefaultRouter()
router.register(r"ligas", LigaViewSet)
router.register(r"equipos", EquipoViewSet)
router.register(r"jugadores", JugadorViewSet)
router.register(r"partidos", PartidoViewSet)

urlpatterns = [
    path("", include(router.urls)),
]