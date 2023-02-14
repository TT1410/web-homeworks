import argparse


parser = argparse.ArgumentParser(add_help=True)

parser.add_argument('-a', '--action',
                    dest='action',
                    type=str,
                    required=True,
                    choices=["create", "update", "list", "remove"],
                    help="Commands")

parser.add_argument('-m', '--model',
                    dest='model',
                    type=str,
                    required=True,
                    choices=["Group", "Teacher", "Student", "Subject", "Grade"],
                    help="The model on which the operation will be performed")

parser.add_argument('-n', "--name",
                    type=str,
                    required=False)
parser.add_argument_group()

parser.add_argument('-g', '--group',
                    dest="group_id",
                    type=int,
                    required=False,
                    help="Group id")
parser.add_argument('-t', '--teacher',
                    dest="teacher_id",
                    type=int,
                    required=False,
                    help="Teacher id")
parser.add_argument('-s', '--student',
                    dest="student_id",
                    type=int,
                    required=False,
                    help="Student id")
parser.add_argument('-sub', "--subject",
                    dest="subject_id",
                    type=int,
                    required=False,
                    help="Subject id")
parser.add_argument('-gr', "--grade",
                    dest="grade_id",
                    type=int,
                    required=False,
                    help="Grade id")


def get_command_kwargs() -> dict:
    arguments = dict(parser.parse_args()._get_kwargs())

    return arguments
