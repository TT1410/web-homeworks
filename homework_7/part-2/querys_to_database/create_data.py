from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound

from database import session
from database.models import (
    Group,
    Teacher,
    Student,
    Subject,
    Grade,
)
from exception import ErrorValidation


def create_group(name: str) -> None:
    group = Group(name=name)

    session.add(group)
    try:
        session.commit()
    except IntegrityError:
        raise ErrorValidation(f"The group \"{name}\" already exists")

    print(f"ID: {group.id}, Group: {group.name}")


def create_teacher(name: str) -> None:
    teacher = Teacher(fullname=name)

    session.add(teacher)
    try:
        session.commit()
    except IntegrityError:
        raise ErrorValidation(f"The teacher \"{name}\" already exists")

    print(f"ID: {teacher.id}, Teacher: {teacher.fullname}")


def create_student(name: str, group_id: int) -> None:
    try:
        group = session.execute(
            select(Group).filter(Group.id == group_id)
        ).scalars().one()
    except NoResultFound:
        raise ErrorValidation(f"Groups for ID: {group_id} were not found")

    student = Student(fullname=name, group=group)

    session.add(student)
    try:
        session.commit()
    except IntegrityError:
        raise ErrorValidation(f"The student \"{name}\" already exists")

    print(f"ID: {student.id}, Student: {student.fullname}, Group: {group.name}")


def create_subject(name: str, teacher_id: Optional[int] = None) -> None:
    if teacher_id:
        try:
            teacher = session.execute(
                select(Teacher).filter(Teacher.id == teacher_id)
            ).scalars().one()
        except NoResultFound:
            raise ErrorValidation(f"Teacher for ID: {teacher_id} were not found")

        subject = Subject(name=name, teacher=teacher)
    else:
        subject = Subject(name=name)

    session.add(subject)
    try:
        session.commit()
    except IntegrityError:
        raise ErrorValidation(f"The subject \"{name}\" already exists")

    print(f"ID: {subject.id}, Subject: {subject.name}, Teacher: {teacher.name if teacher_id else '-'}")


def create_grade(grade: int, student_id: int, subject_id: int) -> None:
    try:
        student = session.execute(
            select(Student).filter(Student.id == student_id)
        ).scalars().one()
    except NoResultFound:
        raise ErrorValidation(f"Student for ID: {student_id} were not found")

    try:
        subject = session.execute(
            select(Subject).filter(Subject.id == subject_id)
        ).scalars().one()
    except NoResultFound:
        raise ErrorValidation(f"Subject for ID: {subject_id} were not found")

    grade = Grade(grade=grade, student=student, subject=subject)
    session.add(grade)
    session.commit()

    print(f"ID: {grade.id}, Grade: {grade.grade}, Student: {student.name}, Subject: {subject.id}")


def create_data(model: str, data: dict) -> None:
    match model, data:
        case "Group", {"name": name}:
            create_group(name)

        case "Teacher", {"name": name}:
            create_teacher(name)

        case "Student", {"name": name, "group_id": group_id}:
            create_student(name, group_id)

        case "Subject", {"name": name, "teacher_id": teacher_id}:
            create_subject(name, teacher_id)

        case "Grade", {"grade": grade, "student_id": student_id, "subject_id": subject_id}:
            create_grade(grade, student_id, subject_id)
