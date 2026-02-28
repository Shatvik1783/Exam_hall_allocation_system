from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, List

from models import SubjectData


@dataclass
class SubjectCursor:
    name: str
    rolls: List[str]
    index: int = 0

    def has_next(self) -> bool:
        return self.index < len(self.rolls)

    def pop(self) -> str:
        value = self.rolls[self.index]
        self.index += 1
        return value


class PairingEngine:
    """Provides FCFS active-subject pairing (max 2 active subjects at a time)."""

    def __init__(self, subjects: List[SubjectData]) -> None:
        self.waiting: Deque[SubjectCursor] = deque([SubjectCursor(s.name, s.rolls) for s in subjects])
        self.active: List[SubjectCursor] = []
        self._refresh_active()

    def has_students(self) -> bool:
        return bool(self.active) or any(cursor.has_next() for cursor in self.waiting)

    def snapshot_subject_names(self) -> List[str]:
        self._refresh_active()
        return [cursor.name for cursor in self.active]

    def pop_for_subject(self, subject_name: str) -> Dict[str, str] | None:
        self._refresh_active()
        for cursor in self.active:
            if cursor.name == subject_name and cursor.has_next():
                return {"subject": cursor.name, "roll_no": cursor.pop()}
        return None

    def _refresh_active(self) -> None:
        self.active = [cursor for cursor in self.active if cursor.has_next()]

        while len(self.active) < 2 and self.waiting:
            nxt = self.waiting[0]
            if not nxt.has_next():
                self.waiting.popleft()
                continue
            self.active.append(self.waiting.popleft())
