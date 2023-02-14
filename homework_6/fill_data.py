from random import randint, choice
import sqlite3

import faker

NUMBER_STUDENTS = 50
NUMBER_GROUPS = 3
NUMBER_TEACHERS = 5
NUMBER_SUBJECTS = 8
NUMBER_GRADES = 20


def generate_fake_data(number_students: int,
                       number_groups: int,
                       number_teachers: int,
                       number_subjects: int,
                       number_grades: int) -> tuple:
    fake_data = faker.Faker("uk-UA")

    fake_students = [fake_data.name() for _ in range(number_students)]  # здесь будем хранить студентов

    fake_groups = set()
    ua_alf = "ЙЦУКЕНГШЩЗХЇФІВАПРОЛДЖЄЯЧСМИТБЮ"

    while number_groups > len(fake_groups):
        fake_groups.add(
            str(fake_data.random_int(min=1, max=30)) + choice(ua_alf)
        )

    fake_disciplines = [fake_data.job() for _ in range(number_teachers)]  # здесь будем хранить предметы

    fake_teachers = [fake_data.name() for _ in range(number_subjects)]  # здесь будем хранить преподавателей

    fake_grades = [fake_data.random_int(min=1, max=12) for _ in range(number_grades)]  # здесь будем хранить оценки

    return fake_students, fake_groups, fake_teachers, fake_disciplines, fake_grades


def prepare_data(students: list[str],
                 groups: list[str],
                 teachers: list[str],
                 disciplines: list[str],
                 grades: list[int]) -> tuple:
    # подготавливаем список кортежей имен студентов
    data_students = [(student, randint(1, NUMBER_GROUPS),) for student in students]

    # подготавливаем список кортежей наименований групп
    data_groups = [(group,) for group in groups]

    # подготавливаем список кортежей преподавателей
    data_teachers = [(teacher,) for teacher in teachers]

    # подготавливаем список кортежей предметов
    data_disciplines = [(discipline, randint(1, NUMBER_TEACHERS),) for discipline in disciplines]

    # подготавливаем список кортежей оценок студентов
    data_grades = [
        (choice(grades), randint(1, NUMBER_STUDENTS), randint(1, NUMBER_SUBJECTS)) for _ in students
    ]

    return data_students, data_groups, data_teachers, data_disciplines, data_grades


def insert_data_to_db(students: list[tuple],
                      groups: list[tuple],
                      teachers: list[tuple],
                      subjects: list[tuple],
                      grades: list[tuple]) -> None:
    # Создадим соединение с нашей БД и получим объект курсора для манипуляций с данными
    with sqlite3.connect('salary.db') as con:

        cur = con.cursor()

        sql_to_students = """INSERT INTO students(name, group_id)
                             VALUES (?, ?)"""

        cur.executemany(sql_to_students, students)

        sql_to_groups = """INSERT INTO groups(name)
                           VALUES (?)"""

        cur.executemany(sql_to_groups, groups)

        sql_to_teachers = """INSERT INTO teachers(name)
                             VALUES (?)"""

        cur.executemany(sql_to_teachers, teachers)

        sql_to_subjects = """INSERT INTO disciplines(name, teacher_id)
                             VALUES (?, ?)"""

        cur.executemany(sql_to_subjects, subjects)

        sql_to_grades = """INSERT INTO grades(grade, student_id, discipline_id)
                           VALUES (?, ?, ?)"""

        cur.executemany(sql_to_grades, grades)

        con.commit()


if __name__ == "__main__":
    insert_data_to_db(
        *prepare_data(
            *generate_fake_data(NUMBER_STUDENTS, NUMBER_GROUPS, NUMBER_TEACHERS, NUMBER_SUBJECTS, NUMBER_GRADES)
        )
    )
