from backend.consts import SquareLocation, FieldValue
from backend.sudoku.containers.container import SudokuContainer
from backend.sudoku.field import Field


class Square(SudokuContainer):
    def __init__(self, location: SquareLocation, logger_name: str = "Square", logging_level: int = 10):
        super().__init__(f"{logger_name}_{location}", logging_level)
        self.location = location

    def __repr__(self):
        return f"{self.logger_name} ({[str(field) for field in self.fields]})"