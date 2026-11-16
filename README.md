# Torneos Backend

API REST para la gestión de torneos de fútbol: ligas, equipos, jugadores y partidos, con tabla de posiciones calculada automáticamente.

Este repositorio es el **Back-End** del proyecto de la Evaluación 1 (aplicación de gestión de torneos deportivos con interfaz inspirada en Promiedos, desarrollada en React). Está pensado para que el Front-End pueda consumirlo en una etapa posterior.

## Tecnologías

- Python
- Django
- Django REST Framework
- SQLite (base de datos por defecto de Django)
- django-cors-headers (para permitir peticiones desde React)

## Estructura del proyecto

```
torneos-backend/
├── config/            # Configuración del proyecto (settings.py, urls.py)
├── torneos/           # App principal
│   ├── models.py      # Modelos de datos
│   ├── serializers.py # Validación y conversión a JSON
│   ├── views.py       # ViewSets, filtros y lógica de negocio
│   ├── urls.py        # Rutas de la API (router)
│   ├── admin.py       # Registro de modelos en el panel de administración
│   └── tests.py       # Pruebas automáticas
├── manage.py
├── requirements.txt
├── README.md
└── USO_IA.md
```

## Modelos

| Modelo      | Campos principales                          | Relaciones                                                           |
| ----------- | ------------------------------------------- | -------------------------------------------------------------------- |
| **Liga**    | nombre, país, logo (URL)                    | —                                                                    |
| **Equipo**  | nombre, escudo (URL)                        | `ForeignKey` a Liga                                                  |
| **Jugador** | nombre, posición, edad, número de camiseta  | `ForeignKey` a Equipo                                                |
| **Partido** | fecha, estado, goles local, goles visitante | `ForeignKey` a Liga, y dos `ForeignKey` a Equipo (local y visitante) |

**Posiciones de jugador:** ARQ (Arquero), DEF (Defensor), MED (Mediocampista), DEL (Delantero).

**Estados de partido:** PEN (Pendiente), VIV (En vivo), FIN (Finalizado), POS (Postergado).

## Instalación

1. Clonar el repositorio:

   ```bash
   git clone <https://github.com/NicolasAceiton/Torneos_Backend>
   cd torneos-backend
   ```

2. Crear y activar un entorno virtual:

   ```bash
   python -m venv venv

   # Windows (PowerShell)
   venv\Scripts\Activate.ps1

   # Windows (CMD)
   venv\Scripts\activate.bat

   # Mac / Linux
   source venv/bin/activate
   ```

3. Instalar las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Migraciones y ejecución

1. Crear las tablas en la base de datos:

   ```bash
   python manage.py migrate
   ```

   Las migraciones ya están incluidas en el repositorio (`torneos/migrations/`). Si se modifica algún modelo, se deben ejecutar `python manage.py makemigrations` y luego `python manage.py migrate`.

2. (Opcional) Crear un superusuario para usar el panel de administración:

   ```bash
   python manage.py createsuperuser
   ```

3. Iniciar el servidor:

   ```bash
   python manage.py runserver
   ```

4. Abrir en el navegador:
   - API: <http://127.0.0.1:8000/api/>
   - Panel de administración: <http://127.0.0.1:8000/admin/>

## Endpoints principales

| Método                  | Ruta                           | Descripción                                                         |
| ----------------------- | ------------------------------ | ------------------------------------------------------------------- |
| GET, POST               | `/api/ligas/`                  | Listar y crear ligas                                                |
| GET, PUT, PATCH, DELETE | `/api/ligas/<id>/`             | Consultar, actualizar y eliminar una liga                           |
| GET                     | `/api/ligas/<id>/posiciones/`  | Tabla de posiciones calculada                                       |
| GET, POST               | `/api/equipos/`                | Listar y crear equipos (filtro `?liga=<id>`)                        |
| GET, PUT, PATCH, DELETE | `/api/equipos/<id>/`           | Consultar, actualizar y eliminar un equipo                          |
| GET                     | `/api/equipos/<id>/plantilla/` | Jugadores del equipo agrupados por posición                         |
| GET, POST               | `/api/jugadores/`              | Listar y crear jugadores (filtro `?equipo=<id>`)                    |
| GET, PUT, PATCH, DELETE | `/api/jugadores/<id>/`         | Consultar, actualizar y eliminar un jugador                         |
| GET, POST               | `/api/partidos/`               | Listar y crear partidos (filtros `?liga=<id>` y `?estado=<código>`) |
| GET, PUT, PATCH, DELETE | `/api/partidos/<id>/`          | Consultar, actualizar y eliminar un partido                         |

La documentación completa, con ejemplos de solicitudes y respuestas, está en [`docs/ENDPOINTS.md`](docs/ENDPOINTS.md).

### Ejemplo rápido

Crear una liga:

```http
POST /api/ligas/
Content-Type: application/json

{"nombre": "Liga Chilena", "pais": "Chile"}
```

Respuesta (`201 Created`):

```json
{ "id": 1, "nombre": "Liga Chilena", "pais": "Chile", "liga_logo_url": "" }
```

## Validaciones

- **Liga:** el nombre debe tener al menos 3 caracteres.
- **Jugador:** edad entre 14 y 60 años; número de camiseta entre 1 y 99; el número no puede repetirse dentro del mismo equipo.
- **Partido:**
  - el equipo local y el visitante deben ser distintos;
  - ambos equipos deben pertenecer a la liga del partido;
  - se deben indicar los goles de ambos equipos, o ninguno;
  - los goles no pueden ser negativos;
  - un partido finalizado (`FIN`) debe tener goles registrados;
  - un partido pendiente (`PEN`) o postergado (`POS`) no puede tener goles.

Si los datos son inválidos, la API responde `400 Bad Request` con el detalle del error. Si un registro no existe, responde `404 Not Found`.

## Lógica de negocio: tabla de posiciones

El endpoint `GET /api/ligas/<id>/posiciones/` **calcula la tabla al momento** a partir de los partidos finalizados de la liga. No se guarda en la base de datos, por lo que siempre está actualizada: si se corrige un marcador, la tabla cambia sola.

Reglas aplicadas:

- Victoria: 3 puntos. Empate: 1 punto. Derrota: 0 puntos.
- Solo cuentan los partidos con estado `FIN`.
- Cada equipo muestra: PJ, G, E, P, GF, GC, DG y puntos.
- Orden: puntos, luego diferencia de gol, luego goles a favor, luego nombre.

## Pruebas

### Pruebas automáticas

```bash
python manage.py test
```

### Pruebas manuales de la API

La evidencia de pruebas realizadas con Postman (capturas y colección exportada) se encuentra en la carpeta [`docs/`](docs/).

## Preparado para integración con React

El proyecto incluye `django-cors-headers` configurado para aceptar peticiones desde los puertos de desarrollo de React (`http://localhost:5173` y `http://localhost:3000`). Los serializers incluyen campos de solo lectura con nombres (por ejemplo `liga_nombre`, `equipo_local_nombre`) para que el Front-End no necesite consultas adicionales.

## Uso de inteligencia artificial

La declaración del uso de herramientas de IA está en [`USO_IA.md`](USO_IA.md).

## Autores

- Nicolás Aceitón: (https://github.com/NicolasAceiton)
- Joaquin Schatter: (https://github.com/Juakiru)

Proyecto desarrollado para la Evaluación Regular 2: Desarrollo Back-End con Django.
