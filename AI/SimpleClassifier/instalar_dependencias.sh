#!/bin/bash

# Entrar na pasta do script (assumindo que está na pasta do projeto)
cd "$(dirname "$0")" || exit

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual venv..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
source venv/bin/activate

# Atualizar pip
pip install --upgrade pip

# Instalar dependências
pip install torch torchvision torchaudio tensorboard pillow numpy pandas matplotlib seaborn scikit-learn

# Instalar Tkinter (Ubuntu/Debian)
sudo apt-get install python3-tk -y

echo "Dependências instaladas com sucesso!"
