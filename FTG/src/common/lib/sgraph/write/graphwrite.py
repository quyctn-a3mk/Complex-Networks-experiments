import time
import queue
from copy import deepcopy
import argparse
from typing import Any, Callable, Dict, Set, List, Optional, Tuple, Type, Type, TypeVar, Union
import threading

from sgraph.write.basegraphwrite import BaseGraphWrite

class GraphWrite(BaseGraphWrite):
    def __init__(
		self,
        **kwargs
	) -> None:
        pass