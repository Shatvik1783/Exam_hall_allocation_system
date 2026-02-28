# Exam Hall Allocation System (Desktop Python App)

A modular desktop application for exam seating allocation with:

- Tkinter-based UI
- Validation layer for input integrity checks
- Deterministic seat allocation engine
- Excel and PDF output generation

## Architecture

1. **UI Layer** (`ui/main_window.py`)
2. **Processing Layer** (`services/allocation_engine.py`, `services/pairing_engine.py`)
3. **Validation Layer** (`services/validation_engine.py`)
4. **Output Layer** (`services/output_service.py`)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

## Input expectations

### Rooms Excel
Required columns:
- `Room No`
- `Rows`
- `Columns`

### Subject file(s)
For each subject upload, provide an Excel sheet with column:
- `Roll No`

## Output

Generated files are written to `outputs/`:
- `Exam_Seating.xlsx`
- `Exam_Seating.pdf`
