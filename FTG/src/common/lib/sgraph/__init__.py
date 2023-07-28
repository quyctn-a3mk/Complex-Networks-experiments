import time
import queue
from copy import deepcopy
from typing import Any, Callable, Dict, Set, List, Optional, Tuple, Type, Type, TypeVar, Union
import threading

from sgraph.basegraph import BaseGraph

from utils.readfile import readFile_ParseLine

class SGraph(BaseGraph):
	def __init__(
		self,
		graphNode : Dict[Any, Union[Dict, Set, List]] = None,
		graphNodeLabel : Dict[Any, Any] = None,
		is_directed: bool = True,
		is_multigraph: bool = False,
		reverse_edge : bool = True,		
		numNode : int = None,
		numEdge : int = None,
		**kwargs
	) -> None:
		super.__init__(
			graphNode = graphNode,
			graphNodeLabel = graphNodeLabel,
			is_directed = is_directed,
			is_multigraph = is_multigraph,
			reverse_edge = reverse_edge,
			numNode = numNode,
			numEdge = numEdge,
			**kwargs
		)
		## # if not isinstance(value, dict):
	@classmethod
	def cInit(
		cls,
		graphNode : Dict[Any, Union[Dict, Set, List]] = None,
		graphNodeLabel : Dict[Any, Any] = None,
		is_directed: bool = True,
		is_multigraph: bool = False,
		reverse_edge : bool = True,		
		numNode : int = None,
		numEdge : int = None,
		**kwargs
	) -> Type[BaseGraph]:
		obj = cls(
			graphNode = graphNode,
			graphNodeLabel = graphNodeLabel,
			is_directed = is_directed,
			is_multigraph = is_multigraph,
			reverse_edge = reverse_edge,
			numNode = numNode,
			numEdge = numEdge,
			**kwargs
		)
		return obj
	'''
	read from CSV: edge list
	'''

	'''
	read from text file : edge list
	'''

	'''
	read from text file : adj list
	'''

	'''
	read from text file : adj matrix
	'''