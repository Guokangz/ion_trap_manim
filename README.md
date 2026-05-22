
# Ion Trap Manim Animation

Programmatic Manim animations for explaining the basic confinement mechanism of a linear Paul trap.



**Quantum Control: How Can an Electric Field Trap an Ion?**

---

## Overview

This project illustrates the basic physical picture of ion confinement in a linear Paul trap:

1. Four rod electrodes generate a radial RF quadrupole field.
2. The quadrupole potential near the trap center can be approximated as  
   `Φ(x,y) ∝ x² − y²`.
3. The instantaneous potential has a saddle-shaped profile.
4. Fast RF switching periodically exchanges the focusing and defocusing directions.
5. In the high-frequency regime, the ion experiences an effective pseudopotential confinement.

The animation sequence is designed for presentation use. Each scene is exported as an individual MP4 file so that the talk can be controlled page by page in PowerPoint.

---

## Project Motivation

In quantum control, a central task is to manipulate microscopic particles without direct mechanical contact. Optical tweezers provide a familiar example for neutral particles, while charged particles such as ions can be controlled more directly using electric fields.

However, a static electric potential cannot simply provide a stable three-dimensional trapping minimum in free space. The Paul trap avoids this limitation by using a time-dependent RF quadrupole field. The resulting dynamic stabilization can be understood through the pseudopotential picture.

This project visualizes that mechanism using concise scientific animations.

GitHub repository:

```text
https://github.com/Guokangz/ion_trap_manim
```

This project is intended only for academic presentation, learning, and technical exchange.

---

## Scenes

The formal PPT version contains four main scenes:

| Scene | Physical meaning |
|---|---|
| `RodToRadialPotential` | From the four-rod electrode structure to the radial RF quadrupole field and 2D quadrupole potential. |
| `PotentialToSaddle` | From the 2D quadrupole potential to the 3D saddle-shaped potential surface. |
| `DrivenSaddleComparison` | Qualitative comparison between slow RF switching and fast RF switching. |
| `PseudopotentialConfinement` | Time-averaged pseudopotential confinement in the high-frequency regime. |

Additional or optional scenes may be kept in the source code for development, testing, or alternative presentation structures.

---

## Tools and Methods

This project uses a Python-based programmatic animation workflow.

Main tools:

- **Python** — scripting and scene construction
- **Manim Community Edition** — scientific and mathematical animation engine
- **NumPy** — numerical and geometric calculations
- **FFmpeg / H.264** — video encoding and high-quality PPT export

The animations were generated through an AI-assisted coding workflow. AI tools were used to help draft, refactor, and organize the Manim code, rendering scripts, and project documentation. The physical structure, scene design, terminology, and final scientific presentation were manually reviewed and adjusted.

---

## Environment

The project was developed under a Conda environment named `manim`.

A typical setup is:

```bash
conda create -n manim python=3.11
conda activate manim
pip install manim numpy
```

FFmpeg is also required for video rendering and transcoding.

On Fedora, it can be installed with:

```bash
sudo dnf install ffmpeg
```

If Chinese text is used in the animations, a CJK font is recommended. The code uses:

```python
CJK_FONT = "Noto Sans CJK SC"
```

On Fedora, the font can usually be installed with:

```bash
sudo dnf install google-noto-sans-cjk-fonts
```

---

## Project Structure

```text
ion_trap_manim/
├── scenes/
│   └── ion_trap_intro.py
├── scripts/
│   ├── render_preview.sh
│   ├── render_mp4.sh
│   ├── render_ppt_hq.sh
│   ├── render_all.sh
│   ├── render_all_ppt_hq.sh
│   ├── render_full_video.sh
│   └── clean_outputs.sh
├── CHANGELOG.md
├── README.md
└── .gitignore
```

---

## Rendering

Activate the environment first:

```bash
conda activate manim
```

### Quick preview

Use this for fast checking:

```bash
bash scripts/render_preview.sh RodToRadialPotential
```

### Standard MP4 rendering

```bash
bash scripts/render_mp4.sh RodToRadialPotential
```

### PPT high-quality rendering

For final PowerPoint insertion, use the high-quality H.264 export:

```bash
bash scripts/render_ppt_hq.sh RodToRadialPotential
```

The exported video is written to:

```text
output/ppt_hq/
```

### Render all formal PPT scenes

```bash
bash scripts/render_all_ppt_hq.sh
```

The default formal PPT scene list is:

```text
RodToRadialPotential
PotentialToSaddle
DrivenSaddleComparison
PseudopotentialConfinement
```

### Render the full combined video

```bash
bash scripts/render_full_video.sh
```

The combined video is written to:

```text
output/ppt_hq/IonTrap_FullTalk_PPT_HQ.mp4
```

The individual scene videos are recommended for live presentations, while the full video is useful for sharing or backup playback.

---

## Cleaning Render Outputs

Rendered videos and temporary files are not tracked by Git.

To clean Manim outputs and Python caches:

```bash
bash scripts/clean_outputs.sh
```

This removes:

```text
media/
output/
__pycache__/
.pytest_cache/
```

---

## Git Tracking Policy

The repository is intended to track only source code, scripts, and documentation.

The following generated files are ignored:

```text
media/
output/
__pycache__/
.pytest_cache/
*.pyc
*.mp4
*.mov
*.gif
*.webm
*.ppt
*.pptx
```

Rendered videos can be regenerated locally using the scripts above.

---

## Notes on the Physics

The animations focus on the radial confinement mechanism of a linear Paul trap.

In a real linear Paul trap:

* the radial confinement is mainly provided by the RF quadrupole field;
* opposite rod electrodes have the same RF phase;
* the other pair has the opposite RF phase;
* axial confinement is usually provided by endcap electrodes or segmented DC electrodes.

The visualized saddle potential represents the instantaneous quadrupole potential near the trap center. In the high-frequency regime, the ion motion can be understood through an effective pseudopotential.

---

## Repository

GitHub repository:

```text
https://github.com/Guokangz/ion_trap_manim
```

---

## License and Use

This project is intended for academic demonstration and learning purposes.

If you reuse or modify the code, please cite or link back to this repository when appropriate.

````
