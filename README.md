# Gestión de Datos de Países en Python

**Trabajo Práctico Integrador - Programación 1**
Tecnicatura Universitaria en Programación a Distancia - UTN

## Descripción

Aplicación de consola en Python que gestiona información de países (nombre, población, superficie y continente). Los datos se leen desde un archivo CSV y el programa permite agregar, actualizar, buscar, filtrar y ordenar países, además de mostrar estadísticas básicas.

Conceptos aplicados: listas, diccionarios, funciones, condicionales, bucles, ordenamientos, estadísticas básicas y lectura/escritura de archivos CSV.

## Estructura del proyecto

```
.
├── paises.py             # Código fuente del programa
├── paises.csv            # Dataset base (30 países)
├── diagrama_flujo.png    # Diagrama de flujo de las operaciones principales
├── README.md
└── <documentacion>.pdf   # Informe en PDF (o enlace más abajo)
```

## Requisitos

- Python 3.x (no se necesitan librerías externas; solo se usa el módulo `csv` de la biblioteca estándar).

## Instrucciones de uso

1. Abrí una terminal en la carpeta del proyecto (donde están `paises.py` y `paises.csv`).
2. Ejecutá:

   ```bash
   python paises.py
   ```

3. Elegí una opción del menú escribiendo su número y presionando Enter.

### Menú principal

| Opción | Función |
|--------|---------|
| 1 | Agregar un país (todos los campos son obligatorios) |
| 2 | Actualizar población y superficie de un país |
| 3 | Buscar un país por nombre (coincidencia parcial o exacta) |
| 4 | Filtrar por continente, rango de población o rango de superficie |
| 5 | Ordenar por nombre, población o superficie (ascendente o descendente) |
| 6 | Mostrar estadísticas |
| 7 | Listar todos los países |
| 0 | Salir |

*Los cambios de las opciones 1 y 2 se guardan automáticamente en `paises.csv`.*

## Formato del CSV

""""""""""""""""""""""""""""""""""""""
nombre,poblacion,superficie,continente
Argentina,45376763,2780400,América
Japón,125800000,377975,Asia
Brasil,213993437,8515767,América
Alemania,83149300,357022,Europa
""""""""""""""""""""""""""""""""""""""

*Las filas con formato incorrecto (campos vacíos, valores no numéricos, números menores o iguales a cero) se omiten y el programa informa la línea y el motivo al iniciar.*

## Validaciones y manejo de errores

- Campos vacíos no permitidos al agregar un país.
- Población y superficie deben ser enteros mayores a cero (se vuelve a pedir el dato si es inválido).
- No se permiten países duplicados (se ignoran tildes y mayúsculas).
- Rangos inválidos (mínimo mayor que máximo) y opciones de menú inválidas muestran un mensaje de error sin cortar el programa.
- Búsquedas, filtros o actualizaciones sin resultados informan con un mensaje claro.
- Si el CSV no existe o está mal formado, el programa lo informa y sigue funcionando.

## Ejemplos de entradas y salidas

**Buscar (opción 3, coincidencia parcial, texto `jap`):**

```
Nombre                          Población    Superficie (km²)  Continente
---------------------------------------------------------------------------
Japón                         125.800.000             377.975  Asia
---------------------------------------------------------------------------
Total: 1 país(es).
```

**Agregar un país con datos inválidos (opción 1):**

```
Nombre: Narnia
Población (habitantes): abc
Error: ingresá solo números enteros, sin puntos ni letras.
Población (habitantes): -5
Error: el número debe ser mayor a cero.
Población (habitantes): 1000
Superficie (km²): 2000
Continente: Fantasia
Éxito: se agregó 'Narnia' correctamente.
```

**Estadísticas (opción 6):**

```
=== ESTADÍSTICAS ===
País con mayor población: China (1.412.600.000 hab.)
País con menor población: Uruguay (3.473.727 hab.)
Promedio de población:    169.836.615 hab.
Promedio de superficie:   2.819.559 km²
Cantidad de países por continente:
  - América: 11
  - Asia: 5
  - Europa: 7
  - Oceanía: 2
  - África: 5
```

## Diagrama de flujo

Ver `diagrama_flujo.png`.

## Participación de los integrantes

=== Integrantes ===
--> Guadalupe Nahir Ozan
--> Tomas Joaquin Rivas
