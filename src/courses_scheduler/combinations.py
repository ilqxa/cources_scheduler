from collections import defaultdict
from itertools import product
from typing import Any, Iterable

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

        self._time_slot_index: dict[
            TimeSlot,
            set[tuple[TimeSlot, Students, Teacher, Classroom, AcademicDiscipline]],
        ] = defaultdict(set)
        self._students_index: dict[
            Students,
            set[tuple[TimeSlot, Students, Teacher, Classroom, AcademicDiscipline]],
        ] = defaultdict(set)
        self._teacher_index: dict[
            Teacher,
            set[tuple[TimeSlot, Students, Teacher, Classroom, AcademicDiscipline]],
        ] = defaultdict(set)
        self._classroom_index: dict[
            Classroom,
            set[tuple[TimeSlot, Students, Teacher, Classroom, AcademicDiscipline]],
        ] = defaultdict(set)
        self._discipline_index: dict[
            AcademicDiscipline,
            set[tuple[TimeSlot, Students, Teacher, Classroom, AcademicDiscipline]],
        ] = defaultdict(set)

    def get_options(
        self,
        time_slot: Iterable[TimeSlot] = set(),
        students: Iterable[Students] = set(),
        teacher: Iterable[Teacher] = set(),
        classroom: Iterable[Classroom] = set(),
        academic_discipline: Iterable[AcademicDiscipline] = set(),
    ) -> set[tuple[TimeSlot, Students, Teacher, Classroom, AcademicDiscipline]]:
        return (
            set.union(*(self._time_slot_index.get(ts) or set() for ts in time_slot))
            & set.union(*(self._students_index.get(s) or set() for s in students))
            & set.union(*(self._teacher_index.get(t) or set() for t in teacher))
            & set.union(*(self._classroom_index.get(c) or set() for c in classroom))
            & set.union(
                *(self._discipline_index.get(d) or set() for d in academic_discipline)
            )
        )

    def reindex_collection(self) -> None:
        self._time_slot_index = defaultdict(set)
        self._students_index = defaultdict(set)
        self._teacher_index = defaultdict(set)
        self._classroom_index = defaultdict(set)
        self._discipline_index = defaultdict(set)

        for element in self._collection:
            ts, s, t, c, d = element
            self._time_slot_index[ts].add(element)
            self._students_index[s].add(element)
            self._teacher_index[t].add(element)
            self._classroom_index[c].add(element)
            self._discipline_index[d].add(element)


class BaseAcademicPlan(OptionsSet):
    def __init__(
        self,
        students_workload: dict[Students, dict[AcademicDiscipline, int]] = {},
        teachers_workload: dict[Teacher, dict[AcademicDiscipline, int]] = {},
        available_classrooms: set[Classroom] = set(),
        available_time_slots: set[TimeSlot] = set(),
    ) -> None:
        self.students_workload = students_workload
        self.teachers_workload = teachers_workload
        self.available_classrooms = available_classrooms
        self.available_time_slots = available_time_slots

    @staticmethod
    def reverse_dict(source: dict[Any, dict[Any, int]]) -> dict[Any, dict[Any, int]]:
        res = defaultdict(dict)
        for i1, v1 in source.items():
            for i2, v2 in v1.items():
                res[i2][i1] = v2
        return res

    def build_collection(self) -> None:
        self._collection = []

        students_by_discipline = self.reverse_dict(self.students_workload)
        teachers_by_discipline = self.reverse_dict(self.teachers_workload)

        for d in set(students_by_discipline.keys()) & set(
            teachers_by_discipline.keys()
        ):
            for ts, s, t, c in product(
                self.available_time_slots,
                students_by_discipline[d],
                teachers_by_discipline[d],
                self.available_classrooms,
            ):
                self._collection.append((ts, s, t, c, d))

        self.reindex_collection()
