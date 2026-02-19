# Importa a biblioteca PIL (Python Imaging Library) para manipulação de imagens
from PIL import Image
# Importa matplotlib.pyplot para exibir imagens de forma gráfica
import matplotlib.pyplot as plt

# Nome do arquivo de imagem que será usado como base
ARQUIVO = 'img01.jpeg'
# Quantidade de linhas do mosaico (3 imagens na vertical)
LINHAS = 3
# Quantidade de colunas do mosaico (3 imagens na horizontal)
COLUNAS = 3

# Converter para tons de cinza usando a média dos canais (R+G+B)/3
def filtro_cinza(img):
  largura_cinza, altura_cinza = img.size # retorna a resolução da img
  rgb = img.convert('RGB') # garanto que img esteja em RGB (3 canais)
  # cria imagem resultante em tons de cinza
  img_cinza = Image.new('RGB', (largura_cinza, altura_cinza))
  # trabalha com os pixels da imagem de entrada (in = entrada)
  px_in = rgb.load() # imagem de entrada
  # trabalha com os pixels da imagem de saída (out = saída)
  px_out = img_cinza.load()

  # criar um laço para percorrer todos os pixels da minha imagem
  for y in range(altura_cinza):
    for x in range(largura_cinza):
      r, g, b = px_in[x, y] # manipular os pixels por posição
      media_rgb = (r + g + b) // 3 # calcula média inteira
      # repliquei a media calculada para tons de cinza
      px_out[x, y] = (media_rgb, media_rgb, media_rgb)
  # retorna imagem em tons de cinza
  return img_cinza

# Converter para negativo usando a média dos canais (R+G+B)/3
def filtro_negativo(img):
  largura_negativo, altura_negativo = img.size # retorna a resolução da img
  rgb = img.convert('RGB') # garanto que img esteja em RGB (3 canais)
  # cria imagem resultante em negativo
  img_negativo = Image.new('RGB', (largura_negativo, altura_negativo))
  # trabalha com os pixels da imagem de entrada (in = entrada)
  px_in = rgb.load() # imagem de entrada
  # trabalha com os pixels da imagem de saída (out = saída)
  px_out = img_negativo.load()

  # criar um laço para percorrer todos os pixels da minha imagem
  for y in range(altura_negativo):
    for x in range(largura_negativo):
      r, g, b = px_in[x, y] # manipular os pixels por posição
      # calculo dos pixels em negativo
      px_out[x, y] = (255 - r, 255 - g, 255 - b)
  # retorna imagem em negativo
  return img_negativo


# Converter para rotacao 180º usando a média dos canais (R+G+B)/3
def filtro_rotacao_180(img):
  largura_rotacao, altura_rotacao = img.size # retorna a resolução da img
  rgb = img.convert('RGB') # garanto que img esteja em RGB (3 canais)
  # cria imagem resultante em rotacao
  img_rotacao = Image.new('RGB', (largura_rotacao, altura_rotacao))
  # trabalha com os pixels da imagem de entrada (in = entrada)
  px_in = rgb.load() # imagem de entrada
  # trabalha com os pixels da imagem de saída (out = saída)
  px_out = img_rotacao.load()

  # criar um laço para percorrer todos os pixels da minha imagem
  for y in range(altura_rotacao):
    for x in range(largura_rotacao):
      # calculo dos pixels em rotacao
      px_out[largura_rotacao - 1 - x, altura_rotacao - 1 - y] = px_in[x, y]
  # retorna imagem em rotacao
  return img_rotacao

def filtro_brilho(img):
  largura_brilho, altura_brilho = img.size 
  rgb = img.convert('RGB') 
  img_brilho = Image.new('RGB', (largura_brilho, altura_brilho))
  px_in = rgb.load()
  px_out = img_brilho.load()

  # criar um laço para percorrer todos os pixels da minha imagem
  for y in range(altura_brilho):
    for x in range(largura_brilho):
      r, g, b = px_in[x, y] # manipular os pixels por posição
      # aplico um aumento de brilho de 150 (clipping em 255)
      px_out[x, y] = (min(255, r + 150), min(255, g + 150), min(255, b + 150))
  # retorna imagem com brilho aumentado
  return img_brilho

def filtro_contraste(img):
  largura_contraste, altura_contraste = img.size
  rgb = img.convert('RGB')
  img_contraste = Image.new('RGB', (largura_contraste, altura_contraste))
  px_in = rgb.load()
  px_out = img_contraste.load()

  # criar um laço para percorrer todos os pixels da minha imagem
  fator = 2  # fator de contraste 
  for y in range(altura_contraste):
    for x in range(largura_contraste):
      # pega valores rgb
      r, g, b = px_in[x, y]  
      # aplica fator de contraste 
      r = (128 + fator * (r - 128))
      g = (128 + fator * (g - 128))
      b = (128 + fator * (b - 128))
      # Garantir que valores estejam no intervalo [0, 255]
      px_out[x, y] = (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)))
  return img_contraste

def filtro_maluco(img):
  largura_maluco, altura_maluco = img.size
  rgb = img.convert('RGB')
  img_maluco = Image.new('RGB', (largura_maluco, altura_maluco))
  px_in = rgb.load()
  px_out = img_maluco.load()

  for y in range(altura_maluco):
    for x in range(largura_maluco):
      r, g, b = px_in[x, y]
      # Troca canais de cor e aplica "pesos"
      r = (g + b) * 1
      g = (r + b) * 2
      b = (r + g) * 3
      px_out[x, y] = (r, g, b)
  return img_maluco

TRANSFORMES = [
    'normal',
    'cinza',
    'negativo',
    'rotacao',
    'brilho',
    'contraste',
    'maluco',
    'normal',
    'normal'
]

try:
    # Tenta abrir a imagem base a partir do arquivo informado
    img = Image.open(ARQUIVO)
    # Obtém as dimensões (largura e altura) da imagem original
    largura, altura = img.size

    # Calcula as dimensões do mosaico final:
    # largura total será a largura da imagem vezes o número de colunas
    largura_mosaico = largura * COLUNAS
    # altura total será a altura da imagem vezes o número de linhas
    altura_mosaico = altura * LINHAS

    # Cria uma nova imagem vazia (canvas), no modo RGB,
    # com o tamanho calculado para armazenar o mosaico
    mosaico = Image.new('RGB', (largura_mosaico, altura_mosaico))

    idx = 0 # indice linear 0..8 (percorrer o array TRANSFORMES)
    # Percorre cada posição da grade 3x3
    for lin in range(LINHAS):  # percorre as linhas
        for col in range(COLUNAS):  # percorre as colunas
            # Calcula a posição x (horizontal) onde a imagem será colada
            x = col * largura
            # Calcula a posição y (vertical) onde a imagem será colada
            y = lin * altura
            # Escolher a transformação a ser aplicada na imagem
            modo = TRANSFORMES[idx]
            # aplico tons de cinza a imagem
            if modo == 'cinza':
              img_filtrada = filtro_cinza(img)
            elif modo == 'negativo':
              img_filtrada = filtro_negativo(img)
            elif modo == 'rotacao':
              img_filtrada = filtro_rotacao_180(img)
            elif modo == 'brilho':
              img_filtrada = filtro_brilho(img)
            elif modo == 'contraste':
              img_filtrada = filtro_contraste(img)
            elif modo == 'maluco':
              img_filtrada = filtro_maluco(img)
            else: # se nao for filtro, imagem normal
              img_filtrada = img

            idx += 1 # avanço para a prox. label do TRANSFORMES

            # Cola a imagem original na posição (x, y) do mosaico
            mosaico.paste(img_filtrada, (x, y))

    # Salva o mosaico gerado em um arquivo JPEG com qualidade 95%
    mosaico.save('mosaico_3x3.jpeg', format='JPEG', quality=95)

    # Exibe o mosaico usando matplotlib
    plt.figure(figsize=(8, 8))   # Define o tamanho da janela de exibição
    plt.imshow(mosaico)          # Mostra a imagem do mosaico
    plt.title('Mosaico 3x3')     # Define o título da exibição
    plt.axis('off')              # Remove os eixos para visualização mais limpa
    plt.show()                   # Exibe a imagem na tela

# Caso o arquivo de imagem não seja encontrado, trata o erro
except FileNotFoundError:
    print(f"Arquivo '{ARQUIVO}' não encontrado.")
