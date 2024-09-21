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
        self.model = GEKKO(remote=False)

        logger.info("Start declaring optimized vars")
        self.vars = [
            self.model.Var(
                value=0,
                lb=0,
                ub=1,
                integer=True,
                name=str(i),
            )
            for i in tqdm(range(len(options)))
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

        self.obj = self.model.Minimize(self.model.sum(self.vars))

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
