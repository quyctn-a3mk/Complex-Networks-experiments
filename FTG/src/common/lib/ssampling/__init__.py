from copy import deepcopy
from typing import Any, Dict, Set, Union, List, Type

from ssampling.model.basesamplingmodel import BaseSamplingModel
from ssampling.model.ic import IndependentCascade as IC
from ssampling.model.lt import LinearThreshold as LT

MODEL: Dict[str, List[Type[BaseSamplingModel]]] = {
	"IC" : IC,
	"LT" : LT,
}

class SSampling:
	def __init__(
		self,
		adjList : Dict[Any, Union[Dict, Set]] = None,
		reverse_edge: bool = True,
		model: str = MODEL["IC"],
		model_kwargs: List[Any] = None,
		**kwargs
	) -> None:
		self.model = model.cInit(
			adjList = adjList,
			reverse_edge = reverse_edge,
			kwargs = model_kwargs,
		)
	@classmethod
	def cInit(
		cls, 
		**kwargs
	) -> Type[BaseSamplingModel]:
		obj = cls(**kwargs)
		return obj
	def sampling(self,):
		return self.model.sampling()


