# 3D Reconstruction via Photometric Stereo

This project enables the digital 3D surface reconstruction of an object (such as limestone samples) from a series of 2D photographs.

## Principle of the Code

The program is based on the principle of **photometric stereo**. The idea is to take multiple photos of the same object with a fixed camera (top-down view), while changing the incidence angle of the light for each shot.

1. **Normals extraction:** By analyzing the shadows and brightness variations across the 5 images, the algorithm calculates the normal vector (orientation) of each surface pixel.

2. **Surface integration:** The script uses mathematics (finite differences and discrete cosine transform via Simchony's method) to "integrate" these normals and compute the altitude ($Z$) of each point.

3. **3D Rendering:** The resulting altitude matrix is converted into an interactive 3D model that can be viewed directly in a web browser.

## Prerequisites and Setup (Ubuntu / Linux)

To run this program on an Ubuntu machine, you need to install Python 3 and the required scientific libraries.

1. **Update the system and install pip (Python package manager):**

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **Install project dependencies:**
   Navigate to the root directory of the project and run:

   ```bash
   pip3 install -r requirements.txt
   ```

   *(Make sure your `requirements.txt` file contains: `numpy`, `matplotlib`, `Pillow`, `scipy`, `pandas`, `plotly` and `opencv-python`)*.

## Folder Preparation and Photo Naming

The naming of the photos is **strict**. For the mathematical calculation of the lighting matrix ($S$) to work, the algorithm reads the light source's azimuth angle directly from the file name.

* Create a folder per sample (e.g., `sample_A/`).

* Place exactly **5 photos** in it (taken from above).

* The light elevation angle must be approximately **26°**.

* **Naming:** The files must be named with the light source angle in degrees, followed by the extension (e.g., `.jpg`).

**Example of a valid folder structure:**

```text
sample_A/
├── 0.jpg      (light at 0°)
├── 72.jpg     (light at 72°)
├── 144.jpg    (light at 144°)
├── 216.jpg    (light at 216°)
└── 288.jpg    (light at 288°)
```

## Usage (Command Line)

### Step 1: Cropping and Normalization

The algorithm requires the images to be perfectly aligned and normalized in brightness.
Open a Python terminal or execute the function `recadrer_normaliser('sample_A/')`.

* **Interaction:** A window will open for each image. You must **click** with your mouse on a common reference point (a crevice, a mark) on each photo so the program automatically crops the image stack. If the images are already perfectly still and identical, you can close the windows directly.

### Step 2: Processing

Then execute the function `traitement('sample_A/')`.

### (Tip) Direct launch from the Linux terminal

If you want to run the entire program at once via a command line like in the past (`python3 reconstruction_v3.py sample_A/`), add these lines at the very end of your `reconstruction_v3.py` file:

```python
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        target_folder = sys.argv[1]
        # Make sure the folder name ends with a "/"
        if not target_folder.endswith('/'):
            target_folder += '/'
        print(f"Starting cropping for folder: {target_folder}")
        recadrer_normaliser(target_folder)
        print("Starting 3D reconstruction...")
        traitement(target_folder)
    else:
        print("Please provide the folder to process. Example: python3 reconstruction_v3.py data/")
```

## Outputs (What the code returns)

Once the processing is complete, the program generates the following items in the analyzed folder:

1. **`reconstruction.html`:** The final result. An HTML file containing an interactive 3D plot (generated with Plotly) of the reconstructed surface. You can open it with any web browser (Chrome, Firefox...) to zoom and rotate your sample.

2. **A `.jpg` image:** A backup of the depth map (named after the standard deviation of the calculated altitudes).

3. **Matplotlib windows:** During execution, the program temporarily displays the albedo image (the 2D texture without shadows) and the histogram of the calculated depths.
