# auto_pipeline.py
import os
import cv2
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as PSNR
from skimage.metrics import structural_similarity as SSIM
from skimage import filters
from skimage.restoration import denoise_tv_chambolle
# Pipeline automático para suavização e detecção de bordas em imagens ruidosas.
# ==========================================================
# CONFIGURAÇÕES
# ==========================================================
FOLDER_RUIDOS = "salvos/ruidos"
FOLDER_SUAVIZADOS = "salvos/suavizados"
FOLDER_BORDAS = "salvos/bordas"
CSV_OUTPUT = "salvos/resultados_metrics.csv"

suavizacoes = {
    "median": [3, 7, 11],
    "gaussian": [3, 7, 11],
    "tv": [0.05, 0.1, 0.2]
}

bordas = {
    "sobel": None,
    "prewitt": None,
    "canny": [(30,90), (50,150), (80,200)]
}

# ==========================================================
# GARANTIR PASTAS
# ==========================================================
os.makedirs(FOLDER_SUAVIZADOS, exist_ok=True)
os.makedirs(FOLDER_BORDAS, exist_ok=True)

# ==========================================================
# ENCONTRAR A IMAGEM ORIGINAL
# ==========================================================
orig_path = None
for root, dirs, files in os.walk("salvos"):
    for f in files:
        if "original" in f.lower():
            orig_path = os.path.join(root, f)

if orig_path is None:
    raise ValueError("Coloque 'original.png' dentro da pasta salvos/")

original = cv2.imread(orig_path, cv2.IMREAD_GRAYSCALE)

# ==========================================================
# CARREGAR RUIDOS
# ==========================================================
ruidos = sorted([f for f in os.listdir(FOLDER_RUIDOS) if f.endswith(".png")])

print(f"Encontradas {len(ruidos)} imagens ruidosas.")

# ==========================================================
# FUNÇÕES
# ==========================================================
def suavizar(img, tipo, param):
    if tipo == "median":
        return cv2.medianBlur(img, param)
    if tipo == "gaussian":
        return cv2.GaussianBlur(img, (param, param), 0)
    if tipo == "tv":
        img_norm = img.astype(np.float32)/255.0
        tv = denoise_tv_chambolle(img_norm, weight=param)
        return (tv*255).astype(np.uint8)

def detectar_borda(img, tipo, param=None):
    if tipo == "sobel":
        sob = filters.sobel(img)
        return (sob*255).astype(np.uint8)
    if tipo == "prewitt":
        pr = filters.prewitt(img)
        return (pr*255).astype(np.uint8)
    if tipo == "canny":
        low, high = param
        return cv2.Canny(img, low, high)

# ==========================================================
# EXECUTAR PIPELINE
# ==========================================================
results = []

for ruido_file in ruidos:
    rpath = os.path.join(FOLDER_RUIDOS, ruido_file)
    ruido = cv2.imread(rpath, cv2.IMREAD_GRAYSCALE)

    nome_base_ruido = ruido_file.replace(".png","")

    # -----------------------------
    # SUAVIZAÇÕES
    # -----------------------------
    for tipo_suav, params in suavizacoes.items():
        for p in params:

            suave = suavizar(ruido, tipo_suav, p)
            suave_name = f"{nome_base_ruido}_{tipo_suav}_{p}.png"
            suave_path = os.path.join(FOLDER_SUAVIZADOS, suave_name)
            cv2.imwrite(suave_path, suave)

            # métricas da suavização
            psnr_s = PSNR(original, suave, data_range=255)
            ssim_s = SSIM(original, suave, data_range=255)

            # -------------------------
            # DETECÇÃO DE BORDAS
            # -------------------------
            for tipo_borda, bparams in bordas.items():

                if tipo_borda == "canny":
                    for thr in bparams:
                        bord = detectar_borda(suave, "canny", thr)
                        bname = f"{suave_name.replace('.png','')}_canny_{thr[0]}-{thr[1]}.png"
                        bpath = os.path.join(FOLDER_BORDAS, bname)
                        cv2.imwrite(bpath, bord)

                        psnr_b = PSNR(original, bord, data_range=255)
                        ssim_b = SSIM(original, bord, data_range=255)

                        results.append([
                            suave_name, bname, psnr_s, ssim_s, psnr_b, ssim_b
                        ])
                else:
                    bord = detectar_borda(suave, tipo_borda)
                    bname = f"{suave_name.replace('.png','')}_{tipo_borda}.png"
                    bpath = os.path.join(FOLDER_BORDAS, bname)
                    cv2.imwrite(bpath, bord)

                    psnr_b = PSNR(original, bord, data_range=255)
                    ssim_b = SSIM(original, bord, data_range=255)

                    results.append([
                        suave_name, bname, psnr_s, ssim_s, psnr_b, ssim_b
                    ])

# ==========================================================
# SALVAR CSV
# ==========================================================
import csv

with open(CSV_OUTPUT, "w", newline="", encoding="utf8") as f:
    w = csv.writer(f)
    w.writerow(["suavizado", "borda", "psnr_suave", "ssim_suave", "psnr_borda", "ssim_borda"])
    w.writerows(results)

print("\nPROCESSO FINALIZADO!")
print(f"Imagens suavizadas em: {FOLDER_SUAVIZADOS}")
print(f"Imagens de bordas em: {FOLDER_BORDAS}")
print(f"Métricas salvas em: {CSV_OUTPUT}\n")
