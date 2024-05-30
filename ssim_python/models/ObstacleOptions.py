from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class ObstacleOptions:
    RADIUS: int
    COLOR: Tuple[int, int, int]
    POSITIONS: List[Tuple[int, int]]
