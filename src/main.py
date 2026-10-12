"""Pipeline principal de preprocesamiento del dataset TEM Cell Segmentation.

Lee las imagenes desde `data/`, aplica el pipeline definido en el modulo
`preprocesamiento` y guarda los resultados en `outputs/`.

Uso:
    python src/main.py --input data --output outputs
"""

import argparse
from pathlib import Path

import cv2

from preprocesamiento.preprocesamiento import IMAGE_EXTENSIONS, preprocesar


def listar_imagenes(directorio):
    """Devuelve la lista de imagenes validas dentro de un directorio."""
    return sorted(
        p
        for p in Path(directorio).rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )


def ejecutar_pipeline(entrada, salida, size=256):
    """Recorre las imagenes, las preprocesa y guarda los resultados."""
    entrada = Path(entrada)
    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)

    imagenes = listar_imagenes(entrada)
    if not imagenes:
        print(f"No se encontraron imagenes en '{entrada}'.")
        return

    tamano = (size, size)
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


def main():
    parser = argparse.ArgumentParser(description="Preprocesamiento del dataset TEM.")
    parser.add_argument("--input", default="data", help="Carpeta con las imagenes.")
    parser.add_argument("--output", default="outputs", help="Carpeta de resultados.")
    parser.add_argument("--size", type=int, default=256, help="Lado de la imagen.")
    args = parser.parse_args()

    ejecutar_pipeline(args.input, args.output, args.size)


if __name__ == "__main__":
    main()
