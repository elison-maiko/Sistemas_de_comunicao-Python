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

#------------------------------------------------------------------------

valores = np.load('valores_8B6T.npy')

def indices_hexa():
    mapeamento = [['00', [0, 0, 0, 0, 0, 0]] for _ in range(256)]  # cria uma matriz do tipo [HEXADECIMAL, Sequencia de Valores de Tensão ]

    #preencher a 1 coluna do mapeamento como sendo os valores em hexadecimal
    for i in range(0, 255):                     #Nao vai até 255 pois o arquivo importado n tem o tamanho certo
        aux = format(i, '02X')
        mapeamento[i][0] = aux                  #Adiciona o hexadeximal 
        mapeamento[i][1] = valores[i].tolist()  #Adiciona os niveis de tensão correspondentes
                                                #Se retirar .tolist apresenta insconsistencia de formato
    
    #Correções de erros na lista importada: (adicionar a medida que descobrir)
    mapeamento[255][0] = 'FF'
    mapeamento[255][1] = [0,0,1,-1,0,1]

#   Print para verificação da matriz de mapeamento
#   for j in range (0, len(valores)+1):
#       print(mapeamento[j][0],mapeamento[j][1], end= '\n')

    return mapeamento


map_8B6T = indices_hexa()
#Definida a matriz de conversao, partimos para o tratamento do sinal recebido

def cod_8B6T(sinal):
    #Receber string com os bits
    #Separar de 8 em 8 bits
    #Converter de string pra binário para:
    #Converter de Binário pra HEXA (6bits)
    #Usar matriz de mapeamento
    #Relacionar mapping com hexa


    for i in range (0, len(sinal), 8):
        strinig_bin = sinal[i:i+8]              #Separa de 8 em 8            
        bin = int(strinig_bin,2)                #Converete p BIN
        hexa = format(bin, 'X')                 #Converte p HEXA
    
    i = 0 #Sim, quero reutilizar o i
    for i in range(0, 256):                     #Varre o mapeamento até econtrar o HEXA
        if hexa == map_8B6T[i][0]:              #Se encontar
            return map_8B6T[i][1]               #Retorna a lista de valores de tensão
    print("Não econtrado!!!")
    return [0,0,0,0,0,0]                        #Retorna sinais nulos de tensão pra indicar erro

ex_prof = '01010011'
print(cod_8B6T(ex_prof))


