from sqlalchemy import delete, select, and_
from sqlalchemy.exc import NoResultFound

from database import session
from database.models import (
    Group,
    Teacher,
    Student,
    Subject,
    Grade,
)
from exception import ErrorValidation


def remove_group(group_id: int) -> None:
    try:
        group = session.execute(
            delete(Group)
            .filter(Group.id == group_id)
            .returning(Group.name)
        ).one()
    except NoResultFound:
        raise ErrorValidation(f"Group with ID \"{group_id}\" not found for deletion")

    session.commit()

    print(f"\nGroup \"{group.name}\" with ID \"{group_id}\" has been successfully deleted")


def remove_teacher(teacher_id: int) -> None:
    try:
        teacher = session.execute(
            delete(Teacher)
            .filter(Teacher.id == teacher_id)
            .returning(Teacher.fullname)
        ).one()
    except NoResultFound:
        raise ErrorValidation(f"Teacher with ID \"{teacher_id}\" not found for deletion")

    session.commit()

    print(f"\nTeacher \"{teacher.fullname}\" with ID \"{teacher_id}\" has been successfully deleted")


def remove_student(student_id: int) -> None:
    try:
        student = session.execute(
            delete(Student)
            .filter(Student.id == student_id)
            .returning(Student.fullname)
        ).one()
    except NoResultFound:
        raise ErrorValidation(f"Student with ID \"{student_id}\" not found for deletion")

    session.commit()

    print(f"\nStudent \"{student.fullname}\" with ID \"{student_id}\" has been successfully deleted")


def remove_subject(subject_id: int) -> None:
    try:
        subject = session.execute(
            delete(Subject)
            .filter(Subject.id == subject_id)
            .returning(Subject.name)
        ).one()
    except NoResultFound:
        raise ErrorValidation(f"Subject with ID \"{subject_id}\" not found for deletion")

    session.commit()

    print(f"\nSubject \"{subject.name}\" with ID \"{subject_id}\" has been successfully deleted")


def remove_grade(grade_id: int) -> None:
    try:
        grade: Grade = session.execute(
            delete(Grade)
            .filter(Grade.id == grade_id)
            .returning(Grade.id, Grade.grade, Grade.date_of, Grade.student_id, Grade.subject_id)
        ).one()
    except NoResultFound:
        raise ErrorValidation(f"Grade with ID \"{grade_id}\" not found for deletion")

    session.commit()

    result = session.execute(
        select(Student.fullname.label("student_fullname"),
               Subject.name.label("subject"),
               Teacher.fullname.label("teacher_fullname"))
        .select_from(Student)
        .outerjoin(Subject, Subject.id == grade.subject_id)
        .outerjoin(Teacher, Teacher.id == Subject.teacher_id)
        .filter(and_(Student.id == grade.student_id))
    ).one()

    print(f"\nGrade \"{grade.grade}\" with ID \"{grade_id}\" has been successfully deleted.\n"
          f"This grade was given on \"{str(grade.date_of)}\" to the student \"{result.student_fullname}\" "
          f"by the teacher \"{result.teacher_fullname}\" from the subject \"{result.subject}\"")


def remove_data(model: str, data: dict) -> None:
    id_ = data.get("id")

    match model:
        case "Group":
            remove_group(id_)
        case "Teacher":
            remove_teacher(id_)
        case "Student":
            remove_student(id_)
        case "Subject":
            remove_subject(id_)
        case "Grade":
            remove_grade(id_)


if __name__ == '__main__':
    # remove_group(5)
    # remove_teacher(1)
    # remove_student(1)
    # remove_subject(1)
    remove_grade(450)
