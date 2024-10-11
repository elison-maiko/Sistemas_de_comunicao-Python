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

print (dados, end = "\n\n")

# Tratamento de dados:
# Tratar como string, pra facilitar os indices do 
#---------------------------------------------------------------------
ex_prof = '0011011001'
def cod_2BQ1 (sinal):
    mapping =  {
        '00': 1,
        '01': 3,
        '10': -1,
        '11': -3
    }
    cod = []
    nivel_anterior = 1
    for i in range(0, len(sinal), 2):       #Ir pegando duplas de bits
        dupla = mapping[sinal[i:i+2]]       #converte pra inteiro, de 2 em 2 da string sinal
        if nivel_anterior > 0:              #condição pra invesões
            cod.append(dupla)               #adiciona o inteiro a string de codificação
            nivel_anterior = dupla          #Atualiza o nivel para verificação no proximo loop
        else :
            cod.append(-dupla)
            nivel_anterior = -dupla
    return cod

print (cod_2BQ1(ex_prof))


