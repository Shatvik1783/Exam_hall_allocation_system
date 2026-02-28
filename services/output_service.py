from __future__ import annotations

import os
from pathlib import Path
from typing import List

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from models import RoomAllocation


class OutputService:
    @staticmethod
    def generate_excel(allocations: List[RoomAllocation], output_path: str) -> str:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        with pd.ExcelWriter(out, engine="openpyxl") as writer:
            for allocation in allocations:
                rows = []
                for row in allocation.grid:
                    rows.append([
                        "\n".join(f"{seat.subject}: {seat.roll_no}" for seat in bench) if bench else ""
                        for bench in row
                    ])
                df = pd.DataFrame(rows)
                df.to_excel(writer, sheet_name=str(allocation.room_no)[:31], index=False, header=False)

        return os.fspath(out)

    @staticmethod
    def generate_pdf(allocations: List[RoomAllocation], output_path: str) -> str:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(os.fspath(out), pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        for idx, allocation in enumerate(allocations):
            story.append(Paragraph(f"Room {allocation.room_no}", styles["Title"]))
            story.append(Spacer(1, 12))

            data = []
            for row in allocation.grid:
                data.append([
                    "\n".join(f"{seat.subject}: {seat.roll_no}" for seat in bench) if bench else "-"
                    for bench in row
                ])

            table = Table(data)
            table.setStyle(
                TableStyle(
                    [
                        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ]
                )
            )
            story.append(table)

            if idx < len(allocations) - 1:
                story.append(Spacer(1, 24))

        doc.build(story)
        return os.fspath(out)
