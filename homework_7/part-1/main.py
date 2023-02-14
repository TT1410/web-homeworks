from sqlalchemy import func, desc, select, and_
from sqlalchemy.orm import joinedload, outerjoin

from seeds import create_fake_data
from database import session
from database.models import (
    Group,
    Teacher,
    Student,
    Subject,
    Grade,
)


def query_1() -> None:
    """
    -- 5 студентів з найвищим середнім балом з усіх предметів.
    """
    print(query_1.__doc__)

    students = session.execute(
        select(Student.fullname,
               Group.name.label("group_name"),
               func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .join(Group)
        .join(Grade)
        .group_by(Student.fullname, Group.name)
        .order_by(desc("avg_grade"))
        .limit(5)
    ).all()

    print("{0:^20}|{1:^10}| {2}".format("Студент", "Група", "Середній бал"))
    for student in students:
        print(f'{student.fullname:<20}|{student.group_name:^10}| {student.avg_grade:^10}')


def query_2(subject_id: int) -> None:
    """
    -- Cтудент з найвищим середнім балом з окремого предмету
    """
    print(query_2.__doc__)

    student = session.execute(
        select(Student.fullname,
               Subject.name.label("subject_name"),
               func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .outerjoin(Student)
        .outerjoin(Subject)
        .filter(Subject.id == subject_id)
        .group_by(Student.id, Subject.id)
        .order_by(desc("avg_grade"))
        .limit(1)
    ).one()

    print(f"Студент \"{student.fullname}\" із предмету \"{student.subject_name}\" "
          f"має середній бал \"{student.avg_grade}\"")


def query_3(subject_id: int) -> None:
    """
    -- Cередній бал в групах з окремого предмету.
    """
    print(query_3.__doc__)

    subjects = session.execute(
        select(Subject.name,
               Group.name.label("group_name"),
               func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .select_from(Grade)
        .outerjoin(Student)
        .outerjoin(Subject)
        .outerjoin(Group)
        .filter(Subject.id == subject_id)
        .group_by(Subject.name, Group.name)
        .order_by(desc("avg_grade"))
    ).all()

    print("{0:^12}|{1:^10}| {2}".format("Предмет", "Група", "Середній бал"))
    for subject in subjects:
        print(f"{subject.name:<12}|{subject.group_name:^10}| {subject.avg_grade:^10}")


def query_4() -> None:
    """
    -- Cередній бал на потоці
    """
    print(query_4.__doc__)

    stream = session.execute(
        select(func.round(func.avg(Grade.grade), 2).label("avg_grade"))
    ).one()

    print(f"Середній бал: {stream.avg_grade}")


def query_5(teacher_id: int) -> None:
    """
    -- Які предмети викладає певний викладач
    """
    print(query_5.__doc__)

    subjects = session.execute(
        select(Teacher.fullname.label("teacher_fullname"), Subject.name)
        .outerjoin(Teacher)
        .filter(Teacher.id == teacher_id)
        .order_by(Teacher.fullname)
    )

    print("{0:^20}| {1}".format("Викладач", "Предмет"))
    for subject in subjects:
        print(f"{subject.teacher_fullname:<20}| {subject.name}")


def query_6(group_id: int) -> None:
    """
    -- Список студентів в групі
    """
    print(query_6.__doc__)

    students = session.execute(
        select(Group.name.label("group_name"), Student.fullname)
        .outerjoin(Group)
        .filter(Group.id == group_id)
    ).all()

    print("{0:^10}| {1:^20}".format("Група", "Студент"))
    for student in students:
        print(f"{student.group_name:<10}| {student.fullname}")


def query_7(subject_id: int, group_id: int) -> None:
    """
    -- Оцінки студентів в групі з конкретного предмету
    """
    print(query_7.__doc__)

    grades = session.execute(
        select(Group.name.label("group_name"),
               Subject.name.label("subject_name"),
               Student.fullname.label("student_fullname"),
               Grade.date_of,
               Grade.grade)
        .select_from(Grade)
        .outerjoin(Student)
        .outerjoin(Subject)
        .outerjoin(Group)
        .filter(and_(Subject.id == subject_id, Group.id == group_id))
    ).all()

    print("{0:^10}|{1:^15}|{2:^20}|{3:^13}| {4}".format("Група", "Предмет", "Студент", "Дата оцінки", "Оцінка"))
    for grade in grades:
        print(f"{grade.group_name:<10}|{grade.subject_name:^15}|{grade.student_fullname:^20}|"
              f"{str(grade.date_of):^13}| {grade.grade}")


def query_8(teacher_id: int) -> None:
    """
    -- Середній бал, який ставить конкретний викладач зі своїх предметів
    """
    print(query_8.__doc__)

    teacher = session.execute(
        select(Teacher.fullname, func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .select_from(Grade)
        .outerjoin(Subject)
        .outerjoin(Teacher)
        .filter(Teacher.id == teacher_id)
        .group_by(Teacher.fullname)
    ).one()

    print(f"{teacher.fullname}: {teacher.avg_grade}")


def query_9(student_id: int) -> None:
    """
    -- Список предметів, на які ходить студент
    """
    print(query_9.__doc__)

    subjects = session.execute(
        select(Student.fullname.label("student_fullname"), Subject.name)
        .select_from(Grade)
        .outerjoin(Student)
        .outerjoin(Subject)
        .filter(Grade.student_id == student_id)
        .group_by(Student.fullname, Subject.name)
    ).all()

    print("{0:^20}| {1:^10}".format("Студент", "Предмет"))
    for subject in subjects:
        print(f"{subject.student_fullname:^20}| {subject.name}")


def query_10(student_id: int, teacher_id: int) -> None:
    """
    -- Список предметів, які окремому студенту читає окремий викладач
    """
    print(query_10.__doc__)

    subjects = session.execute(
        select(Student.fullname.label("student_fullname"),
               Teacher.fullname.label("teacher_fullname"),
               Subject.name)
        .select_from(Grade)
        .join(Subject, isouter=True)
        .join(Teacher, isouter=True)
        .join(Student, isouter=True)
        .filter(and_(Grade.student_id == student_id, Teacher.id == teacher_id))
        .group_by(Subject.name, Student.fullname, Teacher.fullname)
    ).all()

    print("{0:^20}|{1:^20}| {2:^10}".format("Студент", "Викладач", "Предмет"))
    for subject in subjects:
        print(f"{subject.student_fullname:<20}|{subject.teacher_fullname:^20}| {subject.name}")


def query_11(teacher_id: int, student_id: int) -> None:
    """
    -- Середня оцінка, яку ставить окремий викладач окремому студенту
    """
    print(query_11.__doc__)

    grade = session.execute(
        select(Teacher.fullname.label("teacher_fullname"),
               Student.fullname.label("student_fullname"),
               func.round(func.avg(Grade.grade), 2).label("avg_grade"))
        .outerjoin(Student)
        .outerjoin(Subject)
        .outerjoin(Teacher)
        .filter(and_(Teacher.id == teacher_id, Grade.student_id == student_id))
        .group_by(Teacher.fullname, Student.fullname)
    ).one()

    print(f"Викладач \"{grade.teacher_fullname}\" студенту \"{grade.student_fullname}\" "
          f"ставить середній бал \"{grade.avg_grade}\"")


def query_12(group_id: int, subject_id: int, ) -> None:
    """
    -- Оцінки студентів у певній групі з певного предмета на останньому занятті
    """
    print(query_12.__doc__)

    subquery = (
        select(func.max(Grade.date_of))
        .select_from(Grade)
        .outerjoin(Student)
        .outerjoin(Group)
        .filter(Grade.subject_id == subject_id)
    )

    grades = session.execute(
        select(Student.fullname.label("student_fullname"),
               Group.name.label("group"),
               Subject.name.label("subject"),
               Grade.date_of,
               Grade.grade)
        .select_from(Grade)
        .outerjoin(Student)
        .outerjoin(Subject)
        .outerjoin(Group)
        .filter(and_(Group.id == group_id, Grade.date_of == subquery.scalar_subquery()))
        .order_by(desc(Grade.date_of))
    ).all()

    print("{:^20}|{:^10}|{:^15}|{:^13}| {}"
          .format("Студент", "Група", "Предмет", "Дата уроку", "Оцінка"))
    for grade in grades:
        print(f"{grade.student_fullname:<20}|{grade.group:^10}|{grade.subject:^15}|{str(grade.date_of):^13}| "
              f"{grade.grade}")


if __name__ == '__main__':
    # create_fake_data()

    # query_1()
    # query_2(subject_id=2)
    # query_3(subject_id=5)
    # query_4()
    # query_5(teacher_id=3)
    # query_6(group_id=1)
    # query_7(subject_id=3, group_id=3)
    # query_8(teacher_id=4)
    # query_9(student_id=25)
    # query_10(student_id=33, teacher_id=3)
    # query_11(teacher_id=3, student_id=5)
    query_12(group_id=1, subject_id=7)
