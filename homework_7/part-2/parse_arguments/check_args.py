from exception import ErrorValidation


def model_group(action: str, data: dict) -> dict:
    name = data.get("name")
    group_id = data.get("group_id")

    match action, name, group_id:
        case "create", str(name), _:
            return {"name": name, "group_id": group_id}

        case "update", str(name), int(group_id):
            return {"name": name, "group_id": group_id}

        case "remove", _, int(group_id):
            return {"id": group_id}

        case "list", _, _:
            return {}

        case _:
            raise ErrorValidation("name", "group_id")


def model_teacher(action: str, data: dict) -> dict:
    name = data.get("name")
    teacher_id = data.get("teacher_id")

    match action, name, teacher_id:
        case "create", str(name), _:
            return {"name": name, "teacher_id": teacher_id}

        case "update", str(name), int(teacher_id):
            return {"name": name, "teacher_id": teacher_id}

        case "remove", _, int(teacher_id):
            return {"id": teacher_id}

        case "list", _, _:
            return {}

        case _:
            raise ErrorValidation("name", "teacher_id")


def model_student(action: str, data: dict) -> dict:
    name = data.get("name")
    group_id = data.get("group_id")
    student_id = data.get("student_id")

    match action, name, group_id, student_id:
        case "create", str(name), int(group_id), _:
            return {"name": name, "group_id": group_id}

        case "update", str(name), _, int(student_id):
            return {"name": name, "student_id": student_id}

        case "remove", _, _, int(student_id):
            return {"id": student_id}

        case "list", _, _, _:
            return {}

        case _:
            raise ErrorValidation("name", "group_id", "student_id")


def model_subject(action: str, data: dict) -> dict:
    name = data.get("name")
    teacher_id = data.get("teacher_id")
    subject_id = data.get("subject_id")

    match action, name, teacher_id, subject_id:

        case "create", str(name), int(teacher_id), _:
            return {"name": name, "teacher_id": teacher_id}

        case "update", str(name), _, int(subject_id):
            return {"name": name, "subject_id": subject_id}

        case "remove", _, _, int(subject_id):
            return {"id": subject_id}

        case "list", _, _, _:
            return {}

        case _:
            raise ErrorValidation("name", "teacher_id", "subject_id")


def model_grade(action: str, data: dict) -> dict:
    grade_id = data.get("grade_id")
    grade = data.get("grade")
    student_id = data.get("student_id")
    subject_id = data.get("subject_id")

    match action, grade, grade_id, student_id, subject_id:

        case "create", str(grade), _, int(student_id), int(subject_id):
            return {"grade": grade, "student_id": student_id, "subject_id": subject_id}

        case "update", str(grade), _, int(grade_id), _, _:
            return {"grade": grade, "grade_id": grade_id}

        case "remove", _, int(grade_id), _, _:
            return {"id": grade_id}

        case "list", _, _, _, _:
            return {}

        case _:
            raise ErrorValidation("grade", "grade_id", "student_id", "subject_id")


def check_args(data: dict) -> tuple[str, str, dict]:
    action = data.get("action")
    model = data.get("model")

    try:
        match model:
            case "Group":
                data = model_group(action, data)
            case "Teacher":
                data = model_teacher(action, data)
            case "Student":
                data = model_student(action, data)
            case "Subject":
                data = model_subject(action, data)
            case "Grade":
                data = model_grade(action, data)
    except ErrorValidation as e:
        raise ErrorValidation(f"One or more mandatory arguments to the {action} command of the "
                              f"\"{model}\" model are not specified.\n"
                              f"Arguments model: {e.args}")

    return action, model, data
