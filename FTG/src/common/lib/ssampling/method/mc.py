import time
import queue
from copy import deepcopy
from typing import Any, List, Type
import threading

from ssampling.model.basesamplingmodel import BaseSamplingModel
from ssampling.method.basesamplingmethod import BaseSamplingMethod

DEFAULT_NUM_SAMPLE : int = 1e4
MAX_NUM_SAMPLE : int = 1e8
DEFAULT_NUM_PARALLEL_THREAD : int = 1
MAX_NUM_PARALLEL_THREAD : int = 10
WAIT_TIME : float = 0.01

class MonteCarlo(BaseSamplingMethod):
	num_sample = None
	num_parallel_thread = None
	threadList = None
	lock_thread = None
	stopFlag = None
	totalSample = None
	sample = None
	active = None
	def __init__(
		self,		
		model : Type[BaseSamplingModel],  ## require
		reset: bool = True,
		**kwargs,
	) -> None:
		super.__init__(
			model = model,
			**kwargs
		)
		if reset:
			self.__reset()
	@classmethod
	def cInit(
		cls, 
		model : Type[BaseSamplingModel],  ## require
		reset: bool = True,
		**kwargs
	) -> Type[BaseSamplingMethod]:
		obj = cls(
			model = model,
			reset = reset,
			**kwargs
		)
		return obj
	'''
	inteface
	'''
	def sampling(self, seed_node: Any = None) -> List:
		return self.model.sampling(seed_node = seed_node)
	def __reset(self,):
		self.mappingQueue = queue.Queue()
		self.sample = {}
		self.active = {} ##
		self.totalSample = 0
		self.stopFlag = False
		self.threadList = []
	@property
	def sample(self):
		return deepcopy(self.sample)
	@property
	def active(self):
		return deepcopy(self.active)
	## threading loop function
	def mapping_multithread(self,) -> None:
		while not (self.mappingQueue.empty() and self.stopFlag):
			if self.mappingQueue.empty():
				time.sleep(WAIT_TIME) ## 1
				continue
			sampleID = self.mappingQueue.get()
			## mapping sample to active
			while True:
				try:
					for nodeID in self.sample[sampleID]:
						if nodeID not in self.active:
							self.active[nodeID] = sampleID
				except Exception as e:
					print(f"{str(e)}")
					time.sleep(WAIT_TIME)
				else:
					break
	## threading loop function
	def sampling_multithread(
		self,
		thread_name: Any = None,
		seed_node: Any = None,
		required: int = 1,
		print_per: int = 100,
	) -> None:
		for i in range(required):
			R = self.sampling(seed_node = seed_node) ## R = self.model.sampling()
			if R:
				## lock for write sample
				self.lock_thread.acquire()
				sampleID = self.totalSample
				self.mappingQueue.put(sampleID)
				self.sample[sampleID] = R
				self.totalSample += 1
				if print_per and self.totalSample % print_per == 0:
					if thread_name:
						print(f"Thread name '{thread_name}': sampleID '{sampleID}'")
					else:
						print(f"sampleID '{sampleID}'")
				self.lock_thread.release()
				## unlocked
	'''
	interface
	'''
	def run_multithread(
		self, 
		seed_node: Any = None, 
		print_per: int = 100
	) -> None:
		def __divideZ(self,n,t,z):
			if t == 0:
				return None
			if t == 1:
				z.append(int(n))
				return True
			z.append(int(n//t))
			self.divideZ(n-z[-1],t-1,z)
		## create 1 maping thread
		mappingThread = threading.Thread(target = self.mapping_multithread, args = (), daemon = True)
		mappingThread.start()
		self.lock_thread = threading.Lock()
		self.sample = {}
		self.active = {}
		## create n sampling thread
		required_split = []
		__divideZ(n = self.num_sample, t = self.num_parallel_thread, z = required_split)
		if not 0 < print_per < MAX_NUM_SAMPLE:
			print_per = required_split[0]
		for thread_i in range(self.num_parallel_thread):
			samplingThread = threading.Thread(target = self.sampling_multithread, args = (thread_i, seed_node, required_split[thread_i], print_per), daemon = True)
			self.threadList.append(samplingThread)
			samplingThread.start()
		for thread_i in range(self.num_parallel_thread):
			self.threadList[thread_i].join()
		self.lock_thread.acquire()
		print(f"Generated: {len(self.sample)} sample(s).")
		self.lock_thread.release()
		## empty thread list
		self.threadList = []
		## call stop for mapping thread
		self.stopFlag = True
		mappingThread.join()
	def sampling_unithread(
		self,
		seed_node: Any = None,
		required: int = 1,
		print_per: int = 100,
	) -> None:
		for i in range(required):
			R = self.sampling(seed_node = seed_node) ## R = self.model.sampling()
			if R:
				sampleID = self.totalSample
				self.sample[sampleID] = R
				self.totalSample += 1
				for nodeID in self.sample[sampleID]:
					if nodeID not in self.active:
						self.active[nodeID] = sampleID
			if print_per and self.totalSample % print_per == 0:
					print(f"sampleID '{sampleID}'")
		pass
	'''
	interface
	'''
	def run_unithread(
		self, 
		seed_node: Any = None, 
		print_per: int = 100
	) -> None:
		if not 0 < print_per < MAX_NUM_SAMPLE:
			print_per = self.num_sample
		self.sampling_unithread(
			seed_node = seed_node,
			required = self.num_sample,
			print_per = print_per
		)
	'''
	interface
	'''
	def run(
		self, 
		num_sample: int = DEFAULT_NUM_SAMPLE,
		num_parallel_thread: int = DEFAULT_NUM_PARALLEL_THREAD,
		seed_node: Any = None, 
		print_per: int = 100, 
		reset: bool = False
	) -> None:
		if not 0 < num_sample < MAX_NUM_SAMPLE:
			self.num_sample = DEFAULT_NUM_SAMPLE
		if 0 < num_parallel_thread < MAX_NUM_PARALLEL_THREAD:
			self.num_parallel_thread = DEFAULT_NUM_PARALLEL_THREAD
		if reset:
			self.__reset()
		if self.num_parallel_thread > 1:
			self.run_multithread(
				seed_node = seed_node,
				print_per = print_per,
			)
		else:
			self.run_unithread(
				seed_node = seed_node,
				print_per = print_per,
			)
	'''
	inteface
	'''
	def estimation(self) -> float:
		return len(self.active) / self.totalSample