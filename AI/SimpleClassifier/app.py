import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import torch
from torchvision import transforms
from PIL import Image, ImageTk

# Import seguro do módulo principal
init_import_error = None
try:
    from main import model, device, labels_map, tamanho_imagens, classificaumaimagem
except Exception as e:
    init_import_error = e
    model = None
    device = 'cpu'
    labels_map = {}
    tamanho_imagens = 224
    classificaumaimagem = None

# Transformação para inferência (com normalização típica de modelos pré-treinados)
def preparar_transform(tamanho):
    return transforms.Compose([
        transforms.Resize((tamanho, tamanho)),
        transforms.ToTensor()
    ])

# Classe principal da aplicação
class APP:
    def __init__(self, root):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.title("Identificador de Enchentes")
        self.root_width = 1080
        self.root_height = 720

        self.caminhoImgselec = None
        self.foto_exib = None

        self.setup_ui()
        self.centralizar_janela()

    def setup_ui(self):
        fonte = ("Helvetica", 16)
        self.frame_tela_inicial = tk.Frame(self.root)
        self.frame_tela_inicial.pack(pady=20)
        # Canvas para exibir a imagem
        self.canvas_image = tk.Canvas(self.frame_tela_inicial, width=400, height=400, bg="gray")
        self.canvas_image.pack(pady=10)
        # Label para resultado
        self.label_resultado = tk.Label(self.frame_tela_inicial, text="", font=fonte)
        self.label_resultado.pack(pady=5)
        # Botão de seleção de imagem
        self.selecImg = tk.Button(
            self.frame_tela_inicial,
            text="Selecione a imagem",
            command=self.selecionar_imagem,
            font=fonte
        )
        self.selecImg.pack(pady=10)
        # Botão para confirmar classificação
        self.button_conf = tk.Button(
            self.frame_tela_inicial,
            text="Classificar Imagem",
            command=self.confirmar_selecao,
            font=fonte,
            state="disabled"
        )
        self.button_conf.pack(pady=5)
    
    def centralizar_janela(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_axis = int((screen_width / 2) - (self.root_width / 2))
        y_axis = int((screen_height / 2) - (self.root_height / 2))
        self.root.geometry(f"{self.root_width}x{self.root_height}+{x_axis}+{y_axis}")

    def selecionar_imagem(self):
        self.label_resultado.config(text="")
        filename = filedialog.askopenfilename(
            initialdir="/DAC/Classificador/",
            title="Selecione uma imagem",
            filetypes=(("Imagens", "*.jpg *.jpeg *.png *.bmp *.tiff"), ("Todos os arquivos", "*.*"))
        )

        if filename:
            try:
                image_pil = Image.open(filename)
                image_pil_display = image_pil.copy()
                image_pil_display.thumbnail((400, 400))  
                self.foto_exib = ImageTk.PhotoImage(image_pil_display)
                self.canvas_image.delete("all")
                self.canvas_image.create_image(200, 200, image=self.foto_exib)
                self.caminhoImgselec = filename
                self.button_conf.config(state="normal")
            except (FileNotFoundError, OSError) as e:
                messagebox.showerror("Erro", f"Não foi possível abrir a imagem:\n{e}")
                self.caminhoImgselec = None
                self.button_conf.config(state="disabled")
            except Exception as e:
                messagebox.showerror("Erro desconhecido", str(e))
                self.caminhoImgselec = None
                self.button_conf.config(state="disabled")

    def confirmar_selecao(self):
        if self.caminhoImgselec is None:
            messagebox.showwarning("Aviso", "Selecione uma imagem primeiro.")
            return

        # Verifica se o modelo e a função de classificação estão disponíveis
        if model is None or classificaumaimagem is None:
            msg = "Modelo não carregado."
            if init_import_error is not None:
                msg += f"\nErro de importação: {init_import_error}"
            messagebox.showerror("Erro", msg)
            return

        try:
            self.label_resultado.config(text="Processando...")
            # Atualiza a interface enquanto processa
            self.root.update()  
            infer_transform = preparar_transform(tamanho_imagens)
            pred_label, pred_idx = classificaumaimagem(
                model, self.caminhoImgselec, infer_transform, device, labels_map
            )

            # Se pred_label estiver vazio ou None, tenta pegar pelo índice
            if not pred_label and pred_idx is not None:
                pred_label = labels_map.get(pred_idx, "Desconhecido")

            # Padroniza a label: remove espaços, hífens, minúsculas e plural
            pred_label_clean = pred_label.strip().lower().replace("-", "").rstrip("s")
            # Mostra resultado na interface
            self.label_resultado.config(text=f"Resultado: {pred_label}")
            # ALERTA para enchente ou alerta
            if pred_label_clean in ["enchente", "alerta"]:
                messagebox.showwarning(
                    "ALERTA DE ENCHENTE",
                    f"Imagem classificada como '{pred_label}'!\nRecomenda-se verificar a região imediatamente."
                )
            else:
                messagebox.showinfo(
                    "Status Normal",
                    f"Imagem classificada como '{pred_label}'. Nenhum alerta necessário."
                )

            # DEBUG opcional: imprime no console
            print(f"Predição recebida: '{pred_label}' (limpa: '{pred_label_clean}')")
            print(f"Predição do modelo: índice={pred_idx}, label='{pred_label}'")

        except Exception as e:
            messagebox.showerror("Erro na classificação", str(e))

    def on_closing(self):
        try:
            self.root.destroy()
        except Exception:
            pass
        sys.exit(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = APP(root)
    root.mainloop()
