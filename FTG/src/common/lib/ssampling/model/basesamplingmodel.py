import random
import time
import queue
from copy import deepcopy
from typing import Any, Callable, Dict, Set, List, Optional, Tuple, Type, TypeVar, Union
import threading

SelfBaseSamplingModel = TypeVar("SelfBaseSamplingModel", bound="BaseSamplingModel")

class BaseSamplingModel:
    def __init__(
		self,
        adjList : Dict[int, Union[Dict, Set]] = None,
        reverse_edge: bool = True,
        **kwargs
	) -> None:
        self.adjList = adjList
        self.reverse_edge = reverse_edge
    @classmethod
    def cInit(
        cls, 
        **kwargs
	) -> SelfBaseSamplingModel:
        obj = cls(**kwargs)
        return obj
