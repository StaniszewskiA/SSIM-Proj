from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class BirdOptions:
    AMOUNT: int
    SIZE: int
    COLOR: Tuple[int, int, int]
    PERCEPTION_RADIUS: List[int]
