# Codigo criado para simular a codificação de sinais de informação por meio de protocolos
# Principio de funcionamento:
#   O Usuário deve inserir 4 caracteres que devem ser codificados em 32bits pela ASCII
#   Em seguida a seguencia de bits deve será transmitida segundo os protocolos:
#   2B1Q
#   8B6T
#   4DPAM5
#   MLT3

import numpy as np
import matplotlib.pyplot as plt

#leitura
dados = ""
while (len(dados) != 3):
    dados = input("Insira 4 caracteres:")

print(dados)





