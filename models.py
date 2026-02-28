from dataclasses import dataclass
from typing import List


@dataclass
class Room:
    room_no: str
    rows: int
    columns: int


@dataclass
class SubjectData:
    name: str
    rolls: List[str]


@dataclass
class SeatEntry:
    subject: str
    roll_no: str


@dataclass
class RoomAllocation:
    room_no: str
    rows: int
    columns: int
    grid: List[List[List[SeatEntry]]]
