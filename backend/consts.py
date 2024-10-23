from enum import IntEnum, Enum
from typing import List, Tuple, Set, Generator

""" This file contains constants and enums used in the code.
For the simplification, following view of the sudoku is used:

      y
      -------------------------------------------
      0 |0,0         |             |            |
      1 |  LEFT_TOP  |  CENTER_TOP | RIGHT_TOP  |
      2 |            |2,3          |            |
      -------------------------------------------
      3 |            |             |            |
      4 |LEFT_CENTER |    CENTER   |RIGHT_CENTER|
      5 |            |             |            |
      -------------------------------------------
      6 |            |             |            |
      7 |LEFT_BOTTOM |CENTER_BOTTOM|RIGHT_BOTTOM|
      8 |            |             |            |
      -------------------------------------------
    x   | 0   1   2  |  3   4   5  |  6   7   8 |

    
In addition, every square has its internal counting (taking LEFT_BOTTOM as example):
     
      y
      ----------------
      6 | 0   1   2  |
      7 | 3   4   5  |
      8 | 6   7   8  |
      ----------------
    x   | 0   1   2  |
    
"""


class Position(IntEnum):
    """ Position of the object in Sudoku - either a field, or a line

    NOTE: NINE element is not to be used directly, it was added to simplify internal operations
    """
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9

    @classmethod
    def get_possible_values(cls) -> Generator:
        """ Get all values that can be used further as position

        Returns:
            (generator): values 0 <= x <= 8 (without NINE)
        """
        return (pos for pos in cls if pos != cls.NINE)

    @staticmethod
    def permutations(x_range: range, y_range: range) -> List[Tuple]:
        """ Generate all possible permutations of values in given x_ and y_range

        Args:
            x_range (range):
            y_range (range):

        Returns:
             (list[tuple]): list of (x,y) tuples
        """
        permutations = set()
        for x in x_range:
            for y in y_range:
                permutations.add((x, y))
        return list(permutations)


class SquareLocation(Enum):
    """ Square-typical location in the sudoku
    """
    LEFT_TOP = 0
    CENTER_TOP = 1
    RIGHT_TOP = 2
    LEFT_CENTER = 3
    CENTER = 4
    RIGHT_CENTER = 5
    LEFT_BOTTOM = 6
    CENTER_BOTTOM = 7
    RIGHT_BOTTOM = 8

    @classmethod
    def get_possible_values(cls) -> Generator:
        """ Get all values that can be used further as square location

        Returns:
            (generator): all possible locations
        """
        return (pos for pos in cls)

    @classmethod
    def from_position(cls, x_pos: Position, y_pos: Position):
        position_to_square_mapping = {
            **dict.fromkeys(Position.permutations(x_range=range(Position.ZERO, Position.THREE),
                                                  y_range=range(Position.ZERO, Position.THREE)),
                            cls.LEFT_TOP),
            **dict.fromkeys(Position.permutations(x_range=range(Position.THREE, Position.SIX),
                                                  y_range=range(Position.ZERO, Position.THREE)),
                            cls.CENTER_TOP),
            **dict.fromkeys(Position.permutations(x_range=range(Position.SIX, Position.NINE),
                                                  y_range=range(Position.ZERO, Position.THREE)),
                            cls.RIGHT_TOP),
            **dict.fromkeys(Position.permutations(x_range=range(Position.ZERO, Position.THREE),
                                                  y_range=range(Position.THREE, Position.SIX)),
                            cls.LEFT_CENTER),
            **dict.fromkeys(Position.permutations(x_range=range(Position.THREE, Position.SIX),
                                                  y_range=range(Position.THREE, Position.SIX)),
                            cls.CENTER),
            **dict.fromkeys(Position.permutations(x_range=range(Position.SIX, Position.NINE),
                                                  y_range=range(Position.THREE, Position.SIX)),
                            cls.RIGHT_CENTER),
            **dict.fromkeys(Position.permutations(x_range=range(Position.ZERO, Position.THREE),
                                                  y_range=range(Position.SIX, Position.NINE)),
                            cls.LEFT_BOTTOM),
            **dict.fromkeys(Position.permutations(x_range=range(Position.THREE, Position.SIX),
                                                  y_range=range(Position.SIX, Position.NINE)),
                            cls.CENTER_BOTTOM),
            **dict.fromkeys(Position.permutations(x_range=range(Position.SIX, Position.NINE),
                                                  y_range=range(Position.SIX, Position.NINE)),
                            cls.RIGHT_BOTTOM),
        }
        
        return position_to_square_mapping[(x_pos, y_pos)]


class FieldValue(IntEnum):
    NONE = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9

    @classmethod
    def get_possible_values(cls) -> Set:
        return set(value for value in cls if value != cls.NONE)

    def __str__(self):
        return str(self.value)

    def __bool__(self):
        if self.value == self.NONE:
            return False
        return True
