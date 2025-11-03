import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sn
import os
import torch
from sklearn.metrics import precision_recall_fscore_support as score, confusion_matrix

# ------------------------------
# Função para salvar métricas
# ------------------------------
def salvar_metricas(model, dataloader, loss_fn, labels_map, device, result_dir, nome_rede):
    """
    Avalia o modelo no conjunto de validação e salva métricas e matriz de confusão.

    Parâmetros:
    - model: modelo PyTorch treinado
    - dataloader: DataLoader do conjunto de validação
    - loss_fn: função de perda
    - labels_map: dicionário {índice: label}
    - device: 'cpu' ou 'cuda'
    - result_dir: diretório base onde salvar os resultados
    - nome_rede: nome da arquitetura do modelo (ex: 'resnet')
    
    Retorna:
    - precision, recall, f1 (valores globais ponderados)
    """

    # Criar pasta de resultados específica para a rede
    result_dir = os.path.join(result_dir, nome_rede)
    os.makedirs(result_dir, exist_ok=True)

    model.eval()
    y_true, y_pred = [], []
    val_loss_total = 0

    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            outputs = model(X)
            val_loss_total += loss_fn(outputs, y).item()
            preds = outputs.argmax(1)
            y_true.extend(y.cpu().numpy())
            y_pred.extend(preds.cpu().numpy())

    # Métricas globais ponderadas
    precision, recall, f1, _ = score(y_true, y_pred, average='weighted')

    # Matriz de confusão
    conf_matrix = confusion_matrix(y_true, y_pred)
    df_cm = pd.DataFrame(conf_matrix, index=[labels_map[i] for i in range(len(labels_map))],
                         columns=[labels_map[i] for i in range(len(labels_map))])
    plt.figure(figsize=(8,6))
    sn.heatmap(df_cm, annot=True, fmt='d', cmap='Blues')
    plt.ylabel('Classe Real')
    plt.xlabel('Classe Prevista')
    plt.title(f'Matriz de Confusão - {nome_rede}')
    plt.tight_layout()
    plt.savefig(os.path.join(result_dir, "matriz_confusao.png"))
    plt.close()

    # Métricas gerais
    with open(os.path.join(result_dir, "metricas_classificacao.txt"), "w") as f:
        f.write(f"Loss médio: {val_loss_total/len(dataloader):.4f}\n")
        f.write(f"Precision: {precision:.4f}\n")
        f.write(f"Recall: {recall:.4f}\n")
        f.write(f"F1-score: {f1:.4f}\n")

    # Métricas por classe
    metrics_per_class = score(y_true, y_pred, labels=list(range(len(labels_map))))
    with open(os.path.join(result_dir, "metricas_por_classe.txt"), "w") as f:
        f.write("Classe | Precision | Recall | F1\n")
        for idx, label in labels_map.items():
            f.write(f"{label} | {metrics_per_class[0][idx]:.4f} | {metrics_per_class[1][idx]:.4f} | {metrics_per_class[2][idx]:.4f}\n")

    print(f"Métricas salvas em {result_dir}")
    return precision, recall, f1
