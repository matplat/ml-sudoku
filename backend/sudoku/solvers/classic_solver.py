import time
from copy import deepcopy
from typing import List, Dict, Tuple

from backend.sudoku import Field, Row, Column, Square
from backend.consts import FieldValue, SquareLocation, Position
from backend.sudoku.solvers.solver import Solver


class ClassicSolver(Solver):

    MAX_ITERATIONS = 81*9*9

    def __init__(self, logger_name: str = "ClassicSolver", logging_level: int = 10):
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.iterations = 0
        self.stop = False

    @staticmethod
    def _get_rows_columns_squares(fields: List[Field]) -> Tuple[List[Row], List[Column], Dict[SquareLocation, Square]]:
        rows = [Row(x) for x in Position.get_possible_values()]
        columns = [Column(x) for x in Position.get_possible_values()]
        squares = {x: Square(x) for x in SquareLocation.get_possible_values()}

        for row in rows:
            row.add_many([field for field in fields if field.y_pos.value == row.number])

        for column in columns:
            column.add_many([field for field in fields if field.x_pos.value == column.number])

        for location, square in squares.items():
            square.add_many([field for field in fields
                             if SquareLocation.from_position(field.x_pos, field.y_pos) == location])
        return rows, columns, squares

    @staticmethod
    def _field_for_check(fields, rows, columns, squares) -> Field:
        most_full_containers = sorted((cnt for cnt in rows + columns + list(squares.values())),
                                      key=lambda c: len(c.empty_fields()))
        least_options_fields = sorted((f for f in fields if len(f.possible_values) > 1),
                                      key=lambda f: f.possible_values)
        guessing_field = None
        for cnt in most_full_containers:
            for field in least_options_fields:
                if field in cnt.fields and (guessing_field is None or
                                            len(field.possible_values) < len(guessing_field.possible_values)):
                    guessing_field = field
        return guessing_field

    def solve(self, fields: List[Field]) -> Tuple[str, List[Field]]:
        start_time = time.time()
        solved, solution, fields = self._backtrack_solve(fields)

        solving_time = time.time() - start_time
        if solving_time > 61:
            solving_time = f"{round(solving_time // 60, 0)} minutes {solving_time % 60}"
        if solved:
            self.log_info(f"Solved in {self.iterations} iterations")
        else:
            self.log_warning(f"Sudoku could not be solved within {self.iterations} iterations")
        self.log_info(f"Solving time using {self.__class__.__name__}: {solving_time} seconds")
        return solution, fields

    def _backtrack_solve(self, fields: List[Field]) -> Tuple[bool, str, List[Field]]:
        current_solution = self.solution_string(fields)
        if self.is_complete(fields):
            return True, current_solution, fields

        if self.iterations > self.MAX_ITERATIONS:
            return False, current_solution, fields

        rows, columns, squares = self._get_rows_columns_squares(fields)
        diff = 1
        while diff != 0:
            for field in fields:
                if not field.value:
                    if len(field.possible_values) == 1:
                        field.fill()
                        square = squares[SquareLocation.from_position(field.x_pos, field.y_pos)]
                        row = rows[field.y_pos]
                        column = columns[field.x_pos]
                        for r_field in row.fields:
                            self._limit_field(r_field, rows, columns, squares)
                        for c_field in column.fields:
                            self._limit_field(c_field, rows, columns, squares)
                        for s_field in square.fields:
                            self._limit_field(s_field, rows, columns, squares)
            new_solution = self.solution_string(fields)
            diff = int("".join('1' if cf != nf else '0' for cf, nf in zip(current_solution, new_solution)))
            current_solution = new_solution

        field_to_check = self._field_for_check(fields, rows, columns, squares)
        row = rows[field_to_check.y_pos]
        column = columns[field_to_check.x_pos]
        square = squares[SquareLocation.from_position(field_to_check.x_pos, field_to_check.y_pos)]
        for value in field_to_check.possible_values:
            if self.safe_to_place(row, column, square, value):
                self.iterations += 1
                field_to_check.guess(value)
                solved, solution, fs = self._backtrack_solve(deepcopy(fields))
                if solved:
                    return solved, solution, fs
                field_to_check.restore_guess()
                field_to_check.eliminate(value)
        return False, current_solution, fields

    def _limit_field(self, field: Field, rows: List[Row], columns: List[Column], squares: Dict[SquareLocation, Square]):
        square = squares[SquareLocation.from_position(field.x_pos, field.y_pos)]
        row = rows[field.y_pos]
        column = columns[field.x_pos]
        return field.limit(square.get_fields_values(), row.get_fields_values(), column.get_fields_values())
