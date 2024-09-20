import numpy as np
import matplotlib.pyplot as plt

# Larguras de banda em Hz
larguras_de_banda = [3e6, 10e6, 20e6]

# Valores de SNR em dB
valores_SNR_dB = np.array([5, 10, 15, 20, 25, 30, 35, 40, 45, 50])

# Convertendo SNR de dB para forma linear
valores_SNR_linear = 10**(valores_SNR_dB / 10)

# Calculando as capacidades do canal para diferentes larguras de banda
capacidades = {}
for largura in larguras_de_banda:
    capacidades[largura] = largura * np.log2(1 + valores_SNR_linear)

# Criando o gráfico
plt.figure(figsize=(10, 6))
for largura in larguras_de_banda:
    plt.plot(valores_SNR_dB, capacidades[largura] / 1e6, label=f'{largura / 1e6} MHz')

# Configurações do gráfico
plt.title('Capacidade do Canal vs SNR para Diferentes Larguras de Banda')
plt.xlabel('SNR (dB)')
plt.ylabel('Capacidade (Mbps)')
plt.grid(True)
plt.legend(title="Largura de Banda")
plt.show()
