# =============================== #
# SLAVE NRF24L01 - OLED SSD1306  #
# Comunicación inalámbrica con   #
# visualización en pantalla OLED #
# =============================== #

import usys
import ustruct as struct
import utime
from machine import Pin, I2C, SPI
from ssd1306 import SSD1306_I2C
from nrf24l01 import NRF24L01
from micropython import const

# --- Configuración de la pantalla OLED ---
# Pantalla I2C de 128x32 pixeles conectada al bus I2C1 del Raspberry Pi Pico
OLED_WIDTH = 128
OLED_HEIGHT = 32
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400_000)  # I2C con frecuencia de 400kHz
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)      # Inicialización de la pantalla

# Mostrar mensaje de espera al encender
oled.fill(1)  # Fondo blanco (1 = pixeles encendidos)
oled.text("ESPERANDO...", 20, 12, 0)  # Texto centrado en negro (0 = pixeles apagados)
oled.show()

# --- Constantes de configuración del NRF24L01 ---
TX_POWER = {  # Potencia de transmisión (cuanto mayor, mayor alcance y consumo)
    "0dBm": const(0x06),
    "-6dBm": const(0x04),
    "-12dBm": const(0x02),
    "-18dBm": const(0x00)
}

DATA_RATE = {  # Velocidad de transmisión de datos
    "250kbps": const(0x20),
    "1Mbps": const(0x00),
    "2Mbps": const(0x08),
}

CHANNEL = 13  # Canal de radiofrecuencia (frecuencia = 2400 MHz + canal)

# --- Definición de pines para el módulo NRF24L01 ---
nrf_pins = {
    "spi_id": 0,     # SPI0 del Raspberry Pi Pico
    "miso": 16,      # Pin MISO
    "mosi": 19,      # Pin MOSI
    "sck": 18,       # Pin de reloj SPI
    "csn": 5,        # Chip Select Not
    "ce": 17         # Chip Enable
}

# Inicializar pines CSN y CE como salida
csn_pin = Pin(nrf_pins["csn"], Pin.OUT, value=1)
ce_pin = Pin(nrf_pins["ce"], Pin.OUT, value=0)

# --- Inicialización del módulo NRF24L01 ---
spi = SPI(nrf_pins["spi_id"])  # Inicialización del bus SPI
nrf = NRF24L01(spi, csn_pin, ce_pin, channel=CHANNEL, payload_size=32)

# Configurar la potencia de transmisión y la tasa de bits
nrf.set_power_speed(TX_POWER["0dBm"], DATA_RATE["2Mbps"])

# --- Configurar tuberías de comunicación ---
# Las tuberías definen los canales de comunicación únicos para identificar cada dispositivo
rx_pipe = b"\xe1\xf0\xf0\xf0\xf0"  # Dirección para recepción (data desde el maestro)
tx_pipe = b"\xd2\xf0\xf0\xf0\xf0"  # Dirección para transmisión (no se usa aquí, pero obligatoria)
nrf.open_tx_pipe(tx_pipe)
nrf.open_rx_pipe(1, rx_pipe)
nrf.start_listening()  # Modo escucha: espera datos del maestro

# --- Bucle principal de recepción ---
ultimo_tiempo = 0  # Guarda el timestamp de la última recepción

while True:
    # Verifica si hay datos recibidos del maestro
    if nrf.any():
        tiempo_recepcion = utime.ticks_ms()  # Guarda el tiempo actual

        while nrf.any():
            # Recibe un paquete de datos (esperamos un float de 4 bytes)
            (potencia_recibida,) = struct.unpack("f", nrf.recv())

            # Mostrar por consola
            print("Potencia recibida:", potencia_recibida, "dBm")

            # Mostrar en pantalla OLED
            oled.fill(1)  # Borra pantalla (fondo blanco)
            oled.text("Potencia:", 30, 5, 0)  # Texto: etiqueta
            oled.text(f"{potencia_recibida:.1f} dBm", 25, 20, 0)  # Texto: valor
            oled.show()

        # Guarda el último momento de recepción
        ultimo_tiempo = tiempo_recepcion

