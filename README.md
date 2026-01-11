# AI-Face-Recognition-System

## Requirements
- Python 3.13
- Packages: pillow, numpy, opencv-contrib-python, mysql-connector-python

Install:

```powershell
& C:/Python313/python.exe -m pip install pillow numpy opencv-contrib-python mysql-connector-python
```

## Dataset Naming
Training ID is parsed from filenames using the second dot-separated token:

- Expected pattern: `anything.<id>.anything.jpg`
- Example: `user.1.sample1.jpg`, `person.2.001.png`

Files not matching this pattern are skipped during training.

## Training Tips
- Use face-only images or let the trainer crop faces automatically.
- Provide 30–50 varied samples per person (lighting, angles, expressions).
- Keep faces centered and unobstructed; avoid backlight.

## Recognition Thresholds
This project uses LBPH distance directly; lower distance is better.

- Default acceptance: distance ≤ 75 (editable in `face_recognition.py`).
- If many correct matches are just above the threshold, raise it to 80–90.

## Run

```powershell
& C:/Python313/python.exe "e:/Mujtaba CUI/4th Semester/AI lab/Face Recognition App/Face Recognition App/main.py"
```