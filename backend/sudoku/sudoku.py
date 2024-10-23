import re
from typing import Tuple, List

from backend._base import SudokuBase
from backend.consts import Position, FieldValue, SquareLocation
from backend.sudoku.field import Field
from backend.sudoku.containers.line import Row, Column
from backend.sudoku.solvers.classic_solver import ClassicSolver
from backend.sudoku.containers.square import Square


class Sudoku(SudokuBase):

    def __init__(self, setup: str = None, logger_name: str = "Sudoku", logging_level: int = 10):
        super().__init__(logger_name, logging_level)

        self.fields = [Field(x, y) for y in Position.get_possible_values() for x in Position.get_possible_values()]
        self.rows = [Row(x) for x in Position.get_possible_values()]
        self.columns = [Column(x) for x in Position.get_possible_values()]
        self.squares = {x: Square(x) for x in SquareLocation.get_possible_values()}

        for row in self.rows:
            row.add_many([field for field in self.fields if field.y_pos.value == row.number])

        for column in self.columns:
            column.add_many([field for field in self.fields if field.x_pos.value == column.number])

        for location, square in self.squares.items():
            square.add_many([field for field in self.fields
                             if SquareLocation.from_position(field.x_pos, field.y_pos) == location])

        if setup:
            self.setup(setup)

    def setup(self, initial_setup: str):
        """ Fill in known starting fields and limit their possible values, based only on what's known

        Args:
            initial_setup (str): sudoku board string with values to set
        """
        initial_setup = initial_setup.strip()
        initial_setup = re.sub(r"\s", "", initial_setup)

        for idx, field in enumerate(self.fields):
            field.set(FieldValue(int(initial_setup[idx])))

        for idx, field in enumerate(self.fields):
            if not field.value:
                square = self.squares[SquareLocation.from_position(field.x_pos, field.y_pos)]
                row = self.rows[field.y_pos]
                column = self.columns[field.x_pos]
                field.limit(square.get_fields_values(), row.get_fields_values(), column.get_fields_values())

    def field(self, *args: int | Position | Tuple[Position, Position] | Tuple[int, int]) -> Field:
        """ Return a single field of given index or in certain position

        Args:
            args: field position as ints or tuple of ints

        Returns:
            (Field): a field at given coordinates
        """
        if len(args) == 1:
            if isinstance(args[0], int) or isinstance(args[0], Position):
                return self.fields[args[0]]
            elif isinstance(args[0], tuple):
                return self.fields[args[0][0] + args[0][1] * 9]
        if len(args) == 2:
            return self.fields[args[0] + args[1] * 9]
        else:
            self.log_error("Given field is not available")
            raise RuntimeError("Given field is not available")

    def row(self, position: int | Position) -> Row:
        """ Return a single row on a given position

        Args:
            position (int | Position): position of the row

        Returns:
            (Row): a Row at given position
        """
        return self.rows[position]

    def column(self, position: int | Position) -> Column:
        """ Return a single column on a given position

        Args:
            position (int | Position): position of the column

        Returns:
            (Column): a Column at given position
        """
        return self.columns[position]

    def solve(self):
        """ Run a solving algorithm
        """
        solver = ClassicSolver()
        solution, fields = solver.solve(self.fields)

        if solution:
            print(solution)
        else:
            self.log_error("No solution was found")
        self.show(fields)

    def __call__(self):
        """ Return a list of fields
        """
        return [str(field) for field in self.fields]

    def show(self, fields: List[Field] = None):
        """ Print a sudoku
        """
        show_fields = fields if fields else self.fields
        s = "-" * 33
        s += "\n"
        current_row = show_fields[0].y_pos
        for field in show_fields:
            if field.y_pos != current_row:
                s += "|\n"
                if current_row % 3 == 2:
                    s += "=" * 33
                else:
                    s += "-" * 33
                s += "\n"
                current_row = field.y_pos
            if field.x_pos % 3 == 0:
                s += "|"
                if field.x_pos > 0:
                    s += "|"
            s += f" {str(field)} "
        s += "|\n" + "-" * 33
        print(s)

    def stringify(self) -> str:
        """ Return a sudoku as string

        Returns:
            (str): sudoku string
        """
        return "".join([str(field) for field in self.fields])


if __name__ == '__main__':
    boards = [
        "000260701 680070090 190004500 820100040 004602900 050003028 009300074 040050036 703018000",
        "000004028406000005100030600000301000087000140000709000002010003900000507670400000",
        "309000400200709000087000000750060230600904008028050041000000590000106007006000104",
    ]
