# Importar la clase 'UART' y 'Pin' desde el módulo 'machine' para trabajar con puertos UART y pines
from machine import UART, Pin
# Importar el módulo 'time' para agregar retrasos (delays) en el código
import time

# Configurar la comunicación UART (puerto serie) con parámetros específicos
# UART(0, baudrate=921600, tx=Pin(0), rx=None, txbuf=4096)
# 'UART(0)' crea un objeto UART en el puerto 0 (puede ser otro puerto dependiendo de la placa)
# 'baudrate=921600' establece la velocidad de transmisión de datos a 921600 baudios (muy alta)
# 'tx=Pin(0)' define el pin que se usará para la transmisión (TX)
# 'rx=None' indica que no se usará el pin de recepción (RX)
# 'txbuf=4096' configura el tamaño del buffer de transmisión para almacenar datos en cola
uart = UART(0, baudrate=921600, tx=Pin(0), rx=None, txbuf=4096)

# Intentar abrir el archivo 'file.txt' en modo binario de lectura ('rb')
try:
    with open('file.txt', 'rb') as file:  # 'rb' abre el archivo en modo binario
        # Leer todo el contenido del archivo y guardarlo en la variable 'content'
        content = file.read()
    
    # Enviar el tamaño del archivo (en bytes)
    # len(content) devuelve el tamaño del archivo (número de bytes)
    # to_bytes(4, 'big') convierte el tamaño a una secuencia de 4 bytes en formato 'big-endian'
    uart.write(len(content).to_bytes(4, 'big'))
    time.sleep(0.01)  # Introducir un pequeño retraso de 0.01 segundos para asegurar la correcta transmisión
    
    # Enviar el contenido del archivo
    # 'uart.write(content)' envía el contenido binario del archivo a través del puerto UART
    uart.write(content)
    
    # Imprimir "Enviado" si el proceso fue exitoso
    print("Enviado")
    
# Si ocurre algún error durante la lectura del archivo o el envío, se maneja la excepción
except:
    # Imprimir un mensaje de error si algo falla
    print("Error")
