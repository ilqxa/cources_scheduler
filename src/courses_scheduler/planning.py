from collections import defaultdict
from itertools import product
from typing import Any

from loguru import logger
from tqdm import tqdm

from courses_scheduler.combinations import OptionsSet
from courses_scheduler.objects import (
    AcademicDiscipline,
    Classroom,
    Students,
    Teacher,
    TimeSlot,
)
from courses_scheduler.optimization import PlanOptimizer


class AcademicPlan:
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

        self.optimizer = self.build_optimizer()

    @staticmethod
    def reverse_dict(source: dict[Any, dict[Any, int]]) -> dict[Any, dict[Any, int]]:
        res = defaultdict(dict)
        for i1, v1 in source.items():
            for i2, v2 in v1.items():
                res[i2][i1] = v2
        return res

    @staticmethod
    def flat_dict(source: dict[Any, dict[Any, int]]) -> dict[tuple[Any, Any], int]:
        res = {}
        for i1, v1 in source.items():
            for i2, v2 in v1.items():
                res[(i1, i2)] = v2
        return res

    def build_options(self) -> OptionsSet:
        logger.info("Start building options")
        collection = []

        students_by_discipline = self.reverse_dict(self.students_workload)
        teachers_by_discipline = self.reverse_dict(self.teachers_workload)

        for d in tqdm(
            set(students_by_discipline.keys()) & set(teachers_by_discipline.keys())
        ):
            for ts, s, t, c in product(
                self.available_time_slots,
                students_by_discipline[d],
                teachers_by_discipline[d],
                self.available_classrooms,
            ):
                collection.append((ts, s, t, c, d))

        return OptionsSet(collection)

    def build_optimizer(self) -> PlanOptimizer:
        logger.info("Start building optimizer")
        return PlanOptimizer(
            options=self.build_options(),
            students_discipline_workload=self.flat_dict(self.students_workload),
            teacher_discipline_max_workload=self.flat_dict(self.teachers_workload),
        )
