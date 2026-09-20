# MRI 3D Medical Viewer

An educational / research desktop application for loading, visualizing, and
performing basic classical segmentation of brain MRI volumes, with an
interactive 3D viewport built on PyVista/VTK and a PySide6 (Qt) interface.

> **Medical Disclaimer**
> This software is intended for educational and research purposes only. It
> is **not** a medical diagnostic device, and segmentation results must
> **not** be used for clinical diagnosis or treatment decisions. The
> skull-stripping and tumor-segmentation algorithms included are classical,
> experimental image-processing heuristics — not clinically validated
> methods. See [Limitations](#limitations--experimental-segmentation) below.

---

## Features

- **Import MRI data**: DICOM (`.dcm` series or single file), NIfTI (`.nii`,
  `.nii.gz`), preserving voxel spacing, origin and orientation.
- **2D slice viewer**: synchronized axial / sagittal / coronal views, each
  with its own slice slider, plus window/level (intensity) controls.
- **Interactive 3D viewport**: rotate, zoom, pan, reset camera, fit to
  screen, and jump to standard viewing angles (front/back/top/bottom/
  left/right/isometric).
- **Visualization modes A–G**: everything / brain only / skull only / tumor
  only / brain+tumor / skull+brain / fully custom combination, switchable in
  real time without reloading the volume.
- **Preprocessing pipeline**: intensity normalization, Gaussian/median/
  non-local-means denoising, CLAHE / histogram equalization, global / Otsu /
  multi-Otsu / manual thresholding, morphological opening/closing/erosion/
  dilation.
- **Classical skull stripping** and **classical tumor segmentation**,
  clearly labeled as experimental, with an architecture designed for a
  trained deep-learning model to be swapped in later (see
  [Extending With a Trained Model](#extending-with-a-trained-ai-model)).
- **3D reconstruction**: Marching Cubes surface extraction, per-structure
  mesh smoothing/decimation, independent visibility/opacity/color per
  structure.
- **Export**: 3D meshes as `.stl` / `.obj` / `.ply`; segmentation masks
  (brain / skull / tumor / combined) as NIfTI.
- **Demo Mode**: generates a synthetic skull/brain/tumor phantom and runs the
  complete pipeline, so you can try the whole application without any real
  MRI dataset.
- **Responsive UI**: long-running operations (segmentation, reconstruction,
  file loading) run on a background thread with a progress indicator, so the
  interface never freezes.

---

## Screenshots

This is a source-code deliverable; no bundled screenshots are included. Run
**File → Demo Mode** after installation (see below) to see the full
interface — 3D viewport, 2D slice views, and the structures/processing
panels — populated with a synthetic dataset within a few seconds.

---

## Requirements

- Windows 10 or 11 (the app is pure Python/Qt and also runs on macOS/Linux,
  but these instructions focus on Windows as requested).
- Python 3.10, 3.11, or 3.12 (64-bit).
- A GPU with a working OpenGL driver is recommended for smooth 3D
  rendering, but not strictly required.

---

## Installation (Windows + Visual Studio / VS Code)

### 1. Install Python

1. Download Python from [python.org/downloads](https://www.python.org/downloads/)
   (3.10–3.12, 64-bit).
2. Run the installer. **Check "Add python.exe to PATH"** on the first
   screen before clicking Install.
3. Verify the install in a new **Command Prompt** or **PowerShell** window:

   ```powershell
   python --version
   ```

   You should see `Python 3.1x.x`.

### 2. Get the project into Visual Studio Code (or Visual Studio)

**Using VS Code (recommended):**

1. Install [Visual Studio Code](https://code.visualstudio.com/) and its
   official **Python extension** (search "Python" by Microsoft in the
   Extensions panel).
2. Unzip `MRI_3D_Viewer.zip` to a folder, e.g. `C:\Projects\MRI_3D_Viewer`.
3. In VS Code: **File → Open Folder…** and select that folder.
4. Open a terminal inside VS Code: **Terminal → New Terminal** (this opens
   PowerShell in the project folder by default).

**Using Visual Studio (2022+):**

1. Unzip the project as above.
2. **File → Open → Folder…** and select the project folder — Visual Studio
   will detect it as a Python project via its Python workload (install the
   "Python development" workload from the Visual Studio Installer if you
   don't already have it).
3. Use the built-in **Developer PowerShell** or **Terminal** panel for the
   commands below.

### 3. Create and activate a virtual environment

From the project's terminal (with the project folder as the working
directory):

```powershell
python -m venv venv
venv\Scripts\activate
```

Your prompt should now start with `(venv)`. (In VS Code, you can also let
the Python extension create/select this environment for you via the
**Python: Select Interpreter** command — pick the `venv` one afterward.)

> If PowerShell refuses to run the activation script with an execution-policy
> error, run this once in an **administrator** PowerShell, then retry:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

This installs PySide6 (GUI), NumPy/SciPy/scikit-image (numerics/image
processing), SimpleITK/nibabel/pydicom (medical image IO), and
PyVista/pyvistaqt/VTK (3D visualization). It can take a few minutes,
mostly for VTK.

### 5. Run the application

```powershell
python run.py
```

The main window should open. If PySide6 failed to install for any reason,
`run.py` prints a clear message instead of crashing with a raw traceback.

### 6. Try it: Demo Mode

Use **File → Demo Mode (synthetic MRI)**. This generates a synthetic
skull/brain/tumor phantom and runs the entire pipeline (segmentation +
3D reconstruction) automatically, so you can explore every feature —
2D slices, the 3D viewport, visualization modes, opacity/color controls,
export — without needing a real dataset.

### 7. Load a real MRI (optional)

- **File → Open MRI File…** for a single `.nii`, `.nii.gz`, or `.dcm` file
  (a `.dcm` file is auto-detected as part of a series if its folder
  contains one).
- **File → Open DICOM Folder…** to pick a folder containing a full DICOM
  series directly.

### 8. Run segmentation and view the 3D reconstruction

1. **Processing Controls** panel: adjust denoising / CLAHE / threshold
   preview options if desired (optional — sensible defaults are used
   automatically even if you skip this).
2. Click **Skull Strip** (experimental classical algorithm — see
   [Limitations](#limitations--experimental-segmentation)).
3. Click **Tumor Segmentation** (requires skull stripping to have run
   first, since it searches within the estimated brain region).
4. Click **3D Reconstruction** to generate the surface meshes.
5. Use the **Structures** panel to switch visualization modes (A–G),
   toggle individual structures, and adjust opacity/color. Use the 3D
   viewport's mouse controls (left-drag to rotate, wheel to zoom,
   right/middle-drag to pan) and **View** menu for camera presets.
6. **File → Export** to save meshes (`.stl`/`.obj`/`.ply`) or masks
   (NIfTI).

---

## Running the Tests

The test suite uses Python's built-in `unittest` (no extra dependency
required), and is also fully discoverable by `pytest` if you have it
installed. Tests that need an optional library (SimpleITK, nibabel,
PyVista) are automatically skipped if that library isn't installed, so the
suite runs in any subset of the full environment.

```powershell
python -m unittest discover -s tests -v
```

or, if you have pytest installed (`pip install pytest`):

```powershell
pytest tests/ -v
```

All non-GUI tests use synthetic data generated on the fly (see
`app/utils/demo_data.py`), so no real MRI dataset is needed to run them.

---

## Project Architecture

```
MRI_3D_Viewer/
│
├── README.md
├── requirements.txt
├── run.py                      <- entry point: python run.py
├── LICENSE
├── .gitignore
│
├── app/
│   ├── gui/                    <- PySide6 interface
│   │   ├── main_window.py      <- ties everything together, menus, worker threads
│   │   ├── controls.py         <- Structures panel + Processing Controls panel
│   │   ├── slice_viewer.py     <- axial / sagittal / coronal 2D views
│   │   ├── three_d_viewer.py   <- PyVista/pyvistaqt 3D viewport
│   │   └── workers.py          <- background QThread worker for long operations
│   │
│   ├── io/                     <- file format loaders
│   │   ├── dicom_loader.py     <- SimpleITK-based DICOM series/file loading
│   │   ├── nifti_loader.py     <- nibabel-based NIfTI load/save
│   │   └── image_loader.py     <- unified load_mri() dispatcher
│   │
│   ├── preprocessing/          <- classical image-processing building blocks
│   │   ├── normalization.py
│   │   ├── denoising.py
│   │   ├── contrast.py
│   │   ├── thresholding.py
│   │   └── morphology.py
│   │
│   ├── segmentation/           <- skull stripping / tumor segmentation
│   │   ├── base_segmenter.py   <- BaseSegmenter interface (AI-swap extension point)
│   │   ├── skull_stripping.py  <- ClassicalSkullStripper
│   │   ├── tumor_segmentation.py <- ClassicalTumorSegmenter
│   │   └── engine.py           <- SegmentationEngine orchestrator
│   │
│   ├── reconstruction/         <- masks -> 3D surface meshes
│   │   ├── marching_cubes.py   <- scikit-image Marching Cubes surface extraction
│   │   ├── mesh_generator.py   <- orchestration + MeshData <-> PyVista conversion
│   │   ├── mesh_processing.py  <- smoothing / decimation / cleaning (PyVista)
│   │   └── mesh_export.py      <- dependency-free STL/OBJ/PLY writers
│   │
│   ├── models/
│   │   └── data_models.py      <- MRIVolume, SegmentationMasks, MeshData, PipelineState
│   │
│   └── utils/
│       ├── config.py           <- default parameters, structure colors/opacities
│       ├── logging.py          <- centralized logging setup
│       ├── helpers.py          <- small shared helpers + exception types
│       └── demo_data.py        <- synthetic MRI phantom generator (Demo Mode)
│
├── tests/
│   ├── test_loaders.py
│   ├── test_preprocessing.py
│   ├── test_segmentation.py
│   └── test_reconstruction.py
│
├── data/        <- put your own MRI datasets here (empty in the repo)
└── output/      <- default location for exported files and logs
```

### Data flow

```
MRI file (.dcm / .nii / .nii.gz)
    │  app/io
    ▼
MRIVolume (NumPy array + spacing/origin/direction)
    │  app/preprocessing
    ▼
Preprocessed volume
    │  app/segmentation (ClassicalSkullStripper / ClassicalTumorSegmenter)
    ▼
SegmentationMasks (skull / brain / tumor boolean masks)
    │  app/reconstruction (Marching Cubes)
    ▼
MeshData per structure
    │  app/gui/three_d_viewer.py (PyVista/VTK)
    ▼
Interactive 3D viewport
```

---

## Limitations & Experimental Segmentation

This project intentionally distinguishes **visualization** (always
functional and geometrically accurate, given correctly loaded spacing/
orientation) from **experimental segmentation** (a best-effort classical
approximation):

- **Skull stripping** uses thresholding + morphological "peeling" of a
  fixed-thickness outer shell, because — unlike a thin bridge that erosion
  could sever — the skull and brain are adjacent along their *entire*
  shared surface in a raw scan, so simple connectivity-based methods cannot
  cleanly separate them. This is a deliberately simple, inspectable
  heuristic, not an anatomically accurate brain extraction. It will not
  match tools such as FSL BET, FreeSurfer, HD-BET, or a trained model.
- **Tumor segmentation** uses multi-level (multi-Otsu) intensity
  thresholding restricted to the estimated brain region, followed by
  morphological cleanup and size filtering. It will produce false
  positives/negatives on real data and is not a diagnostic tool.
- Both algorithms log a warning when their output looks implausible (e.g.
  a "tumor" candidate covering an unreasonable fraction of the brain), but
  they do not attempt to hide or fake a better-looking result — see
  `app/segmentation/skull_stripping.py` and `tumor_segmentation.py` for the
  exact, fully-commented algorithm.

## Extending With a Trained AI Model

The segmentation architecture is built around a small abstract interface,
`BaseSegmenter` (`app/segmentation/base_segmenter.py`):

```python
class BaseSegmenter(ABC):
    name: str
    is_experimental: bool

    @abstractmethod
    def segment(self, volume: np.ndarray, spacing=(1.0, 1.0, 1.0), **kwargs) -> np.ndarray:
        ...
```

To integrate a trained U-Net / 3D U-Net / nnU-Net / MONAI model later,
implement this interface, e.g.:

```python
class UNetSegmenter(BaseSegmenter):
    name = "unet_brain"
    is_experimental = False  # once properly validated

    def __init__(self, weights_path: str):
        self._model = load_trained_model(weights_path)  # your model-loading code

    def segment(self, volume, spacing=(1.0, 1.0, 1.0), **kwargs) -> np.ndarray:
        preprocessed = self._preprocess_for_model(volume)
        prediction = self._model.predict(preprocessed)
        return self._postprocess_to_mask(prediction, volume.shape)
```

Then construct the engine with your model in place of the classical one:

```python
from app.segmentation.engine import SegmentationEngine

engine = SegmentationEngine(
    skull_stripper=UNetSegmenter(weights_path="weights/brain_unet.pt"),
    tumor_segmenter=MONAISegmenter(weights_path="weights/tumor_monai.pt"),
)
```

**No GUI code needs to change** — `main_window.py` and the reconstruction
pipeline only ever call `segmenter.segment(...)`, never anything specific
to the classical implementation. In practice you would wire your model
choice into `MainWindow.segmentation_engine` (and optionally add a
"Segmentation Backend" menu to switch between classical/AI at runtime).

MONAI, PyTorch, or TensorFlow are **not** included in `requirements.txt`
since the base application doesn't use them — add whichever framework your
trained model needs when you take this step.

---

## Troubleshooting

- **`PySide6 is not installed`** when running `run.py`: re-run
  `pip install -r requirements.txt` inside your activated virtual
  environment.
- **3D viewport shows a text message instead of a 3D scene**: PyVista/VTK
  failed to import (often an OpenGL/driver issue). 2D slice viewing,
  segmentation, and mesh export still work; try updating your GPU drivers
  or reinstalling `pyvista pyvistaqt vtk`.
- **"No DICOM series found in this folder"**: make sure you selected the
  folder that directly contains the `.dcm` files (not a parent folder), and
  that the files belong to a single series.
- **Slow performance on very large volumes**: segmentation and
  reconstruction run on a background thread so the UI stays responsive, but
  the operations themselves take longer on large volumes — this is
  expected; watch the status-bar progress indicator.

---

## License

MIT License — see [LICENSE](LICENSE). This is an educational/research tool;
see the [Medical Disclaimer](#mri-3d-medical-viewer) at the top of this
file and in `LICENSE` for important usage restrictions.
