from collections import defaultdict
from copy import copy

from gekko import GEKKO
from loguru import logger
from tqdm import tqdm

from courses_scheduler.combinations import OptionsSet
from courses_scheduler.objects import AcademicDiscipline, Students, Teacher


class PlanOptimizer:
    def __init__(
        self,
        options: OptionsSet,
        students_discipline_workload: dict[
            tuple[Students, AcademicDiscipline], int
        ] = {},
        teacher_discipline_max_workload: dict[
            tuple[Teacher, AcademicDiscipline], int
        ] = {},
    ) -> None:
        self.options = options
        self.students_discipline_workload = students_discipline_workload
        self.teacher_discipline_max_workload = teacher_discipline_max_workload

        self.model = GEKKO(remote=False)
        self.model.options.SOLVER = 1
        self.model.options.REDUCE = 3
        self.model.options.DIAGLEVEL = 0
        # self.model.options.IMODE = 2
        # self.model.options.OTOL = 1e-4

        logger.info("Start declaring optimized vars")
        self.vars = [
            self.model.Var(
                value=val,
                lb=0,
                ub=1,
                integer=True,
                name=str(i),
            )
            for i, val in tqdm(zip(range(len(options)), self.make_first_approx()))
        ]

        logger.info("Start declaring students_discipline equations")
        self.students_discipline_equations = [
            self.model.Equation(
                self.model.sum(
                    [
                        self.vars[o_id]
                        for o_id in options.get_options_idx(
                            students=(s,), academic_discipline=(d,)
                        )
                    ]
                )
                == workload
            )
            for (s, d), workload in tqdm(students_discipline_workload.items())
        ]

        logger.info("Start declaring teacher_discipline equations")
        self.teacher_discipline_equations = [
            self.model.Equation(
                self.model.sum(
                    [
                        self.vars[o_id]
                        for o_id in options.get_options_idx(
                            teacher=(t,), academic_discipline=(d,)
                        )
                    ]
                )
                <= max_workload
            )
            for (t, d), max_workload in tqdm(teacher_discipline_max_workload.items())
        ]

        self.obj = self.model.Minimize(
            self.model.sum(self.vars)
            + self.model.sum(
                [v * ts.date_from for (ts, _, _, _, _), v in zip(self.options, self.vars)]
            )
        )

    @property
    def var_values(self) -> list[int]:
        res = []
        for v in self.vars:
            try:
                res.append(int(v.VALUE[0]))
            except TypeError:
                res.append(0)
        return res

    @property
    def choosen_options_idx(self) -> list[int]:
        return [i for i, v in enumerate(self.var_values) if v > 0]

    @property
    def choosen_options(self) -> list[int]:
        return [self.options[i] for i, v in enumerate(self.var_values) if v > 0]

    def test_solution_existing(self) -> bool:
        discipline_needs = defaultdict(int)
        for (_, d), v in self.students_discipline_workload.items():
            discipline_needs[d] += v

        discipline_resources = defaultdict(int)
        for (_, d), v in self.teacher_discipline_max_workload.items():
            discipline_resources[d] += v

        for d, needs in discipline_needs.items():
            if needs < discipline_resources[d]:
                return False

        return True

    def make_first_approx(self) -> list[int]:
        sd_balance = copy(self.students_discipline_workload)
        td_balance = copy(self.teacher_discipline_max_workload)

        res = []
        for ts, s, t, c, d in self.options:
            if sd_balance[(s, d)] - 1 >= 0 and td_balance[(t, d)] - 1 >= 0:
                sd_balance[(s, d)] -= 1
                td_balance[(t, d)] -= 1
                res.append(1)
            else:
                res.append(0)
        return res
