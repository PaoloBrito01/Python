'''
    - Entrada: Pedir para o usuario digitar os vértices; Perguntar quais são os vizinhos de cada vértice
    - Meios:
            Junção dos vértices e arestas em uma só coisa para poder visualizar
    - Funções com cada proprieadade de grafos
    - Função para mostrar grafos prontos
    - Pelo menos 11 Funções:
    
    GrauMax, GrauMin, NumeroCromatico, Raio, Diametro, Perimetro, Árvore Geradora Mín
    Se o Grafo é Conexo, Aciclico, Completo, Euleriano, ...
    
    
    - Entrada com arquivo CSV
    - Permitir usuário salvar grafo que ele fez em um arquivo CSV
    - Mostrar grafo apartir do arquivo CSV

'''

import networkx as nx 
import matplotlib.pyplot as plt
import pandas as pd
import os
from itertools import count, cycle

#================================================================
# Função para criar grafo
#================================================================

def criarGrafo():
    # Pergunta para o usuário quais são os vértices do grafo
    vertices = list(input("Entre com a sequência de vértices (exemplo: abcd): "))
    print('Muito obrigado, os vértices ficaram assim:', vertices)
    # Para cada vértice, pergunta quais são seus vizinhos
    arestas = []
    for vertice in vertices:
        vizinhos = list(input("Quais os vizinhos de " + vertice + " ? "))
        for vizinho in vizinhos:
            aresta = (vertice, vizinho)
            arestas.append(aresta)

    print('Muito obrigado, as arestas ficaram assim:', arestas)
    # Apenas junta vértices e arestas em uma única estrutura de dados
    grafo = (vertices, arestas)
    print('Grafo com tudo junto:    ', grafo)
    print('Vértices do grafo:', grafo[0])
    print('Arestas do grafo:', grafo[1])
    # Cria um grafo vazio
   
    
    G = nx.DiGraph()
    G.add_nodes_from(grafo[0])
    G.add_edges_from(grafo[1])

    # Mostrando todas propriedades dos grafos
    print('O total de arestas é ',totalArestas(grafo))
    print('O grau máximo do grafo é ',grauMaximo(grafo))
    print('O grau mínimo do grafo é ',grauMinimo(grafo))
    print('O grafo é completo:', completo(grafo))
    GrafoConexo(grafo)
    GrafoAciclico(grafo)
    GrafoEuleriano(grafo)
    GrafoBipartido(grafo)
    numeroCromatico(grafo)
    diametro(grafo)
    perimetro(grafo)
    
    # Obtém a coloração dos vértices
    chromatic_number = colorirVertices(grafo)
    pos = nx.spring_layout(G, seed=42)
    node_colors = [chromatic_number[node] for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_size=500, node_color=node_colors, font_size=10, font_color='black', arrows=True)
    # Mostra o número cromático na legenda
    plt.text(0.5, 1.05, f"Número Cromático: {max(chromatic_number.values()) + 1}", transform=plt.gca().transAxes, fontsize=12)
    
    plt.show()
    
    
    
    
    #função para salvar o grafo
    salvar = input("Deseja salvar o grafo em um arquivo CSV? (S/N): ").strip().lower()
    if salvar == 's':
        pasta_salvos = './CSV/salvos/'
        if not os.path.exists(pasta_salvos):
            os.makedirs(pasta_salvos)
        nome_arquivo = input("Digite o nome do arquivo (sem extensão): ").strip()
        arquivo_csv = os.path.join(pasta_salvos, f"{nome_arquivo}.csv")
        nx.write_edgelist(G, arquivo_csv, delimiter=',', data=False)
        print(f"Grafo salvo em {arquivo_csv}")

#================================================================
# Função para mostrar grafos prontos em arquivos CSV
#================================================================

# Função para permitir usuario colocar seus grafos dentro de uma pasta e mostrar
def carregarGrafoSalvo():
    # Definição do diretório 
    pasta_salvos = './CSV/salvos/'
    arquivos = os.listdir(pasta_salvos)
    # Mostrando e enumerando arquivos presentes na pasta
    print("Arquivos CSV na pasta:")
    for i, arquivo in enumerate(arquivos):
        print(f"{i + 1}: {arquivo}")
    # Utilizando método try para o user poder escolher qual arquivo abrir
    try:
        escolha = int(input("Selecione o número do arquivo CSV para abrir: ")) - 1
        arquivo_selecionado = arquivos[escolha]
        arquivo_path = os.path.join(pasta_salvos, arquivo_selecionado)

        df = pd.read_csv(arquivo_path, delimiter=',', names=['source', 'target'])
        G = nx.from_pandas_edgelist(df, source='source', target='target', create_using=nx.DiGraph())


        # Obtém a coloração dos vértices
        chromatic_number = nx.coloring.greedy_color(G, strategy="largest_first")

        pos = nx.spring_layout(G, seed=42)
        node_colors = [chromatic_number[node] for node in G.nodes()]
        nx.draw(G, pos, with_labels=True, node_size=500, node_color=node_colors, font_size=10, font_color='black', arrows=True)
        # Mostra o número cromático na legenda
        plt.text(0.5, 1.05, f"Número Cromático: {max(chromatic_number.values()) + 1}", transform=plt.gca().transAxes, fontsize=12)
        
        plt.show()
    
    
    except (ValueError, IndexError):
        print("Seleção inválida. Por favor, escolha um número válido.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

#================================================================
# Funções com propriedades dos grafos
#================================================================

def totalArestas(grafo):
    return len(grafo[1])

def grauMaximo(grafo):
    grau_maximo = 0
    # Laço para iterar sobre cada vértice
    for vertice in grafo[0]:
        # Contagem de vezes em que arestas estão presentes na lista de arestas
        grau = sum(1 for aresta in grafo[1] if vertice in aresta)
        # Condição para caso o grau seja maior que grau_max
        if grau > grau_maximo:
            grau_maximo = grau
    return grau_maximo

def grauMinimo(grafo):
    grau_minimo = float('inf')  # Inicializa com um valor infinito como ponto de partida
    for vertice in grafo[0]:
        # Conta o número de arestas incidentes ao vértice
        grau = sum(1 for aresta in grafo[1] if vertice in aresta)
        # Atualiza o grau mínimo, se o grau atual for menor
        if grau < grau_minimo:
            grau_minimo = grau
    return grau_minimo

# Caso o grau min e max sejam iguais o grafo é completo!
def completo(grafo):
    if grauMaximo(grafo) == grauMinimo(grafo):
        #print('Grafo é completo')
        return True
    else:
        #print('Grafo não é completo')
        return False
    
def GrafoAciclico(grafo):
    # Cria um grafo direcionado a partir do grafo dado
    G = nx.DiGraph()
    G.add_nodes_from(grafo[0])
    G.add_edges_from(grafo[1])

    # Verifica se o grafo direcionado é acíclico
    if nx.is_directed_acyclic_graph(G):
        print("O grafo é acíclico.")
    else:
        print("O grafo não é acíclico.")
        
def GrafoEuleriano(grafo):
    # Cria um grafo direcionado a partir do grafo dado
    G = nx.Graph()
    G.add_nodes_from(grafo[0])
    G.add_edges_from(grafo[1])

    # Verifica se o grafo é euleriano
    if nx.is_eulerian(G):
        print("O grafo é euleriano.")
    else:
        print("O grafo não é euleriano.")
        
def GrafoConexo(grafo):
    # Cria um grafo não direcionado a partir do grafo dado
    G = nx.Graph()
    G.add_nodes_from(grafo[0])
    G.add_edges_from(grafo[1])

    # Verifica se o grafo é conexo
    if nx.is_connected(G):
        print("O grafo é conexo.")
    else:
        print("O grafo não é conexo.")

def GrafoBipartido(grafo):
    # Cria um grafo a partir do grafo dado
    G = nx.Graph()
    G.add_nodes_from(grafo[0])
    G.add_edges_from(grafo[1])

    # Verifica se o grafo é bipartido
    if nx.is_bipartite(G):
        print("O grafo é bipartido.")
    else:
        print("O grafo não é bipartido.")
        
def numeroCromatico(grafo):
    G = nx.Graph()
    G.add_nodes_from(grafo[0])
    G.add_edges_from(grafo[1])
    chromatic_number = nx.coloring.greedy_color(G, strategy="largest_first")
    print("Número cromático do grafo:", max(chromatic_number.values()) + 1)

def diametro(grafo):
    G = nx.Graph()
    G.add_nodes_from(grafo[0])
    G.add_edges_from(grafo[1])
    diameter = nx.diameter(G)
    print("Diâmetro do grafo:", diameter)
    
def perimetro(grafo):
    G = nx.Graph()
    G.add_nodes_from(grafo[0])
    G.add_edges_from(grafo[1])
    eccentricities = nx.eccentricity(G)
    perimeter = sum(eccentricities.values())
    print("Perímetro do grafo:", perimeter)
    
def colorirVertices(grafo):
    G = nx.Graph()
    G.add_nodes_from(grafo[0])
    G.add_edges_from(grafo[1])
    chromatic_number = nx.coloring.greedy_color(G, strategy="largest_first")
    return chromatic_number

#================================================================
# Funções com propriedades de grafos já prontos
#================================================================

def gerar_grafo(vertices, arestas):
    G = nx.DiGraph()
    G.add_nodes_from(vertices)
    G.add_edges_from(arestas)
    nx.draw(G, with_labels=True, node_size=400)
    plt.show()
    
#================================================================
# Função para mostrar Grafos já prontos CSV
#================================================================

def mostrarGrafoPronto():
    pasta = './CSV/prontos'
    arquivos = os.listdir(pasta)
    # Imprime a lista de arquivos CSV
    print("Arquivos CSV na pasta:")
    for i, arquivo in enumerate(arquivos):
        print(f"{i + 1}: {arquivo}")

    try:
        # Pede para o usuário escolher um arquivo
        escolha = int(input("Selecione o número do arquivo CSV para abrir: ")) - 1
        arquivo_selecionado = arquivos[escolha]
        arquivo_path = os.path.join(pasta, arquivo_selecionado)
        # Fazendo leitura do arquivo CSV 
        df = pd.read_csv(arquivo_path, delimiter=',')
        G = nx.from_pandas_edgelist(df, source='source', target='target', create_using=nx.DiGraph())
        # Visualiza o grafo
        # Definição layout do grafo
        pos = nx.spring_layout(G, seed=42)  
        nx.draw(G, pos, with_labels=True, node_size=500, node_color='lightblue', font_size=10, font_color='black', arrows=True)
        plt.show()
    except (ValueError, IndexError):
        print("Seleção inválida. Por favor, escolha um número válido.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

#================================================================
# Menu principal do programa
#================================================================

def menu():
    while True:
        grafo = None
        print("----------------")
        print("1- Criar Grafo")
        print("2- Grafos Prontos Exemplos")
        print("3- Carregar Grafo Salvo")
        print("4- Sair")
        print("----------------")
        opcao = int(input("Digite uma opção:"))

        if opcao == 1:
            criarGrafo()
        elif opcao == 2:
            mostrarGrafoPronto()
        elif opcao == 3:
            carregarGrafoSalvo()
        elif opcao == 4:
            print("Saindo!")
            break
        else:
            print("Opção Inválida, tente novamente!")

if __name__ == "__main__":
    menu()

