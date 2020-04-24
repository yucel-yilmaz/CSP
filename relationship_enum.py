from enum import Enum


class Relationship(Enum):
    EQ = 1  # Equals: a == b
    NE = 2  # Not Equals: a != b
    LT = 3  # Less than: a < b
    GT = 4  # Less than or equal to: a <= b
    LE = 5  # Greater than: a > b
    GE = 6  # Greater than or equal to: a >= b