from typing import List

from backend._base import SudokuBase
from backend.consts import FieldValue
from backend.sudoku.field import Field


class SudokuContainer(SudokuBase):
    """ Base sudoku container class, which represents any kind of container of numbers.

    Attributes:
        fields (list): a list of fields in the container
    """
    def __init__(self, logger_name: str = "SudokuContainer", logging_level: int = 10):
        super().__init__(logger_name, logging_level)
        self.fields = []  # type: list[Field]

    def get_fields_values(self) -> List[FieldValue]:
        """ Get values from all fields in the container

        Returns:
            (list[FieldValue]): fields' values
        """
        values = list()
        for field in self.fields:
            if field.value:
                values.append(field.value)
        return values

    def add(self, field: Field):
        """ Add a Field to container

        Args:
            field (Field): field to add
        """
        self.fields.append(field)

    def add_many(self, fields: list[Field]):
        """ Add multiple Field instances to container

        Args:
            fields (list[Field]): a list of fields to add
        """
        for field in fields:
            self.add(field)

    def remove_possible_value(self, value: FieldValue):
        """ Remove a single value from all Fields possible_values set, so that it can't be set in any of them

        Args:
            value (FieldValue): a value to remove
        """
        for field in self.fields:
            if value in field.possible_values:
                field.eliminate(value)

    def empty_fields(self) -> List[Field]:
        """ Get a list of fields in container without values

        Returns:
            (list[Field]): a list of Fields that have no value set
        """
        return [field for field in self.fields if field.value == FieldValue.NONE]
