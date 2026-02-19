## Calculo das posições de colagem:

Cada imagem tem uma largura e altura original. Para eu calcular as posições de colagem eu apenas multipliquei um valor para altura e largura para que uma nova imagem fosse deslocada esse mesmo tanto em altura e largura fazendo com que as imagens fiquem lado a lado sem sobreposições.

O calculo é feito na linha 20:

```         
  for linha in range(3):
    for coluna in range(3):
      x = coluna * largura_original
      y = linha * altura_original
      img_nova.paste(img, (x, y))
```

x desloca imagem na horizontal e y na vertical

### Calculo do filtro maluco:

Como a imagem trabalhada têm 3 canais de cores: R G B optei por trocar eles entre si.
O canal r: recebeu o valor de g e b.
O canal g: recebeu o valor de r e b
O canal b: recebeu o valor de r e g

Assim eles trocam de cores entre si e dão uma cor única por imagem.

### Calculo de contraste

Como acima, cada imagem tem 3 canais de cores: R G B, onde o valor de cada canal vai de 0 a 255.
Esse valor representa a itensidade de cor (0 mais fraco e 255 mais forte)
O contraste de uma imagem é a diferença entre claro e escuro. Para eu saber o que é mais claro e escuro posso
pegar o meio do caminho, ou seja, metade do valor mais forte que é 128. Mas para eu saber o quão diferente ela está do meio
eu preciso pegar o valor do canal e diminuir do meio: original - 128. Que me dá o quanto um pixel está longe ou perto do meio.
E esse fator é apenas para deixar ou não mais afastado do meio.
