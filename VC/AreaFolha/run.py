import cv2
import numpy as np
import matplotlib.pyplot as plt

# Função para carregar imagem
def carrega_imagem(caminho: str):
    img_bgr = cv2.imread(caminho)
    if img_bgr is None:
        raise FileNotFoundError(f"Não encontrei '{caminho}'")
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return img_bgr, img_rgb

# Função para processar imagem e calcular área
def processa_imagem(imagem, largura_real_cm=5.0):
    img_bgr, img_rgb = imagem
    img_cinza = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    # Detecção de retângulo vermelho para escala
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    # Faixa de cor para vermelho em HSV
    lower_red1 = np.array([0, 50, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 50, 50])
    upper_red2 = np.array([179, 255, 255])
    # Cria mascára para o vermelho
    mask_red = cv2.inRange(img_hsv, lower_red1, upper_red1) + cv2.inRange(img_hsv, lower_red2, upper_red2)
    contornos_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contornos_red:
        raise ValueError("Nenhum retângulo encontrado!")

    contorno_retangulo = max(contornos_red, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(contorno_retangulo)
    largura_pixels = max(w, h)
    cm_por_pixel = largura_real_cm / largura_pixels
    print(f"Largura do retângulo: {largura_pixels}px | Escala: {cm_por_pixel:.5f} cm/px")

    img_retangulo = img_rgb.copy()
    cv2.rectangle(img_retangulo, (x, y), (x + w, y + h), (0, 255, 0), 3)
    # Segmentação da folha 
    lower_green = np.array([30, 30, 30])
    upper_green = np.array([80, 255, 255])
    mask_leaf = cv2.inRange(img_hsv, lower_green, upper_green)
    k = np.ones((5,5), np.uint8)
    mask_leaf = cv2.morphologyEx(mask_leaf, cv2.MORPH_OPEN, k, iterations=1)
    mask_leaf = cv2.morphologyEx(mask_leaf, cv2.MORPH_CLOSE, k, iterations=1)
    # Cálculo da área
    area_px = np.count_nonzero(mask_leaf)
    area_cm2 = area_px * (cm_por_pixel ** 2)
    print(f"Área da folha: {area_px} px² -> {area_cm2:.2f} cm²")

    return img_rgb, img_retangulo, mask_leaf, area_cm2

# Pasta das imagens
caminho_antes = './images/antes.jpg'
caminho_depois = './images/depois.jpg'

# Função carregar imagem
imagem_antes = carrega_imagem(caminho_antes)
imagem_depois = carrega_imagem(caminho_depois)
# Processar imagens
img_rgb_antes, img_retangulo_antes, mask_leaf_antes, area_cm2_antes = processa_imagem(imagem_antes)
img_rgb_depois, img_retangulo_depois, mask_leaf_depois, area_cm2_depois = processa_imagem(imagem_depois)
# Calcular diferença de área
area_perdida = area_cm2_antes - area_cm2_depois
print(f"Área antes: {area_cm2_antes:.2f} cm²")
print(f"Área depois: {area_cm2_depois:.2f} cm²")
print(f"Área perdida: {area_perdida:.2f} cm²")

# Exibir imagens
plt.figure(figsize=(16, 12))
plt.subplot(2, 3, 1)
plt.title("Imagem Original (Antes)")
plt.imshow(img_rgb_antes)
plt.axis("off")

plt.subplot(2, 3, 2)
plt.title("Retângulo Detectado (Antes)")
plt.imshow(img_retangulo_antes)
plt.axis("off")

plt.subplot(2, 3, 3)
plt.title(f"Folha Segmentada (Antes)\nÁrea: {area_cm2_antes:.2f} cm²")
plt.imshow(mask_leaf_antes, cmap="gray")
plt.axis("off")

plt.subplot(2, 3, 4)
plt.title("Imagem Original (Depois)")
plt.imshow(img_rgb_depois)
plt.axis("off")

plt.subplot(2, 3, 5)
plt.title("Retângulo Detectado (Depois)")
plt.imshow(img_retangulo_depois)
plt.axis("off")

plt.subplot(2, 3, 6)
plt.title(f"Folha Segmentada (Depois)\nÁrea: {area_cm2_depois:.2f} cm²")
plt.imshow(mask_leaf_depois, cmap="gray")
plt.axis("off")

plt.tight_layout()
plt.show()
