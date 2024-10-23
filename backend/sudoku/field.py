from backend._base import SudokuBase
from backend.consts import FieldValue, Position
from typing import Set, Tuple, Iterable


class Field(SudokuBase):
    """ Class implementing a single field in sudoku.

    Attributes:
        x_pos (Position): x position
        y_pos (Position): y position
        value (FieldValue): value of the field
        guessed (bool): True if value of the field is not certain (not solved using classical methods), but guessed
        given (bool): True if value is set from the beginning
        possible_values (set): a set of possible values for the field
        possible_values_before_guess (set): helper set to save state of possible values when guessing
        possible_values_while_guessing (set): helper set to keep ytack of possible values after guessing
    """

    def __init__(self, x_pos: Position, y_pos: Position, value: FieldValue = FieldValue.NONE,
                 logger_name: str = "Field", logging_level: int = 10):
        """
        Args:
            x_pos (Position | int): x position of the field
            y_pos (Position | int): y position of the field
            value (FieldValue): field's value
            logger_name (str): logger name
            logging_level (int): logging level
        """
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
        """ Set a value of the Field as given from the start

        Args:
            value (FieldValue): value of the field
        """
        self.value = value
        self.given = True

    def guess(self, value: FieldValue) -> FieldValue:
        """ Set a value of the field and mark it as guessed

        Args:
            value (FieldValue): value

        Returns:
            (FieldValue): a value of the field
        """
        self.log_debug(f"Guessing with value {value}")
        self.value = value
        self.guessed = True
        self.possible_values_before_guess = self.possible_values.copy()
        self.possible_values = set()
        return self.value

    def restore_guess(self):
        """ Restore a field to the state from before the guess
        """
        self.value = FieldValue.NONE
        self.guessed = False
        self.possible_values = self.possible_values_before_guess.copy()
        self.possible_values_before_guess = set()

    def position(self) -> Tuple[Position, Position]:
        """ Get a tuple with field's position

        Returns:
            (tuple[Position, Position]): field's position
        """
        return self.x_pos, self.y_pos

    def print_position(self):
        """ Return a string with field's position
        """
        return f"Field ({self.x_pos.value}, {self.y_pos.value})"

    def eliminate(self, values: FieldValue | Iterable[FieldValue], guess: bool = False):
        """ Remove possible values from the field

        Args:
            values (FieldValue | Iterable[FieldValue]): a value or a list of values to remove
            guess (bool): decide which set to eliminate value from
        """
        self.log_debug(f"Removing values {values} from field {self.position()}")
        if isinstance(values, FieldValue):
            values = [values.value]
        if guess:
            self.possible_values_while_guessing -= set(values)
        else:
            self.possible_values -= set(values)

    def get_random_possible_value(self) -> FieldValue:
        """ Get a random value from possible ones

        Returns:
            (FieldValue): a value from possible_values set
        """
        return list(self.possible_values)[0]

    def get_last_possible_value(self) -> FieldValue:
        """ Get last possible value that a field can have

        Returns:
            (FieldValue): a value
        """
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

        Args:
            vals_in_square (list[FieldValue] | set[FieldValue]): values in square where field is
            vals_in_row (list[FieldValue] | set[FieldValue]): values in row where field is
            vals_in_column (list[FieldValue] | set[FieldValue]): values in column where field is
            guess (bool): decide which set to eliminate value from

        Returns:
            (set[FieldValue]): set of possible values
        """
        if self.value:
            if self.possible_values:
                self.possible_values = set()

        else:
            if any(value in self.possible_values for value in vals_in_square):
                self.eliminate(vals_in_square, guess)
            if any(value in self.possible_values for value in vals_in_row):
                self.eliminate(vals_in_row, guess)
            if any(value in self.possible_values for value in vals_in_column):
                self.eliminate(vals_in_column, guess)

        return self.possible_values if not guess else self.possible_values_while_guessing

    def fill(self, value: FieldValue = None):
        """ Fill a field with value if given or with last possible value if possible

        Args:
            value (FieldValue): a value to fill
        """
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
