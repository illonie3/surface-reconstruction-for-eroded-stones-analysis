# 3D Reconstruction & Surface Roughness Analysis via Photometric Stereo

This project provides a complete Python toolchain to reconstruct 3D surface topographies from 2D photographs using **Photometric Stereo**, as well as tools to run batch processing and statistical analyses on multiple rock samples. We wrotte this program to study haloclasty effects on limestones, and different way to limit this phenomenon, such as clay pads or water washings. This program can still be used for various other studies, but may need to be reshuffled. This program is inspired by another program written by jianwu21 : https://github.com/jianwu21/Photometric-Stereo.

## Prerequisites and Setup (Linux / Ubuntu)

**Install dependencies:**
   From the root directory of the repository, run:
   ```bash
   pip3 install -r requirements.txt
   ```


## I. Single-Sample 3D Reconstruction (`reconstruction_v3.py`)

This program covers the processing of an individual sample folder containing 5 directional lighting photographs.

### Principle
Photometric Stereo reconstructs 3D surface elevation ($Z$) by observing the same static surface under varying light angles:
1. **Normal Map Extraction:** Analyzes light intensity variations to compute the normal vector $(n_1, n_2, n_3)$ at each pixel.
2. **Surface Integration:** Integrates normal fields using Poisson integration / Discrete Cosine Transform (DCT) via Simchony's method (`unbiased_integrate`).
3. **Interactive 3D Rendering:** Converts the height matrix into an interactive HTML 3D visualization using Plotly.

### Folder Preparation & Photo Naming
The algorithm extracts the light source azimuth angle directly from the image filenames:

* Create a directory for your sample (e.g., `sample_A/`).
* Place **exactly 5 photos** taken from directly above (top-down view).
* Light elevation angle must be held constant at approximately **26°**.
* **File Naming:** Files must be named according to their azimuth angle in degrees (e.g., `0.jpg`, `72.jpg`, `144.jpg`, `216.jpg`, `288.jpg`).

```text
sample_A/
├── 0.jpg      (light source at 0°)
├── 72.jpg     (light source at 72°)
├── 144.jpg    (light source at 144°)
├── 216.jpg    (light source at 216°)
└── 288.jpg    (light source at 288°)
```

### Execution Steps

1. **Alignment & Brightness Normalization:**
   ```python
   from reconstruction_v3 import recadrer_normaliser
   recadrer_normaliser('sample_A/')
   ```

2. **3D Surface Reconstruction:**
   ```python
   from reconstruction_v3 import traitement
   traitement('sample_A/')
   ```

3. **Outputs Generated in `sample_A/`:**
   * `reconstruction.html`: Interactive 3D surface model viewable in any web browser.
   * `<std_dev>.jpg`: Depth map snapshot saved with the calculated standard deviation.

---

## II. Batch Analysis & Statistical Study (`GENERAL.py`)

`GENERAL.py` automates the reconstruction workflow over large experimental datasets and performs statistical studies.

### 1. Automated Batch Processing (`traitementgeneral`)

To process multiple sample folders sequentially:

1. Organise your samples inside a parent folder (e.g., `experiment_data/`):
   ```text
   experiment_data/
   ├── sample_1/
   ├── sample_2/
   └── sample_3/
   ```

2. Run batch processing with an outlier exclusion threshold $p$ (e.g., $p = 0.95$):
   ```python
   from GENERAL import traitementgeneral
   traitementgeneral('experiment_data/', p=0.95)
   ```

3. **Batch Outputs:**
   * `z.npy`: Elevation matrix saved in each sample folder for future comparison.
   * `repartition.jpg`: Depth distribution and cumulative density function (CDF) plots.
   * `extrema.txt`: Text file recording calculated minimum ($m$) and maximum ($M$) surface bounds per sample.

### 2. Weathering Analysis & Profiling (`prof_moyenne` & `minmax`)

`GENERAL.py` includes predefined experimental datasets categorised by weathering environment:
* **ALT**: Alteration under atmospheric / weathering conditions.
* **P_EAU**: Weathering in water immersion.
* **P_ARGILE**: Weathering in contact with clay.
* **INALT**: Control group (unweathered / intact rock).

To visualize surface roughness profiles and error-bar comparisons across experimental conditions:

```python
from GENERAL import prof_moyenne, minmax

# Display roughness range comparison across all samples
minmax()

# Plot average depth vs. exposure time/intensity with error bars
prof_moyenne()
```
