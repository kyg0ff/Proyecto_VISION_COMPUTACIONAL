# Proyecto de Visión Computacional - Segmentación de Células TEM

Proyecto semestral de la asignatura **Visión Computacional**. Consiste en escoger un
dataset de imágenes desafiador, **preprocesar** sus imágenes y almacenar el trabajo en
este repositorio.

## Integrantes (máximo 3)

- `<Nombre Integrante 1>`
- `<Nombre Integrante 2>`
- `<Nombre Integrante 3>`

## Objetivo

Escoger un dataset de imágenes desafiador para el proyecto semestral y aplicar un
pipeline de **preprocesamiento** con Python, OpenCV y NumPy.

**Fase actual:** preprocesamiento del dataset.
**Fases futuras:** segmentación / clasificación de las células.

## Dataset

**Transmission Electron Microscopy (TEM) Cell Segmentation Datasets**
Grupo de Visión por Computadora, Universidad de Freiburg.
https://lmb.informatik.uni-freiburg.de/resources/datasets/tem.en.html

La colección contiene 6 subconjuntos independientes de imágenes de microscopía
electrónica de transmisión con sus máscaras de segmentación:

| Subconjunto |
|---|
| BMMC (Bone Marrow-Derived Mast Cells) |
| Jurkat Cell |
| Primary Mouse B Cell |
| Primary Human B Cell |
| J558L |
| Human Blast |

**Uso:** los datos son para fines de investigación; se prohíbe su uso comercial.

### Cita

> Volker Morath, Margret Keuper, Marta Rodriguez-Franco, Sumit Deswal, Gina Fiala,
> Britta Blumenthal, Daniel Kaschek, Jens Timmer, Gunther Neuhaus, Olaf Ronneberger,
> Wolfgang Werner A. Schamel: *Semi-automatic procedure for the determination of the
> cell surface area used in systems immunology*, Frontiers in Biosciences, 2012.

## Estructura del repositorio

```
Proyecto_VISION_COMPUTACIONAL/
├── data/                    # Dataset (imágenes crudas y procesadas)
├── src/
│   ├── preprocesamiento/    # Funciones del pipeline (preprocesamiento.py)
│   └── main.py              # Punto de entrada que ejecuta el pipeline
├── outputs/                 # Resultados generados
├── .gitignore
└── README.md
```

## Requisitos e instalación

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install numpy opencv-python matplotlib scikit-image
```

Dependencias:

| Paquete | Uso |
|---|---|
| `numpy` | Operaciones matriciales sobre las imágenes |
| `opencv-python` | Carga, filtros y procesamiento de imágenes |
| `matplotlib` | Visualización de resultados |
| `scikit-image` | Utilidades adicionales de procesamiento |

## Uso

1. Descargar el dataset y colocarlo en `data/`.
2. Ejecutar el preprocesamiento:

```bash
python src/main.py
```

3. Los resultados se guardan en `outputs/`.

## Pipeline de preprocesamiento

1. **Conversión a escala de grises.**
2. **Normalización de intensidad** para estabilizar el contraste.
3. **Reducción de ruido** (filtro gaussiano / mediana).
4. **Realce de contraste** con CLAHE (ecualización adaptativa).
5. **Redimensionado** a un tamaño uniforme.
6. **Binarización / umbralización.**
7. **Operaciones morfológicas** para limpiar las máscaras.

## Licencia

Uso exclusivamente académico y de investigación.
