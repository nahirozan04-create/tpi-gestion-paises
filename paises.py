# Trabajo Práctico Integrador - Programación 1
# Tecnicatura Universitaria en Programación a Distancia (UTN)

# Gestión de Datos de Países: filtros, ordenamientos y estadísticas.

# Estructuras utilizadas:
# - Lista de diccionarios: cada país es un diccionario con las claves
#    "nombre", "poblacion", "superficie" y "continente".
# - Funciones: cada función tiene una única responsabilidad.
# - Archivo CSV: lectura inicial y guardado de los cambios.

import csv

# --------------
#   CONSTANTES
# --------------
RUTA_CSV = "paises.csv"
CAMPOS = ["nombre", "poblacion", "superficie", "continente"]

# Equivalencias para comparar textos sin importar tildes ni mayúsculas
ACENTOS = {
    "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ü": "u", "ñ": "n",
}


# ---------------------------------------
# UTILIDADES DE TEXTO Y ENTRADA DE DATOS
# ---------------------------------------
def normalizar_texto(texto):

    # Devuelve el texto en minúsculas, sin espacios extremos y sin tildes.
    resultado = texto.strip().lower()
    for con_tilde, sin_tilde in ACENTOS.items():
        resultado = resultado.replace(con_tilde, sin_tilde)
    return resultado


def pedir_texto(mensaje):
    
    # Pide un texto por consola y repite hasta que no esté vacío.
    while True:
        valor = input(mensaje).strip()
        if valor != "":
            return valor
        print("Error: el campo no puede estar vacío.")


def pedir_entero_positivo(mensaje):

    # Pide un número entero mayor a cero y repite hasta que sea válido.
    while True:
        texto = input(mensaje).strip()
        try:
            numero = int(texto)
        except ValueError:
            print("Error: ingresá solo números enteros, sin puntos ni letras.")
            continue
        if numero <= 0:
            print("Error: el número debe ser mayor a cero.")
        else:
            return numero


def pedir_entero_opcional(mensaje, valor_actual):

    # Pide un entero positivo. Si el usuario presiona Enter sin escribir nada,
    # se conserva el valor actual.
    while True:
        texto = input(mensaje).strip()
        if texto == "":
            return valor_actual
        try:
            numero = int(texto)
        except ValueError:
            print("Error: ingresá solo números enteros, sin puntos ni letras.")
            continue
        if numero <= 0:
            print("Error: el número debe ser mayor a cero.")
        else:
            return numero


def formatear_numero(numero):

    # Formatea un número con puntos como separador de miles (45.376.763).
    return f"{numero:,.0f}".replace(",", ".")

# -----------------------------
# LECTURA Y ESCRITURA DEL CSV
# -----------------------------
def validar_fila(fila, numero_linea):

    # Valida una fila leída del CSV.
    # Devuelve (pais, None) si es válida o (None, mensaje_de_error) si no lo es.

    for campo in CAMPOS:
        valor = fila.get(campo)
        if valor is None or valor.strip() == "":
            return None, f"Línea {numero_linea}: falta el campo '{campo}'."

    try:
        poblacion = int(fila["poblacion"].strip())
        superficie = int(fila["superficie"].strip())
    except ValueError:
        return None, (f"Línea {numero_linea}: población y superficie deben ser números enteros.")

    if poblacion <= 0 or superficie <= 0:
        return None, (f"Línea {numero_linea}: población y superficie deben ser mayores a cero.")

    pais = {
        "nombre": fila["nombre"].strip(),
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": fila["continente"].strip(),
    }
    return pais, None


def cargar_paises(ruta):
    
    # Lee el CSV y devuelve (lista_de_paises, lista_de_errores).
    # Las filas con formato incorrecto se omiten y se informan en los errores.
    
    paises = []
    errores = []

    try:
        with open(ruta, "r", encoding="utf-8", newline="") as archivo:
            lector = csv.DictReader(archivo)

            if lector.fieldnames is None:
                return [], ["El archivo CSV está vacío."]
            for campo in CAMPOS:
                if campo not in lector.fieldnames:
                    return [], [f"Al CSV le falta la columna '{campo}'."]

            for fila in lector:

                # line_num es el número de línea real dentro del archivo
                pais, error = validar_fila(fila, lector.line_num)
                if error is None:
                    paises.append(pais) 
                else:
                    errores.append(error)
    except FileNotFoundError:
        errores.append(f"No se encontró el archivo '{ruta}'.")
    return paises, errores


def guardar_paises(paises, ruta):

    # Guarda la lista de países en el CSV. Devuelve True si salió bien.
    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
        escritor.writeheader()
        for pais in paises:
            escritor.writerow(pais)
    return True

# ---------------
# VISUALIZACIÓN
# ---------------

def mostrar_paises(paises):
    
    # Muestra una lista de países en formato de tabla.
    if len(paises) == 0:
        print("No se encontraron países.")
        return

    print()
    print(f"{'Nombre':<25}{'Población':>16}{'Superficie (km²)':>20}  Continente")
    print("-" * 75)
    for pais in paises:
        print(f"{pais['nombre']:<25}"
              f"{formatear_numero(pais['poblacion']):>16}"
              f"{formatear_numero(pais['superficie']):>20}"
              f"  {pais['continente']}")
    print("-" * 75)
    print(f"Total: {len(paises)} país(es).")


# -----------
#  BÚSQUEDA
# -----------
def buscar_exacto(paises, nombre):

    # Devuelve el país cuyo nombre coincide exactamente, o None.
    buscado = normalizar_texto(nombre)
    for pais in paises:
        if normalizar_texto(pais["nombre"]) == buscado:
            return pais
    return None


def buscar_parcial(paises, texto):

    # Devuelve la lista de países cuyo nombre contiene el texto.
    buscado = normalizar_texto(texto)
    resultado = []
    for pais in paises:
        if buscado in normalizar_texto(pais["nombre"]):
            resultado.append(pais)
    return resultado


# -----------
#  FILTROS
# -----------
def filtrar_por_continente(paises, continente):

    # Devuelve los países que pertenecen al continente indicado.
    buscado = normalizar_texto(continente)
    resultado = []
    for pais in paises:
        if normalizar_texto(pais["continente"]) == buscado:
            resultado.append(pais)
    return resultado


def filtrar_por_rango(paises, campo, minimo, maximo):

    # Devuelve los países cuyo campo numérico está entre minimo y maximo.
    resultado = []
    for pais in paises:
        if minimo <= pais[campo] <= maximo:
            resultado.append(pais)
    return resultado


def obtener_continentes(paises):

    # Devuelve la lista (sin repetidos) de continentes presentes.
    continentes = []
    for pais in paises:
        if pais["continente"] not in continentes:
            continentes.append(pais["continente"])
    return sorted(continentes)


# ---------------
#  ORDENAMIENTOS
# ---------------
def clave_nombre(pais):

    # Clave de orden por nombre (sin distinguir tildes ni mayúsculas).
    return normalizar_texto(pais["nombre"])


def clave_poblacion(pais):

    # Clave de orden por población.
    return pais["poblacion"]


def clave_superficie(pais):

    # Clave de orden por superficie.
    return pais["superficie"]


# Diccionario que asocia cada criterio de orden con su función clave
CLAVES_ORDEN = {
    "nombre": clave_nombre,
    "poblacion": clave_poblacion,
    "superficie": clave_superficie,
}


def ordenar_paises(paises, criterio, descendente):

    # Devuelve una NUEVA lista ordenada según el criterio indicado.
    return sorted(paises, key=CLAVES_ORDEN[criterio], reverse=descendente)


#---------------------------
#   ESTADÍSTICAS
# ----------------------------
def calcular_estadisticas(paises):
    
    # Calcula las estadísticas y las devuelve en un diccionario:
    # mayor, menor, promedio_poblacion, promedio_superficie, por_continente.

    mayor = paises[0]
    menor = paises[0]
    suma_poblacion = 0
    suma_superficie = 0
    por_continente = {}

    for pais in paises:
        if pais["poblacion"] > mayor["poblacion"]:
            mayor = pais
        if pais["poblacion"] < menor["poblacion"]:
            menor = pais
        suma_poblacion += pais["poblacion"]
        suma_superficie += pais["superficie"]

        continente = pais["continente"]
        if continente in por_continente:
            por_continente[continente] += 1
        else:
            por_continente[continente] = 1

    cantidad = len(paises)
    return {
        "mayor": mayor,
        "menor": menor,
        "promedio_poblacion": suma_poblacion / cantidad,
        "promedio_superficie": suma_superficie / cantidad,
        "por_continente": por_continente,
    }


def mostrar_estadisticas(paises):

    # Muestra por consola las estadísticas del dataset.
    if len(paises) == 0:
        print("No hay países cargados para calcular estadísticas.")
        return

    stats = calcular_estadisticas(paises)
    print("\n=== ESTADÍSTICAS ===")

    print(f"País con mayor población: {stats['mayor']['nombre']} "
          f"({formatear_numero(stats['mayor']['poblacion'])} hab.)")
    
    print(f"País con menor población: {stats['menor']['nombre']} "
          f"({formatear_numero(stats['menor']['poblacion'])} hab.)")
    
    print(f"Promedio de población:    "
          f"{formatear_numero(stats['promedio_poblacion'])} hab.")
    
    print(f"Promedio de superficie:   "
          f"{formatear_numero(stats['promedio_superficie'])} km²")
    
    print("Cantidad de países por continente:")

    for continente in sorted(stats["por_continente"]):
        print(f"  - {continente}: {stats['por_continente'][continente]}")


# ----------------------------------------------------
# OPERACIONES DEL MENÚ (interacción con el usuario)
# ----------------------------------------------------
def opcion_agregar(paises):

    # Agrega un país nuevo (todos los campos son obligatorios).
    print("\n=== AGREGAR PAÍS ===")
    nombre = pedir_texto("Nombre: ")
    if buscar_exacto(paises, nombre) is not None:
        print(f"Error: ya existe un país llamado '{nombre}'.")
        return

    poblacion = pedir_entero_positivo("Población (habitantes): ")
    superficie = pedir_entero_positivo("Superficie (km²): ")
    continente = pedir_texto("Continente: ")

    paises.append({
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente,
    })
    if guardar_paises(paises, RUTA_CSV):
        print(f"Éxito: se agregó '{nombre}' correctamente.")


def opcion_actualizar(paises):

    # Actualiza población y/o superficie de un país existente.
    print("\n=== ACTUALIZAR PAÍS ===")
    nombre = pedir_texto("Nombre exacto del país a actualizar: ")
    pais = buscar_exacto(paises, nombre)
    if pais is None:
        print(f"Error: no existe ningún país llamado '{nombre}'.")
        return

    print(f"Datos actuales -> Población: {formatear_numero(pais['poblacion'])}"
          f" | Superficie: {formatear_numero(pais['superficie'])} km²")
    print("(Presioná Enter para mantener el valor actual)")
    pais["poblacion"] = pedir_entero_opcional("Nueva población: ", pais["poblacion"])
    pais["superficie"] = pedir_entero_opcional("Nueva superficie (km²): ", pais["superficie"])
    if guardar_paises(paises, RUTA_CSV):
        print(f"Éxito: se actualizó '{pais['nombre']}' correctamente.")


def opcion_buscar(paises):

    # Busca países por nombre (coincidencia exacta o parcial).
    print("\n=== BUSCAR PAÍS ===")
    print("1. Coincidencia parcial (contiene el texto)")
    print("2. Coincidencia exacta")
    modo = input("Elegí el tipo de búsqueda: ").strip()
    if modo not in ("1", "2"):
        print("Error: opción inválida.")
        return

    texto = pedir_texto("Nombre a buscar: ")
    if modo == "1":
        resultado = buscar_parcial(paises, texto)
    else:
        pais = buscar_exacto(paises, texto)
        resultado = [pais] if pais is not None else []

    if len(resultado) == 0:
        print(f"No se encontraron países para '{texto}'.")
    else:
        mostrar_paises(resultado)


def pedir_rango(etiqueta):

    # Pide un mínimo y un máximo, y valida que el rango sea coherente.
    while True:
        minimo = pedir_entero_positivo(f"{etiqueta} mínima: ")
        maximo = pedir_entero_positivo(f"{etiqueta} máxima: ")
        if minimo <= maximo:
            return minimo, maximo
        print("Error: el mínimo no puede ser mayor que el máximo.")


def opcion_filtrar(paises):
    
    # Submenú de filtros: continente, rango de población o de superficie.
    print("\n=== FILTRAR PAÍSES ===")
    print("1. Por continente")
    print("2. Por rango de población")
    print("3. Por rango de superficie")
    opcion = input("Elegí un filtro: ").strip()

    if opcion == "1":
        print("Continentes disponibles: " + ", ".join(obtener_continentes(paises)))
        continente = pedir_texto("Continente: ")
        resultado = filtrar_por_continente(paises, continente)
        if len(resultado) == 0:
            print(f"No hay países en el continente '{continente}'.")
        else:
            mostrar_paises(resultado)
    elif opcion == "2":
        minimo, maximo = pedir_rango("Población")
        mostrar_paises(filtrar_por_rango(paises, "poblacion", minimo, maximo))
    elif opcion == "3":
        minimo, maximo = pedir_rango("Superficie (km²)")
        mostrar_paises(filtrar_por_rango(paises, "superficie", minimo, maximo))
    else:
        print("Error: opción inválida.")


def opcion_ordenar(paises):

    # Submenú de ordenamiento: criterio y sentido (ascendente/descendente).
    print("\n=== ORDENAR PAÍSES ===")
    print("1. Por nombre")
    print("2. Por población")
    print("3. Por superficie")
    opcion = input("Elegí el criterio: ").strip()

    criterios = {"1": "nombre", "2": "poblacion", "3": "superficie"}
    if opcion not in criterios:
        print("Error: opción inválida.")
        return

    print("1. Ascendente")
    print("2. Descendente")
    sentido = input("Elegí el sentido: ").strip()
    if sentido not in ("1", "2"):
        print("Error: opción inválida.")
        return

    ordenados = ordenar_paises(paises, criterios[opcion], sentido == "2")
    mostrar_paises(ordenados)


# -----------------
#  MENÚ PRINCIPAL
# -----------------
def mostrar_menu():
    
    # Imprime las opciones del menú principal.
    print("\n" + "=" * 40)
    print("   GESTIÓN DE DATOS DE PAÍSES")
    print("=" * 40)
    print("1. Agregar un país")
    print("2. Actualizar población y superficie")
    print("3. Buscar un país por nombre")
    print("4. Filtrar países")
    print("5. Ordenar países")
    print("6. Mostrar estadísticas")
    print("7. Listar todos los países")
    print("0. Salir")


def main():

    # Función principal: carga los datos y ejecuta el menú en bucle.
    paises, errores = cargar_paises(RUTA_CSV)
 
    if len(errores) > 0:
        print("Se encontraron problemas al leer el CSV:")
        for error in errores:
            print(f"  - {error}")
    print(f"Se cargaron {len(paises)} país(es) desde '{RUTA_CSV}'.")
 
    continuar = True
    while continuar:
        mostrar_menu()
        opcion = input("Elegí una opción: ").strip()
 
        if opcion == "1":
            opcion_agregar(paises)
        elif opcion == "2":
            opcion_actualizar(paises)
        elif opcion == "3":
            opcion_buscar(paises)
        elif opcion == "4":
            opcion_filtrar(paises)
        elif opcion == "5":
            opcion_ordenar(paises)
        elif opcion == "6":
            mostrar_estadisticas(paises)
        elif opcion == "7":
            mostrar_paises(paises)
        elif opcion == "0":
            continuar = False
        else:
            print("Error: opción inválida. Ingresá un número del 0 al 7.")
 
    print("¡Hasta luego!")
 
 
if __name__ == "__main__":
    main()