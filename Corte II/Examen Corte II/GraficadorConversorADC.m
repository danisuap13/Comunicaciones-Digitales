% Parámetros de la señal
A = 1;
B = 0.5;
C = 1.2;
f = 1000;             % Frecuencia fundamental: 1 kHz
DC = 2.5;
fs = 5000;            % Frecuencia de muestreo (1/200 µs)
Ts = 1/fs;            % Periodo de muestreo
N_bits = 8;
Vmax = 5;             % Rango máximo del ADC
Vmin = 0;             % Rango mínimo del ADC
levels = 2^N_bits;
deltaV = (Vmax - Vmin) / levels;

% Tiempo de simulación: 2 ms (dos periodos)
t_cont = 0:1e-6:2e-3;     % Tiempo continuo para la señal original
t_samp = 0:Ts:2e-3;       % Tiempo discreto para la señal muestreada

% Señal continua
V_cont = A*sin(2*pi*f*t_cont) + B*sin(2*pi*2*f*t_cont) + C*sin(2*pi*3*f*t_cont) + DC;

% Señal muestreada
V_samp = A*sin(2*pi*f*t_samp) + B*sin(2*pi*2*f*t_samp) + C*sin(2*pi*3*f*t_samp) + DC;

% Cuantización SAR
V_clipped = min(max(V_samp, Vmin), Vmax);             % Limitar al rango del ADC
quantized_levels = floor((V_clipped - Vmin) / deltaV);
V_quantized = quantized_levels * deltaV + deltaV/2;    % Centro del nivel
binary_values = dec2bin(quantized_levels, N_bits);

% Mostrar resultados
disp('Tiempo (us) | Voltaje (V) | Nivel | Binario')
for i = 1:length(t_samp)
    fprintf('%10.0f | %11.4f | %5d | %s\n', t_samp(i)*1e6, V_samp(i), quantized_levels(i), binary_values(i,:));
end

% Gráfica
figure;
plot(t_cont*1e3, V_cont, 'b', 'LineWidth', 1.5); hold on;
stem(t_samp*1e3, V_quantized, 'r', 'filled', 'LineWidth', 1.2);
xlabel('Tiempo (ms)');
ylabel('Voltaje (V)');
title('Señal original vs. señal cuantizada (2 ms)');
legend('Señal Original', 'Cuantizada (SAR 8 bits)');
grid on;
