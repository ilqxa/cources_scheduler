from gekko import GEKKO

from courses_scheduler.combinations import OptionsSet


class ProblemSolver:
    def __init__(
        self,
        options: OptionsSet,
    ) -> None:
        self.options = options
        self.model = GEKKO(remote=False)

        self.vars = [
            self.model.Var(
                value=0,
                lb=0,
                ub=1,
                integer=True,
            )
            for _ in self.options
        ]
