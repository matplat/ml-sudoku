from typing import List, Dict
from collections import Counter

from backend._base import SudokuBase
from backend.consts import FieldValue, SquareLocation
from backend.sudoku import Field, Row, Column, Square


class Solver(SudokuBase):
    def __init__(self, logger_name: str, logging_level: int):
        super().__init__(logger_name=logger_name, logging_level=logging_level)

    def solve(self, *args, **kwargs) -> List[Field]:
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        return self.solve(*args, **kwargs)

    @staticmethod
    def solution_string(fields: List[Field]) -> str:
        return "".join(str(field) for field in fields)

    @staticmethod
    def check_validity(fields, rows, columns, squares: Dict[SquareLocation, Square]):
        for container in rows + columns + list(squares.values()):
            counts = Counter(container.get_fields_values())
            if any(value > 1 for value in counts.values()):
                return False
        return True

    @staticmethod
    def is_complete(fields: List[Field]) -> bool:
        return all(field.value for field in fields)

    @staticmethod
    def safe_to_place(row, column, square, value) -> bool:
        if value in row.get_fields_values():
            return False
        if value in column.get_fields_values():
            return False
        if value in square.get_fields_values():
            return False
        return True
