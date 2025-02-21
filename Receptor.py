# Importar la clase 'UART' y 'Pin' desde el módulo 'machine' para trabajar con puertos UART y pines
from machine import UART, Pin
# Importar el módulo 'time' para agregar retrasos (delays) en el código
import time

# Configurar la comunicación UART para recibir datos
# 'UART(0)' crea un objeto UART en el puerto 0 (puede ser otro puerto dependiendo de la placa)
# 'baudrate=921600' establece la velocidad de transmisión de datos a 921600 baudios
# 'tx=None' indica que no se usará el pin de transmisión (TX)
# 'rx=Pin(1)' define el pin 1 para la recepción de datos (RX)
# 'rxbuf=4096' configura el tamaño del buffer de recepción
uart = UART(0, baudrate=921600, tx=None, rx=Pin(1), rxbuf=4096)

# Intentar recibir y procesar los datos enviados por UART
try:
    # Imprimir un mensaje indicando que se está esperando recibir datos
    print("Esperando datos...")
    
    # Recibir el tamaño del archivo (en bytes)
    # Primero, asegurarse de que haya al menos 4 bytes disponibles (el tamaño se envía como 4 bytes)
    while uart.any() < 4:
        time.sleep(0.001)  # Retrasar un poco para no sobrecargar el procesador
    
    # Leer los 4 primeros bytes que indican el tamaño del archivo
    size = int.from_bytes(uart.read(4), 'big')  # Convertir los 4 bytes a un entero (big-endian)
    
    # Recibir el contenido del archivo
    data = bytearray()  # Crear un array vacío para almacenar los datos recibidos
    while len(data) < size:
        if uart.any():  # Comprobar si hay datos disponibles para leer
            data.extend(uart.read())  # Leer y agregar los datos al array 'data'
    
    # Guardar los datos recibidos en un archivo
    with open('File_RX.txt', 'wb') as file:
        file.write(data)  # Escribir los datos recibidos en el archivo 'File_RX.txt'
    
    # Imprimir "Guardado" cuando el archivo ha sido guardado correctamente
    print("Guardado")
    
# Si ocurre algún error durante la recepción o el proceso, se maneja la excepción
except:
    # Imprimir un mensaje de error si algo falla
    print("Error")
