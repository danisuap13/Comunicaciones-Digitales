import network
import time
import math
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

# Configuración de la pantalla OLED
WIDTH = 128  # Ancho de la pantalla
HEIGHT = 32  # Alto de la pantalla
# Configuración de la comunicación I2C con la OLED
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=100000)
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Configuración de la conexión WiFi
wifi = network.WLAN(network.STA_IF)  # Modo estación
wifi.active(True)  # Activar WiFi
ssid = "iPhone de Daniel"  # Nombre de la red WiFi
password = "quimica123"  # Contraseña de la red

# Configuración de los LEDs indicadores
led_avanzar = Pin(16, Pin.OUT)  # LED que indica avance de medición
led_midiendo = Pin(17, Pin.OUT)  # LED que indica que se está midiendo
led_wifi = Pin(19, Pin.OUT)  # LED que indica estado de conexión WiFi

# Configuración del botón físico para iniciar mediciones
button = Pin(18, Pin.IN, Pin.PULL_UP)

# Función para conectar a la red WiFi
def connect_wifi():
    print("Conectando a WiFi...")
    led_wifi.value(1)  # Encender LED WiFi
    wifi.connect(ssid, password)  # Intentar conexión
    timeout = 10  # Tiempo límite para conexión en segundos
    start_time = time.time()
    
    while not wifi.isconnected():
        if time.time() - start_time > timeout:
            print("No se pudo conectar a WiFi")
            display_disconnected()
            return False  # Retorna False si no se conecta
        time.sleep(0.5)
        led_wifi.value(not led_wifi.value())  # Parpadeo del LED
    
    print("Conexión establecida!")
    print("Dirección IP:", wifi.ifconfig()[0])
    led_wifi.value(0)  # Apagar LED WiFi
    return True

# Función para mostrar en OLED que la conexión WiFi se perdió
def display_disconnected():
    oled.fill(0)
    oled.text("Desconectado", 2, 6)
    oled.show()
    while not wifi.isconnected():
        led_wifi.value(not led_wifi.value())  # Parpadeo rápido
        time.sleep(1)
    connect_wifi()

# Función para medir el nivel de señal WiFi (RSSI) a una distancia específica
def measure_rssi(distance):
    rssi_values = []  # Lista para almacenar valores de RSSI
    led_midiendo.value(1)  # Indicar que la medición está en curso
    filename = f"rssi_measurements_{distance}m.txt"  # Nombre del archivo para guardar datos
    
    with open(filename, "w") as file:
        file.write("Tiempo (s)\tRSSI (dBm)\n")  # Encabezado del archivo
        for i in range(200):  # Tomar 200 mediciones
            if not wifi.isconnected():
                display_disconnected()
                return [], 0, 0
            elapsed_time = i * 0.1  # Intervalo de 0.1 segundos
            rssi = wifi.status('rssi')  # Obtener RSSI
            rssi_values.append(rssi)
            file.write(f"{elapsed_time:.1f}\t{rssi}\n")
            display_rssi(rssi, distance)  # Mostrar en pantalla OLED
            time.sleep(0.1)
    
    led_midiendo.value(0)  # Apagar LED de medición
    rssi_average = sum(rssi_values) / len(rssi_values)  # Calcular promedio
    variance = sum((x - rssi_average) ** 2 for x in rssi_values) / len(rssi_values)  # Variancia
    stddev_rssi = math.sqrt(variance)  # Desviación estándar
    
    print(f"Distancia: {distance}m, Promedio RSSI: {rssi_average:.2f} dBm, Desviación: {stddev_rssi:.2f} dBm")
    
    with open(filename, "a") as file:
        file.write(f"\nResumen:\nDistancia: {distance}m\nPromedio RSSI: {rssi_average:.2f} dBm\nDesviación Estándar: {stddev_rssi:.2f} dBm\n")
    
    with open("rssi_measurements.txt", "a") as summary_file:
        summary_file.write(f"Distancia: {distance}m, Promedio: {rssi_average:.2f} dBm, Desv: {stddev_rssi:.2f} dBm\n")
    
    return rssi_values, rssi_average, stddev_rssi

# Función para mostrar el RSSI en la pantalla OLED
def display_rssi(rssi, distance):
    max_rssi = -15
    min_rssi = -100
    bar_width = int((rssi - min_rssi) / (max_rssi - min_rssi) * WIDTH)
    bar_width = max(0, min(WIDTH, bar_width))
    
    oled.fill(0)
    oled.text(f"Dist: {distance}m", 2, 6)
    oled.text(f"RSSI: {rssi} dBm", 2, 16)
    oled.rect(2, 26, 124, 6, 1)
    oled.fill_rect(2, 26, bar_width, 6, 1)
    oled.show()

# Función para indicar en OLED que la medición ha comenzado
def display_measurement_start():
    oled.fill(0)
    oled.text("Iniciando medición", 2, 6)
    oled.show()
    led_avanzar.value(0)
    led_midiendo.value(1)

# Función para indicar en OLED que la medición ha terminado
def display_measurement_done():
    oled.fill(0)
    oled.text("Medición terminada", 2, 6)
    oled.show()
    led_avanzar.value(1)
    led_midiendo.value(0)

# Función para hacer parpadear los LEDs mientras se presiona el botón
def leds_parpadear():
    while not button.value():
        led_avanzar.value(1)
        led_midiendo.value(1)
        led_wifi.value(1)
        time.sleep(0.5)
        led_avanzar.value(0)
        led_midiendo.value(0)
        led_wifi.value(0)
        time.sleep(0.5)

# Función principal del programa
def main():
    if not connect_wifi():  # Intentar conexión WiFi
        return
    
    global distance
    distance = 1  # Distancia inicial
    
    while distance <= 5:  # Realizar mediciones de 1 a 5 metros
        if not button.value():  # Esperar a que se presione el botón
            display_measurement_start()
            leds_parpadear()
            rssi_values, rssi_average, stddev_rssi = measure_rssi(distance)
            if rssi_values:
                display_rssi(rssi_average, distance)
                display_measurement_done()
                time.sleep(5)
                distance += 1  # Incrementar distancia
                oled.fill(0)
                oled.text(f"Nueva Dist: {distance}m", 2, 6)
                oled.show()
        time.sleep(0.1)

main()
