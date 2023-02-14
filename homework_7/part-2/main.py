from exception import ErrorValidation
from parse_arguments import (
    get_command_kwargs,
    check_args,
)
import querys_to_database


def main():
    action, model, data = check_args(get_command_kwargs())

    try:
        match action:
            case "create":
                querys_to_database.create_data(model, data)
            case "update":
                querys_to_database.update_data(model, data)
            case "list":
                querys_to_database.list_data(model)
            case "remove":
                querys_to_database.remove_data(model, data)
    except ErrorValidation as e:
        print(e)


if __name__ == '__main__':
    main()
