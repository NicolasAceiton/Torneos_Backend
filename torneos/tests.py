from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Liga, Equipo, Jugador, Partido


class TorneosAPITest(APITestCase):

    def setUp(self):
        self.liga = Liga.objects.create(
            nombre="Liga de Asenso de Chile",
            pais="Chile"
        )

        self.equipo1 = Equipo.objects.create(
            nombre="Deportes Temuco",
            liga=self.liga
        )

        self.equipo2 = Equipo.objects.create(
            nombre="Cobreloa",
            liga=self.liga
        )

    def test_listar_ligas(self):
        url = reverse("liga-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_liga(self):
        url = reverse("liga-list")

        datos = {
            "nombre": "Liga Argentina",
            "pais": "Argentina"
        }

        response = self.client.post(url, datos, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Liga.objects.count(), 2)

    def test_nombre_liga_invalido(self):
        url = reverse("liga-list")

        datos = {
            "nombre": "AB",
            "pais": "Chile"
        }

        response = self.client.post(url, datos, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_jugador(self):
        url = reverse("jugador-list")

        datos = {
            "nombre": "Diego Buonanotte",
            "equipo": self.equipo1.id,
            "posicion": "MED",
            "edad": 38,
            "numero_camiseta": 18
        }

        response = self.client.post(url, datos, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_numero_camiseta_repetido(self):
        Jugador.objects.create(
            nombre="Jugador Uno",
            equipo=self.equipo1,
            posicion="DEL",
            edad=25,
            numero_camiseta=10
        )

        url = reverse("jugador-list")

        datos = {
            "nombre": "Jugador Dos",
            "equipo": self.equipo1.id,
            "posicion": "DEL",
            "edad": 24,
            "numero_camiseta": 10
        }

        response = self.client.post(url, datos, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_partido(self):
        url = reverse("partido-list")

        datos = {
            "liga": self.liga.id,
            "equipo_local": self.equipo1.id,
            "equipo_visitante": self.equipo2.id,
            "estado": "PEN",
            "fecha": "2026-11-20T18:00:00-03:00",
            "goles_local": None,
            "goles_visitante": None
        }

        response = self.client.post(url, datos, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_partido_con_mismo_equipo(self):
        url = reverse("partido-list")

        datos = {
            "liga": self.liga.id,
            "equipo_local": self.equipo1.id,
            "equipo_visitante": self.equipo1.id,
            "estado": "PEN",
            "fecha": "2026-11-20T18:00:00-03:00",
            "goles_local": None,
            "goles_visitante": None
        }

        response = self.client.post(url, datos, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
