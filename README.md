
# Hand Recognition

Introduction and what not

## Demo


## Installation
```bash
pip install -r requirements.txt
```

## Usage

### Running

##### Video Capture Device (WebCam):

```bash
python3 main.py <video-capture-device-id>
```
if run without parameters it will default to video capture device with id 0

##### Specific File

```bash
python3 main.py <file-path>
```
only `.mp4`m `.jpg` and `.png` files are supported

### Basic Usage
When first open press `ENTER` to sample hand skin color, using the mouse, confirm the region by pressing `ENTER` again.

Press `C` to open the calibration window, confirm calibration by pressing `ENTER`.

Press `S` to open the sampling window, confirm the region by pressing `ENTER`.

Press `Space` to pause/resume if it's a video input.

Press `Esc` to quit the program.

## Team
 - [Margarida Abranches](https://github.com/margaridaabranches)
- [Maria Francisca Pessanha](https://github.com/franciscapessanha)
- [Paulo Correia](https://github.com/pipas)
