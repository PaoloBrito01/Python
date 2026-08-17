# biblioteca para trabalhar com fila
from collections import deque
# biblioteca para exibir as métricas
import time

# Estado objetivo do 8-Puzzle (0 representa o espaço vazio)
# A meta é deixar os números de 1 a 8 em ordem e o 0 (vazio) no canto inferior direito.
GOAL = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)
METRICAS = {}
# exibir o tabuleixo no formato 3x3
# recebe uma tupla (estado) com 9 inteiros
def show(state: tuple) -> None:
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()  # linha em branco apenas para separar visualmente

# Mapear todas as possibilidades de movimentação
# up = subir linha -> '-3'
# down = descer linha -> '+3'
# left = mover a esquerda -> '-1'
# right = mover a direita -> '+1'
MOVES = {"up": -3, "down": 3, "left": -1, "right": 1}
#    c= 0  1  2
#r = 0 (1, 2, 3,
#r = 1  4, 5, 7,
#r = 2  8, 6, 0)
# responsável por retornar o index da posição '0'
def find_zero(state: tuple) -> int:
  return state.index(0)

# movimentações validas de acordo com a posição do '0'
def valid_moves(z: int) -> list:
  r, c = divmod(z, 3)  # r (row) - linha | c (column) - coluna
  moves = []
  if r > 0: moves.append("up")
  if r < 2: moves.append("down")
  if c > 0: moves.append("left")
  if c < 2: moves.append("right")
  return moves

# responsável por aplicar a movimentação
def apply_moves(state: tuple, move: str) -> tuple:
  # descobrir a posição do '0'
  z = find_zero(state)
  # novo 'z' = receber a nova posição
  nz = z + MOVES[move]
  # lista/tuple p/ modificar/trocar as posições
  s = list(state)
  # a troca das posições (0 para o nova posição)
  s[z], s[nz] = s[nz], s[z]
  return tuple(s)

# função de busca em LARGURA (bfs)
def bfs(start: tuple) -> list | None:
  # métricas de início
  start_time = time.time()   # mede início do algoritmo
  nodes_expanded = 0    # conta quantos estados foram expandidos
  frontier_max = 1      # maior tamanho já objservado da fila
  # fronteiras sempre populadas
  # opções possíveis
  frontier = deque([[start]])
  # gerencia a quantidade de visitados
  visited = {start}
  # enquanto houver fronteiras
  while frontier:
    # Retirar o caminho mais antigo (propriedades BFS)
    path = frontier.popleft()
    # último estado do caminho atual
    state = path[-1]

    # Métricas
    # adicinar um nó expandido
    nodes_expanded += 1
    # Verifica qual é o maior valor
    frontier_max = max(frontier_max, len(frontier))

    # Teste do nosso objetivo (GOAL)
    # se for igual, retorna o caminho (BFS)
    if state == GOAL:
      # exibição das métricas do processamento
      #tempo de processamento
      elapsed = time.time() - start_time
      # profundidade/qtde de passos até a solução
      depth = len(path) - 1
      print("[BFS] - Busca em largura - Métricas")
      print(f" - Profundidade(solução)={depth}")
      print(f" - Expandidos={nodes_expanded}")
      print(f" - Fronteira máxima={frontier_max}")
      print(f" - Tempo={elapsed:.8f}")
      METRICAS["BFS"] = {"profundidade": depth, "expandidos": nodes_expanded,
                         "fronteira_max": frontier_max, "tempo": elapsed}
      return path
    # encontrar a posição do valor '0'
    z = find_zero(state)
    # validar as movimentações possíveis de acordo com a posição '0'
    for m in valid_moves(z):
      # gera novo estado aplicando a movimentação
      new_state = apply_moves(state, m)
      # validar se ele não foi visitado
      if new_state not in visited:
        visited.add(new_state)
        # atualiza a fronteira/possibilidades
        # com base no último estado
        frontier.append(path + [new_state])

  # não encontrar nenhuma solução
  #tempo de processamento caso de errado (não encontrou solução)
  elapsed = time.time() - start
  print(f"[BFS] falhou: expanded={nodes_expanded}, frontier_max={frontier_max}, time={elapsed}")
  return None

# Main inicial
start = (1, 2, 3,
         0, 5, 6,
         4, 7, 8)

print("Estado inicial:")
show(start)

# Executa BFS para encontrar o caminho
solution = bfs(start)

# Verifica se encontrou solução (deve encontrar)
if solution is None:
    print("Nenhuma solução encontrada (improvável neste exemplo).")
else:
    # A quantidade de passos (bfs)
    steps = len(solution) - 1
    print(f"Solução encontrada em {steps} passo(s).")
    print("Reproduzindo o caminho (estado a estado):")
    for st in solution:
        show(st)

# busca por profundidade (DFS)
# - não tem conjunto de visitados
# - usa pilha (stack), seguindo a lógica LIFO (Last-in First-out)
# - para evitar ciclos, verificar se o novo estado já tem no caminho atual
def dfs(start: tuple) -> list | None:
    # Métricas de desempenho
    start_time = time.time() # marca o instante em que a busca começou
    nodes_expanded = 0       # conta quantos estados foram expandidos
    frontier_max = 1         # guarda o amio tamanho já atingido pela pilha

    # A pilha começa com um único estado
    stack = [[start]]
    # stack = [ [ start ] ]
    #           |_______|
    #            caminho
    #         |___________|
    #             pilha
    # stack = [ [A, B, D], [A, B, C]  ]
    #           |_______|  |_______|
    #            caminho     caminho
    #         |_______________________|
    #                   pilha

    # Loop principal da DFS
    # enquanto exisitir elementos na pilha
    while stack:
        # Atualiza o pico do tamanho da pilha
        # max(valor1, valor2) -> compara e retorna o maior valor entre os 2
        frontier_max = max(frontier_max, len(stack))

        # Remover o último caminho da pilha
        path = stack.pop()
        # path = [A, B, C]
        #         0  1  2
        # O estado atual é o último estado do caminho
        state = path[-1]
        # path[0] -> A
        # path[1] -> B
        # path[2] -> C
        # path[-1] = path[len(path) - 1] = path[3 - 1] = path[2]
        # path[-1] -> C

        # contamos uma expansão
        nodes_expanded += 1

        # Teste objetivo/final
        if state == GOAL:
            # tempo de processamento
            # time.time() -> busca a hora atual
            # start_time  -> momento em que iniciou a execução do código
            elapsed = time.time() - start_time
            # profundidade
            depth = len(path) - 1
            print("[DFS] - Busca em profundidade")
            print(f" - Profundidade(solução)={depth}")
            print(f" - Expandidos={nodes_expanded}")
            print(f" - Tempo={elapsed:.8f}")
            print(f" - Tamanho máximo pilha={frontier_max}")
            METRICAS["DFS"] = {"profundidade": depth, "expandidos": nodes_expanded,
                               "fronteira_max": frontier_max, "tempo": elapsed}
            return path

        # geração de vizinho
        # encontrar o zero do estado atual
        z = find_zero(state)

        # laço de acordo com as movimentações possíveis
        for m in valid_moves(z):
            # gerar um novo estado aplicando a movimentação 'm'
            ns = apply_moves(state, m)

            # controle de ciclo (sem usar o visited)
            # se já apareceu não vai empilhar
            if ns not in path:
                stack.append(path + [ns])

    # Se não encontrou solução
    elapsed = time.time() - start_time

    print("[DFS] - Busca em profundidade falhou")
    print(f" - Expandidos={nodes_expanded}")
    print(f" - Tempo={elapsed:.8f}")
    print(f" - Tamanho máximo pilha={frontier_max}")

    return None

# executando o DFS - busca em profundidade
solution_dfs = dfs(start)

if solution_dfs is None:
    print("DFS não encontrou solução")
else:
    steps = len(solution_dfs) - 1 # calcula a quantidade de passos
    print("Reproduzir o caminho (estado a estado):")
    for estado_profundidade in solution_dfs: # laço para exibir os resultados
        show(estado_profundidade)

        
# Busca por aprofundamento feito em sala
# IDS repete uma busca em profundidade com limites crescentes
# Limite 0, 1, 2, 3, ... até encontrar o objetivo




def busca_por_profundidade_limitada(start: tuple, limit: int):
    # cria fronteira de busca (pilha) para cada limite
    pilha = [[start]]
    
    # enquanto tiver caminhos para analisar
    while pilha:
        # remove o ultimo caminho inserido na pilha
        path = pilha.pop()

        # estado atual é o último elemento do caminho
        # path[0] = 1
        # path[1] = 4
        # path[-1] = 4 = path(len(path) - 1) = path[2 - 1]
        state = path[-1]

        # Calcula a profundidade que foi percorrida até o momento
        # Estado inicial está na profundidade zero (0)
        depth = len(path) - 1

        # Só se gera novos estados quando não atingiu o limite de profundidade
        if depth < limit:
            # encontra a posição do '0' no estado atual
            z = find_zero(state)

            # percorre as movimentações válidas de acordo com a posição do '0'
            for move in valid_moves(z):
                # move = "up" | "down" | "left" | "right"
                # aplica o movimento e gera um novo estado
                new_state = apply_moves(state, move)

                # verifica se o novo estado já está no caminho atual (para evitar ciclos)
                if new_state not in path:
                    # cria um novo caminho com o novo estado
                    # path = [1, 4]
                    # new_state = [5]
                    # new_path = [1, 4, 5]
                    new_path = path + [new_state]
                    # questao de prova
                    # verifica se o novo estado é o objetivo ( se não tivesse executaria que nem louco)
                    if new_state == GOAL:
                        return new_path

                    # adiciona o novo caminho na pilha para continuar a busca
                    pilha.append(new_path)

        # Se já atingiu o limite de profundidade, não gera novos estados
    
    return None


# max_depth é qntd máxima de limite definido
def ids(start: tuple, max_depth: int = 31):
    # quantas vezes a IDS volta ao estado inicial
    restarts = 0

    # 1º -> depth_limit = 0 até o 11
    # 2º -> depth_limit = 1 até o 11
    # 3º -> depth_limit = 2 até o 11
    # ...
    for depth_limit in range(max_depth + 1):
        if depth_limit == 0:
            print(f"Iniciando o IDS com limte {depth_limit}")
        else:
            # registra um novo restart
            restarts += 1
            # exibe quantas vezes a busca reiniciou e o novo limite
            print(f"Retorna ao ínicio #{restarts}\n")
            print(f"Novo limite é {depth_limit}")

        # chama a busca por profundidade com o limite definido
        solution = busca_por_profundidade_limitada(start, depth_limit)

        # verifica se encontrou solução
        if solution is not None:
            # encontrou solução, retorna o caminho
            # mostra a quantidade de passos até a solução
            print(f"Solução encontrada em {len(solution) - 1} passo(s) com limite {depth_limit}")
            return solution

        # não encontrou solução, continua o laço para aumentar o limite
        print(f"Não encontrou solução com limite {depth_limit}\n")
        print("--------------------------------------------------\n")
        print("Total de reinícios até agora:", restarts)

# executando a IDS - busca por aprofundamento iterativo
solution_ids = ids(start, max_depth=31)