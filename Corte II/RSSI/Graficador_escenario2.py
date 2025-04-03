import numpy as np
import matplotlib.pyplot as plt

# Datos del archivo "Medidas Escenario 1.txt"
distancia_esc1 = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
rssi_esc1 = np.array([-47.90, -52.43, -61.22, -66.69, -63.00, -63.15, -74.71, -73.03, -77.15, -79.18,
                      -79.49, -77.86, -82.29, -83.42, -84.42, -84.87, -84.40, -85.99, -82.78])
desviacion_esc1 = np.array([2.64, 2.26, 5.60, 3.33, 5.03, 3.21, 3.90, 2.23, 2.35, 1.37,
                            2.51, 1.94, 3.00, 2.34, 1.82, 2.23, 1.67, 1.58, 2.43])

# Filtrar solo las muestras 2 (índices pares)
distancia_muestras2 = distancia_esc1[::2]
rssi_muestras2 = rssi_esc1[::2]
desviacion_muestras2 = desviacion_esc1[::2]

# Cálculo del error estándar para las muestras 2
error_estandar_muestras2 = desviacion_muestras2 / np.sqrt(len(rssi_muestras2))

# Crear figura y graficar solo las muestras 2
plt.figure(figsize=(10, 5))
plt.errorbar(distancia_muestras2, rssi_muestras2, yerr=error_estandar_muestras2, fmt='ro', capsize=5, label="Error estándar")
plt.errorbar(distancia_muestras2, rssi_muestras2, yerr=desviacion_muestras2, fmt='r-', capsize=5, label="Desviación estándar")

# Agregar valores de la desviación estándar debajo de la línea de desviación
for i in range(len(distancia_muestras2)):
    plt.text(distancia_muestras2[i], rssi_muestras2[i] - desviacion_muestras2[i] - 2,  
             f"{desviacion_muestras2[i]:.2f}", fontsize=9, ha='center', color='red')

# Etiquetas y leyenda
plt.xlabel("Distancia (m)", fontsize=12, fontweight='bold')
plt.ylabel("RSSI (dBm)", fontsize=12, fontweight='bold')
plt.title("Medidas Escenario 2", fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True)

# Mostrar la gráfica
plt.show()
