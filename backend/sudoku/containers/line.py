from backend._base import SudokuBase
from backend.consts import Position, FieldValue
from backend.sudoku.containers.container import SudokuContainer
from backend.sudoku.field import Field


class Line(SudokuContainer):
    """ A representation of a container visible as line, either vertical (column) or horizontal (row)

    Attributes:
        number (int): a distinctive number of a line (it's position)
    """
    def __init__(self, number: int = None, logger_name: str = "Line", logging_level: int = 10):
        super().__init__(logger_name, logging_level)
        self.number = number

    def __repr__(self):
        return f"{self.logger_name} ({[str(field) for field in self.fields]})"


class Row(Line):
    def __init__(self, number: Position, logger_name: str = "Row", logging_level: int = 10):
        super().__init__(number, f"{logger_name}_{number}", logging_level)

    def add(self, field: Field):
        if field.y_pos != self.number:
            self.log_warning(f"{field} in row {field.y_pos} can't be added to row {self.number}")
            return
        super().add(field)
        self.fields = sorted(self.fields, key=lambda f: f.x_pos)


class Column(Line):
    def __init__(self, number: Position, logger_name: str = "Column", logging_level: int = 10):
        super().__init__(number, f"{logger_name}_{number}", logging_level)

    def add(self, field: Field):
        if field.x_pos != self.number:
            self.log_warning(f"{field} in column {field.x_pos} can't be added to column {self.number}")
            return
        super().add(field)
        self.fields = sorted(self.fields, key=lambda f: f.y_pos)
