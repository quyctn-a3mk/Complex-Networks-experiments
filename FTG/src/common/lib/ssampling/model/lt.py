import random
import queue
from copy import deepcopy
from typing import Any, Dict, Set, Union

from ssampling.model.basesamplingmodel import BaseSamplingModel

DEFAULT_CONSTANT_WEIGHT: float = 1.0

class LinearThreshold(BaseSamplingModel):
	def __init__(
		self,
		adjList : Dict[Any, Union[Dict, Set]] = None,
		reverse_edge: bool = True,
		weight_edge: bool = True,
		random_weight: bool = False,
		constant_weight: float = DEFAULT_CONSTANT_WEIGHT,
		**kwargs
	) -> None:
		if not weight_edge:
			adjList = self.assign_weight(
				adjList = deepcopy(adjList),
				random_weight = random_weight,
				constant_weight = constant_weight
			)
		super.__init__(
			adjList = adjList,
			reverse_edge = reverse_edge,
		)
	@staticmethod
	def assign_weight(
		adjList : Dict[Any, Any] = None,
		random_weight: bool = False,
		constant_weight: float = DEFAULT_CONSTANT_WEIGHT,
	) -> Dict[Any, Dict]:
		try:
			for key, value in adjList.items():
				if not isinstance(value, dict):
					if random_weight:
						new_value = {k: random.random() for k in value}
					else:
						new_value = {k: constant_weight for k in value}
					adjList[key] = new_value
			return adjList
		except Exception as e:
			print(f"{str(e)}")
			return None
	def sampling(self,):
		rand_node = random.choice(list(self.adjList.keys()))
		Q = queue.Queue()
		R = []
		Q.put(rand_node)
		R.append(rand_node)
		## influence spread
		while not Q.empty():
			v = Q.get()
			totalProb = 0
			for u in self.adjList[v]:
				if self.adjList[v][u]:
					prob = self.adjList[v][u]
				else: ## if None
					prob = random.random()
				if not u in R and totalProb >= prob:
					Q.put(u)
					R.append(u)
					break
				totalProb += prob
		## R sample
		return R

