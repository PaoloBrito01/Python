# DAC - Projeto Controle de Cheia Urbana:

Este projeto tem como objetivo desenvolver um sistema de monitoramento e controle de cheias urbanas, capaz de classificar imagens em duas categorias: com enchente e sem enchente. A partir dessa classificação, o sistema poderá analisar as condições do ambiente e emitir alertas em casos de enchente, auxiliando os órgãos responsáveis e a população na tomada de medidas preventivas e corretivas.

### Instalando dependências:

Execute os seguintes comandos para instalação das bibliotecas nescessárias

WINDOWS:

Utilize python 3.10 ou 3.11

```
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

```
conda install numpy pandas matplotlib seaborn scikit-learn -y
```


```
pip install tensorboard pillow
```

LINUX: 

É nescessário criar um ambiente virtual (venv) caso não esteja usando o Anaconda/Conda

```
chmod +x instalar_dependencias.sh
```

```
./instalar_dependencias.sh
```

## Executando o programa:

Para a execução do classificador separe as imagens dentro de pastas train e teste em suas respectivas classes e execute:

```
python .\main.py
```

Para a execução do programa de identificação de enchentes execute:

```
python .\app.py
```

Caso tenha GPU dedicada verifique se o Pytorch detecta corretamente com:

```
python -c "import torch; print(torch.cuda.is_available())"
```

## Construído com:

Foram utilizadas as seguintes ferramentas e o código base : exemplo_pytorch_v5

* [INOVISAO](http://git.inovisao.ucdb.br/inovisao/exemplos_pytorch/-/blob/master/exemplo_pytorch_v4.py) - Exemplo de Rede Neural Profunda 
* [Pytorch](https://docs.pytorch.org/docs/stable/index.html) - Framework para aprendizado profundo
* [Tkinter](https://docs.python.org/3/library/tkinter.html) - Módulo padrão python para interfaces gráficas
* [Exemplo Classificação](https://pytorch.org/hub/pytorch_vision_resnet/) - Exemplo de classificador

Imagens obtidas em:

* [MendeleyData](https://data.mendeley.com/datasets/t395bwcvbw/1) - Imagens de enchentes
* [Kaggle](https://www.kaggle.com/datasets/heonh0/daynight-cityview) - Imagens sem enchentes

## Autores:

* **Desenvolvedor** - *Paolo Brito* - https://github.com/PaoloBrito01
* **Desenvolvedor** - *Gustavo Espinosa* - https://github.com/Gustavoe29
* **Desenvolvedor** - *Gustavo Freitas   * - https://github.com/gustxv0






