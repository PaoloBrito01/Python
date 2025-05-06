import numpy as np
import random
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivada(x):
    s = sigmoid(x)
    return s * (1 - s)

EPOCAS = 1000
LIMIAR_DECISAO1 = 0.5
LIMIAR_DECISAO2 = 0.7
PESOS_INICIAIS = [random.uniform(0, 1), random.uniform(0, 1)]
TAXA_APRENDIZAGEM = 0.01

erros = []
pesos = []
gradientes = []

def treina(rede, entradas, saidas_corretas):
    for i in range(EPOCAS):
        entrada_bruta = np.dot(entradas, rede)
        saidas_IA = sigmoid(entrada_bruta)

        erros_neuronios = []
        for j in range(rede.shape[0]):
            erros_neuronio = 0.5 * np.mean((saidas_corretas[:, j] - saidas_IA[:, j]) ** 2)
            erros_neuronios.append(erros_neuronio)

        erro = np.mean(erros_neuronios)
        erro_bruto = (saidas_IA - saidas_corretas) * sigmoid_derivada(entrada_bruta)
        gradiente = np.dot(entradas.T, erro_bruto)
        erros.append(erro)
        pesos.append(rede.copy())
        gradientes.append(gradiente)
        print('Época:', i, ' Peso:', rede, 'Erro:', erro, 'Gradiente', gradiente)
        rede = rede - TAXA_APRENDIZAGEM * gradiente

    return saidas_IA

def testa(rede, entrada, limiar):
    entrada = np.array(entrada)
    entrada_bruta = np.dot(entrada, rede)
    
    saida = sigmoid(entrada_bruta)
    saida_neuronio1 = saida[0] > limiar[0]
    saida_neuronio2 = saida[1] > limiar[1]
    return saida, (saida_neuronio1, saida_neuronio2)

rede = np.random.uniform(0, 1, size=(2, 2))

entradas = np.array([
    [0.3, 0.1], [0.88, 0.5], [0.2, 0.3], [0.18, 0.2], [0.99, 0.4],
    [0.83, 0.6], [0.33, 0.2], [0.4, 0.3], [0.20, 0.1], [0.33, 0.2],
    [0.82, 0.4]
])

saidas = np.array([
    [0, 0], [1, 1], [0, 0], [0, 0], [1, 1],
    [1, 1], [0, 0], [0, 0], [0, 0], [0, 0],
    [1, 1]
])

saida_IA = treina(rede, entradas, saidas)

testes = [
    [0.15, 0.1], [0.001, 0.05], [0.1015, 0.2], [0.95, 0.4], [0.314, 0.2],
    [0.43, 0.3], [0.81, 0.6], [0.232, 0.1], [0.24, 0.2], [0.1, 0.05], [0.90, 0.4]
]

for teste in testes:
    saida_continua, (saida_neuronio1, saida_neuronio2) = testa(rede, teste, [LIMIAR_DECISAO1, LIMIAR_DECISAO2])
    print(f'Saída contínua: {saida_continua}')
    print(f'Neurônio 1: O número {teste} é maior que {LIMIAR_DECISAO1}: {saida_neuronio1}')
    print(f'Neurônio 2: O número {teste} é maior que {LIMIAR_DECISAO2}: {saida_neuronio2}')

fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
ax1.scatter(entradas[:, 0], saidas[:, 0])
ax1.scatter(entradas[:, 0], saida_IA[:, 0], marker='x', color='red')
ax1.scatter(entradas[:, 1], saidas[:, 1])
ax1.scatter(entradas[:, 1], saida_IA[:, 1], marker='x', color='green')
ax1.axhline(y=LIMIAR_DECISAO1, color='black', linestyle='--')
ax1.axhline(y=LIMIAR_DECISAO2, color='blue', linestyle='--')
ax1.legend(['Saída correta 1', 'Saída predita 1', 'Saída correta 2', 'Saída predita 2'])
ax1.set_xlabel('Entradas')
ax1.set_ylabel('Saídas')
ax1.set_title('Dados de treinamento')

ax2.plot(erros)
ax2.set_xlabel('Épocas')
ax2.set_ylabel('Erro')
ax2.set_title('Função de Perda (Erro)')

gradientes_array = np.array(gradientes)
for i in range(2):
    for j in range(2):
        ax3.plot(gradientes_array[:, i, j], label=f'g[{i},{j}]')

ax3.set_xlabel('Épocas')
ax3.set_ylabel('Gradiente')
ax3.set_title('Gradiente durante o treinamento')
ax3.legend()
plt.tight_layout()
plt.show()
