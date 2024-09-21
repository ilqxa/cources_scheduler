from random import randint

from courses_scheduler.combinations import BaseAcademicPlan
from courses_scheduler.objects import (
    AcademicDiscipline,
    Classroom,
    Students,
    Teacher,
    TimeSlot,
)


def make_students(count: int = 1) -> list[Students]:
    return [Students(group_id=str(randint(1, 100000))) for _ in range(count)]


def make_teachers(count: int = 1) -> list[Teacher]:
    return [Teacher(name=str(randint(1, 100000))) for _ in range(count)]


def make_classrooms(count: int = 1) -> list[Classroom]:
    return [Classroom(room_number=str(randint(1, 100000))) for _ in range(count)]


def make_disciplines(count: int = 1) -> list[AcademicDiscipline]:
    return [AcademicDiscipline(title=str(randint(1, 100000))) for _ in range(count)]


def make_time_slots(count: int = 1) -> list[TimeSlot]:
    return [TimeSlot(date_from=randint(1, 100000)) for _ in range(count)]


def test_simple_plan():
    d_a = AcademicDiscipline(title="A")
    d_b = AcademicDiscipline(title="B")

    s_a = Students(group_id="A")
    s_b = Students(group_id="B")

    t_a = Teacher(name="A")
    t_b = Teacher(name="B")
    
    c_1 = Classroom(room_number="1")
    c_2 = Classroom(room_number="2")

    ts = {TimeSlot(date_from=i) for i in range(10)}
    
    ap = BaseAcademicPlan(
        students_workload={s_a: {d_a: 1}},
        teachers_workload={t_a: {d_a: 1}},
        available_classrooms=set([c_1]),
        available_time_slots=ts,
    )
    ap.build_collection()
    assert len(ap._collection) == len(ts)

    ap = BaseAcademicPlan(
        students_workload={s_a: {d_a: 1}},
        teachers_workload={t_a: {d_a: 1}},
        available_classrooms={c_1, c_2},
        available_time_slots=ts,
    )
    ap.build_collection()
    assert len(ap._collection) == len(ts) * 2
