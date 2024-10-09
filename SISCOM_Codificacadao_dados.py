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
leitura = "d"
while (len(leitura) != 4):
    leitura = input("Insira 4 caracteres:")

#ASCII
dados = []
for i in leitura:
    bin = format(ord(i), '08b')  
    print(f"Char: {i} --> {ord(i)} --> {bin}")  
    dados.append(bin)
dados = ''.join(dados) #usar como int()?
print(dados)

#tratamento de dados:





