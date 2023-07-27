import random
import time
import queue
from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar, Union
import threading

from ssampling.method.basesamplingmethod import BaseSamplingMethod

DEFAULT_NUM_SAMPLE : int = 1e4
MAX_NUM_SAMPLE : int = 1e8
DEFAULT_NUM_PARALLEL_THREAD : int = 1
MAX_NUM_PARALLEL_THREAD : int = 10

SelfBaseSamplingMethod = TypeVar("SelfBaseSamplingMethod", bound="BaseSamplingMethod")

class BaseSamplingMethod:
	def __init__(
		self,		
		# sampling : Callable[... , List] = None,
		model : Type[BaseSamplingMethod],  ## require
		num_sample: int = DEFAULT_NUM_SAMPLE,
		num_parallel_thread: int = DEFAULT_NUM_PARALLEL_THREAD,
		**kwargs,
	) -> None:
		self.model = model
		if 0 < num_sample < MAX_NUM_SAMPLE:
			self.num_sample = num_sample
		else:
			self.num_sample = DEFAULT_NUM_SAMPLE
		if 1 < num_parallel_thread < MAX_NUM_PARALLEL_THREAD:
			self.num_parallel_thread = num_parallel_thread
		else:
			self.num_parallel_thread = MAX_NUM_PARALLEL_THREAD
	@classmethod
	def cInit(
		cls, 
		model : Type[BaseSamplingMethod],  ## require
		num_sample: int = DEFAULT_NUM_SAMPLE,
		num_parallel_thread: int = DEFAULT_NUM_PARALLEL_THREAD,
		**kwargs
	) -> SelfBaseSamplingMethod:
		obj = cls(
			model = model,
			num_sample = num_sample,
			num_parallel_thread = num_parallel_thread,
			**kwargs
		)
		return obj
	def sampling(self,):
		return self.model.sampling