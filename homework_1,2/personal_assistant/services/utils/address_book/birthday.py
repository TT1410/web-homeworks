from datetime import date

from personal_assistant.services.utils.field import Field


class Birthday(Field):
    @Field.value.setter
    def value(self, value) -> None:
        self._value: date = self._value_validation(value)

    @staticmethod
    def _value_validation(value: str) -> date:
        """
        Format string date is YYYY.MM.DD or DD.MM.YYYY
        Instead of a dot, a comma, dash or colon is allowed
        :param value:
        :return:
        """
        value = value.strip()

        for separator in (".", ",", "-", ":", "/"):
            value, *args = value.split(separator)

            if args:
                break

        if not args or len(args) > 2:
            raise ValueError("Invalid date format. Date format should be YYYY.MM.DD or DD.MM.YYYY.")

        if int(value) > 31:
            return date(int(value), int(args[0]), int(args[1]))

        return date(int(args[1]), int(args[0]), int(value))
