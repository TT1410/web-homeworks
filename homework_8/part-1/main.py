from src.querys import (
    get_quotes_from_author,
    get_quotes_from_tags,
)


def main() -> None:
    print("Hello!\n")

    while True:
        command, *args = input("Enter command with arguments: ").split(":", maxsplit=1)

        args = args[0] if args else None

        match command, args:
            case "name", str(args):
                func = get_quotes_from_author
            case "tag" | "tags" as cmd, str(args):
                args = args.split(',') if cmd == "tags" else args
                func = get_quotes_from_tags
            case "exit", _:
                print("\nGood buy!")
                break
            case _:
                print(f"An unknown command was entered or the command arguments "
                      f"were not entered through the \":\" character!\n")
                continue

        result = func(args)

        print(result + "\n")


if __name__ == '__main__':
    main()
