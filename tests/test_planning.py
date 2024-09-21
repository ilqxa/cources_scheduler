from courses_scheduler.planning import AcademicPlan
from courses_scheduler.objects import (
    AcademicDiscipline,
    Classroom,
    Students,
    Teacher,
    TimeSlot,
)


def test_simple_plan():
    d_a = AcademicDiscipline(title="A")

    s_a = Students(group_id="A")

    t_a = Teacher(name="A")

    c_1 = Classroom(room_number="1")
    c_2 = Classroom(room_number="2")

    ts = {TimeSlot(date_from=i) for i in range(10)}

    ap = AcademicPlan(
        students_workload={s_a: {d_a: 1}},
        teachers_workload={t_a: {d_a: 1}},
        available_classrooms=set([c_1]),
        available_time_slots=ts,
    )
    assert len(ap.optimizer.options._collection) == len(ts)
    assert len(ap.optimizer.vars) == len(ts)
    assert len(ap.optimizer.teacher_discipline_equations) == 1
    assert len(ap.optimizer.students_discipline_equations) == 1

    ap = AcademicPlan(
        students_workload={s_a: {d_a: 1}},
        teachers_workload={t_a: {d_a: 1}},
        available_classrooms={c_1, c_2},
        available_time_slots=ts,
    )
    assert len(ap.optimizer.options) == len(ts) * 2
    assert len(ap.optimizer.vars) == len(ts) * 2
    assert len(ap.optimizer.teacher_discipline_equations) == 1
    assert len(ap.optimizer.students_discipline_equations) == 1

    assert len(ap.optimizer.choosen_options_idx) == 0
    ap.optimizer.model.solve(disp=False)
    assert len(ap.optimizer.choosen_options_idx) == 1
