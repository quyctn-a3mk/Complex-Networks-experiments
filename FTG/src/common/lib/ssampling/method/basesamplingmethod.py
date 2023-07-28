from typing import Any, List, Type, TypeVar

from ssampling.model.basesamplingmodel import BaseSamplingModel

DEFAULT_NUM_SAMPLE : int = 1e4
MAX_NUM_SAMPLE : int = 1e8
DEFAULT_NUM_PARALLEL_THREAD : int = 1
MAX_NUM_PARALLEL_THREAD : int = 10

SelfBaseSamplingMethod = TypeVar("SelfBaseSamplingMethod", bound="BaseSamplingMethod")

class BaseSamplingMethod:
	num_sample = None
	num_parallel_thread = None
	def __init__(
		self,		
		model : Type[BaseSamplingModel],  ## require
		**kwargs,
	) -> None:
		self.model = model
	@classmethod
	def cInit(
		cls, 
		model : Type[BaseSamplingModel],  ## require
		**kwargs
	) -> SelfBaseSamplingMethod:
		obj = cls(
			model = model,
			**kwargs
		)
		return obj
	'''
	inteface
	'''
	def sampling(self, seed_node: Any = None) -> List:
		return self.model.sampling(seed_node = seed_node)
	# def cleanup(self):
	# 	del self
	'''
	interface
	'''
	def run_multithread(
		self,
	) -> None:
		pass
	'''
	interface
	'''
	def run_unithread(
		self,
	) -> None:
		pass
	'''
	interface
	'''
	def run(
		self,
		num_sample: int = DEFAULT_NUM_SAMPLE,
		num_parallel_thread: int = DEFAULT_NUM_PARALLEL_THREAD,
	) -> None:
		if not 0 < num_sample < MAX_NUM_SAMPLE:
			self.num_sample = DEFAULT_NUM_SAMPLE
		if 0 < num_parallel_thread < MAX_NUM_PARALLEL_THREAD:
			self.num_parallel_thread = DEFAULT_NUM_PARALLEL_THREAD
		if self.num_parallel_thread > 1:
			self.run_multithread()
		else:
			self.run_unithread()
	'''
	inteface
	'''
	def estimation(self,) -> float:
		pass