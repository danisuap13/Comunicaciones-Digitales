import numpy as np
import matplotlib.pyplot as plt

# Parámetros del modelo de propagación en espacio libre
f = 2.4e9  # Frecuencia en Hz (2.4 GHz)
c = 3e8  # Velocidad de la luz en m/s
lambda_ = c / f  # Longitud de onda
Pt = 0  # Potencia transmitida en dBm
Gt = 0  # Ganancia de la antena transmisora en dB
Gr = 0  # Ganancia de la antena receptora en dB

# Datos experimentales - Escenario 2
distancia_esc2 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 
                           19, 20, 21, 22, 23, 24, 25, 26, 27, 28])
rssi_esc2 = np.array([-36.4, -49.29, -65.43, -63.61, -65.2, -73.51, -73.9, -73.68, -76.38, -79.48, 
                       -79.11, -79.78, -76.96, -76.86, -79.93, -78.61, -76.71, -79.97, -83.15, -83.31, 
                       -83, -84.39, -80.05, -82.71, -81.96, -80.88, -81.41, -84.68, -87.88])
desviacion_esc2 = np.array([4.69, 3.75, 4.33, 1.8, 1.82, 3.67, 4.49, 2.57, 3.35, 2.46, 
                             2.63, 4.48, 1.71, 2.09, 2.1, 1.5, 1.77, 1.61, 1.97, 1.23, 
                             1.63, 2.04, 1.86, 2.17, 2.22, 1.65, 3.11, 1.99, 2.15])

# Modelo teórico sin ajuste
d_teorico = np.linspace(1, 28, 100)  # Distancias para la curva teórica
rssi_teorico = Pt + Gt + Gr - 20 * np.log10(d_teorico) - 20 * np.log10(f) - 32.44  # Fórmula teórica

# Ajuste de la curva teórica para coincidir mejor con los datos experimentales
desplazamiento_esc2 = np.mean(rssi_esc2[:5] - rssi_teorico[:5])
rssi_ajustado_esc2 = rssi_teorico + desplazamiento_esc2

# --- GRÁFICO 1: Datos experimentales con dispersión ---
plt.figure(figsize=(8, 5))
plt.errorbar(distancia_esc2, rssi_esc2, yerr=desviacion_esc2, fmt='o-', color='red', capsize=5, label="Datos experimentales")

# Etiquetas de los valores de desviación estándar (intercalados)
for i in range(len(distancia_esc2)):
    offset = -6 if i % 2 == 0 else 6  # Alterna arriba y abajo
    plt.text(distancia_esc2[i], rssi_esc2[i] + offset, f"{desviacion_esc2[i]:.2f}", 
             fontsize=8, color='red', ha='center')

# Configuración del gráfico
plt.xlabel("Distancia (m)")
plt.ylabel("RSSI (dBm)")
plt.title("Medidas Escenario 2 - Datos experimentales con dispersión")
plt.legend()
plt.grid(True)
plt.show()

# --- GRÁFICO 2: Comparación curva teórica y experimental ---
plt.figure(figsize=(8, 5))
plt.scatter(distancia_esc2, rssi_esc2, color='red', label="Datos experimentales")
plt.plot(d_teorico, rssi_teorico, linestyle='dashed', color='blue', label="Curva teórica (sin ajuste)")

# Configuración del gráfico
plt.xlabel("Distancia (m)")
plt.ylabel("RSSI (dBm)")
plt.title("Medidas Escenario 2 - Comparación Curva Teórica y Experimental")
plt.legend()
plt.grid(True)
plt.show()

# --- GRÁFICO 3: Comparación curva teórica ajustada ---
plt.figure(figsize=(8, 5))
plt.scatter(distancia_esc2, rssi_esc2, color='red', label="Datos experimentales")
plt.plot(d_teorico, rssi_ajustado_esc2, linestyle='solid', color='green', label="Curva ajustada")

# Configuración del gráfico
plt.xlabel("Distancia (m)")
plt.ylabel("RSSI (dBm)")
plt.title("Medidas Escenario 2 - Comparación con Curva Ajustada")
plt.legend()
plt.grid(True)
plt.show()
