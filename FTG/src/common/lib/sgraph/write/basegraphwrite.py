import time
import queue
from copy import deepcopy
import argparse
from typing import Any, Callable, Dict, Set, List, Optional, Tuple, Type, Type, TypeVar, Union
import threading

SelfBaseGraphWrite = TypeVar("SelfBaseGraphWrite", bound="BaseGraphWrite")

class BaseGraphWrite:
	def __init__(
		self,
		**kwargs
	) -> None:
		pass
	def cInit(
		cls,
		**kwargs
	) -> SelfBaseGraphWrite:
		obj = cls(
			**kwargs
		)
		return obj