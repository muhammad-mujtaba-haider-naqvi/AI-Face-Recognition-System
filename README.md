# AI-Face-Recognition-System

## Requirements
- Python 3.13
- Packages: pillow, numpy, opencv-contrib-python, mysql-connector-python

For the modern web-style desktop UI shell:
- PyQt5
- PyQtWebEngine

Install:

```powershell
& C:/Python313/python.exe -m pip install pillow numpy opencv-contrib-python mysql-connector-python
```

Install modern shell packages:

```powershell
& C:/Python313/python.exe -m pip install PyQt5 PyQtWebEngine
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

## Run Modern UI (PyQt5 + HTML/CSS)

```powershell
& C:/Python313/python.exe "e:/Mujtaba CUI/4th Semester/AI lab/Face Recognition App/Face Recognition App/modern_main.py"
```

## Migration Notes

- Existing backend logic remains unchanged.
- Existing Tkinter modules are launched by the modern UI bridge to preserve current workflows.
- Frontend assets live under `frontend/` and bridge/backend helpers live under `backend/`.
- See `UI_MIGRATION_PLAN.md` for detailed architecture and mapping.