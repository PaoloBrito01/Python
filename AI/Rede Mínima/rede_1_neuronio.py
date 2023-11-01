# Exemplo de uma rede neural artificial MÍNIMA
# Autor: Hemerson Pistori e VOCÊ AQUI !!!
# Implementa uma "rede" com um único neurônio, uma única entrada e
# uma única saída.

import numpy as np # Importa a biblioteca que contém funções matemáticas
import random # Importa a biblioteca que contém funções aleatórias
import matplotlib.pyplot as plt # Importa a biblioteca que contém funções para plotar gráficos

EPOCAS=100  # Define total de vezes que IA vai passar por todos os exemplo de treinamento
LIMIAR_DECISAO=0.5   # Define o limiar para dar uma resposta "True" ou "False" a partir da saída do neurônio
'''
LIMIAR DE DECISAO:
Se a saída do neurônio (que é o resultado do produto escalar entre a entrada e o peso do neurônio) for maior do que o 
limiar de decisão (LIMIAR_DECISAO), a saída discreta é definida como "True".
Caso contrário, se a saída for menor ou igual ao limiar de decisão, a saída discreta é definida como "False".
'''
PESO_INICIAL=[random.uniform(0, 1)]   # Valor inicial do único peso da rede, número aleatório entre 0 e 1
TAXA_APRENDIZAGEM=0.01  # Define a taxa de aprendizagem da rede

erros=[] ## Armazena os erros durante o treinamento para plotar o gráfico
pesos=[] ## Armazena os pesos durante o treinamento para plotar o gráfico
gradientes=[] ## Armazena os gradientes durante o treinamento para plotar o gráfico

# Função que treina a IA (aqui é onde ocorre o aprendizado) 
#
# Rede: vetor com os pesos da rede
# Entradas: vetor com os dados de entrada
# Saidas_corretas: vetor com as saídas corretas para cada entrada
def treina(rede, entradas, saidas_corretas):

    # Para cada época, calcula a saída do neurônio e atualiza os pesos
    for i in range(EPOCAS):

        # Calcula a saída do neurônio para cada entrada
        saidas_IA = np.dot(entradas,rede)

        # Calcula o erro quadrático médio (que é a função de perda - loss - escolhida)
        erro=0.5*np.sum((saidas_corretas - saidas_IA)**2)

        # Calcula o gradiente da função de perda
        gradiente=np.sum((saidas_corretas - saidas_IA)*-entradas)

        # Armazena os valores para plotar o gráfico
        erros.append(erro)
        pesos.append(rede)
        gradientes.append(gradiente)

        # Imprime os valores para acompanhar o treinamento
        print('Época:',i,' Peso:',rede,'Erro:',erro, 'Gradiente',gradiente)

        # Atualize os pesos do neurônio (aqui é a chave do aprendizado)
        # Usando a descida de gradiente
        rede = rede - TAXA_APRENDIZAGEM*gradiente*rede

    # Retorna a saída final da rede após o treinamento
    return saidas_IA

# Função que usa a IA já treinada
def testa(rede, entrada):

    # Calcule a saída da rede para uma única entrada
    saida=np.dot(entrada,rede)

    # Retorna a saída e um valor True ou False a partir do limiar de decisão
    return saida,np.dot(entrada,rede)>LIMIAR_DECISAO



# Cria a rede com um neurônio artificial com uma única entrada
# Por isso, tem apenas um peso
rede = np.array(PESO_INICIAL)   



# Define os dados de treinamento para ensinar a rede a identificar números maiores que 0.8) 
# Saidas dadas poi se trata de um treinamento superviosanado
entradas = np.array([[0.3],[0.88],[0.2],[0.18],[0.99],[0.83],[0.33],[0.4],[0.20],[0.33],[0.82]])
saidas = np.array(  [   0,     1,    0,     0,     1,     1,     0  ,  0  ,   0   ,  0   ,  1])



# Treina a rede 
saida_IA = treina(rede, entradas, saidas)



# Cria um conjunto de este com valores que não estavam no conjunto de treinamento
# Conjunto de testes com valores diferentes para avaliar se a rede está generalizando
testes=[[0.15],[0.001],[0.1015],[0.95],[0.314],[0.43],[0.81],[0.232],[0.24],[0.1],[0.90]]



# Imprima a saída do neurônio para os dados de teste
for teste in testes:
    saida_continua,saida_discreta=testa(rede, teste)
    print(f'O número {teste} é maior que 0.8: {saida_discreta} (saida contínua = {saida_continua})')




# Cria 3 subplots lado a lado para mostrar os gráficos
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12,4))


# O primeiro gráfico mostra os valores anotados do conjunto de treinamento (ground truth) 
# mostrados com quadrados azuis
# e os valores preditos mostrados com x vermelhos
ax1.scatter(entradas,saidas)
ax1.scatter(entradas,saida_IA,marker='x',color='red')
# Desenha uma linha horizontal no limiar de decisão
ax1.axhline(y=LIMIAR_DECISAO, color='black', linestyle='--')
ax1.legend(['Saída correta','Saída predita'])
ax1.set_xlabel('Entradas')
ax1.set_ylabel('Saídas')
ax1.set_title('Dados de treinamento')

# O segundo mostra a função de perde em relação aos pesos 
ax2.plot(pesos,erros)
ax2.scatter(pesos,erros,marker='x',color='red')
ax2.quiver(pesos,erros,pesos,gradientes,color='green')
ax2.set_xlabel('Pesos')
ax2.set_ylabel('Erros')
ax2.set_title('Função de Perda (ou Erro)')

# O terceiro mostra o erro em função das épocas
ax3.plot(erros)
ax3.set_xlabel('Épocas')
ax3.set_ylabel('Perda')
ax3.set_title('Histórico da aprendizagem')


plt.show()