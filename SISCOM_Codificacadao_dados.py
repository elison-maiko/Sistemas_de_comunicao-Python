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
    sinais_tensao = []
    nivel_anterior = 1
    for i in range(0, len(sinal), 2):       #Ir pegando duplas de bits
        dupla = mapping[sinal[i:i+2]]       #converte pra inteiro, de 2 em 2 da string sinal
        if nivel_anterior > 0:              #condição pra invesões
            sinais_tensao.append(dupla)               #adiciona o inteiro a string de codificação
            nivel_anterior = dupla          #Atualiza o nivel para verificação no proximo loop
        else :
            sinais_tensao.append(-dupla)
            nivel_anterior = -dupla
    return sinais_tensao

def plot_2BQ1(sinal):
    # Definindo o eixo do tempo
    tempo = np.arange(len(sinal))  # Eixo do tempo
    plt.figure(figsize=(10, 6))
    plt.step(tempo, sinal, where='post', color='magenta')  # Gráfico em escada
    plt.title('Codificação 2BQ1')
    plt.xlabel('Tempo')
    plt.ylabel('Tensão')
    plt.ylim(-4, 4)             # Define os limites do eixo y
    plt.yticks([-3, -1, 1, 3])  # Define os ticks do eixo y
    plt.xticks([])              # Remove os índices do eixo X
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')  # Linha no eixo x

    for x in range(0, len(sinal), 1):
        plt.axvline(x=x, color='gray', linestyle='--', linewidth=0.5)  # Linha vertical

    plt.xlim(0, len(sinal)+1)  
#-------------------------------------------------------------------------------

def analise_peso(tensoes):                  #Definição da função para inversão
    #Utilização: Se o peso do sinal 6T for positivo e o seu anterior também, o atual é invertido para não gerar DC
    sum = 0
    for i in range(0,len(tensoes)):
        sum += tensoes[i]
    if sum > 0:                             #Assuminque que os pesos são apenas 1,0 e -1    
        return 1
    if sum == 0:
        return 0
    else:
        return -1
       
valores = np.load('valores_8B6T.npy')

def indices_hexa():
    mapeamento = [['00', [0, 0, 0, 0, 0, 0],0] for _ in range(256)]  
    # cria uma matriz do tipo [HEXADECIMAL, Sequencia de Valores de Tensão, peso]

    #preencher a 1 coluna do mapeamento como sendo os valores em hexadecimal
    for i in range(0, 255):                     #Nao vai até 255 pois o arquivo importado n tem o tamanho certo
        aux = format(i, '02X')
        mapeamento[i][0] = aux                  #Adiciona o hexadeximal 
        mapeamento[i][1] = valores[i].tolist()  #Adiciona os niveis de tensão correspondentes
        mapeamento[i][2] = analise_peso(mapeamento[i][1]) #Se retirar .tolist apresenta insconsistencia de formato
    
    #Correções de erros na lista importada: (adicionar a medida que descobrir)
    mapeamento[255][0] = 'FF'
    mapeamento[255][1] = [0,0,1,-1,0,1]
    mapeamento[255][2] = 1

#   Print para verificação da matriz de mapeamento
#    for j in range (0, len(valores)+1):
#       print(mapeamento[j][0],mapeamento[j][1],mapeamento[j][2],  end= '\n')

    return mapeamento

map_8B6T = indices_hexa()
#Definida a matriz de conversao e pesos, partimos para o tratamento do sinal recebido:
     
def cod_8B6T(sinal):
    #Receber string com os bits
    #Separar de 8 em 8 bits
    #Converter de string pra binário para:
    #Converter de Binário pra HEXA (6bits)
    #Usar matriz de mapeamento
    #Relacionar mapping com hexa
    sinais_tensao = []                          #inicializa a lista de sinais para retorno
    peso_anterior = 0                           #Inicializa com peso inicial igual a 0

    for i in range (0, len(sinal), 8):
        strinig_bin = sinal[i:i+8]              #Separa de 8 em 8            
        bin = int(strinig_bin,2)                #Converete p BIN
        hexa = format(bin, 'X')                 #Converte p HEXA

    
        for i in range(0, 256):                          #Varre o mapeamento até econtrar o HEXA
            if hexa == map_8B6T[i][0]:                   #Se encontar
                peso_atual = map_8B6T[i][2]              #Armazena o peso do sinal atual
                if (peso_atual == 0) or (peso_atual != peso_anterior):         #Se o peso atual for 0 ou diferente do anterior, não inverte
                    sinais_tensao.extend(map_8B6T[i][1])                       #
                elif (peso_atual == peso_anterior):                            #Se o atual e o anterior tivere o mesmo peso: 
                    sinais_tensao.extend([-valor for valor in map_8B6T[i][1]]) #Adiciona um a um os valores invertidos
                peso_anterior = peso_atual
                break
        else:
            print("Não econtrado!!!")
            sinais_tensao.extend([0,0,0,0,0,0])      #Retorna sinais nulos de tensão pra indicar erro
    
    return sinais_tensao

def plot_8b6T(sinal):
    # Definindo o eixo do tempo
    tempo = np.arange(len(sinal))  # Eixo do tempo
    plt.figure(figsize=(10, 6))
    plt.step(tempo, sinal, where='post', color='magenta')  # Gráfico em escada
    plt.title('Codificação 8BT6')
    plt.xlabel('Tempo')
    plt.ylabel('Tensão')
    plt.ylim(-2, 2)         # Define os limites do eixo y
    plt.yticks([-1, 0, 1])  # Define os ticks do eixo y
    plt.xticks([])          # Remove os índices do eixo X
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')  # Linha no eixo x

    # Traçar linhas verticais a cada 6 valores de x
    for x in range(0, len(sinal), 6):
        plt.axvline(x=x, color='gray', linestyle='--', linewidth=0.5)  # Linha vertical

    # Garantir que o eixo X vai até o final
    plt.xlim(0, len(sinal))  # Para alinhar à borda direita

#-------------------------------------------------------------------------------------

def cod_4DPAM5(sinal):
    #4D: Dados são enviados por meio de 4 canais, teremos 4 plots
    #5 niveis de tensão: 2,1,0,-1,-2 (nivel 0 para detecção de erros)
    chave = {
        '00': -2,
        '01': -1,
        '10': 1,
        '11': 2
    }
    fio1 = []
    fio2 = []
    fio3 = []
    fio4 = []
    sinais_tensao = []
    for i in range(0, len(sinal), 2):       #Ir pegando duplas de bits
        dupla =chave[sinal[i:i+2]] 
        sinais_tensao.append(dupla)        #Gera a lista de sinais de tensão completa
    
    #separando em 4 fios:
    for j in range(0, len(sinais_tensao), 4):
        fio1.extend([sinais_tensao[j],0,0,0])
        fio2.extend([0,sinais_tensao[j+1],0,0])
        fio3.extend([0,0,sinais_tensao[j+2],0])
        fio4.extend([0,0,0,sinais_tensao[j+3]])

    return sinais_tensao, fio1,fio2,fio3,fio4

def plot_4DPAM5(sinal, fio1,fio2,fio3,fio4):
    # PLOT GERAL
    tempo = np.arange(len(sinal))  # Eixo do tempo
    plt.figure(figsize=(10, 6))
    plt.step(tempo, sinal, where='post', color='magenta')  # Gráfico em escada
    plt.title('Codificação 4DPAM5 - GERAL')
    plt.xlabel('Tempo')
    plt.ylabel('Tensão')
    plt.ylim(-3, 3)         # Define os limites do eixo y
    plt.yticks([-2, -1, 1, 2])  # Define os ticks do eixo y
    plt.xticks([])          # Remove os índices do eixo X
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')  # Linha no eixo x

    for x in range(0, len(sinal), 4):
        plt.axvline(x=x, color='gray', linestyle='--', linewidth=0.5)  # Linha vertical

    plt.xlim(0, len(sinal)+1)

    #Plot dos 4 fios:
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))  # Criar subplots
    plt.suptitle('Codificação 4DPAM5 - FIOS')
    axs = axs.flatten()  # Para facilitar o acesso aos eixos

    # Plotar cada sinal em um subplot
    indices = [fio1, fio2, fio3, fio4]

    for i in range(4):
        axs[i].step(tempo, indices[i], where='post', color='blue')
        axs[i].set_ylim(-3, 3)  # Limites do eixo y
        axs[i].axhline(0, color='black', lw=0.5)  # Linha horizontal no eixo y = 0
        axs[i].set_title(f'FIO {i+1}')
        axs[i].set_xlabel('Tempo')
        axs[i].set_ylabel('Tensão')
        axs[i].set_yticks([-2, -1, 1, 2])
        axs[i].set_xlim(left =0)
        axs[i].set_xticks([])  # Remove valores do eixo x
        
        # Adiciona linhas verticais ao eixo atual
        for x in range(0, len(indices[i]), 4):
            axs[i].axvline(x=x, color='gray', linestyle='--', linewidth=0.5)  # Linha vertical



    plt.tight_layout()  # Ajusta o layout
      
#----------------------------------------------------------------------

def transicao_nivel(atual, prox, lastlevel):
    # ---------- logica p o zero ----------------
    if (atual == 0) and (prox == 1):
        if lastlevel == 1: return -1
        else: return 1
    elif (atual == 0) and (prox == 0): return 0 
    # ---------- logica p 1 ---------------------
    elif (atual == 1):
        if (prox == 0): return 1 * lastlevel
        else: return 0

            
    return 

def cod_MLT3(sinal):
    # 3 níveis: 1V, 0, -1V
    # Tem 3 regras para transição de nível

    sinais_tensao = []                                                           #Inicia o sinal
    lastnivel = -1                                                               #Definicao do nivel anterior inicial, segundo o autor
    sinais_tensao.append(int(sinal[0]))                                          #Iteração inicial
    for i in range(1,len(sinal)):
        sin = transicao_nivel(abs(sinais_tensao[i-1]), int(sinal[i]), lastnivel)
        sinais_tensao.append(sin)
        if sin != 0: 
            lastnivel = sin                                                      # Atualiza o último nível para o próximo ciclo
    return sinais_tensao
    
def plot_MLT3(sinal):
    # Definindo o eixo do tempo
    tempo = np.arange(len(sinal))  # Eixo do tempo
    plt.figure(figsize=(10, 6))
    plt.step(tempo, sinal, where='post', color='magenta')  # Gráfico em escada
    plt.title('Codificação MLT3')
    plt.xlabel('Tempo')
    plt.ylabel('Tensão')
    plt.ylim(-2, 2)         # Define os limites do eixo y
    plt.yticks([-1, 0, 1])  # Define os ticks do eixo y
    plt.xticks([])          # Remove os índices do eixo X
    plt.axhline(0, color='black', linewidth=0.5, linestyle='--')  # Linha no eixo x

    # Traçar linhas verticais a cada 6 valores de x
    for x in range(0, len(sinal), 1):
        plt.axvline(x=x, color='gray', linestyle='--', linewidth=0.5)  # Linha vertical

    # Garantir que o eixo X vai até o final
    plt.xlim(0, len(sinal))  # Para alinhar à borda direita
# ---------------------------------------------------------------------

#leitura
leitura = ""
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

signal = conv_ASCII(leitura)
print(signal, end = "\n\n")

#ex_prof = '000100010101001101010000'
plot_2BQ1(cod_2BQ1(signal))
plot_8b6T(cod_8B6T(signal))
result, f1,f2,f3,f4 = cod_4DPAM5(signal)
plot_4DPAM5(result,f1,f2,f3,f4)
#ex_prof2 = '01011011'
plot_MLT3(cod_MLT3(signal))
plt.show()

