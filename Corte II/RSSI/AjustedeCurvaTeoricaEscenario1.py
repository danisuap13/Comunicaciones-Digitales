import numpy as np
import matplotlib.pyplot as plt

# Parámetros del modelo de propagación en espacio libre
f = 2.4e9  # Frecuencia en Hz (2.4 GHz)
c = 3e8  # Velocidad de la luz en m/s
lambda_ = c / f  # Longitud de onda
Pt = 0  # Potencia transmitida en dBm
Gt = 0  # Ganancia de la antena transmisora en dB
Gr = 0  # Ganancia de la antena receptora en dB

# Datos experimentales - Escenario 1
distancia_esc1 = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
rssi_esc1 = np.array([-52.43, -61.22, -66.69, -63.00, -63.15, -74.71, -73.03, -77.15, -79.18,
                      -79.49, -77.86, -82.29, -83.42, -84.42, -84.87, -84.40, -85.99, -82.78])

# Modelo teórico sin ajuste
d_teorico = np.linspace(1, 18, 100)  # Distancias para la curva teórica
rssi_teorico = Pt + Gt + Gr - 20 * np.log10(d_teorico) - 20 * np.log10(f) - 32.44  # Fórmula teórica

# Ajuste de la curva teórica para que coincida mejor con los datos experimentales
desplazamiento_esc1 = np.mean(rssi_esc1[:5] - rssi_teorico[:5])
rssi_ajustado_esc1 = rssi_teorico + desplazamiento_esc1

# --- GRAFICAR ESCENARIO 1 ---
plt.figure(figsize=(10, 5))
plt.scatter(distancia_esc1, rssi_esc1, color='red', label="Datos experimentales", zorder=2)
plt.plot(d_teorico, rssi_teorico, linestyle='dashed', color='blue', label="Curva teórica (sin ajuste)", zorder=1)

# Configuración del gráfico
plt.xlabel("Distancia (m)")
plt.ylabel("RSSI (dBm)")
plt.title("Escenario 1 - Comparación con modelo teórico (sin ajuste)")
plt.legend()
plt.grid(True)
plt.show()

# --- GRAFICAR ESCENARIO 1 CON AJUSTE ---
plt.figure(figsize=(10, 5))
plt.scatter(distancia_esc1, rssi_esc1, color='red', label="Datos experimentales", zorder=2)
plt.plot(d_teorico, rssi_ajustado_esc1, linestyle='solid', color='green', label="Curva ajustada", zorder=1)

# Configuración del gráfico
plt.xlabel("Distancia (m)")
plt.ylabel("RSSI (dBm)")
plt.title("Escenario 1 - Comparación con modelo teórico (ajustado)")
plt.legend()
plt.grid(True)
plt.show()

