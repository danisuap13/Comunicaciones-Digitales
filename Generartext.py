# Importar el módulo 'random' para generar valores aleatorios
import random
# Importar el módulo 'string' para acceder a cadenas de caracteres predefinidas (letras, dígitos, etc.)
import string

# Definir la función 'generar_linea'
def generar_linea():
    # Usar 'random.choices()' para elegir 60 caracteres aleatorios de letras y dígitos
    # 'string.ascii_letters' contiene las letras mayúsculas y minúsculas (A-Z, a-z)
    # 'string.digits' contiene los dígitos (0-9)
    # 'k=60' significa que se seleccionarán 60 caracteres aleatorios
    return ''.join(random.choices(string.ascii_letters + string.digits, k=60))

# Intentar abrir (y crear si no existe) un archivo llamado "file.txt" en modo escritura ("w")
try:
    # Abre el archivo "file.txt" en modo escritura
    with open("file.txt", "w") as file:
        # Bucle que se ejecuta 100 veces (se generarán 100 líneas)
        for _ in range(100):
            # Escribir una línea en el archivo con 60 caracteres aleatorios
            # Después de cada línea se agrega un salto de línea ("\n")
            file.write(generar_linea() + "\n")
    # Si todo va bien, imprimir "Generado"
    print("Generado")
# Si ocurre cualquier error, se entra en el bloque 'except'
except:
    # Imprimir "Error" si hay una excepción
    print("Error")
    # Mensaje adicional sobre el tipo de error
    print("Error al enviar")
