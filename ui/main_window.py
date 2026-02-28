from __future__ import annotations

import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import pandas as pd

from models import Room, SubjectData
from services.allocation_engine import AllocationEngine
from services.output_service import OutputService


class MainWindow:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Exam Hall Allocation System")
        self.root.geometry("760x520")

        self.rooms: list[Room] = []
        self.subjects: list[SubjectData] = []

        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Button(frame, text="Upload Rooms Excel", command=self.upload_rooms).grid(row=0, column=0, sticky="w")
        self.rooms_label = ttk.Label(frame, text="No room file uploaded")
        self.rooms_label.grid(row=0, column=1, sticky="w", padx=12)

        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=3, sticky="ew", pady=10)

        ttk.Label(frame, text="Subject Name").grid(row=2, column=0, sticky="w")
        self.subject_name = ttk.Entry(frame, width=24)
        self.subject_name.grid(row=2, column=1, sticky="w")
        ttk.Button(frame, text="Add Subject", command=self.upload_subject).grid(row=2, column=2, sticky="w")

        self.subject_list = tk.Listbox(frame, width=60, height=8)
        self.subject_list.grid(row=3, column=0, columnspan=3, sticky="ew", pady=8)

        ttk.Label(frame, text="Students per bench").grid(row=4, column=0, sticky="w")
        self.students_per_bench = ttk.Entry(frame, width=8)
        self.students_per_bench.insert(0, "2")
        self.students_per_bench.grid(row=4, column=1, sticky="w")

        ttk.Label(frame, text="Allocation mode").grid(row=5, column=0, sticky="w", pady=8)
        self.mode = ttk.Combobox(frame, values=["Column Alternating", "Zig-Zag Alternating"], state="readonly")
        self.mode.set("Column Alternating")
        self.mode.grid(row=5, column=1, sticky="w")

        ttk.Label(frame, text="Output").grid(row=6, column=0, sticky="w")
        self.want_excel = tk.BooleanVar(value=True)
        self.want_pdf = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Excel", variable=self.want_excel).grid(row=6, column=1, sticky="w")
        ttk.Checkbutton(frame, text="PDF", variable=self.want_pdf).grid(row=6, column=2, sticky="w")

        ttk.Button(frame, text="Allocate Seats", command=self.allocate).grid(row=7, column=0, pady=16, sticky="w")

        frame.columnconfigure(1, weight=1)

    def upload_rooms(self) -> None:
        path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx *.xls")])
        if not path:
            return

        df = pd.read_excel(path)
        expected = {"Room No", "Rows", "Columns"}
        if not expected.issubset(set(df.columns)):
            raise ValueError("Room sheet must contain columns: Room No, Rows, Columns")

        self.rooms = [
            Room(str(row["Room No"]).strip(), int(row["Rows"]), int(row["Columns"]))
            for _, row in df.iterrows()
        ]
        self.rooms_label.configure(text=f"Loaded {len(self.rooms)} rooms")

    def upload_subject(self) -> None:
        name = self.subject_name.get().strip()
        if not name:
            messagebox.showerror("Error", "Enter a subject name before uploading.")
            return

        path = filedialog.askopenfilename(filetypes=[("Excel", "*.xlsx *.xls")])
        if not path:
            return

        df = pd.read_excel(path)
        if "Roll No" not in df.columns:
            raise ValueError("Subject sheet must contain column: Roll No")

        rolls = [str(val).strip() for val in df["Roll No"].dropna().tolist() if str(val).strip()]
        self.subjects.append(SubjectData(name=name, rolls=rolls))
        self.subject_list.insert(tk.END, f"{name} - {len(rolls)} students")
        self.subject_name.delete(0, tk.END)

    def allocate(self) -> None:
        try:
            students_per_bench = int(self.students_per_bench.get())
            allocations = AllocationEngine.allocate(
                rooms=self.rooms,
                subjects=self.subjects,
                students_per_bench=students_per_bench,
                mode=self.mode.get(),
            )

            generated_files = []
            output_dir = Path("outputs")
            if self.want_excel.get():
                excel_path = OutputService.generate_excel(allocations, os.fspath(output_dir / "Exam_Seating.xlsx"))
                generated_files.append(excel_path)
            if self.want_pdf.get():
                pdf_path = OutputService.generate_pdf(allocations, os.fspath(output_dir / "Exam_Seating.pdf"))
                generated_files.append(pdf_path)

            if not generated_files:
                messagebox.showwarning("No Output", "Select at least one output format.")
                return

            messagebox.showinfo("Success", "Generated:\n" + "\n".join(generated_files))
        except Exception as exc:
            messagebox.showerror("Allocation Error", str(exc))
