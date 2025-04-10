# =============================== #
#         Master NRF24L01         #
# Comunicación inalámbrica con    #
#        medición de RSSi         #
# =============================== #


import usys
import ustruct as struct
import network
import time
import math
from machine import Pin, SPI
from nrf24l01 import NRF24L01
from micropython import const

# ===========================
# CONFIGURACIÓN DEL HARDWARE
# ===========================

# --- Configuración de potencia y velocidad para el NRF24L01 ---
POWER = {"0 dBm": const(0x06), "-6 dBm": const(0x04), "-12 dBm": const(0x02), "-18 dBm": const(0x00)}         # Potencia máxima de transmisión
DATA_RATE =  {"250 kbps": const(0x20), "1 Mbps": const(0x00), "2 Mbps": const(0x08)}    # Tasa de datos rápida
CHANNEL = 13                           # Canal de comunicación (frecuencia = 2.413 GHz)

# --- Pines físicos conectados al módulo NRF24L01 ---
nrf_pins = {
    "spi": 0,      # Bus SPI 0
    "miso": 16,
    "mosi": 19,
    "sck": 18,
    "csn": 5,
    "ce": 17
}

# --- Inicialización de pines para el módulo NRF24L01 ---
csn = Pin(nrf_pins["csn"], Pin.OUT, value=1)
ce = Pin(nrf_pins["ce"], Pin.OUT, value=0)
spi = SPI(nrf_pins["spi"])             # Inicialización del bus SPI

# --- Inicialización del módulo NRF24L01 ---
nrf = NRF24L01(spi, csn, ce, channel=CHANNEL, payload_size=32)
nrf.set_power_speed(POWER["0 dBm"], DATA_RATE["2 Mbps"])  # Configura potencia y velocidad

# Direcciones únicas para canal de transmisión y recepción
nrf.open_tx_pipe(b"\xe1\xf0\xf0\xf0\xf0")
nrf.open_rx_pipe(1, b"\xd2\xf0\xf0\xf0\xf0")
nrf.start_listening()  # Modo escucha (requerido por la biblioteca aunque solo transmitimos)

# --- Botón físico conectado al pin GP20 ---
button = Pin(20, Pin.IN, Pin.PULL_UP)  # Con resistencia interna pull-up

# ===========================
# CONFIGURACIÓN DE RED WI-FI
# ===========================

wifi = network.WLAN(network.STA_IF)  # Interfaz WiFi en modo estación
wifi.active(True)
SSID = "digitales"
PASSWORD = "ola1234***"

# ===========================
# VARIABLES DE CONTROL
# ===========================

wifi_ok = True            # Bandera para indicar estado WiFi
measurement_count = 0     # Número de mediciones realizadas

# ===========================
# FUNCIONES AUXILIARES
# ===========================

# Reconectar al WiFi si se pierde la conexión
def reconnect_wifi():
    global wifi_ok
    retry = 0
    while not wifi.isconnected():
        print("[WiFi] Desconectado. Reintentando...")
        time.sleep(1)
        retry += 1
        if retry >= 3:
            wifi.connect(SSID, PASSWORD)
            retry = 0
    print("[WiFi] Conectado:", wifi.ifconfig()[0])
    wifi_ok = True

# Calcular desviación estándar de una lista de valores
def calculate_std(values):
    n = len(values)
    avg = sum(values) / n
    variance = sum((x - avg) ** 2 for x in values) / (n - 1)
    return math.sqrt(variance)

# Esperar una pulsación de botón (presionar y soltar)
def wait_for_button_press():
    while button.value() == 0:  # Espera a que se suelte si está presionado
        time.sleep(0.05)
    while button.value() == 1:  # Espera a que se presione
        time.sleep(0.05)

# ===========================
# INICIO DEL PROGRAMA
# ===========================

# Conectar al WiFi al inicio del script
wifi.connect(SSID, PASSWORD)
reconnect_wifi()

print(">> Sistema listo. Presiona el botón para iniciar mediciones.\n")

# ===========================
# BUCLE PRINCIPAL
# ===========================

while True:
    wait_for_button_press()  # Esperar que el usuario presione el botón

    # Verifica si la conexión WiFi sigue activa
    if not wifi.isconnected():
        wifi_ok = False
        reconnect_wifi()

    print(f"[{measurement_count + 1}] Iniciando medición...")

    rssi_values = []  # Lista para almacenar los valores RSSI (potencia de señal)

    for i in range(200):
        rssi = wifi.status('rssi')  # Lee la señal WiFi (en dBm)
        rssi_values.append(rssi)
        time.sleep(0.1)  # Espera entre muestras (100 ms)

        # Enviar el valor cada 2 muestras
        if i % 2 == 0:
            nrf.stop_listening()
            try:
                nrf.send(struct.pack("f", rssi))  # Empaqueta el valor como float de 4 bytes
                print(f"  RSSI enviado: {rssi} dBm")
            except OSError:
                print("  ⚠️ Error al enviar")
            nrf.start_listening()

        # Si la señal WiFi desaparece (valor 0), se asume desconexión
        if rssi == 0.0:
            print("⚠️ Señal WiFi perdida durante la medición.")
            wifi_ok = False
            reconnect_wifi()
            break

    # Si la medición fue válida (sin perder WiFi), se calculan los resultados
    if wifi_ok:
        avg_rssi = sum(rssi_values) / len(rssi_values)
        std_dev = calculate_std(rssi_values)
        print(f"[{measurement_count + 1}] RSSI Promedio: {avg_rssi:.2f} dBm | Desv. estándar: {std_dev:.2f} dBm\n")
        measurement_count += 1
    else:
        print("⛔ Medición descartada. WiFi reconectado.\n")
        wifi_ok = True
