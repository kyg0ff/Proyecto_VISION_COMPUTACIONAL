"""Modulo de preprocesamiento para el dataset TEM Cell Segmentation.

Contiene las funciones del pipeline basadas en OpenCV/NumPy.
"""

import cv2
import numpy as np

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"}


def leer_imagen(ruta):
    """Lee una imagen (incluye TIFF) preservando su profundidad de bits."""
    return cv2.imread(str(ruta), cv2.IMREAD_UNCHANGED)


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
