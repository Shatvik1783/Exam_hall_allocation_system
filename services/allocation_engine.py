from __future__ import annotations

from typing import List

from models import Room, RoomAllocation, SeatEntry, SubjectData
from services.capacity_service import CapacityService
from services.pairing_engine import PairingEngine
from services.validation_engine import ValidationEngine


class AllocationEngine:
    MODES = {"Column Alternating", "Zig-Zag Alternating"}

    @staticmethod
    def allocate(
        rooms: List[Room],
        subjects: List[SubjectData],
        students_per_bench: int,
        mode: str,
    ) -> List[RoomAllocation]:
        if mode not in AllocationEngine.MODES:
            raise ValueError(f"Unsupported allocation mode: {mode}")

        ValidationEngine.validate(rooms, subjects, students_per_bench)
        CapacityService.validate_capacity(rooms, subjects, students_per_bench)

        pairing = PairingEngine(subjects)
        allocations: List[RoomAllocation] = []

        for room in rooms:
            grid: List[List[List[SeatEntry]]] = [[[] for _ in range(room.columns)] for _ in range(room.rows)]

            for row in range(room.rows):
                for col in range(room.columns):
                    if not pairing.has_students():
                        break

                    subject_names = pairing.snapshot_subject_names()
                    if not subject_names:
                        continue

                    order = AllocationEngine._subject_order(mode, subject_names, row, col)
                    bench_capacity = min(students_per_bench, len(order))

                    for i in range(bench_capacity):
                        item = pairing.pop_for_subject(order[i])
                        if not item:
                            continue
                        grid[row][col].append(SeatEntry(item["subject"], item["roll_no"]))

                if not pairing.has_students():
                    break

            allocations.append(RoomAllocation(room.room_no, room.rows, room.columns, grid))

        return allocations

    @staticmethod
    def _subject_order(mode: str, subject_names: List[str], row: int, col: int) -> List[str]:
        if mode == "Column Alternating":
            return subject_names

        if mode == "Zig-Zag Alternating":
            if len(subject_names) < 2:
                return subject_names
            return subject_names if ((row + col) % 2 == 0) else list(reversed(subject_names))

        return subject_names
