from models import Room, SubjectData
from services.allocation_engine import AllocationEngine
from services.validation_engine import ValidationError


def test_allocation_column_alternating_two_subjects():
    rooms = [Room("LHC104", 2, 2)]
    subjects = [
        SubjectData("Math", ["M1", "M2", "M3"]),
        SubjectData("Physics", ["P1", "P2", "P3"]),
    ]

    allocations = AllocationEngine.allocate(rooms, subjects, students_per_bench=2, mode="Column Alternating")
    first_bench = allocations[0].grid[0][0]

    assert first_bench[0].subject == "Math"
    assert first_bench[1].subject == "Physics"


def test_capacity_validation_error():
    rooms = [Room("LHC104", 1, 1)]
    subjects = [SubjectData("Math", ["M1", "M2", "M3"])]

    try:
        AllocationEngine.allocate(rooms, subjects, students_per_bench=1, mode="Column Alternating")
    except ValidationError as exc:
        assert "Insufficient capacity" in str(exc)
    else:
        raise AssertionError("Expected capacity validation error")
