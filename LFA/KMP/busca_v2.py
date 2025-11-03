import tkinter as tk
from tkinter import scrolledtext, filedialog
from time import time

# Classe para busca básica
class Busca:
    def buscar(self, texto, padrao):
        raise NotImplementedError("Método buscar não implementado")

class BuscaComparacao(Busca):
    def buscar(self, texto, padrao):
        ocorrencias = []
        qntd_comparacoes = 0
        output_text.insert(tk.END, "=====:: BUSCA BASICA COMPARACOES ::=====\n")
        # Percorre o texto
        for i in range(len(texto) - len(padrao) + 1):  
            achou = True
            # Percorre o padrão
            for j in range(len(padrao)):
                # Incrementa a quantidade de comparações
                qntd_comparacoes += 1
                # Exibe a comparação
                output_text.insert(tk.END, f"Comparando: [{texto[i:i+len(padrao)]}] com [{padrao}]\n")
                # Se os caracteres forem diferentes, sai do loop
                if padrao[j] != texto[i + j]:
                    # Se não achou, sai do loop
                    achou = False
                    break 
            # Se achou, adiciona a posição na lista de ocorrências
            if achou:
                # Adiciona a posição na lista de ocorrências
                ocorrencias.append(i)
                # Exibe a posição da ocorrência
        return ocorrencias, qntd_comparacoes

class BuscaKMP(Busca):
    def prefixo(self, padrao):
        # Inicializa a lista de prefixos
        prefixo = [0] * len(padrao)
        p = 0
        # Percorre o padrão
        for i in range(1, len(padrao)):
            # Se os caracteres forem diferentes
            while p > 0 and padrao[p] != padrao[i]:
                # Atualiza o valor de p
                p = prefixo[p - 1]
                # Se os caracteres forem iguais
            if padrao[p] == padrao[i]:
                p += 1
                # Atualiza o valor do prefixo
            prefixo[i] = p
            # Retorna a lista de prefixos
        return prefixo
    
    # Método para buscar o padrão no texto
    def buscar(self, texto, padrao):
        prefixo = self.prefixo(padrao)
        i = 0
        j = 0
        ocorrencias = []
        comparacoes = 0
        output_text.insert(tk.END, "\n==== :: BUSCA KMP COMPARACOES ::======\n")
        # Percorre o texto
        while i < len(texto):
            comparacoes += 1
            output_text.insert(tk.END, f"Comparando: [{texto[i:i+len(padrao)]}] com [{padrao}]\n")
            # Se os caracteres forem iguais
            if padrao[j] == texto[i]:
                i += 1
                j += 1
                # Se achou o padrão
                if j == len(padrao):
                    # Adiciona a posição na lista de ocorrências
                    ocorrencias.append(i - j)  
                    # Atualiza o valor de j
                    j = prefixo[j - 1]
            else:
                # Se os caracteres forem diferentes
                if j != 0:
                    # Atualiza o valor de j
                    j = prefixo[j - 1]
                else:
                    # Atualiza o valor de i
                    i += 1
        return ocorrencias, comparacoes

# Função para selecionar o arquivo e ler seu conteúdo
def abrir_arquivo():
    caminho_arquivo = filedialog.askopenfilename(title="Selecione o arquivo de texto", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    if caminho_arquivo:
        try:
            with open(caminho_arquivo, 'r') as file:
                texto = file.read().strip()
            entry_texto.delete(1.0, tk.END)
            entry_texto.insert(tk.END, texto)
        except Exception as e:
            output_text.insert(tk.END, f"Erro ao abrir arquivo: {e}\n")

def mostrar_resultados():
    texto = entry_texto.get("1.0", tk.END).strip()
    padrao = entry_padro.get().strip().lower()
    
    if not padrao:
        output_text.insert(tk.END, "Padrão de busca não informado!\n")
        return
    
    # Limpa os resultados anteriores
    output_text.delete("1.0", tk.END)

    # Inicializa variáveis para consolidar os resultados
    resultados_finais = []

    # Busca Básica
    busca = BuscaComparacao()
    t0 = time()
    ocorrencias, qntd_comparacoes = busca.buscar(texto, padrao)
    t1 = time()
    tempo_compara = (t1 - t0) * 1000
    resultados_finais.append("\n")
    resultados_finais.append("====:: BUSCA BASICA ::====")
    resultados_finais.append(f"Posições das ocorrências: {ocorrencias}")
    resultados_finais.append(f"Quantidade de comparações: {qntd_comparacoes}")
    resultados_finais.append(f"Tempo de execução: {tempo_compara:.3f} ms")
    resultados_finais.append("======================================")
    resultados_finais.append("\n")

    # Busca KMP
    busca = BuscaKMP()
    t2 = time()
    ocorrencias, qntd_comparacoes = busca.buscar(texto, padrao)
    t3 = time()
    tempo_kmp = (t3 - t2) * 1000
    resultados_finais.append("====:: BUSCA KMP ::=====")
    resultados_finais.append(f"Posições das ocorrências: {ocorrencias}")
    resultados_finais.append(f"Quantidade de comparações: {qntd_comparacoes}")
    resultados_finais.append(f"Tempo de execução: {tempo_kmp:.3f} ms")
    resultados_finais.append("======================================")

    # Exibe os resultados de forma consolidada no final
    output_text.insert(tk.END, "\n".join(resultados_finais) + "\n")


# Criar a interface gráfica
root = tk.Tk()
root.title("Busca de Padrões no Texto")
root.geometry("700x500")  # Ajuste do tamanho da janela principal
# Labels
label_texto = tk.Label(root, text="Texto a ser pesquisado:")
label_texto.pack()
# Campo de texto para o conteúdo com tamanho maior
entry_texto = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=15)  # Aumenta o tamanho da área de texto
entry_texto.pack()
label_padro = tk.Label(root, text="Digite o padrão de busca:")
label_padro.pack()
# Campo de entrada para o padrão com tamanho maior
entry_padro = tk.Entry(root, width=50)  # Aumenta o tamanho do campo de entrada
entry_padro.pack()
# Botões
btn_abrir_arquivo = tk.Button(root, text="Abrir Arquivo", command=abrir_arquivo)
btn_abrir_arquivo.pack()
btn_buscar = tk.Button(root, text="Buscar", command=mostrar_resultados)
btn_buscar.pack()
# Área de texto para exibir resultados
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=15)  # Aumenta a área de resultados
output_text.pack()
root.mainloop()
