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
leitura = "dddd"
while (len(leitura) != 4):
    leitura = input("Insira 4 caracteres:")

#ASCII
def conv_ASCII(sinal):
    dados = []
    for i in sinal:
        bin = format(ord(i), '08b')  
        print(f"Char: {i} --> {ord(i)} --> {bin}")  
        dados.append(bin)
    dados = ''.join(dados) #usar como int()?
    return dados

#print (dados, end = "\n\n")

# Tratamento de dados:
# Tratar como string, pra facilitar os indices do 
#---------------------------------------------------------------------
ex_prof = '11001100'
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

#print (cod_2BQ1(ex_prof))
#------------------------------------------------------------------------
def cod_8B6T(sinal):
    #Receber string com os bits
    #Separar de 8 em 8 bits
    #Converter de string pra binário para:
    #Converter de Binário pra HEXA (6bits)
    #Converter de HEXA p string para tratar os dados
    #Relacionar mapping com hexa

    #Mapeando segundo a Tabela FORUZAN APENDICE D
    mapping = {
        '00': [-1,1,0,0,-1,1], '01': [0,-1,1,-1,1,0], '02': [0,-1,1,0,-1,1], '03': [0,-1,1,1,0 ,-1], '04': [-1,1,0,1,0,-1], '05': [1,0,-1,-1,1,0]
    }

    for i in range (0, len(sinal), 8):
        strinig_bin = sinal[i:i+8]              #Separa de 8 em 8            
        bin = int(strinig_bin,2)                #Converete p BIN
        hexa = format(bin, 'X')                 #Converte p HEXA
              

    return bin, hexa

print(cod_8B6T(ex_prof))


