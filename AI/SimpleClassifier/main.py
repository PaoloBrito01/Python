import torch
from torch import nn
from torch.utils.data import DataLoader, Subset
from torchvision import datasets, models, transforms
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support as score, confusion_matrix
from PIL import Image
import os
import shutil

# ------------------------------
# Configurações
# ------------------------------
epocas = 30
tamanho_lote = 64
taxa_aprendizagem = 0.001
momentum = 0.2
paciencia = 10
tolerancia = 0.01
perc_val = 0.2

nome_rede = "resnet"
tamanho_imagens = 224

pasta_treino = os.path.abspath('./train/')
pasta_teste = os.path.abspath('./test/')

device = "cuda" if torch.cuda.is_available() else "cpu"


# Transformações para o dataset
transform = transforms.Compose([
    transforms.Resize((tamanho_imagens, tamanho_imagens)),
    transforms.ToTensor()
])


# Preparando o banco de imagens de treino e teste
if os.path.isdir(pasta_treino):
    trainig_val_data = datasets.ImageFolder(root=pasta_treino, transform=transform)
else:
    raise RuntimeError(f"Pasta de treino '{pasta_treino}' não encontrada.")

if os.path.isdir(pasta_teste):
    test_data = datasets.ImageFolder(root=pasta_teste, transform=transform)
else:
    test_data = None

# Índice - label
labels_map = {idx: label for label, idx in trainig_val_data.class_to_idx.items()}
total_classes = len(labels_map)

# Criando o modelo: seleção da arquitetura a partir do nome da rede
if nome_rede == "resnet":
    model = models.resnet18(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, total_classes)
elif nome_rede == "squeezenet":
    model = models.squeezenet1_0(pretrained=True)
    model.classifier[1] = nn.Conv2d(512, total_classes, kernel_size=(1,1))
    model.num_classes = total_classes
elif nome_rede == "densenet":
    model = models.densenet161(pretrained=True)
    model.classifier = nn.Linear(model.classifier.in_features, total_classes)

model = model.to(device)

#----------------------------------------------
# Função de classificação de uma imagem
#----------------------------------------------
def classificaumaimagem(model, caminho_imagem, transform, device, labels_map):
    img = Image.open(caminho_imagem).convert('RGB')
    img_t = transform(img).unsqueeze(0).to(device)
    model.eval()
    with torch.no_grad():
        outputs = model(img_t)
        pred_idx = int(outputs.argmax(dim=1).item())
        pred_label = labels_map.get(pred_idx, f"classe_{pred_idx}")
    return pred_label, pred_idx

# ------------------------------
# Diretório de checkpoint
# ------------------------------
cache_dir = os.path.join(os.path.dirname(__file__), "checkpoints")
os.makedirs(cache_dir, exist_ok=True)

# ------------------------------
# Carregar checkpoint existente
# ------------------------------
cache_load_path = os.path.join(cache_dir, f"trainmodelo_treinado_{nome_rede}.pth")
pasta_load_path = os.path.join(pasta_treino, f"modelo_treinado_{nome_rede}.pth")

if os.path.exists(cache_load_path):
    load_path = cache_load_path
elif os.path.exists(pasta_load_path):
    load_path = pasta_load_path
else:
    load_path = None  # Nenhum checkpoint encontrado

if load_path:
    model.load_state_dict(torch.load(load_path, map_location=device))

# ------------------------------
# Código de treinamento
# ------------------------------
if __name__ == "__main__":
    from torch.utils.tensorboard import SummaryWriter
    import torch.optim as optim
    import os
    from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
    from salva_metricas import salvar_metricas
    # Preparar dataloaders
    train_idx, val_idx = train_test_split(list(range(len(trainig_val_data))), test_size=perc_val)
    training_data = Subset(trainig_val_data, train_idx)
    val_data = Subset(trainig_val_data, val_idx)
    train_dataloader = DataLoader(training_data, batch_size=tamanho_lote, shuffle=True)
    val_dataloader = DataLoader(val_data, batch_size=tamanho_lote, shuffle=False)
    otimizador = optim.SGD(model.parameters(), lr=taxa_aprendizagem, momentum=momentum)
    funcao_perda = nn.CrossEntropyLoss()
    writer = SummaryWriter()
    # Funções de treino e validação
    def train(dataloader, model, loss_fn, optimizer):
        size = len(dataloader.dataset)
        num_batches = len(dataloader)
        model.train()
        train_loss, train_correct = 0, 0
        for batch, (X, y) in enumerate(dataloader):
            X, y = X.to(device), y.to(device)
            pred = model(X)
            loss = loss_fn(pred, y)
            train_loss += loss.item()
            train_correct += (pred.argmax(1) == y).type(torch.float).sum().item()
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        return train_loss / num_batches, train_correct / size

    def validation(dataloader, model, loss_fn):
        size = len(dataloader.dataset)
        num_batches = len(dataloader)
        model.eval()
        val_loss, val_correct = 0, 0
        with torch.no_grad():
            for X, y in dataloader:
                X, y = X.to(device), y.to(device)
                pred = model(X)
                val_loss += loss_fn(pred, y).item()
                val_correct += (pred.argmax(1) == y).type(torch.float).sum().item()
        return val_loss / num_batches, val_correct / size

    # Treinamento
    maior_acuracia = 0
    total_semMelhoria = 0
    # Criar pasta de resultados por arquitetura
    result_dir = os.path.join(os.path.dirname(__file__), "results", nome_rede)
    os.makedirs(result_dir, exist_ok=True)

    for epoca in range(epocas):
        train_loss, train_acc = train(train_dataloader, model, funcao_perda, otimizador)
        val_loss, val_acc = validation(val_dataloader, model, funcao_perda)

        print(f"Época {epoca+1}: train_loss={train_loss:.4f}, train_acc={train_acc:.4f}, val_loss={val_loss:.4f}, val_acc={val_acc:.4f}")

        # TensorBoard
        writer.add_scalar('Loss/Train', train_loss, epoca)
        writer.add_scalar('Loss/Validation', val_loss, epoca)
        writer.add_scalar('Accuracy/Train', train_acc, epoca)
        writer.add_scalar('Accuracy/Validation', val_acc, epoca)
        
        if val_acc > (maior_acuracia + tolerancia):
            save_path = os.path.join(cache_dir, f"trainmodelo_treinado_{nome_rede}.pth")
            torch.save(model.state_dict(), save_path)
            maior_acuracia = val_acc
            total_semMelhoria = 0
            print(f"Melhoria detectada. Modelo salvo em {save_path}")
        else:
            total_semMelhoria += 1

        if total_semMelhoria >= paciencia:
            print("Parando treino por paciência excedida.")
            break

    # Avaliar e salvar métricas finais **apenas uma vez, ao final do treino**
    salvar_metricas(model, val_dataloader, funcao_perda, labels_map, device, os.path.join(os.path.dirname(__file__), "results"), nome_rede)
    print("Treino concluído.")
    writer.close()
