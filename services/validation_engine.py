from __future__ import annotations

from collections import Counter
from typing import List

from models import Room, SubjectData


class ValidationError(Exception):
    """Raised when input validation fails."""


class ValidationEngine:
    @staticmethod
    def validate(
        rooms: List[Room],
        subjects: List[SubjectData],
        students_per_bench: int,
    ) -> None:
        ValidationEngine._validate_rooms(rooms)
        ValidationEngine._validate_subjects(subjects)
        ValidationEngine._validate_students_per_bench(students_per_bench)

    @staticmethod
    def _validate_rooms(rooms: List[Room]) -> None:
        if not rooms:
            raise ValidationError("At least one room must be uploaded.")

        duplicates = [item for item, count in Counter([r.room_no for r in rooms]).items() if count > 1]
        if duplicates:
            raise ValidationError(f"Duplicate room numbers found: {', '.join(duplicates)}")

        for room in rooms:
            if room.rows <= 0 or room.columns <= 0:
                raise ValidationError(f"Invalid room dimensions for room {room.room_no}.")

    @staticmethod
    def _validate_subjects(subjects: List[SubjectData]) -> None:
        if not subjects:
            raise ValidationError("At least one subject must be uploaded.")

        duplicate_subjects = [
            item for item, count in Counter([s.name.strip().lower() for s in subjects]).items() if count > 1
        ]
        if duplicate_subjects:
            raise ValidationError("Duplicate subject uploads detected.")

        all_rolls = []
        for subject in subjects:
            if not subject.rolls:
                raise ValidationError(f"Subject '{subject.name}' has no roll numbers.")
            all_rolls.extend(subject.rolls)

        duplicate_rolls = [item for item, count in Counter(all_rolls).items() if count > 1]
        if duplicate_rolls:
            raise ValidationError(f"Duplicate roll numbers found: {', '.join(duplicate_rolls[:10])}")

    @staticmethod
    def _validate_students_per_bench(students_per_bench: int) -> None:
        if students_per_bench <= 0:
            raise ValidationError("Students per bench must be greater than zero.")
