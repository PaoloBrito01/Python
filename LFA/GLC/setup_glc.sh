#!/bin/bash

# Nome do ambiente conda
ENV_NAME="GLC"

# Lista de dependências conda
CONDA_DEPENDENCIES=(
    "python=3.8"
    "numpy"
    "pyqt=5"
    "pip"
)

# Lista de dependências pip
PIP_DEPENDENCIES=(
    "pyvis"
)

# Função para verificar se um ambiente conda existe
env_exists() {
    conda env list | grep -q "$1"
}

# Função para verificar se uma dependência conda está instalada
conda_installed() {
    conda list | grep -q "^$1"
}

# Função para verificar se uma dependência pip está instalada
pip_installed() {
    pip show "$1" &> /dev/null
}

# Ativa o conda base para garantir que os comandos conda estejam disponíveis
source $(conda info --base)/etc/profile.d/conda.sh

# Verifica se o ambiente existe
if env_exists $ENV_NAME; then
    echo "O ambiente $ENV_NAME já existe. Ativando..."
    conda activate $ENV_NAME

    # Verifica e instala as dependências conda
    for dep in "${CONDA_DEPENDENCIES[@]}"; do
        package=$(echo $dep | cut -d'=' -f1)
        if ! conda_installed $package; then
            echo "Dependência conda faltando: $dep. Instalando..."
            conda install -y $dep
        fi
    done

    # Verifica e instala as dependências pip
    for dep in "${PIP_DEPENDENCIES[@]}"; do
        if ! pip_installed $dep; then
            echo "Dependência pip faltando: $dep. Instalando..."
            pip install $dep
        fi
    done
else
    echo "O ambiente $ENV_NAME não existe. Criando..."
    conda create -n $ENV_NAME -y "${CONDA_DEPENDENCIES[@]}"
    conda activate $ENV_NAME
    pip install "${PIP_DEPENDENCIES[@]}"
fi

# Executa o script Python
python glc.py