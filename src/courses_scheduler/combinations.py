from collections import defaultdict
from typing import Iterable

from courses_scheduler.objects import (
    AcademicDiscipline,
    Classroom,
    Students,
    Teacher,
    TimeSlot,
)


class OptionsSet:
    def __init__(
        self,
        collection: Iterable[
            tuple[TimeSlot, Students, Teacher, Classroom, AcademicDiscipline]
        ] = [],
    ) -> None:
        self._collection = list(collection)

        self._time_slot_index: dict[TimeSlot, list[int]] = defaultdict(list)
        self._students_index: dict[Students, list[int]] = defaultdict(list)
        self._teacher_index: dict[Teacher, list[int]] = defaultdict(list)
        self._classroom_index: dict[Classroom, list[int]] = defaultdict(list)
        self._discipline_index: dict[AcademicDiscipline, list[int]] = defaultdict(list)

        self.reindex_collection()

    def __len__(self) -> int:
        return len(self._collection)

    def get_options_idx(
        self,
        time_slot: Iterable[TimeSlot] | None = None,
        students: Iterable[Students] | None = None,
        teacher: Iterable[Teacher] | None = None,
        classroom: Iterable[Classroom] | None = None,
        academic_discipline: Iterable[AcademicDiscipline] | None = None,
    ) -> set[int]:
        time_slot = time_slot or self._time_slot_index.keys()
        students = students or self._students_index.keys()
        teacher = teacher or self._teacher_index.keys()
        classroom = classroom or self._classroom_index.keys()
        academic_discipline = academic_discipline or self._discipline_index.keys()

        return (
            set.union(*(set(self._time_slot_index.get(ts)) for ts in time_slot))
            & set.union(*(set(self._students_index.get(s)) for s in students))
            & set.union(*(set(self._teacher_index.get(t)) for t in teacher))
            & set.union(*(set(self._classroom_index.get(c)) for c in classroom))
            & set.union(
                *(set(self._discipline_index.get(d)) for d in academic_discipline)
            )
        )

    def reindex_collection(self) -> None:
        self._time_slot_index = defaultdict(list)
        self._students_index = defaultdict(list)
        self._teacher_index = defaultdict(list)
        self._classroom_index = defaultdict(list)
        self._discipline_index = defaultdict(list)

        for i, (ts, s, t, c, d) in enumerate(self._collection):
            self._time_slot_index[ts].append(i)
            self._students_index[s].append(i)
            self._teacher_index[t].append(i)
            self._classroom_index[c].append(i)
            self._discipline_index[d].append(i)
