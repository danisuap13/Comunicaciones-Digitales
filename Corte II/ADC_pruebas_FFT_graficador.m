% El siguiente código permite filtrar varios períodos de las muestras tomadas en el laboratorio  
% para graficar la señal en el dominio del tiempo y poder analizarla, además de graficar la FFT.  
% Se encuentra en un bucle, ya que graficará todas las muestras por frecuencia. Únicamente  
% hay que asegurarse de modificar el nombre de cada archivo según corresponda, por ejemplo:  
% 'muestras_300_64.txt' y que el archivo .m se encuentre en la misma carpeta.

% Definir los valores de N_FFT a procesar
n_fft_values = [64, 128, 256, 512, 1024];

% Pedir al usuario la frecuencia teórica de la señal
f_teorica = input('Ingrese la frecuencia teórica de la señal (Hz): ');

for i = 1:length(n_fft_values)
    n_fft = n_fft_values(i);

    % Construir nombres de archivos dinámicamente
    muestras_file = sprintf('muestras_300_%d.txt', n_fft);
    fft_file = sprintf('fft_300_%d.txt', n_fft);
    
    % Cargar datos de muestras
    data = readmatrix(muestras_file);
    tiempo = data(:,1);
    voltaje = data(:,2);
    
    % Determinar el período de la señal basado en la frecuencia teórica
    periodo_teorico = 1 / f_teorica;
    t_max = 5 * periodo_teorico; % Tiempo máximo para 5 ciclos
    idx = tiempo <= t_max; % Índices que cumplen la condición
    tiempo_corto = tiempo(idx);
    voltaje_corto = voltaje(idx);

    % Cargar datos de FFT
    fft_data = readmatrix(fft_file);
    frecuencia = fft_data(:,1);
    magnitud = fft_data(:,2);

    % --- GRAFICAR MUESTRAS EN EL TIEMPO ---
    figure;
    plot(tiempo_corto, voltaje_corto, '-b', 'LineWidth', 1.2); % Señal continua
    hold on;
    stem(tiempo_corto, voltaje_corto, 'r', 'MarkerSize', 4); % Muestras discretas
    hold off;
    xlabel('Tiempo (ms)');
    ylabel('Voltaje (V)');
    title(strrep(sprintf('Señal en el tiempo para N_FFT = %d, F_teórica = %.2f Hz', n_fft, f_teorica), '_', '\_'));
    grid on;
    saveas(gcf, sprintf('Muestras_NFFT_%d.png', n_fft));

    % --- GRAFICAR FFT CON ESCALA MEJORADA ---
    figure;
    stem(frecuencia, magnitud, 'bo', 'MarkerSize', 4, 'LineWidth', 1); % Añadir stem a la FFT
    hold on;
    plot(frecuencia, magnitud, '-r', 'LineWidth', 1.2); % FFT completa
    hold off;
    xlabel('Frecuencia (Hz)');
    ylabel('Magnitud (V)');
    title(strrep(sprintf('FFT para N_FFT = %d, F_teórica = %.2f Hz', n_fft, f_teorica), '_', '\_'));
    xlim([0, 2*f_teorica]); % Ajustar el límite de la gráfica para enfocarse en la fundamental
    grid on;
    saveas(gcf, sprintf('FFT_NFFT_%d.png', n_fft));

    pause(1);  % Pausa para visualizar antes de la siguiente iteración
end

disp("Gráficos generados y guardados.");
