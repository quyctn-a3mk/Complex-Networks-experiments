import random

import math
from copy import deepcopy
import argparse
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar, Union

from common.lib.sgraph import SGraph
from basealgo import BaseAlgorithm

MODEL: List[str] = ["IC", "LT",]
METHOD : List[str] = ["RIS", "MC"]
DEFAULT_NUM_SAMPLE = 1e2
MAX_NUM_SAMPLE = 1e8
DEFAULT_NUM_PARALLEL_THREAD = 1
MAX_NUM_PARALLEL_THREAD = 10

SelfBaseAlgorithm = TypeVar("SelfBaseAlgorithm", bound="BaseAlgorithm")

class FastThresholdGreedy(BaseAlgorithm):
	def __init__(
		self,
		# algo_kwargs: Any = None,
		graph: SGraph = None,
		sampling_model: str = "IC",
		sampling_method: str = "RIS",
		num_sample: int = 0,
		num_parallel_thread: int = 1,
		instance_mode: str = "RVN", # "MC"
		threshold_T: int = 100,
		epsilon: float = 0.01,
		Lambda: float = 0.01,
		**kwargs
	) -> None:
		super().__init__(
			graph = graph,
			# sample = 		   
			sampling_model = sampling_model,
			sampling_method = sampling_method,
			num_sample = num_sample,
			num_parallel_thread = num_parallel_thread,
		)
		self.threshold_T = threshold_T
		self.epsilon : float = epsilon
		self.Lambda : float = Lambda	
	'''
	sArgumentParse: static function for parsing arguments template
	return argparse obj
	'''
	@staticmethod
	def sArgumentParse():
		parser = argparse.ArgumentParser()
		parser.add_argument(
			"--threshold-T",
			"-T",
			type = int, 
			default = 100,
			help = "Parameter 'threshold' for both algorithm, an integer."
		)
		parser.add_argument(
			"--epsilon",
			"-e",
			default = 0.1, 
			type = float, 
			help = "Parameter 'epsilon', a float."
		)
		parser.add_argument(
			"--delta",
			"-d",
			default = 0.1, 
			type = float, 
			help = "Parameter 'delta', a float."
		)
		parser.add_argument(
			"--Lambda",
			"-l",
			default = 0.1, 
			type = float, 
			help = "Parameter 'lambda', a float."
		)
		parser.add_argument(
			"--opt-v",
			default = 1.0, 
			type = float, 
			help = "Parameter 'optimal v', a float."
		)
		parser.add_argument(
			"--remain-kwargs",
			type=str, 
			nargs=argparse.REMAINDER,
			help="Optional keyword argument to pass to the FTG algorithm",
		)
		return parser
	'''
	cLoad: class function for parsing argurment to class onject
	return self obj
	'''
	@classmethod
	def cLoad(
		cls: Type[SelfBaseAlgorithm],
		sys_argv: List[Any],
		**kwargs,
	) -> SelfBaseAlgorithm:
		base_args, unknown_args = super().optionArgumentParse().parse_known_args(args=sys_argv)
		if hasattr(base_args, "remain_kwargs"):
			delattr(base_args, "remain_kwargs")
		##
		args, unknown_args = cls.optionArgumentParse().parse_known_args(args=sys_argv)
		if hasattr(args, "remain_kwargs"):
			delattr(args, "remain_kwargs")
		init_params = {**vars(base_args),**vars(args),**kwargs}
		return cls(**init_params)
	'''
	'''
	@staticmethod
	def __shuffleNode(objnodes):
		if isinstance(objnodes, dict):
			keys = [e for e in objnodes.keys()]
			random.shuffle(keys)
			return keys
		elif isinstance(objnodes, set):
			vals = list(objnodes)
			random.shuffle(vals)
			return vals
		elif isinstance(objnodes, tuple):
			vals = [e[0] for e in objnodes]
			random.shuffle(vals)
			return vals
		elif isinstance(objnodes, list):
			vals = objnodes
			random.shuffle(vals)
			return vals
		else:
			return None
	'''
	'''
	@staticmethod
	def __orderNode(objnodes, dec = True, att_name = "cost"):
		if isinstance(objnodes, dict):
			key_att = [{k: v[att_name]} for k, v in objnodes.items()]
			sorted_att = sorted(key_att, key=lambda x: list(x.values())[0], reverse=dec)
			return sorted_att
		else:
			return None
	'''
	MAIN-ALGORITHM:
	- [ ] ftgopt: algorithm 1
	- [ ] ftg: algorithm 2
	'''
	def ftgotp(
		self,
		func_g,
		nodes_V,
		threshold_T : int = 100,
		epsilon : float = 0.1,
		Lambda : float = 0.1,
		optcost_v: float = 1.0,
		**kwargs
	):
		## line 1
		def __f(T, G_S):
			return min(T, G_S), G_S		
		S = set()		
		## init
		R_S = set()
		F_S = 0
		G_S = 0
		V = nodes_V
		count_g = 0
		## main algorithm
		max_L = math.ceil(math.log(1.0 / Lambda) / epsilon)
		## line 2
		for l in range(max_L):
			## line 3
			theta = (1.0 - epsilon) * (threshold_T - F_S) / optcost_v
			## line 4
			for e in V:
				## suppose e in S: 
				S_e = S.union({e})
				## calculate g(), f()
				F_S_e, G_S_e = __f(threshold_T, func_g(S_e))
				count_g += 1
				## line 5
				if F_S_e/self.graph.graphNode[e]["cost"] >= theta:
					## line 6
					S = S.union({e})
					F_S = F_S_e
					G_S = G_S_e
					V.discard(e)
				## line 8
				if F_S >= (1.0-Lambda) * threshold_T:
					break
		## line 11
		return S, G_S, count_g
	def ftg(
		self,
		func_g,
		nodes_V,
		threshold_T : int = 100,
		epsilon : float = 0.1,
		Lambda : float = 0.1,
		optcost_v: float = 1.0,
		**kwargs
	):
		'''
		sub-functions
		'''
		def __find_j(func_g, nodes_V, threshold_T):
			S = set()
			G_S = 0
			count_g = 0
			for e in V:
				S_e = S.union({e})
				G_S_e = func_g(S_e)
				if G_S_e >= threshold_T:
					break
			return len(S)
		def __g_V_0(func_g, V, V_0):
			return func_g(V) - func_g(V_0)
		## line 1
		S = []
		epsilon_q = epsilon / 8
		G_S = []
		C_S = []
		## line 2
		numNode_n = len(V)
		V = self.__orderNode(objnodes = nodes_V, dec = True, att = "cost")
		## line 3
		j = __find_j(func_g, V, threshold_T)
		## line 4
		u_j = V[j-1]
		c_q_min = epsilon * self.graph.graphNode[u_j]["cost"] / numNode_n
		c_q_max = j * self.graph.graphNode[u_j]["cost"]
		## line 5
		## line 5
		V_0 = {u for u in V if u < c_q_min}
		## line 6
		V_1 = {u for u in V if u > c_q_max}
		## line 7
		V_q = {u for u in V if c_q_min <= u <= c_q_max}
		threshold_T_q = threshold_T - func_g(V_0)
		func_g_q = __g_V_0
		## line 8
		equa_line8 = math.log(math.pow(numNode_n,3) /epsilon_q, 1/(1-epsilon))
		for i in range(equa_line8): ## parallel (?)
			## line 9
			v_i = c_q_min / math.pow(1-epsilon_q, i)
			## line 10
			S_alg_1, G_S_alg_1, _ = self.ftgopt(
				func_g = func_g_q,
				nodes_V = V_q,
				threshold_T = threshold_T_q,
				epsilon = epsilon_q,
				Lambda = Lambda,
				optcost_v = v_i,
			) ## call into alg 1
			S.append(S_alg_1)
			G_S.append(G_S_alg_1)
		## line 12
		t = threshold_T_q * (1-Lambda)
		S_min = set()
		G_S_min = 0
		C_S_min = 0
		for i in range(equa_line8):
			if G_S[i] >= t:
				if S_min == None or C_S[i] < C_S_min:
					S_min = S[i]
					G_S_min = G_S[i]
					C_S_min = C_S[i]
		## line 13
		S_final = S_min.union(V_0)
		return S_final
	'''
	estimation functions: func_g
	'''
	def estimation_max_cover(self):
		pass
	def estimation_revenue(self):
		pass
	def run(self, mode = "revenue"):
		if mode == "revenue":
			func_g = self.estimation_revenue
		else:
			func_g = self.estimation_max_cover
		return self.ftg(
			func_g = func_g,
			nodes_V= self.graphNode,
			threshold_T = self.threshold_T,
			epsilon = self.epsilon,
			Lambda = self.Lambda
		)
