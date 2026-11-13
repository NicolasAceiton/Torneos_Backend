from rest_framework import serializers
from .models import Liga, Equipo, Jugador, Partido


class LigaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liga
        fields = ["id", "nombre", "pais", "liga_logo_url"]

    def validate_nombre(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "El nombre debe tener al menos 3 caracteres."
            )
        return value.strip()


class EquipoSerializer(serializers.ModelSerializer):
    liga_nombre = serializers.CharField(source="liga.nombre", read_only=True)

    class Meta:
        model = Equipo
        fields = ["id", "nombre", "liga", "liga_nombre", "escudo_url"]


class JugadorSerializer(serializers.ModelSerializer):
    equipo_nombre = serializers.CharField(source="equipo.nombre", read_only=True)
    posicion_display = serializers.CharField(source="get_posicion_display", read_only=True)

    class Meta:
        model = Jugador
        fields = ["id", "nombre", "equipo", "equipo_nombre",
                  "posicion", "posicion_display", "edad", "numero_camiseta"]
        extra_kwargs = {
            "edad": {"min_value": 14, "max_value": 60},
            "numero_camiseta": {"min_value": 1, "max_value": 99},
        }

    def validate(self, attrs):
        # En un PATCH pueden faltar campos: usamos lo enviado
        # y, si no viene, lo que ya está guardado.
        equipo = attrs.get("equipo", getattr(self.instance, "equipo", None))
        numero = attrs.get("numero_camiseta", getattr(self.instance, "numero_camiseta", None))

        if equipo and numero is not None:
            repetidos = Jugador.objects.filter(equipo=equipo, numero_camiseta=numero)
            if self.instance:
                repetidos = repetidos.exclude(pk=self.instance.pk)
            if repetidos.exists():
                raise serializers.ValidationError(
                    {"numero_camiseta": f"El número {numero} ya está en uso en {equipo.nombre}."}
                )
        return attrs


class PartidoSerializer(serializers.ModelSerializer):
    liga_nombre = serializers.CharField(source="liga.nombre", read_only=True)
    equipo_local_nombre = serializers.CharField(source="equipo_local.nombre", read_only=True)
    equipo_visitante_nombre = serializers.CharField(source="equipo_visitante.nombre", read_only=True)
    estado_display = serializers.CharField(source="get_estado_display", read_only=True)

    class Meta:
        model = Partido
        fields = ["id", "liga", "liga_nombre",
                  "equipo_local", "equipo_local_nombre",
                  "equipo_visitante", "equipo_visitante_nombre",
                  "estado", "estado_display", "fecha",
                  "goles_local", "goles_visitante"]
        extra_kwargs = {
            "goles_local": {"min_value": 0},
            "goles_visitante": {"min_value": 0},
        }

    def validate(self, attrs):
        def valor(campo):
            return attrs.get(campo, getattr(self.instance, campo, None))

        liga = valor("liga")
        local = valor("equipo_local")
        visitante = valor("equipo_visitante")
        estado = valor("estado")
        goles_local = valor("goles_local")
        goles_visitante = valor("goles_visitante")

        if local and visitante and local == visitante:
            raise serializers.ValidationError(
                "El equipo local y el visitante no pueden ser el mismo."
            )

        if liga:
            for campo, equipo in (("equipo_local", local), ("equipo_visitante", visitante)):
                if equipo and equipo.liga_id != liga.id:
                    raise serializers.ValidationError(
                        {campo: f"{equipo.nombre} no pertenece a la liga {liga.nombre}."}
                    )

        if (goles_local is None) != (goles_visitante is None):
            raise serializers.ValidationError(
                "Debes indicar los goles de ambos equipos, o ninguno."
            )

        if estado == "FIN" and goles_local is None:
            raise serializers.ValidationError(
                {"estado": "Un partido finalizado debe tener goles registrados."}
            )

        if estado in ("PEN", "POS") and goles_local is not None:
            raise serializers.ValidationError(
                {"estado": "Un partido pendiente o postergado no puede tener goles."}
            )

        return attrs