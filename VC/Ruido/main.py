import sys
import os
import cv2
import numpy as np
from skimage import filters
from skimage.restoration import denoise_tv_chambolle
from skimage.util import random_noise
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QHBoxLayout, QFileDialog, QComboBox, QSlider, QGroupBox,
    QFormLayout, QSpinBox, QMessageBox
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import unicodedata



def save_image(path, img):
    """
    Salvamento seguro de imagens usando imencode.
    Evita erros de permissão do Windows / OneDrive / Unicode.
    """
    try:
        path = os.path.normpath(path)
        ext = os.path.splitext(path)[1].lower()

        ok, encoded = cv2.imencode(ext, img)
        if not ok:
            return False

        with open(path, "wb") as f:
            f.write(encoded.tobytes())

        return True

    except Exception as e:
        print("Erro ao salvar:", e)
        return False


# ======================================================

def ensure_odd(k):
    k = int(k)
    return k if (k % 2 == 1) else k + 1


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Processamento de Imagens - Ruído, Suavização e Bordas")
        self.resize(1400, 760)

        self.original_img = None
        self.processed_noise = None
        self.processed_blur = None
        self.processed_edge = None

        main_layout = QHBoxLayout()
        controls = self.create_controls()
        images = self.create_image_display()
        main_layout.addWidget(controls, 0)
        main_layout.addLayout(images, 1)
        self.setLayout(main_layout)

    # ----------------------------------------------------

    def create_controls(self):
        group = QGroupBox("Configurações")
        vbox = QVBoxLayout()
        form = QFormLayout()

        # Load
        btn_load = QPushButton("Carregar Imagem")
        btn_load.clicked.connect(self.load_image)
        vbox.addWidget(btn_load)

        # Ruído
        self.combo_noise = QComboBox()
        self.combo_noise.addItems(["none", "gaussian", "salt-pepper", "poisson", "speckle"])
        form.addRow(QLabel("Tipo de Ruído:"), self.combo_noise)

        self.slider_noise = QSlider(Qt.Horizontal)
        self.slider_noise.setRange(1, 50)
        self.slider_noise.setValue(20)
        form.addRow(QLabel("Intensidade do Ruído (escala):"), self.slider_noise)

        # Suavização
        self.combo_blur = QComboBox()
        self.combo_blur.addItems(["none", "gaussian", "median", "mean", "bilateral", "tv_denoise"])
        form.addRow(QLabel("Tipo de Suavização:"), self.combo_blur)

        self.slider_kernel = QSlider(Qt.Horizontal)
        self.slider_kernel.setRange(1, 31)
        self.slider_kernel.setValue(5)
        form.addRow(QLabel("Kernel (suavização):"), self.slider_kernel)

        # Bilateral
        self.spin_bilateral_d = QSpinBox(); self.spin_bilateral_d.setRange(1, 50); self.spin_bilateral_d.setValue(9)
        self.spin_bilateral_sigmaColor = QSpinBox(); self.spin_bilateral_sigmaColor.setRange(1,200); self.spin_bilateral_sigmaColor.setValue(75)
        self.spin_bilateral_sigmaSpace = QSpinBox(); self.spin_bilateral_sigmaSpace.setRange(1,200); self.spin_bilateral_sigmaSpace.setValue(75)
        form.addRow("Bilateral d:", self.spin_bilateral_d)
        form.addRow("Bilateral sigmaColor:", self.spin_bilateral_sigmaColor)
        form.addRow("Bilateral sigmaSpace:", self.spin_bilateral_sigmaSpace)

        # TV
        self.slider_tv_weight = QSlider(Qt.Horizontal)
        self.slider_tv_weight.setRange(1, 100)
        self.slider_tv_weight.setValue(10)
        form.addRow(QLabel("TV weight x0.01:"), self.slider_tv_weight)

        # Edge
        self.combo_edge = QComboBox()
        self.combo_edge.addItems(["sobel", "prewitt", "canny", "laplacian"])
        form.addRow(QLabel("Detector de Bordas:"), self.combo_edge)

        self.spin_canny_low = QSpinBox(); self.spin_canny_low.setRange(0,255); self.spin_canny_low.setValue(50)
        self.spin_canny_high = QSpinBox(); self.spin_canny_high.setRange(0,255); self.spin_canny_high.setValue(150)
        form.addRow("Canny low:", self.spin_canny_low)
        form.addRow("Canny high:", self.spin_canny_high)

        vbox.addLayout(form)

        btn_process = QPushButton("Processar")
        btn_process.clicked.connect(self.process_image)
        vbox.addWidget(btn_process)

        btn_save = QPushButton("Salvar Resultado Atual")
        btn_save.clicked.connect(self.save_results)
        vbox.addWidget(btn_save)

        btn_export = QPushButton("Exportar Batch (salva combinações)")
        btn_export.clicked.connect(self.export_batch)
        vbox.addWidget(btn_export)

        group.setLayout(vbox)
        return group

    # ----------------------------------------------------

    def create_image_display(self):
        layout = QVBoxLayout()
        top = QHBoxLayout()
        bottom = QHBoxLayout()

        self.label_original = QLabel("Original")
        self.label_noise   = QLabel("Com Ruído")
        self.label_blur    = QLabel("Suavizada")
        self.label_edge    = QLabel("Bordas")

        for lbl in [self.label_original, self.label_noise]:
            lbl.setFixedSize(640, 320)
            lbl.setStyleSheet("border: 1px solid black")
            lbl.setAlignment(Qt.AlignCenter)
            top.addWidget(lbl)

        for lbl in [self.label_blur, self.label_edge]:
            lbl.setFixedSize(640, 320)
            lbl.setStyleSheet("border: 1px solid black")
            lbl.setAlignment(Qt.AlignCenter)
            bottom.addWidget(lbl)

        layout.addLayout(top)
        layout.addLayout(bottom)
        return layout

    # ----------------------------------------------------

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Escolher Imagem", "", "Images (*.jpg *.png *.jpeg *.bmp)")
        if not path:
            return

        data = np.fromfile(path, dtype=np.uint8)  # evita erro UNICODE
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)

        if img is None:
            QMessageBox.critical(self, "Erro", "Não foi possível abrir a imagem.")
            return

        self.original_img = img
        self.display_image(self.original_img, self.label_original)

    # ----------------------------------------------------

    def display_image(self, img, label):
        if img is None:
            label.setText("Sem imagem")
            return

        if len(img.shape) == 2:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        h, w, ch = img_rgb.shape
        qimg = QImage(img_rgb.data, w, h, ch*w, QImage.Format_RGB888)
        label.setPixmap(QPixmap.fromImage(qimg).scaled(label.width(), label.height(), Qt.KeepAspectRatio))

    # ----------------------------------------------------

    def process_image(self):
        if self.original_img is None:
            QMessageBox.information(self, "Aviso", "Carregue uma imagem primeiro.")
            return

        gray = cv2.cvtColor(self.original_img, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255.0

        # Ruído
        noise_type = self.combo_noise.currentText()
        noise_param = self.slider_noise.value() / 100.0

        if noise_type == "none":
            noisy = gray.copy()
        elif noise_type == "gaussian":
            noisy = random_noise(gray, mode='gaussian', var=max(1e-6, noise_param))
        elif noise_type == "salt-pepper":
            noisy = random_noise(gray, mode='s&p', amount=noise_param)
        elif noise_type == "poisson":
            noisy = random_noise(gray, mode='poisson')
        elif noise_type == "speckle":
            noisy = random_noise(gray, mode='speckle', var=noise_param)

        self.processed_noise = (noisy * 255).astype(np.uint8)
        self.display_image(self.processed_noise, self.label_noise)

        # Suavização
        blur_type = self.combo_blur.currentText()
        k = ensure_odd(self.slider_kernel.value())

        if blur_type == "none":
            blurred = self.processed_noise.copy()
        elif blur_type == "gaussian":
            blurred = cv2.GaussianBlur(self.processed_noise, (k, k), 0)
        elif blur_type == "median":
            blurred = cv2.medianBlur(self.processed_noise, max(3, k))
        elif blur_type == "mean":
            blurred = cv2.blur(self.processed_noise, (k, k))
        elif blur_type == "bilateral":
            temp = cv2.cvtColor(self.processed_noise, cv2.COLOR_GRAY2BGR)
            temp = cv2.bilateralFilter(
                temp,
                self.spin_bilateral_d.value(),
                self.spin_bilateral_sigmaColor.value(),
                self.spin_bilateral_sigmaSpace.value()
            )
            blurred = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
        elif blur_type == "tv_denoise":
            w = self.slider_tv_weight.value() * 0.01
            den = denoise_tv_chambolle(
                self.processed_noise.astype(np.float32)/255.0,
                weight=w,
                channel_axis=None
            )
            blurred = (den * 255).astype(np.uint8)

        self.processed_blur = blurred
        self.display_image(blurred, self.label_blur)

        # Bordas
        edge_type = self.combo_edge.currentText()
        if edge_type == "sobel":
            edges = filters.sobel(blurred.astype(np.float32)/255.0) * 255
        elif edge_type == "prewitt":
            edges = filters.prewitt(blurred.astype(np.float32)/255.0) * 255
        elif edge_type == "canny":
            edges = cv2.Canny(blurred, self.spin_canny_low.value(), self.spin_canny_high.value())
        elif edge_type == "laplacian":
            edges = cv2.convertScaleAbs(cv2.Laplacian(blurred, cv2.CV_16S))

        self.processed_edge = edges.astype(np.uint8)
        self.display_image(self.processed_edge, self.label_edge)

    # ----------------------------------------------------

    def save_results(self):
        if self.original_img is None:
            QMessageBox.warning(self, "Erro", "Nenhuma imagem processada ainda.")
            return

        folder = QFileDialog.getExistingDirectory(self, "Escolher Pasta para Salvar")
        if not folder:
            return

        folder = unicodedata.normalize("NFC", folder)

        arquivos = {
            "original.png": self.original_img,
            "ruido.png": self.processed_noise,
            "suavizado.png": self.processed_blur,
            "bordas.png": self.processed_edge
        }

        erros = []

        for nome, img in arquivos.items():
            caminho = os.path.join(folder, nome)
            if not save_image(caminho, img):
                erros.append(nome)

        if erros:
            QMessageBox.critical(self, "Erro", "Falha ao salvar:\n" + "\n".join(erros))
        else:
            QMessageBox.information(self, "Sucesso", "Imagens salvas em:\n" + folder)

    # ----------------------------------------------------

    def export_batch(self):
        if self.original_img is None:
            QMessageBox.information(self, "Aviso", "Carregue uma imagem antes de exportar o batch.")
            return

        folder = QFileDialog.getExistingDirectory(self, "Escolher Pasta do Batch")
        if not folder:
            return

        folder = unicodedata.normalize("NFC", folder)

        noises = ["gaussian", "salt-pepper", "speckle"]
        noise_params = [5, 20, 40]
        blurs = ["median", "gaussian", "tv_denoise"]
        kernels = [3, 7]
        edges = ["sobel", "canny", "prewitt"]

        gray = cv2.cvtColor(self.original_img, cv2.COLOR_BGR2GRAY).astype(np.float32)/255.0

        count = 0

        for n in noises:
            for npv in noise_params:

                if n == "gaussian":
                    noisy = random_noise(gray, mode="gaussian", var=npv/100.0)
                elif n == "salt-pepper":
                    noisy = random_noise(gray, mode="s&p", amount=npv/100.0)
                elif n == "speckle":
                    noisy = random_noise(gray, mode="speckle", var=npv/100.0)

                noisy_u8 = (noisy * 255).astype(np.uint8)

                for b in blurs:
                    for k in kernels:

                        kk = ensure_odd(k)

                        if b == "median":
                            blurred = cv2.medianBlur(noisy_u8, max(3, kk))
                        elif b == "gaussian":
                            blurred = cv2.GaussianBlur(noisy_u8, (kk, kk), 0)
                        elif b == "tv_denoise":
                            den = denoise_tv_chambolle(
                                noisy_u8.astype(np.float32)/255.0,
                                weight=0.1,
                                channel_axis=None
                            )
                            blurred = (den * 255).astype(np.uint8)

                        for e in edges:

                            if e == "sobel":
                                edge = filters.sobel(blurred.astype(np.float32)/255.0) * 255
                                edge = edge.astype(np.uint8)
                            elif e == "prewitt":
                                edge = filters.prewitt(blurred.astype(np.float32)/255.0) * 255
                                edge = edge.astype(np.uint8)
                            elif e == "canny":
                                edge = cv2.Canny(blurred, 50, 150)

                            prefix = f"n-{n}{npv}_b-{b}{k}_e-{e}"

                            if not save_image(os.path.join(folder, f"{prefix}_ruido.png"), noisy_u8):
                                continue
                            if not save_image(os.path.join(folder, f"{prefix}_suave.png"), blurred):
                                continue
                            if not save_image(os.path.join(folder, f"{prefix}_borda.png"), edge):
                                continue

                            count += 1

        QMessageBox.information(self, "Exportado", f"{count} conjuntos salvos em:\n{folder}")


# ======================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = App()
    win.show()
    sys.exit(app.exec_())
