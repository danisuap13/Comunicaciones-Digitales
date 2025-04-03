import numpy as np
import matplotlib.pyplot as plt

# Datos del archivo "Medidas Escenario 1.txt"
distancia_esc1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
rssi_esc1 = np.array([-47.90, -52.43, -61.22, -66.69, -63.00, -63.15, -74.71, -73.03, -77.15, -79.18,
                      -79.49, -77.86, -82.29, -83.42, -84.42, -84.87, -84.40, -85.99, -82.78])
desviacion_esc1 = np.array([2.64, 2.26, 5.60, 3.33, 5.03, 3.21, 3.90, 2.23, 2.35, 1.37,
                            2.51, 1.94, 3.00, 2.34, 1.82, 2.23, 1.67, 1.58, 2.43])

# Cálculo del error estándar
error_estandar_esc1 = desviacion_esc1 / np.sqrt(len(rssi_esc1))

# Crear figura y graficar
plt.figure(figsize=(10, 5))
plt.errorbar(distancia_esc1, rssi_esc1, yerr=error_estandar_esc1, fmt='bo', capsize=5, label="Error estándar")
plt.errorbar(distancia_esc1, rssi_esc1, yerr=desviacion_esc1, fmt='b-', capsize=5, label="Desviación estándar")

# Agregar valores de la desviación estándar debajo de la barra de desviación
for i in range(len(distancia_esc1)):
    plt.text(distancia_esc1[i], rssi_esc1[i] - desviacion_esc1[i] - 2,  # Ubicación debajo de la línea
             f"{desviacion_esc1[i]:.2f}", fontsize=9, ha='center', color='blue')

# Etiquetas y leyenda
plt.xlabel("Distancia (m)", fontsize=12, fontweight='bold')
plt.ylabel("RSSI (dBm)", fontsize=12, fontweight='bold')
plt.title("Medidas Escenario 1", fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True)


# Mostrar la gráfica
plt.show()
