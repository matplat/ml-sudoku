from backend._base import SudokuBase
from backend.consts import FieldValue, Position
from typing import Set, Tuple, Iterable


class Field(SudokuBase):
    """ Class implementing a single field in sudoku.

    """

    def __init__(self, x_pos: Position, y_pos: Position, value: FieldValue = FieldValue.NONE,
                 logger_name: str = "Field", logging_level: int = 10):
        super().__init__(logger_name=f"{logger_name} ({x_pos},{y_pos})", logging_level=logging_level)
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.value = value
        self.guessed = False
        self.given = False
        self.possible_values = FieldValue.get_possible_values() if self.value == FieldValue.NONE else set()
        self.possible_values_before_guess = set()
        self.possible_values_while_guessing = self.possible_values.copy()

    def set(self, value: FieldValue):
        """

        :param value:
        :return:
        """
        self.value = value
        self.given = True

    def guess(self, value: FieldValue) -> FieldValue:
        # self.log_debug(f"Guessing with value {value}")
        self.value = value
        self.guessed = True
        self.possible_values_before_guess = self.possible_values.copy()
        self.possible_values = set()
        return self.value

    def restore_guess(self):
        self.value = FieldValue.NONE
        self.guessed = False
        self.possible_values = self.possible_values_before_guess.copy()
        self.possible_values_before_guess = set()

    def position(self) -> Tuple[Position, Position]:
        """

        :return:
        """
        return self.x_pos, self.y_pos

    def print_position(self):
        return f"Field ({self.x_pos.value}, {self.y_pos.value})"

    def eliminate(self, values: FieldValue | Iterable[FieldValue], guess: bool = False):
        # self.log_debug(f"Removing values {values} from field {self.position()}")
        if isinstance(values, FieldValue):
            values = [values.value]
        if guess:
            self.possible_values_while_guessing -= set(values)
        else:
            self.possible_values -= set(values)
        # self.log_debug(f"Possible values left: {self.possible_values}")

    def get_random_possible_value(self) -> FieldValue:
        return list(self.possible_values)[0]

    def get_last_possible_value(self) -> FieldValue:
        if len(self.possible_values) > 1:
            raise RuntimeError("There are more possible values than one")
        for value in self.possible_values:
            return value

    def limit(self,
              vals_in_square: list[FieldValue] | Set[FieldValue] = None,
              vals_in_row: list[FieldValue] | Set[FieldValue] = None,
              vals_in_column: list[FieldValue] | Set[FieldValue] = None,
              guess: bool = False) -> Set[FieldValue]:
        """ Remove possible values based on the values in the square, row and column

        :param vals_in_square:
        :param vals_in_row:
        :param vals_in_column:
        :return:
        """
        if self.value:
            if self.possible_values:
                self.possible_values = set()

        else:
            if any(value in self.possible_values for value in vals_in_square):
                self.eliminate(vals_in_square)
            if any(value in self.possible_values for value in vals_in_row):
                self.eliminate(vals_in_row)
            if any(value in self.possible_values for value in vals_in_column):
                self.eliminate(vals_in_column)
            # self.possible_values -= set(vals_in_square) if vals_in_square else set()
            # self.possible_values -= set(vals_in_row) if vals_in_row else set()
            # self.possible_values -= set(vals_in_column) if vals_in_column else set()

            # if len(self.possible_values) == 1 and fill:
            #     for value in self.possible_values:
            #         self.value = value
            #     self.log_debug(f"Field ({self.x_pos}, {self.y_pos}) filled with {self.value}")
            #     self.possible_values = set()

        return self.possible_values if not guess else self.possible_values_while_guessing

    def fill(self, value: FieldValue = None):
        if not self.value:
            if value:
                if value not in self.possible_values:
                    self.log_error(f"Value {value} is not in possible values for this field ({self.possible_values})")
                    raise RuntimeError(f"Value {value} is not in possible values for this field ({self.possible_values})")
                self.value = value
                self.log_debug(f"Field ({self.x_pos}, {self.y_pos}) filled with {self.value}")

            elif len(self.possible_values) == 1:
                for value in self.possible_values:
                    self.value = value
                self.possible_values = set()
                self.log_debug(f"Field ({self.x_pos}, {self.y_pos}) filled with {self.value}")
        return self.value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"Field ({self.x_pos}, {self.y_pos}), value: {self.value}"

    def __bool__(self):
        return bool(self.value.value)
