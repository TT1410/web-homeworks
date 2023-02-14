from sqlalchemy import select, func

from database import session
from database.models import (
    Group,
    Teacher,
    Student,
    Subject,
    Grade,
)


def list_groups() -> None:
    groups: list[Group] = session.execute(
        select(Group)
    ).scalars()

    print(f"\n{'ID':^5}| {'Name':^8}")
    for group in groups:
        print(f"{group.id:^5}| {group.name}")


def list_teachers() -> None:
    teachers: list[Teacher] = session.execute(
        select(Teacher.id, Teacher.fullname, func.array_agg(Subject.name).label("subjects"))
        .outerjoin(Subject)
        .group_by(Teacher.id)
        .order_by(Teacher.id)
    ).all()

    print(f"\n{'ID':^5}| {'Full name':^25}| {'Subjects':^20}")
    for teacher in teachers:
        subjects = teacher.subjects if teacher.subjects[0] else []
        print(f"{teacher.id:^5}| {teacher.fullname:<25}| {', '.join(subjects)}")


def list_students() -> None:
    students: list[Student] = session.execute(
        select(Student)
    ).scalars()

    print(f"\n{'ID':^5}| {'Full name':^25}| {'Group':^8}")
    for student in students:
        print(f"{student.id:^5}| {student.fullname:<25}| {student.group.name}")


def list_subjects() -> None:
    subjects: list[Subject] = session.execute(
        select(Subject)
    ).scalars()

    print(f"\n{'ID':^5}| {'Name':^20}| {'Teacher':^25}")
    for subject in subjects:
        print(f"{subject.id:^5}| {subject.name:<20}| {subject.teacher.fullname}")


def list_grades() -> None:
    grades: list[Grade] = session.execute(
        select(Grade.id,
               Grade.grade,
               Grade.date_of,
               Student.fullname.label("teacher_fullname"),
               Subject.name.label("subject_name"))
        .outerjoin(Student)
        .outerjoin(Subject)
    ).all()

    print(f"\n{'ID':^5}|{'Grade':^7}| {'Date':^12}| {'Teacher':^25}| {'Subject':^15}")
    for grade in grades:
        print(f"{grade.id:^5}|{grade.grade:^7}| {str(grade.date_of):^12}| {grade.teacher_fullname:<25}| "
              f"{grade.subject_name}")


def list_data(model: str) -> None:
    match model:
        case "Group":
            list_groups()
        case "Teacher":
            list_teachers()
        case "Student":
            list_students()
        case "Subject":
            list_subjects()
        case "Grade":
            list_grades()


if __name__ == '__main__':
    # list_groups()
    # list_teachers()
    # list_students()
    # list_subjects()
    list_grades()
