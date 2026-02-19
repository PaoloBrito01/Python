# Atividade - Aprendizado Profundo:

Este projeto tem como objetivo desenvolver um modelo capaz de distinguir entre condições mild (leve) e severe (severa) de estenose a partir de imagens de narinas de bulldogs, com potencial aplicação em diagnósticos.

### Instalando dependências:

Execute os seguintes comandos para instalação das bibliotecas nescessárias

WINDOWS:

Utilize python 3.10 ou 3.11

```
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

```
conda install numpy pandas matplotlib seaborn scikit-learn pillow -y
```


```
pip install tensorboard pillow
```

LINUX: 

É nescessário criar um ambiente virtual (venv) caso não esteja usando o Anaconda/Conda

```
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```
```
conda install numpy pandas matplotlib seaborn scikit-learn pillow -y
```
```
pip install tensorboard
```


## Executando o programa:

Para a execução do classificador separe as imagens dentro da pasta data, em suas respectivas classes e execute:
Dentro de /utils:
```
python .\preparaConjuntoDados.py
```

```
python .\main.py
```

Caso não funcione tente executar no diretório:

```
python src/main.py
```

Caso tenha GPU dedicada verifique se o Pytorch detecta corretamente com:

```
python -c "import torch; print(torch.cuda.is_available())"
```

## Construído com:

Foram utilizadas as seguintes ferramentas e o código base : exemplo_pytorch_v5

* [INOVISAO](http://git.inovisao.ucdb.br/inovisao/exemplos_pytorch/-/blob/master/exemplo_pytorch_v4.py) - Exemplo de Rede Neural Profunda 
* [Pytorch](https://docs.pytorch.org/docs/stable/index.html) - Framework para aprendizado profundo
* [Exemplo Classificação](https://pytorch.org/hub/pytorch_vision_resnet/) - Exemplo de classificador


## Autor:

* **Desenvolvedor** - *Paolo Brito* - https://github.com/PaoloBrito01






