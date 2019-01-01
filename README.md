
# Hand Recognition

In the present work, we applied a computer vision approach,  based on the hand position and outline, to recognition of simple hand gestures: digits from zero to five and four gestures, the OK, not OK, pointer and all right. 

## Demo
![demo image](https://github.com/franciscapessanha/HandPoseRecognition/blob/master/hand.gif)


## Installation
```bash
pip install -r requirements.txt
```
## Running

#### Video Capture Device (WebCam):

```bash
python3 main.py <video-capture-device-id>
```
if run without parameters it will default to video capture device with id 0

#### Specific File

```bash
python3 main.py <file-path>
```
only `.mp4`, `.jpg` and `.png` files are supported

## Usage
When first opened press `ENTER` to sample hand skin color using the mouse, confirm the region by pressing `ENTER` again.

The threshold values calculated from this sample are saved locally on a 'thresholds' file, and are used by default the next time the program is opened. To change this values, the user can calibrate or re-sample the skin color.

To calibrate the values, press `C` to open the calibration window, confirm calibration by pressing `ENTER`.

To re-sample skin color and calculate new values, press `S` to open the sampling window, confirm the region by pressing `ENTER`.

Press `Space` to pause/resume if it's a video input.

Press `Esc` to quit the program.

## Team
 - [Margarida Abranches](https://github.com/margaridaabranches)
- [Maria Francisca Pessanha](https://github.com/franciscapessanha)
- [Paulo Correia](https://github.com/pipas)
