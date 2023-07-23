from copy import deepcopy
import argparse
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar, Union

from lib import sgraph
from lib import sampling
from lib import otpheap

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
		**kwargs
	) -> None:
		pass
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