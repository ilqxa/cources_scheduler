from gekko import GEKKO

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

        self.vars = [
            self.model.Var(
                value=0,
                lb=0,
                ub=1,
                integer=True,
                name=str(i),
            )
            for i in range(len(options))
        ]

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
            for (s, d), workload in students_discipline_workload.items()
        ]

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
            for (t, d), max_workload in teacher_discipline_max_workload.items()
        ]

        self.obj = self.model.Minimize(self.model.sum(self.vars))

    @property
    def choosen_options_idx(self) -> list[int]:
        return [i for i, v in enumerate(self.vars) if v.VALUE[0] > 0]
