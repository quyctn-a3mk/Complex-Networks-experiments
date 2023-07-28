import time
import queue
from copy import deepcopy
from typing import Any, Callable, Dict, Set, List, Optional, Tuple, Type, Type, TypeVar, Union
import threading

SelfBaseGraph = TypeVar("SelfBaseGraph", bound="BaseGraph")

class BaseGraph:
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
		## graph main attribute
		self.graphNode = graphNode,
		self.graphNodeLabel = graphNodeLabel
		## graph side attribute
		self.is_directed = is_directed
		self.is_multigraph = is_multigraph
		self.reverse_edge = reverse_edge
		## 
		if numNode:
			self.numNode = numNode
		else:
			self.numNode = self.count_num_node()
		if numEdge:
			self.numEdge = numEdge
		else:
			self.numEdge = self.count_num_edge()
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
	) -> SelfBaseGraph:
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
	@property
	def graphNode(self):
		return deepcopy(self.__graphNode)
	@property
	def graphNodeLabel(self):
		return self.__graphNodeLabel	
	@property
	def numNode(self):
		return self.__numNode
	@property
	def numEdge(self):
		return self.__numEdge
	'''
	'''
	def count_num_node(self,):
		num_edge  = 0
		# do somethings
		return num_edge
	def count_num_edge(self,):
		num_edge  = 0
		# do somethings
		return num_edge