import sys
import random
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QImage, QPixmap
from pyvis.network import Network
import webbrowser
import turtle
import math

class GrammarEntryWidget(QWidget):
    grammar_saved = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        # Área de texto para entrada da gramática
        self.grammar_text = QTextEdit(self)
        self.grammar_text.setPlaceholderText("Insira a gramática no formato:\nS -> NP | VP\nNP -> 'Ana' | 'João'\n...")
        layout.addWidget(QLabel("Defina a gramática:"))
        layout.addWidget(self.grammar_text)

        # Botão para salvar gramática
        save_button = QPushButton("Salvar Gramática", self)
        save_button.clicked.connect(self.save_grammar_dialog)
        layout.addWidget(save_button)

        # Botão para carregar gramática pronta
        load_button = QPushButton("Carregar Gramática", self)
        load_button.clicked.connect(self.load_grammar)
        layout.addWidget(load_button)

        # Botão para gerar gramática de exemplo
        example_button = QPushButton("Gerar Gramática de Exemplo", self)
        example_button.clicked.connect(self.generate_example_grammar)
        layout.addWidget(example_button)

        self.setLayout(layout)
    
    def generate_example_grammar(self):
        """Gera uma gramática de exemplo e a insere no campo de texto."""
        example_grammar = {
            "S": ["NP VP"],
            "NP": ["Det N", "'Ana'", "'João'"],
            "VP": ["V NP", "V"],
            "Det": ["'o'", "'a'"],
            "N": ["'menino'", "'menina'"],
            "V": ["'viu'", "'gostou'"]
        }
        # Converte a gramática em texto e insere no campo
        self.grammar_text.setPlainText(self.format_grammar_as_text(example_grammar))
        self.grammar_saved.emit(example_grammar)  # Emite o sinal com a gramática gerada

    def save_grammar_dialog(self):
        """Exibe opções para salvar a gramática."""
        grammar = self.parse_grammar(self.grammar_text.toPlainText())
        if grammar:
            self.grammar_saved.emit(grammar)  # Emite o sinal com a gramática
            # Pergunta ao usuário o formato de arquivo para salvar
            options = QMessageBox()
            options.setWindowTitle("Salvar Gramática")
            options.setText("Escolha o formato de arquivo para salvar a gramática:")
            options.addButton("JSON", QMessageBox.AcceptRole)
            options.addButton("Texto (TXT)", QMessageBox.AcceptRole)
            options.addButton("Cancelar", QMessageBox.RejectRole)

            choice = options.exec_()

            if choice == 0:  # JSON
                self.save_to_file(grammar, "json")
            elif choice == 1:  # TXT
                self.save_to_file(grammar, "txt")

    def save_to_file(self, grammar, file_format):
        """Salva a gramática no formato especificado."""
        # Abre diálogo para escolher o local do arquivo
        file_dialog = QFileDialog(self)
        if file_format == "json":
            file_path, _ = file_dialog.getSaveFileName(self, "Salvar Gramática", "", "Arquivos JSON (*.json)")
            if file_path:
                with open(file_path, "w", encoding="utf-8") as file:
                    json.dump(grammar, file, indent=4)
        elif file_format == "txt":
            file_path, _ = file_dialog.getSaveFileName(self, "Salvar Gramática", "", "Arquivos de Texto (*.txt)")
            if file_path:
                with open(file_path, "w", encoding="utf-8") as file:
                    for key, values in grammar.items():
                        file.write(f"{key} -> {' | '.join(values)}\n")

#    def save_grammar(self):
#        """Salva a gramática inserida pelo usuário e emite o sinal."""
#        grammar = self.parse_grammar(self.grammar_text.toPlainText())
#        if grammar:
#            self.grammar_saved.emit(grammar)

    def parse_grammar(self, text):
        """Converte o texto da gramática em um dicionário de produções."""
        grammar = {}
        for line in text.splitlines():
            if '->' in line:
                left, right = line.split('->')
                left = left.strip()
                right = [rule.strip() for rule in right.split('|')]
                grammar[left] = right
        return grammar
    
    def load_grammar(self):
        """Carrega uma gramática pronta de um arquivo."""
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "Carregar Gramática", "", "Arquivos JSON ou Texto (*.json *.txt)")
        if file_path:
            try:
                if file_path.endswith(".json"):
                    with open(file_path, "r", encoding="utf-8") as file:
                        grammar = json.load(file)
                elif file_path.endswith(".txt"):
                    with open(file_path, "r", encoding="utf-8") as file:
                        grammar = self.parse_grammar(file.read())
                else:
                    raise ValueError("Formato de arquivo inválido.")
                
                # Atualiza o texto na interface
                self.grammar_text.setPlainText(self.format_grammar_as_text(grammar))
                self.grammar_saved.emit(grammar)  # Emite o sinal com a gramática carregada
                QMessageBox.information(self, "Gramática Carregada", "Gramática carregada com sucesso!")
            except Exception as e:
                QMessageBox.critical(self, "Erro ao Carregar", f"Não foi possível carregar a gramática: {e}")

    def format_grammar_as_text(self, grammar):
        """Formata a gramática como texto para exibição na interface."""
        return "\n".join(f"{key} -> {' | '.join(values)}" for key, values in grammar.items())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gerador de Textos com Gramática")
        self.setGeometry(100, 100, 800, 600)

        # Inicializa a interface
        self.initUI()

    def initUI(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()

        # Área de texto de saída
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        main_layout.addWidget(self.output_text)

        # Widget para entrada da gramática
        self.grammar_widget = GrammarEntryWidget()
        self.grammar_widget.grammar_saved.connect(self.enable_generation)
        main_layout.addWidget(self.grammar_widget)

        # Botões para geração de texto, exibição da árvore e L-System
        button_layout = QHBoxLayout()
        
        # Botão de geração de texto
        self.generate_button = QPushButton("Gerar Texto")
        self.generate_button.setEnabled(False)
        self.generate_button.clicked.connect(self.generate_text)
        button_layout.addWidget(self.generate_button)
        
        # Botão de exibição da árvore de derivação
        self.tree_button = QPushButton("Mostrar Árvore")
        self.tree_button.setEnabled(False)
        self.tree_button.clicked.connect(self.show_tree)
        button_layout.addWidget(self.tree_button)

        # Botão de geração de imagem com L-Systems
        self.lsystem_button = QPushButton("Gerar Imagem com L-System")
        self.lsystem_button.clicked.connect(self.generate_lsystem_image)
        button_layout.addWidget(self.lsystem_button)
        
        # Botão de limpar a tela
        self.clear_button = QPushButton("Limpar Tela")
        self.clear_button.clicked.connect(self.clear_screen)
        button_layout.addWidget(self.clear_button)

        # Adiciona os botões ao layout principal
        main_layout.addLayout(button_layout)

        # Área de texto para exibir o texto gerado
        self.output_text = QTextEdit(self)
        self.output_text.setReadOnly(True)
        main_layout.addWidget(self.output_text)

        self.central_widget.setLayout(main_layout)

    def clear_screen(self):
        """Limpa a tela, mas mantém a gramática salva e reinicia o estado."""
        # Limpa o texto gerado
        self.output_text.clear()
        
        # Remove qualquer imagem ou desenho gerado
        # (Deve remover qualquer QLabel que tenha sido adicionado para exibir imagens)
        for i in range(self.central_widget.layout().count()):
            widget = self.central_widget.layout().itemAt(i).widget()
            if isinstance(widget, QLabel):
                widget.deleteLater()

        # Reinicia o estado dos botões (habilita ou desabilita conforme necessário)
        self.generate_button.setEnabled(False)
        self.tree_button.setEnabled(False)
        self.lsystem_button.setEnabled(True)  # Deixa o botão de L-System disponível

        # Reseta outras variáveis internas, se necessário
        self.generated_symbol = None  # Caso queira reiniciar a geração do texto ou árvore

    @pyqtSlot(dict)
    def enable_generation(self, grammar):
        """Habilita a geração de texto após a gramática ser salva."""
        self.grammar = grammar
        self.generate_button.setEnabled(True)
        self.tree_button.setEnabled(True)
        self.output_text.append("Gramática salva com sucesso.\n")

    def generate_text(self):
        """Gera texto aleatório baseado na gramática."""
        text, productions = self.generate_random_sentence("S")
        self.output_text.append("Texto gerado:\n" + text + "\n")
        self.output_text.append("Produções usadas:\n" + " -> ".join(productions) + "\n")
        self.generated_symbol = "S"  # Salva o símbolo inicial utilizado

    def generate_random_sentence(self, symbol):
        """Gera uma sentença aleatória e a sequência de produções usadas."""
        sentence = []
        productions = []
        self.expand(symbol, sentence, productions)
        return " ".join(sentence), productions

    def expand(self, symbol, sentence, productions):
        """Expande um símbolo de acordo com as regras da gramática."""
        if symbol in self.grammar:
            production = random.choice(self.grammar[symbol])
            productions.append(f"{symbol} -> {production}")
            for sym in production.split():
                self.expand(sym, sentence, productions)
        else:
            sentence.append(symbol)

    def show_tree(self):
        """Mostra a árvore de derivação em um HTML usando pyvis."""
        net = Network(directed=True)
        net.add_node(self.generated_symbol, label=self.generated_symbol)
        self.build_graph(self.generated_symbol, net, self.generated_symbol)  # Passa o símbolo correto
        
        # Defina o caminho do arquivo HTML
        html_path = '/home/luan/Documentos/LFA/GLC/tree_graph.html'
        net.write_html(html_path)  # Salva o HTML no caminho especificado
        
        # Abre automaticamente o arquivo HTML no navegador
        webbrowser.open(f"file://{html_path}")
        
        self.output_text.append(f"Árvore de derivação salva e aberta em: {html_path}")

    def build_graph(self, symbol, net, parent):
        """Constrói a árvore de derivação."""
        if symbol in self.grammar:
            production = random.choice(self.grammar[symbol])
            for sym in production.split():
                # Define o estilo do nó inicial (S) como amarelo
                if sym == "S":
                    net.add_node(sym, label=sym, color="yellow")
                else:
                    net.add_node(sym, label=sym)

                net.add_edge(parent, sym)
                self.build_graph(sym, net, sym)
        else:
            # Define o estilo dos nós terminais como vermelho
            net.add_node(symbol, label=symbol, color="red")

    def generate_lsystem_image(self):
        """Gera a imagem de um L-System com uma sequência aleatória."""
        # Definir parâmetros aleatórios para o L-System
        angle = random.randint(20, 90)  # Ângulo aleatório entre 20 e 90 graus
        iterations = random.randint(3, 7)  # Número de iterações aleatórias entre 3 e 7
        distance = random.randint(5, 15)  # Distância aleatória entre 5 e 15 pixels
        
        # Definir o axiom (estado inicial) e regras de produção
        axiom = "F" 

        # Defina algumas regras de produção variadas
        rules = {
            "F": ["F+F-F-F+F", "F-F+F+F-F", "F+F+F+F"],
            "X": ["F+[[X]-X]-F[-FX]+X", "X-F+[[X]-X]-F[-FX]+X"]
        }
        
        # Símbolos iniciais do L-System
        axiom = random.choice(["X", "F"])  # Aleatoriamente começa com X ou F
        
        # Número de iterações (pode ser variável)
        iterations = random.randint(4, 6)  # Um número aleatório de iterações
        
        # Geração da sequência L-System
        sequence = axiom
        for _ in range(iterations):
            sequence = self.apply_rules(sequence, rules)
        
        # Chama a função de desenho com os parâmetros corretos
        self.draw_lsystem(sequence, angle, distance)

    def apply_rules(self, sequence, rules):
        """Aplica as regras de produção ao L-System para gerar a próxima sequência."""
        new_sequence = ""
        for symbol in sequence:
            # Se o símbolo tem uma regra associada, substitua-o por uma escolha aleatória entre as opções
            new_sequence += random.choice(rules.get(symbol, [symbol]))  # Escolhe aleatoriamente entre as regras
        return new_sequence

    def lsystem_generate(self, axiom, rules, iterations):
        """Gera a sequência do L-System após as iterações."""
        sequence = axiom
        for _ in range(iterations):
            next_sequence = "".join(rules.get(char, char) for char in sequence)
            sequence = next_sequence
        return sequence

    def draw_lsystem(self, sequence, angle, distance):
        """Desenha o L-System em um QImage."""
        width, height = 800, 800  # Dimensões da imagem
        image = QImage(width, height, QImage.Format_ARGB32)
        image.fill(Qt.white)  # Fundo branco

        painter = QPainter(image)
        painter.setPen(QPen(Qt.blue))  # Configura a cor e espessura da linha

        # Posição inicial e pilha para o L-System
        x, y = 400, 400  # Começa no centro da imagem
        stack = []
        direction = 0  # Defina a direção inicial para o ângulo

        # Itera sobre a sequência para desenhar
        for symbol in sequence:
            if symbol == 'F':
                # Calcula as novas coordenadas
                new_x = x + distance * math.cos(math.radians(direction))
                new_y = y + distance * math.sin(math.radians(direction))

                # Converte para inteiros antes de passar para drawLine
                painter.drawLine(int(x), int(y), int(new_x), int(new_y))  # Desenha linha
                x, y = new_x, new_y
            elif symbol == '+':
                direction += angle  # Rotaciona no sentido horário
            elif symbol == '-':
                direction -= angle  # Rotaciona no sentido anti-horário
            elif symbol == '[':
                stack.append((x, y, direction))  # Salva a posição e direção
            elif symbol == ']':
                x, y, direction = stack.pop()  # Restaura a posição e direção

        painter.end()

        # Salvar a imagem gerada e exibir na interface
        img_path = "lsystem_image_qimage.png"
        image.save(img_path)
        self.show_image(img_path)

    def show_image(self, path):
        """Exibe a imagem gerada na interface usando QLabel."""
        label = QLabel(self)
        pixmap = QPixmap(path)
        label.setPixmap(pixmap)
        label.setScaledContents(True)
        label.setFixedSize(800, 800)  # Define o tamanho do QLabel
        self.central_widget.layout().addWidget(label)  # Adiciona o QLabel ao layout principal
        self.output_text.append("Imagem gerada e exibida com sucesso!")

    def clear_screen(self):
        """Limpa a tela, mas mantém a gramática salva e reinicia o estado."""
        # Limpa o texto gerado
        self.output_text.clear()
        
        # Remove qualquer imagem ou desenho gerado
        # (Deve remover qualquer QLabel que tenha sido adicionado para exibir imagens)
        for i in range(self.central_widget.layout().count()):
            widget = self.central_widget.layout().itemAt(i).widget()
            if isinstance(widget, QLabel):
                widget.deleteLater()

        # Reinicia o estado dos botões (habilita ou desabilita conforme necessário)
        self.generate_button.setEnabled(False)
        self.tree_button.setEnabled(False)
        self.lsystem_button.setEnabled(True)  # Deixa o botão de L-System disponível

        # Reseta outras variáveis internas, se necessário
        self.generated_symbol = None  # Caso queira reiniciar a geração do texto ou árvore


# Inicialização da aplicação
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
