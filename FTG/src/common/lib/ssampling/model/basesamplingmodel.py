from copy import deepcopy
from typing import Any, Dict, Set, TypeVar, Union

SelfBaseSamplingModel = TypeVar("SelfBaseSamplingModel", bound="BaseSamplingModel")

class BaseSamplingModel:
	def __init__(
		self,
		adjList : Dict[Any, Union[Dict, Set]] = None,
		reverse_edge: bool = True,
		**kwargs
	) -> None:
		self.adjList = adjList
		self.reverse_edge = reverse_edge
	@classmethod
	def cInit(
		cls, 
		adjList : Dict[Any, Union[Dict, Set]] = None,
		reverse_edge: bool = True,
		**kwargs
	) -> SelfBaseSamplingModel:
		obj = cls(
			adjList = adjList,
			reverse_edge = reverse_edge,
			**kwargs
		)
		return obj
