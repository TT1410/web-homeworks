from sqlalchemy import select

from database import session
from database.models import (
    Group,
    Teacher,
    Student,
    Subject,
    Grade,
)
from exception import ErrorValidation


def update_group(data: dict) -> None:
    new_name = data.get("name")
    group_id: int = data.get("group_id")

    group: Group = session.execute(
        select(Group)
        .filter(Group.id == group_id)
    ).scalar()

    if not group:
        raise ErrorValidation(f"Group for ID: {group_id} were not found")

    old_name = group.name

    group.name = new_name

    session.commit()

    print(f"Group name with ID \"{group.id}\" changed from \"{old_name}\" to \"{new_name}\"")


def update_teacher(data: dict) -> None:
    new_name = data.get('name')
    teacher_id: int = data.get('teacher_id')

    teacher: Teacher = session.execute(
        select(Teacher)
        .filter(Teacher.id == teacher_id)
    ).scalar()

    if not teacher:
        raise ErrorValidation(f"Teacher for ID: {teacher_id} were not found")

    old_name = teacher.fullname

    teacher.fullname = new_name

    session.commit()

    print(f"Teacher full name with ID \"{teacher.id}\" changed from \"{old_name}\" to \"{new_name}\"")


def update_student(data: dict) -> None:
    new_name = data.get('name')
    student_id: int = data.get('student_id')

    student: Student = session.execute(
        select(Student)
        .filter(Student.id == student_id)
    ).scalar()

    if not student:
        raise ErrorValidation(f"Student for ID: {student_id} were not found")

    old_name = student.fullname

    student.fullname = new_name

    session.commit()

    print(f"Student full name with ID \"{student.id}\" changed from \"{old_name}\" to \"{new_name}\"")


def update_subject(data: dict) -> None:
    new_name = data.get('name')
    subject_id: int = data.get('subject_id')

    subject: Subject = session.execute(
        select(Subject)
        .filter(Subject.id == subject_id)
    ).scalar()

    if not subject:
        raise ErrorValidation(f"Subject for ID: {subject_id} were not found")

    old_name = subject.name

    subject.name = new_name

    session.commit()

    print(f"Subject name with ID \"{subject.id}\" changed from \"{old_name}\" to \"{new_name}\"")


def update_grade(data: dict) -> None:
    new_grade = data.get('grade')
    grade_id: int = data.get('grade_id')

    grade: Grade = session.execute(
        select(Grade)
        .filter(Grade.id == grade_id)
    ).scalar()

    if not grade:
        raise ErrorValidation(f"Grade for ID: {grade_id} were not found")

    old_grade = grade.grade

    grade.grade = new_grade

    session.commit()

    print(f"Grade with ID \"{grade.id}\" changed from \"{old_grade}\" to \"{new_grade}\"")


def update_data(model: str, data: dict) -> None:
    match model:
        case "Group":
            update_group(data)
        case "Teacher":
            update_teacher(data)
        case "Student":
            update_student(data)
        case "Subject":
            update_subject(data)
        case "Grade":
            update_grade(data)

