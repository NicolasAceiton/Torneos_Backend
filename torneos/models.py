from django.db import models


class Liga (models.Model):
    nombre= models.CharField(max_length= 255)
    pais= models.CharField(max_length= 255)
    liga_logo_url= models.URLField(blank= True)
    
    def __str__(self):
        return self.nombre    
       

class Equipo (models.Model):
    nombre= models.CharField(max_length= 255)
    liga= models.ForeignKey('Liga' ,on_delete= models.CASCADE, related_name= "equipos") 
    escudo_url= models.URLField(blank= True)

    def __str__(self):
        return self.nombre

    
class Jugador (models.Model):
    POSICIONES= [
        ('ARQ', 'Arquero'),
        ('DEF', 'Defensor'),
        ('MED', 'Mediocampista'),
        ('DEL', 'Delantero'),
    ]
    nombre= models.CharField(max_length= 255)
    equipo= models.ForeignKey('Equipo', on_delete= models.CASCADE, related_name= "jugadores")
    posicion= models.CharField(max_length= 3, choices= POSICIONES)
    edad= models.IntegerField()
    numero_camiseta= models.IntegerField()

    def __str__(self):
        return f"{self.nombre} ({self.equipo})"



class Partido (models.Model):
    ESTADOS= [
        ('PEN', 'Pendiente'),
        ('VIV', 'En Vivo'),
        ('FIN', 'Finalizado'),
        ('POS', 'Postergado'),
    ]
    liga= models.ForeignKey('Liga', on_delete= models.CASCADE, related_name= "partidos")
    equipo_local= models.ForeignKey('Equipo', on_delete= models.CASCADE, related_name= "partidos_local")
    equipo_visitante= models.ForeignKey('Equipo', on_delete= models.CASCADE, related_name   = "partidos_visita")
    estado= models.CharField(max_length= 3, choices= ESTADOS, default= 'PEN')
    fecha= models.DateTimeField()
    goles_local= models.IntegerField(null=True, blank= True)
    goles_visitante= models.IntegerField(null=True, blank= True)

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante} - {self.fecha.strftime('%Y-%m-%d %H:%M')}"
    
