import numpy as np
import random
import matplotlib.pyplot as plt

EPOCAS = 500
# LIMIAR PARA DOIS NEURONIOS
# Define o limiar para dar uma resposta "True" ou "False" a partir da saída do neurônio
LIMIAR_DECISAO1 = 0.5
LIMIAR_DECISAO2 = 0.7

# Adicionar outro peso ou seja receber mais um neuronio
PESOS_INICIAIS = [random.uniform(0, 1), random.uniform(0, 1)]
# Define a taxa de aprendizagem da rede
TAXA_APRENDIZAGEM = 0.01
# Armazena os erros durante o treinamento para plotar o gráfico
erros = []
# Armazena os pesos durante o treinamento para plotar o gráfico
pesos = []
# Armazena os gradientes durante o treinamento para plotar o gráfico
gradientes = []

# Função que treina a IA (aqui é onde ocorre o aprendizado)
# Rede: vetor com os pesos da rede
# Entradas: vetor com os dados de entrada
# Saidas_corretas: vetor com as saídas corretas para cada entrada
def treina(rede, entradas, saidas_corretas):
    # Loop de treinamento
    for i in range(EPOCAS):
        # Calcula a saída do neurônio para cada entrada
        #================================================================
        # Aqui é onde ocorre o calculo de produto escalar entre a matriz "entradas" e a matriz "redes"
        # Ou seja multiplicando cada entrada pelos pesos correspondentes e somando-os.
        # Esse seria um exemplo de função limiar de ativação bruta!!!
        # Logo após na linha 97 a decisão de ativação ou desativação dos neurônios é feita aplicando um limiar.
        #================================================================
        saidas_IA = np.dot(entradas, rede)
        
        # Calcula o erro quadrático médio para dois neurônios!
        erros_neuronios = []
        # O loop abaixo iteira sobre cada neuronio 
        for j in range(rede.shape[1]):  # Assumindo que a segunda dimensão de 'rede' corresponde ao número de neurônios
            # Aqui é onde ocorre o calculo de eror quadrático médio para cada neuronio
            erros_neuronio = 0.5 * np.mean((saidas_corretas[:, j] - saidas_IA[:, j]) ** 2)
            erros_neuronios.append(erros_neuronio)

        # Agora você pode calcular o erro médio para todos os neurônios
        erro = np.mean(erros_neuronios)
        # Calcula o gradiente global da função de perda
        gradiente = np.sum((saidas_corretas - saidas_IA) * -entradas, axis=0)

        # Armazena os valores para plotar o gráfico
        erros.append(erro)
        pesos.append(rede.copy())  # Certifique-se de copiar os pesos para evitar referências
        gradientes.append(gradiente)
        # Imprime informações do treinamento
        print('Época:', i, ' Peso:', rede, 'Erro:', erro, 'Gradiente', gradiente)
        # Atualiza os pesos usando a descida de gradiente
        rede = rede - TAXA_APRENDIZAGEM * gradiente

    # Retorna a saída final da rede após o treinamento
    return saidas_IA

# Função que usa a IA já treinada
# Mudando return da função para 2 neuronios! Ou seja neuronio1 e neuronio2
def testa(rede, entrada, limiar):

    # Calcule a saída da rede para uma única entrada
    saida = np.dot(entrada, rede)
    # Retorna a saída e um valor True ou False a partir do limiar de decisão
    return saida, saida > limiar

# Cria a rede com dois neurônios artificiais com uma única entrada cada
rede = np.random.uniform(0, 1, size=(2, 2))
#================================================================
# Define os dados de treinamento para ensinar a rede a identificar números maiores que 0.8)
# Saidas dadas poi se trata de um treinamento superviosanado
#================================================================

# Dentro dos colchetes(listas, vetores) adicionar mais um valor, pois agora há 2 neurônios!
entradas = np.array([[0.3, 0.1], [0.88, 0.5], [0.2, 0.3], [0.18, 0.2], [0.99, 0.4], [0.83, 0.6], [0.33, 0.2], [0.4, 0.3], [0.20, 0.1], [0.33, 0.2], [0.82, 0.4]])
saidas = np.array([[0, 0], [1, 1], [0, 0], [0, 0], [1, 1], [1, 1], [0, 0], [0, 0], [0, 0], [0, 0], [1, 1]])

# Treina a rede
# Agora são dois neurônios, então precisamos de duas saídas
saida_IA = treina(rede, entradas, saidas)

# Cria um conjunto de teste com valores que não estavam no conjunto de treinamento
# Conjunto de testes com valores diferentes para avaliar se a rede está generalizando bem

# Adicionando valores adicionais pois há dois neurônios agora!
testes = [[0.15, 0.1], [0.001, 0.05], [0.1015, 0.2], [0.95, 0.4], [0.314, 0.2], [0.43, 0.3], [0.81, 0.6], [0.232, 0.1], [0.24, 0.2], [0.1, 0.05], [0.90, 0.4]]

# Imprime a saída do neurônio para os dados de teste
# Agora são dois neurônios, então adicionar mais uma saída do neurônio 1 e neurônio 2
for teste in testes:
    # =================================================================
    # A decisão de ativação ou desativação dos neurônios é feita aplicando um limiar.
    # Isso é feito quando você verifica se a ativação bruta é maior do que o limiar de decisão
    # =================================================================
    saida_continua = testa(rede, teste, LIMIAR_DECISAO1)
    # Determina se cada neurônio será ativado ou desativado com base na ativação bruta correspondente.
    saida_neuronio1 = saida_continua[0] > LIMIAR_DECISAO1
    saida_neuronio2 = saida_continua[1] > LIMIAR_DECISAO2
    print(f'Saída contínua: {saida_continua}')
    print(f'Neurônio 1: O número {teste} é maior que {LIMIAR_DECISAO1}: {saida_neuronio1}')
    print(f'Neurônio 2: O número {teste} é maior que {LIMIAR_DECISAO2}: {saida_neuronio2}')

# Cria 3 subplots lado a lado para mostrar os gráficos
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))

# O primeiro gráfico mostra os valores anotados do conjunto de treinamento (ground truth)
# mostrados com quadrados azuis
# e os valores preditos mostrados com x vermelhos
ax1.scatter(entradas[:, 0], saidas[:, 0])
ax1.scatter(entradas[:, 0], saida_IA[:, 0], marker='x', color='red')
ax1.scatter(entradas[:, 1], saidas[:, 1])
ax1.scatter(entradas[:, 1], saida_IA[:, 1], marker='x', color='green')
# Desenha uma linha horizontal no limiar de decisão
ax1.axhline(y=LIMIAR_DECISAO1, color='black', linestyle='--')
ax1.axhline(y=LIMIAR_DECISAO2, color='blue', linestyle='--')
ax1.legend(['Saída correta 1', 'Saída predita 1', 'Saída correta 2', 'Saída predita 2'])
ax1.set_xlabel('Entradas')
ax1.set_ylabel('Saídas')
ax1.set_title('Dados de treinamento')
# O segundo mostra a função de perda em relação aos pesos
ax2.plot(erros)
ax2.set_xlabel('Épocas')
ax2.set_ylabel('Erro')
ax2.set_title('Função de Perda (Erro)')
# O terceiro mostra o gradiente em relação às épocas
ax3.plot(gradientes)
ax3.set_xlabel('Épocas')
ax3.set_ylabel('Gradiente')
ax3.set_title('Gradiente durante o treinamento')

plt.tight_layout()
plt.show()


'''
É criado uma rede neural com dois neurônios na camada de saída.

Durante o treinamento, a rede é ajustada para aprender a mapear as:

entradas (pares de valores) para as saídas corretas (duas saídas por par de valores).

Após o treinamento, o código faz previsões para uma série de novos pares de valores de entrada e verifica se a saída de cada neurônio 
é maior ou menor que os limiares de decisão definidos.

A saída do neurônio 1 é comparada com o limiar de decisão 0.5, e a saída do neurônio 2 é comparada com o limiar de decisão 0.7.

Dependendo se a saída de cada neurônio é maior ou menor que seu respectivo limiar, uma decisão é tomada para cada neurônio,
resultando em uma classificação binária (True ou False) para cada neurônio.
'''