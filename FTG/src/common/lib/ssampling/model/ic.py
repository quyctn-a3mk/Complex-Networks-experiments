import random
import queue
from copy import deepcopy
from typing import Any, Dict, Set, Union

from ssampling.model.basesamplingmodel import BaseSamplingModel

DEFAULT_MAX_PROBABILITY : float = 0.9999

class IndependentCascade(BaseSamplingModel):
	def __init__(
		self,
		adjList : Dict[Any, Union[Dict, Set]] = None,
		reverse_edge: bool = True,
		df_max_prob: float = DEFAULT_MAX_PROBABILITY,
		**kwargs
	) -> None:
		super.__init__(
			adjList = adjList,
			reverse_edge = reverse_edge,
		)
		self.df_max_prob = df_max_prob
	def sampling(self,):
		rand_node = random.choice(list(self.adjList.keys()))
		Q = queue.Queue()
		R = []
		Q.put(rand_node)
		R.append(rand_node)
		## influence spread
		while not Q.empty():
			v = Q.get()
			for u in self.adjList[v]:
				if u not in R:
					if len(self.adjList[u]) == 0:
						prob = self.df_max_prob
					else:
						prob = 1/len(self.adjList[u])
					rand_prob = random.random()
					if rand_prob >= prob:
						Q.put(u)
						R.append(u)
						break
		## R sample
		return R

