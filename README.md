# HandDetectionControlMouse

A Python script that uses AI Hand detection to use your webcam to control your mouse with your index finger and a blue circle. If your index finger is inside the blue circle your mouse stops, if your mouse is outsside the circle, it moves the mouse in that direction relative to the circle and if you click your index and thumb together it press your left mouse button.

![Dancing Cat](assets/demo.gif)

## How to use this

You need a webcam for this

Git clone this repo

```
git clone https://github.com/Ben-Ortiz/andDetectionControlMouse.git
```

Create your environment with Python 3.11.0

```
py -3.11 -m venv myenv
```

Activate your environment

```
myenv\Scripts\activate
```

Install the dependencies from the requirements.txt

```
pip install -r requirements.txt
```

Run it

```
python main.py
```
