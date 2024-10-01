from typing import List, Dict, Tuple
from collections import Counter

from backend._base import SudokuBase
from backend.consts import FieldValue, SquareLocation
from backend.sudoku import Field, Row, Column, Square


class Solver(SudokuBase):
    """ Base class for sudoku Solvers.
    Implements standard methods for checking is sudoku:
    - is completed (all fields have values),
    - is valid (no repeating value in either row, column or square),
    - is value safe to place in given field (there is no such value in row, column or square
    """
    def __init__(self, logger_name: str, logging_level: int):
        super().__init__(logger_name=logger_name, logging_level=logging_level)

    def solve(self, *args, **kwargs) -> Tuple[bool, List[Field]]:
        """ Solve sudoku using algorithm implemented by specific Solver
        Note that it only tries to solve the sudoku - this method does not decide or give information whether solution
        exists or not, only if it was found.

        Args:
             depends on implementation

        Returns:
            (bool, list[Field]): a tuple containing boolean information if solution was found or not (as True or False)
                                 and list of fields being a solution (or at point when it was decided that Solver
                                 can't solve it)
        """
        raise NotImplementedError

    def __call__(self, *args, **kwargs) -> Tuple[bool, List[Field]]:
        """ Calling Solver as follows:
        >>> s = Solver()
        >>> s(some_arguments)
        is the same as calling the `solve` method on the instance
        >>> s.solve(some_arguments)

        Returns:
            (bool, list[Field]): a tuple containing boolean information if solution was found or not (as True or False)
                                 and list of fields being a solution (or at point when it was decided that Solver
                                 can't solve it)
        """
        return self.solve(*args, **kwargs)

    @staticmethod
    def solution_string(fields: List[Field]) -> str:
        """ Create a string built from all fields' values

        Args:
            fields (list[Fields]): list of fields to analyze

        Returns:
            (str): string containing all fields' values
        """
        return "".join(str(field) for field in fields)

    @staticmethod
    def check_validity(rows: List[Row], columns: List[Column],
                       squares: Dict[SquareLocation, Square]) -> bool:
        """ Check validity of given set of rows, columns and squares

        Args:
            rows (list[Row]): list of rows
            columns (list[Column]): list of columns
            squares (dict[SquareLocation, Square]: dict of square locations and squares

        Returns:
             (bool): True if there is no error
        """
        for container in rows + columns + list(squares.values()):
            counts = Counter(container.get_fields_values())
            if any(value > 1 for value in counts.values() if not value == FieldValue.NONE):
                return False
        return True

    @staticmethod
    def is_complete(fields: List[Field]) -> bool:
        """ Check if sudoku represented as list of fields is completed

        Args:
            fields (list[Fields]): list of fields to analyze

        Returns:
            (bool): True if given list is completed (each element has a value), False otherwise
        """
        return all(field.value for field in fields)

    @staticmethod
    def safe_to_place(row: Row, column: Column, square: Square, value: FieldValue | int) -> bool:
        """ Check if placing a certain value on the crossing of given row, column and square

        Args:
            row (Row): row
            column (Column): column
            square (Square): square
            value (FieldValue | int)

        Returns:
            (bool): True if value can be placed without breaking sudoku rule, False otherwise
        """
        if value in row.get_fields_values():
            return False
        if value in column.get_fields_values():
            return False
        if value in square.get_fields_values():
            return False
        return True
