import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QFileDialog
from PyQt5.QtCore import QTimer, Qt, QPointF
from PyQt5.QtGui import QPainter, QFont, QPainterPath
import math

class Automato:
    def __init__(self):
        self.estados = set()
        self.transicoes = {}
        self.estados_atuais = set()
        self.estados_finais = set()

    def adicionar_transicao(self, origem, simbolo, destino):
        self.estados.add(origem)
        self.estados.add(destino)
        # Adicionar a transição ao dicionário
        if (origem, simbolo) not in self.transicoes:
            self.transicoes[(origem, simbolo)] = set()
        self.transicoes[(origem, simbolo)].add(destino)
        
    def definir_estado_inicial(self, estado):
        # Garantir que o estado inicial é um estado válido
        self.estado_atual = estado

    def definir_estados_finais(self, finais):
        # Garantir que os estados finais são um conjunto
        self.estados_finais = set(finais)

    def proximo_estado(self, estados_atuais, simbolo):
        # Calcular os próximos estados a partir dos estados atuais e do símbolo
        proximos_estados = set()
        for estado in estados_atuais:
            if (estado, simbolo) in self.transicoes:
                proximos_estados.update(self.transicoes[(estado, simbolo)])
        return proximos_estados


class SimulatorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuração e Simulação de Autômato")
        self.setGeometry(100, 100, 800, 600)
        # Layouts para configuração
        self.label = QLabel("Configuração do Autômato:", self)
        self.label.setAlignment(Qt.AlignCenter)
        # Campos de entrada para configuração
        self.input_estado_inicial = QLineEdit(self)
        self.input_estado_inicial.setPlaceholderText("Estado Inicial")
        self.input_estados_finais = QLineEdit(self)
        self.input_estados_finais.setPlaceholderText("Estados Finais (separados por vírgula)")
        self.input_transicao_origem = QLineEdit(self)
        self.input_transicao_origem.setPlaceholderText("Estado de Origem")
        self.input_transicao_simbolo = QLineEdit(self)
        self.input_transicao_simbolo.setPlaceholderText("Símbolo")
        self.input_transicao_destino = QLineEdit(self)
        self.input_transicao_destino.setPlaceholderText("Estado de Destino")
        self.botao_adicionar_transicao = QPushButton("Adicionar Transição", self)
        self.botao_adicionar_transicao.clicked.connect(self.adicionar_transicao)
        self.input_cadeia = QLineEdit(self)
        self.input_cadeia.setPlaceholderText("Digite a cadeia para simulação")
        self.start_button = QPushButton("Iniciar Simulação", self)
        self.start_button.clicked.connect(self.iniciar_simulacao)
        # Botões para salvar e carregar
        self.botao_salvar = QPushButton("Salvar Projeto", self)
        self.botao_salvar.clicked.connect(self.salvar_projeto)
        self.botao_carregar = QPushButton("Carregar Projeto", self)
        self.botao_carregar.clicked.connect(self.carregar_projeto)
        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        # Layout para configurações do autômato
        layout_config = QHBoxLayout()
        layout_config.addWidget(self.input_estado_inicial)
        layout_config.addWidget(self.input_estados_finais)
        layout.addLayout(layout_config)
        layout_transicoes = QHBoxLayout()
        layout_transicoes.addWidget(self.input_transicao_origem)
        layout_transicoes.addWidget(self.input_transicao_simbolo)
        layout_transicoes.addWidget(self.input_transicao_destino)
        layout_transicoes.addWidget(self.botao_adicionar_transicao)
        layout.addLayout(layout_transicoes)
        layout.addWidget(self.input_cadeia)
        layout.addWidget(self.start_button)
        # Adicionar os botões ao layout
        layout.addWidget(self.botao_salvar)
        layout.addWidget(self.botao_carregar)
        self.setLayout(layout)
        # Timer para simulação
        self.timer = QTimer()
        self.timer.timeout.connect(self.proximo_passo)
        # Inicializar o autômato
        self.automato = Automato()
        self.cadeia = ""
        self.index = 0

    def desenhar_transicao(self, qp, origem_pos, destino_pos, simbolo):
            # Calcular ângulo da linha
            line = QPointF(destino_pos.x() - origem_pos.x(), destino_pos.y() - origem_pos.y())
            angle = math.atan2(line.y(), line.x())
            # Ajustar coordenadas
            start_x = origem_pos.x() + 20 * math.cos(angle)
            start_y = origem_pos.y() + 20 * math.sin(angle)
            end_x = destino_pos.x() - 20 * math.cos(angle)
            end_y = destino_pos.y() - 20 * math.sin(angle)
            # Linha e seta
            qp.drawLine(QPointF(start_x, start_y), QPointF(end_x, end_y))
            arrow_size = 10
            arrow_angle = math.pi / 6
            arrow_x1 = end_x - arrow_size * math.cos(angle - arrow_angle)
            arrow_y1 = end_y - arrow_size * math.sin(angle - arrow_angle)
            arrow_x2 = end_x - arrow_size * math.cos(angle + arrow_angle)
            arrow_y2 = end_y - arrow_size * math.sin(angle + arrow_angle)
            qp.drawPolygon(QPointF(end_x, end_y), QPointF(arrow_x1, arrow_y1), QPointF(arrow_x2, arrow_y2))
            # Símbolo no meio
            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2
            qp.drawText(int(mid_x), int(mid_y), simbolo)


    def adicionar_transicao(self):
        # Adicionar uma transição ao autômato
        origem = self.input_transicao_origem.text()
        simbolo = self.input_transicao_simbolo.text()
        destino = self.input_transicao_destino.text()
        # Verificar se os campos estão preenchidos
        if origem and simbolo and destino:
            self.automato.adicionar_transicao(origem, simbolo, destino)
            self.label.setText(f"Transição adicionada: {origem} --{simbolo}--> {destino}")
        else:
            self.label.setText("Por favor, preencha todos os campos da transição.")

    def iniciar_simulacao(self):
        estado_inicial = self.input_estado_inicial.text()
        # Verificar se o estado inicial é válido
        estados_finais = self.input_estados_finais.text().split(',')

        if estado_inicial:
            # Atualizar o estado inicial no autômato
            self.automato.definir_estado_inicial(estado_inicial)
            self.automato.estados_atuais = {estado_inicial}
        self.automato.definir_estados_finais(estados_finais)

        self.cadeia = self.input_cadeia.text()
        if self.cadeia:
            self.index = 0
            self.label.setText("Simulação em andamento...")
            self.timer.start(1000)
        else:
            self.label.setText("Por favor, insira uma cadeia válida.")


    def proximo_passo(self):
        # Verificar se a cadeia foi completamente lida
        if self.index < len(self.cadeia):
            # Ler o próximo símbolo e calcular os próximos estados
            simbolo = self.cadeia[self.index]
            novos_estados = self.automato.proximo_estado(self.automato.estados_atuais, simbolo)
            self.index += 1
            # Atualizar os estados atuais
            if novos_estados:
                # Atualizar os estados atuais e a interface
                self.automato.estados_atuais = novos_estados
                # Atualizar a interface
                self.label.setText(f"Estados atuais: {', '.join(novos_estados)}")
                self.update()
            else:
                self.label.setText("Cadeia rejeitada.")
                self.timer.stop()
        else:
            # Verificar se algum estado atual é final
            if self.automato.estados_atuais & self.automato.estados_finais:
                self.label.setText("Cadeia aceita!")
            else:
                self.label.setText("Cadeia rejeitada.")
            self.timer.stop()

    def salvar_projeto(self):
        nome_arquivo, _ = QFileDialog.getSaveFileName(self, "Salvar Projeto", "", "Arquivos de Texto (*.txt)")
        if not nome_arquivo.endswith(".txt"):
            nome_arquivo += ".txt"
        
        if nome_arquivo:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                # Salvar estados
                f.write("#states\n")
                for estado in sorted(self.automato.estados):  # Ordena os estados
                    f.write(f"{estado}\n")
                
                # Salvar estado inicial
                f.write("#initial\n")
                f.write(f"{self.automato.estado_atual}\n")
                
                # Salvar estados finais
                f.write("#accepting\n")
                if self.automato.estados_finais:
                    f.write("\n".join(sorted(self.automato.estados_finais)) + "\n")  # Ordena os estados finais
                
                # Salvar alfabeto
                f.write("#alphabet\n")
                alfabeto = {simbolo for (_, simbolo) in self.automato.transicoes.keys()}
                for simbolo in sorted(alfabeto):  # Ordena os símbolos do alfabeto
                    f.write(f"{simbolo}\n")
                
                # Salvar transições
                f.write("#transitions\n")
                for (origem, simbolo), destinos in sorted(self.automato.transicoes.items()):  # Ordena as transições
                    for destino in destinos:  # Garante que se houver múltiplos destinos, todos sejam gravados
                        f.write(f"{origem}:{simbolo}>{destino}\n")

    def carregar_projeto(self):
        nome_arquivo, _ = QFileDialog.getOpenFileName(self, "Carregar Projeto", "", "Arquivos de Texto (*.txt)")
        if nome_arquivo:
            try:
                with open(nome_arquivo, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    # Limpar espaços e quebras de linha extras
                    lines = [line.strip() for line in lines if line.strip()]
                    # Iniciar variáveis
                    estados = set()
                    transicoes = {}
                    estado_inicial = None
                    estados_finais = set()
                    alfabeto = set()
                    # Processar as linhas
                    section = None
                    for line in lines:
                        if line.startswith("#"):
                            section = line[1:].strip()  # Pega a seção após o #
                        else:
                            if section == "states":
                                estados.add(line)
                            elif section == "initial":
                                estado_inicial = line
                            elif section == "accepting":
                                if line:
                                    estados_finais.add(line)
                            elif section == "alphabet":
                                alfabeto.add(line)
                            elif section == "transitions":
                                # Tratar a linha de transição (origem:símbolo>destino)
                                origem, resto = line.split(":")
                                simbolo, destino = resto.split(">")
                                transicoes[(origem, simbolo)] = destino

                    # Verificar se todas as seções estão completas
                    if None in [estado_inicial, estados, estados_finais, alfabeto, transicoes]:
                        raise ValueError("Faltam seções ou dados no arquivo.")

                    # Carregar no autômato
                    self.automato.estados = estados
                    self.automato.estado_atual = estado_inicial
                    self.automato.estados_finais = estados_finais
                    for (origem, simbolo), destino in transicoes.items():
                        self.automato.adicionar_transicao(origem, simbolo, destino)

                    self.atualizar_interface()

            except Exception as e:
                print(f"Erro ao carregar o autômato: {e}")
                self.label.setText("Erro ao carregar o autômato. Verifique o arquivo.")
    

    def atualizar_interface(self):
        self.input_estado_inicial.setText(self.automato.estado_atual if self.automato.estado_atual else "")
        self.input_estados_finais.setText(', '.join(self.automato.estados_finais))
        self.input_transicao_origem.clear()
        self.input_transicao_simbolo.clear()
        self.input_transicao_destino.clear()
        self.input_cadeia.clear()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        qp.setFont(QFont("Arial", 10))
        center_x, center_y = 400, 300  # Centro do círculo
        radius = 200  # Raio do círculo

        # Distribuir estados em um círculo
        estados_pos = {}
        num_estados = len(self.automato.estados)
        angle_step = 2 * math.pi / num_estados if num_estados > 0 else 0
        for i, estado in enumerate(self.automato.estados):
            angle = i * angle_step
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            estados_pos[estado] = QPointF(x, y)

        # Desenhar estados
        for estado, pos in estados_pos.items():
            if estado in self.automato.estados_atuais:
                qp.setBrush(Qt.green)  # Estado atual em verde
            elif estado in self.automato.estados_finais:
                qp.setBrush(Qt.red)  # Estado final em vermelho
            else:
                qp.setBrush(Qt.white)  # Outros estados em branco
            qp.drawEllipse(pos, 20, 20)
            qp.drawText(int(pos.x()), int(pos.y()), estado)

        # Desenhar transições com curvas para evitar sobreposição
        transicao_offset = {}  # Para rastrear deslocamento entre pares de estados
        for (origem, simbolo), destinos in self.automato.transicoes.items():
            origem_pos = estados_pos[origem]
            if isinstance(destinos, set):
                destinos = list(destinos)  # Garantir que é iterável

            for destino in destinos:
                if destino in estados_pos:
                    destino_pos = estados_pos[destino]

                    # Evitar sobreposição calculando um deslocamento para cada par de estados
                    pair = (origem, destino)
                    if pair not in transicao_offset:
                        transicao_offset[pair] = 0
                    offset = transicao_offset[pair]
                    transicao_offset[pair] += 1

                    # Determinar pontos de controle para a curva
                    mid_x = (origem_pos.x() + destino_pos.x()) / 2
                    mid_y = (origem_pos.y() + destino_pos.y()) / 2
                    curve_offset = 20 + offset * 10  # Incrementar o deslocamento para múltiplas transições
                    control_x = mid_x + curve_offset * (destino_pos.y() - origem_pos.y()) / radius
                    control_y = mid_y - curve_offset * (destino_pos.x() - origem_pos.x()) / radius
                    # Desenhar a curva
                    path = QPainterPath()
                    path.moveTo(origem_pos)
                    path.quadTo(QPointF(control_x, control_y), destino_pos)
                    qp.drawPath(path)
                    # Adicionar uma seta na direção do destino
                    self.desenhar_seta(qp, origem_pos, destino_pos, control_x, control_y)
                    # Desenhar o símbolo próximo ao ponto de controle
                    simbolo_x = control_x
                    simbolo_y = control_y
                    qp.drawText(int(simbolo_x), int(simbolo_y), simbolo)

        qp.end()

    def desenhar_seta(self, qp, origem, destino, control_x, control_y):
        # Desenhar uma seta no final de uma transição
        angle = math.atan2(destino.y() - origem.y(), destino.x() - origem.x())
        arrow_size = 10
        arrow_angle = math.pi / 6
        end_x = destino.x()
        end_y = destino.y()
        arrow_x1 = end_x - arrow_size * math.cos(angle - arrow_angle)
        arrow_y1 = end_y - arrow_size * math.sin(angle - arrow_angle)
        arrow_x2 = end_x - arrow_size * math.cos(angle + arrow_angle)
        arrow_y2 = end_y - arrow_size * math.sin(angle + arrow_angle)
        qp.drawPolygon(QPointF(end_x, end_y), QPointF(arrow_x1, arrow_y1), QPointF(arrow_x2, arrow_y2))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimulatorApp()
    window.show()
    sys.exit(app.exec_())