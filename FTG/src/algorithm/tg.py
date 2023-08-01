import random
from copy import deepcopy
import argparse
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar, Union

from common.lib.sgraph import SGraph
from algorithm.basealgo import BaseAlgorithm

MODEL: List[str] = ["IC", "LT",]
METHOD : List[str] = ["RIS", "MC"]
DEFAULT_NUM_SAMPLE = 1e2
MAX_NUM_SAMPLE = 1e8
DEFAULT_NUM_PARALLEL_THREAD = 1
MAX_NUM_PARALLEL_THREAD = 10

SelfBaseAlgorithm = TypeVar("SelfBaseAlgorithm", bound="BaseAlgorithm")

class GreedyMCSC(BaseAlgorithm):
    def __init__(
		self, 
		**kwargs
	) -> None:
        super().__init__(**kwargs)
        pass
    def run(self,):
        pass
    
class GreedyRevenue(BaseAlgorithm):
    def __init__(
		self, 
		**kwargs
	) -> None:
        super().__init__(**kwargs)
        pass
    def run(self,):
        pass