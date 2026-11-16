# Herramientas utilizadas

- Claude
- Gemini

## Uso estimado por archivo

| Archivo          | Uso estimado de IA | Descripción                                                                                   |
| ---------------- | ------------------ | --------------------------------------------------------------------------------------------- |
| `models.py`      | [30]%              | [Se utilizó para ayudar con funciones y orden, nosotros creamos los modelos y sus atributos.] |
| `serializers.py` | [60]%              | [Se utilizo para estructurar el codigo, nosotros dimos algunas ideas y la ia estructuró. ]    |
| `views.py`       | [70]%              | [Se utilizó para estructurar el codigo, se le dieron algunas ideas.]                          |
| `urls.py`        | [30]%              | [Se le preguntó como realizarlo, y lo realizamos.]                                            |
| `settings.py`    | [30]%              | [Apoyo para configurar `INSTALLED_APPS`, idioma, zona horaria y CORS.]                        |
| `admin.py`       | [30]%              | [Se le pregunto como realizarlo y lo realizamos.]                                             |
| `tests.py`       | [80]%              | [Se le pidió los Test, Solo comprobamos que funcione.]                                        |
| `README.md`      | [80]%              | [Generado por la IA. solo lo revisamos y cambiamos unas cosas.]                               |

# Preguntas de reflexión

## 1. ¿En qué aspectos del proyecto utilizamos inteligencia artificial?

Utilizamos la IA para ir estructurando el proyecto, nos fue guiando para poder realizarlo de manera ordenada y explicando los conceptos, se utilizó para poder ejecutar ideas pensadas por nosotros tambien.

## 2. ¿Qué partes del código fueron desarrolladas principalmente por nosotros?

Definimos los modelos con sus entidades, el settings, tambien algunos modelos de serializer fueron ideas nuestras, en la mayoria se pidió algun ejemplo y se fue trabajando con eso, para despues pedirle lo estructurara mejor.

## 3. ¿Qué errores o problemas encontramos en las respuestas generadas por IA?

[Ejemplos reales que nos ocurrieron. Conserven los que sean ciertos para ustedes y agreguen otros:]

- Fallo con los Models y Serializers= Los serializers que escribimos primero usaban nombres como `numero` y `fecha_hora`, pero nuestros modelos usaban `numero_camiseta` y `fecha`, por lo cual la api habia fallado, tuvimos que verificar y arreglarlo.
- Falta de Archivo= El comando `startapp` no crea `urls.py` por lo cual tuvimos que buscar por que no funcionaba el servidor.

## 4. ¿Cómo verificamos que el código sugerido funcionaba correctamente?

- Ejecutamos `python manage.py runserver` y probamos los endpoints en el navegador y en Postman.
- Ejecutamos `python manage.py test`.
- Seguimos los pasos del README para ver si funcionaba-

### 5. ¿Qué conocimientos adquirimos durante el desarrollo?

- Cómo se conectan `models.py`, `serializers.py`, `views.py` y `urls.py` en Django REST Framework.
- Qué son las migraciones y para qué sirven.
- Cómo se relacionan los modelos con `ForeignKey`, `on_delete` y `related_name`.
- La diferencia entre `validate_<campo>` y `validate`, y cómo usar `self.instance` para que las validaciones funcionen en un `PATCH`.
- Cómo calcular una tabla de posiciones a partir de los datos en vez de guardarla.
- Cómo usar Git y GitHub, y cómo documentar y probar una API.
