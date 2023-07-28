from copy import deepcopy
import argparse
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar, Union

from lib import sgraph
from lib import sampling
from lib import otpheap

from common.lib.sgraph import SGraph
from common.lib.ssampling import RIS

MODEL: List[str] = ["IC", "LT",]
METHOD : List[str] = ["RIS", "MC"]
DEFAULT_NUM_SAMPLE = 1e2
MAX_NUM_SAMPLE = 1e8
DEFAULT_NUM_PARALLEL_THREAD = 1
MAX_NUM_PARALLEL_THREAD = 10

SelfBaseAlgorithm = TypeVar("SelfBaseAlgorithm", bound="BaseAlgorithm")

class BaseAlgorithm():
	def __init__(
			self,
			graph: SGraph = None,
			sample = None,
			sampling_model: str = "IC",
			sampling_method: str = "RIS",
			num_sample: int = 0,
			num_parallel_thread: int = 1,
			**kwargs			 
		) -> None:
			if not graph:
				self.graph = SGraph()
			else:
				self.graph = graph
			##
			if sampling_model not in ("IC", "LT"):
				self.sampling_model= "IC"
			else:
				self.sampling_model = sampling_model
			##
			if sampling_method not in ("RIS", "MC"):
				self.sampling_method = "RIS"
			else:
				self.sampling_method = sampling_method
			##
			if self.sampling_method == "RIS":
				self.sample = RIS(graphNode = self.graph.graphNode, model = self.sampling_model)
			# else:
			# 	self.sample = MC()
			##
			if not 0 <= num_sample <= MAX_NUM_SAMPLE:
				self.num_sample = 0
			else:
				self.num_sample = num_sample
			##
			if not 1 <= num_parallel_thread <= MAX_NUM_PARALLEL_THREAD:
				self.num_parallel_thread = 1
			else:
				self.num_parallel_thread = num_parallel_thread
			##
	##
	@classmethod
	def cInit(cls, **kwargs):
		obj = cls(**kwargs)
		return obj
	##
	@classmethod
	def cArgumentParse():
		parser = argparse.ArgumentParser()
		parser.add_argument(
			"--sampling-model",
			"--model",
			type = str,
			default = MODEL[0],
			required=False,
			choices=MODEL,
			help = "Sampling model: IC for Independent Cascade, LT for Linear Threshold."
		)
		parser.add_argument(
			"--sampling-method",
			"--method",
			type = str,
			default = METHOD[0],
			required=False,
			choices=METHOD,
			help = "Sampling method: RIS for Reverse Influence Sampling, MT for Monte Carlo."
		)
		parser.add_argument(
			"--num-sample",
			"--sample",
			type = int,
			default = DEFAULT_NUM_SAMPLE,
			help = ""
		)
		parser.add_argument(
			"--num-parallel-thread",
			"--thread",
			type = int,
			default = DEFAULT_NUM_PARALLEL_THREAD, 
			help = ""
		)
		parser.add_argument(
			"--remain-kwargs",
			type=str, 
			nargs=argparse.REMAINDER,
			help="Optional keyword argument to pass to the algorithm",
		)
		return parser 
	##
	@classmethod
	def cLoad(
		cls: Type[SelfBaseAlgorithm],
		sys_argv: List[Any],
		**kwargs,
	) -> SelfBaseAlgorithm:
		base_args, unknown_args = cls.optionArgumentParse().parse_known_args(args=sys_argv)
		if hasattr(base_args, "remain_kwargs"):
			delattr(base_args, "remain_kwargs")
		init_params = vars(base_args)	
		return cls(**init_params)
		## return cls.cInit(**init_params)