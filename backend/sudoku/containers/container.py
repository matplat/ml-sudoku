from typing import List

from backend._base import SudokuBase
from backend.consts import FieldValue
from backend.sudoku.field import Field


class SudokuContainer(SudokuBase):
    def __init__(self, logger_name: str = "SudokuContainer", logging_level: int = 10):
        super().__init__(logger_name, logging_level)
        self.fields = []  # type: list[Field]

    def get_fields_values(self) -> List[FieldValue]:
        """

        :return:
        """
        values = list()
        for field in self.fields:
            if field.value:
                values.append(field.value)
        return values

    def add(self, field: Field):
        """

        :param field:
        :return:
        """
        self.fields.append(field)

    def add_many(self, fields: list[Field]):
        """

        :param fields:
        :return:
        """
        for field in fields:
            self.add(field)

    def remove_possible_value(self, value: FieldValue):
        for field in self.fields:
            if value in field.possible_values:
                field.eliminate(value)

    def empty_fields(self) -> List[Field]:
        return [field for field in self.fields if field.value == FieldValue.NONE]
