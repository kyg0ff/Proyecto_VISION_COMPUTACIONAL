"""Pipeline de preprocesamiento para el dataset TEM Cell Segmentation.

Lee las imagenes desde `data/`, aplica el pipeline con OpenCV/NumPy y guarda
los resultados en `outputs/`.

Uso:
    python src/preprocesamiento.py --input data --output outputs
"""

import argparse
from pathlib import Path

import cv2
import numpy as np

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}


def a_escala_de_grises(imagen):
    """Convierte una imagen BGR a escala de grises."""
    if imagen.ndim == 2:
        return imagen
    return cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)


def normalizar_intensidad(gris):
    """Normaliza la intensidad a un rango 0-255 usando min-max."""
    gris = gris.astype(np.float32)
    minimo, maximo = gris.min(), gris.max()
    if maximo - minimo < 1e-6:
        return np.zeros_like(gris, dtype=np.uint8)
    norm = (gris - minimo) / (maximo - minimo) * 255.0
    return norm.astype(np.uint8)


def reducir_ruido(gris, tamano=5):
    """Aplica un filtro de mediana para reducir ruido."""
    return cv2.medianBlur(gris, tamano)


def realzar_contraste(gris, clip_limit=2.0, grid=(8, 8)):
    """Aplica CLAHE para mejorar el contraste local."""
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid)
    return clahe.apply(gris)


def redimensionar(gris, tamano=(256, 256)):
    """Redimensiona la imagen a un tamano uniforme."""
    return cv2.resize(gris, tamano, interpolation=cv2.INTER_AREA)


def binarizar(gris):
    """Umbraliza con el metodo de Otsu."""
    _, binaria = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return binaria


def limpiar_morfologia(binaria, kernel_size=3):
    """Aplica apertura y cierre para limpiar la mascara binaria."""
    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (kernel_size, kernel_size)
    )
    apertura = cv2.morphologyEx(binaria, cv2.MORPH_OPEN, kernel)
    cierre = cv2.morphologyEx(apertura, cv2.MORPH_CLOSE, kernel)
    return cierre


def preprocesar(imagen, tamano=(256, 256)):
    """Ejecuta el pipeline completo sobre una imagen."""
    gris = a_escala_de_grises(imagen)
    gris = normalizar_intensidad(gris)
    gris = reducir_ruido(gris)
    gris = realzar_contraste(gris)
    gris = redimensionar(gris, tamano)
    binaria = binarizar(gris)
    mascara = limpiar_morfologia(binaria)
    return gris, mascara


def listar_imagenes(directorio):
    """Devuelve la lista de imagenes validas dentro de un directorio."""
    return sorted(
        p
        for p in Path(directorio).rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )


def main():
    parser = argparse.ArgumentParser(description="Preprocesamiento del dataset TEM.")
    parser.add_argument("--input", default="data", help="Carpeta con las imagenes.")
    parser.add_argument("--output", default="outputs", help="Carpeta de resultados.")
    parser.add_argument("--size", type=int, default=256, help="Lado de la imagen.")
    args = parser.parse_args()

    entrada = Path(args.input)
    salida = Path(args.output)
    salida.mkdir(parents=True, exist_ok=True)

    imagenes = listar_imagenes(entrada)
    if not imagenes:
        print(f"No se encontraron imagenes en '{entrada}'.")
        return

    tamano = (args.size, args.size)
    for ruta in imagenes:
        imagen = cv2.imread(str(ruta), cv2.IMREAD_UNCHANGED)
        if imagen is None:
            print(f"Advertencia: no se pudo leer '{ruta}'.")
            continue

        gris, mascara = preprocesar(imagen, tamano)

        relativa = ruta.relative_to(entrada).with_suffix(".png")
        ruta_gris = salida / "gris" / relativa
        ruta_mascara = salida / "mascaras" / relativa
        ruta_gris.parent.mkdir(parents=True, exist_ok=True)
        ruta_mascara.parent.mkdir(parents=True, exist_ok=True)

        cv2.imwrite(str(ruta_gris), gris)
        cv2.imwrite(str(ruta_mascara), mascara)
        print(f"Procesada: {ruta}")

    print(f"Listo. {len(imagenes)} imagenes procesadas en '{salida}'.")


if __name__ == "__main__":
    main()
