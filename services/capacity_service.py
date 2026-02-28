from typing import List

from models import Room, SubjectData
from services.validation_engine import ValidationError


class CapacityService:
    @staticmethod
    def room_capacity(room: Room, students_per_bench: int) -> int:
        return room.rows * room.columns * students_per_bench

    @staticmethod
    def total_capacity(rooms: List[Room], students_per_bench: int) -> int:
        return sum(CapacityService.room_capacity(room, students_per_bench) for room in rooms)

    @staticmethod
    def total_students(subjects: List[SubjectData]) -> int:
        return sum(len(subject.rolls) for subject in subjects)

    @staticmethod
    def validate_capacity(rooms: List[Room], subjects: List[SubjectData], students_per_bench: int) -> None:
        capacity = CapacityService.total_capacity(rooms, students_per_bench)
        students = CapacityService.total_students(subjects)
        if capacity < students:
            raise ValidationError(f"Insufficient capacity. Capacity={capacity}, Students={students}")
