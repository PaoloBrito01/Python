## Atividade de Detecção do Bounding Box:

Cada imagem deve ter a região da calça identificada. Para isso utilizo a segmentação por cor, utilizando o espaço de cores HSV. Definimos um intervalo de tonalidades que corresponde ao amarelo claro da calça, e assim criamos uma máscara binária destacando apenas essa região.

A partir dessa máscara, os contornos são extraídos com a função cv2.findContours(). O maior contorno encontrado corresponde à calça. Esse contorno é desenhado sobre a imagem original para visualização. 

Em seguida, eu calculo o bounding box (retângulo que limita) que envolve toda a calça. Esse retângulo fornece informações sobre a posição (x, y) e dimensões (largura e altura em pixels). Então é possível definir o tamanho ocupado pela calça na imagem e inserir um retângulo.




