"""Pipeline principal de preprocesamiento del dataset TEM Cell Segmentation.

Toma las imagenes de `data/`, aplica el pipeline definido en el modulo
`preprocesamiento` y guarda los resultados en `outputs/`.

Uso:
    python src/main.py                          # procesa todo data/
    python src/main.py --archivo ruta.tif       # procesa solo un archivo
"""

import argparse
from pathlib import Path

import cv2

from preprocesamiento.preprocesamiento import IMAGE_EXTENSIONS, leer_imagen, preprocesar

TAMANO = (256, 256)


def listar_imagenes(directorio):
    """Devuelve la lista de imagenes validas dentro de un directorio."""
    return sorted(
        p
        for p in Path(directorio).rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )


def _guardar(imagen, ruta, salida, entrada):
    """Preprocesa una imagen y guarda la imagen resultante en salida."""
    gris, _ = preprocesar(imagen, TAMANO)
    relativa = ruta.relative_to(entrada).with_suffix(".png")
    ruta_salida = salida / relativa
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(ruta_salida), gris)
    print(f"Procesada: {ruta}")


def ejecutar_pipeline(archivo=None):
    """Preprocesa imagenes y guarda los resultados en `outputs/`."""
    entrada = Path("data")
    salida = Path("outputs")
    salida.mkdir(parents=True, exist_ok=True)

    if archivo:
        imagenes = [Path(archivo)]
    else:
        imagenes = listar_imagenes(entrada)
        if not imagenes:
            print(f"No se encontraron imagenes en '{entrada}'.")
            return

    for ruta in imagenes:
        if not (ruta.is_file() and ruta.suffix.lower() in IMAGE_EXTENSIONS):
            print(f"Advertencia: '{ruta}' no es una imagen valida.")
            continue
        imagen = leer_imagen(ruta)
        if imagen is None:
            print(f"Advertencia: no se pudo leer '{ruta}'.")
            continue
        _guardar(imagen, ruta, salida, entrada)

    print(f"Listo. {len(imagenes)} imagenes procesadas en '{salida}'.")


def main():
    parser = argparse.ArgumentParser(description="Preprocesamiento del dataset TEM.")
    parser.add_argument(
        "--archivo",
        default=None,
        help="Ruta de una imagen .tif a procesar. Si no se indica, procesa todo data/.",
    )
    args = parser.parse_args()
    ejecutar_pipeline(args.archivo)


if __name__ == "__main__":
    main()