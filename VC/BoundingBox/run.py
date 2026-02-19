import cv2
import numpy as np
import matplotlib.pyplot as plt

caminho_imagem = 'skate-olimpiadas.jpg'

# Função para carregar imagem
def carrega_imagem(caminho: str):
    img_bgr = cv2.imread(caminho)
    if img_bgr is None:
        raise FileNotFoundError(f"Não encontrei '{caminho}'")
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return img_bgr, img_rgb


def segmenta_imagem(imagem):
    img_bgr, img_rgb = imagem
    # Convertendo para HSV
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    # Faixa de cor ajustada para calça mostarda/marrom claro
    lower_pants = np.array([10, 100, 80])   
    upper_pants = np.array([30, 255, 255])  
    # Criação da máscara
    mask_pants = cv2.inRange(img_hsv, lower_pants, upper_pants)

    if not np.any(mask_pants):
        raise ValueError("Nenhuma calça detectada!")

    # Encontrar contornos
    contornos, _ = cv2.findContours(mask_pants, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contorno_calca = max(contornos, key=cv2.contourArea)

    print(f"Contorno da calça encontrado com {len(contorno_calca)} pontos.")
    return contorno_calca, mask_pants


# Carregar e segmentar imagem
imagem = carrega_imagem(caminho_imagem)
contorno_calca, mask_pants = segmenta_imagem(imagem)
img_bgr, img_rgb = imagem

# Contorno da calça
img_contorno = img_rgb.copy()
cv2.drawContours(img_contorno, [contorno_calca], -1, (0, 255, 0), 2)
# Bounding Box calça
x, y, w, h = cv2.boundingRect(contorno_calca)
print(f"Bounding Box: x={x}, y={y}, w={w}, h={h}")

img_bounding_box = img_rgb.copy()
cv2.rectangle(img_bounding_box, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Salvar resultado
cv2.imwrite("saida_calca.jpg", cv2.cvtColor(img_bounding_box, cv2.COLOR_RGB2BGR))
print("Imagem final salva como 'saida_calca.jpg'")

# Plot imagem
plt.figure(figsize=(18, 6))
plt.subplot(1, 4, 1)
plt.imshow(img_rgb)
plt.title('Imagem Original')
plt.axis('off')
plt.subplot(1, 4, 2)
plt.imshow(mask_pants, cmap='gray')
plt.title('Máscara da Calça')
plt.axis('off')
plt.subplot(1, 4, 3)
plt.imshow(img_contorno)
plt.title('Contorno da Calça')
plt.axis('off')
plt.subplot(1, 4, 4)
plt.imshow(img_bounding_box)
plt.title('Bounding Box')
plt.axis('off')
plt.tight_layout()
plt.show()
