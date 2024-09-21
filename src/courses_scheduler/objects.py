from pydantic import BaseModel


class Students(BaseModel):
    group_id: str

    def __hash__(self) -> str:
        return self.group_id.__hash__()

    def __repr__(self) -> str:
        return self.group_id


class Teacher(BaseModel):
    name: str

    def __hash__(self) -> str:
        return self.name.__hash__()

    def __repr__(self) -> str:
        return self.name


class Classroom(BaseModel):
    room_number: str

    def __hash__(self) -> str:
        return self.room_number.__hash__()

    def __repr__(self) -> str:
        return self.room_number


class AcademicDiscipline(BaseModel):
    title: str

    def __hash__(self) -> str:
        return self.title.__hash__()

    def __repr__(self) -> str:
        return self.title


class TimeSlot(BaseModel):
    date_from: int

    def __hash__(self) -> str:
        return self.date_from.__hash__()

    def __repr__(self) -> str:
        return self.date_from
