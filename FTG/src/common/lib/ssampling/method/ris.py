import random
import time
import queue
from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar, Union
import threading

from ssampling.model.basesamplingmodel import BaseSamplingModel
from ssampling.method.basesamplingmethod import BaseSamplingMethod

DEFAULT_NUM_SAMPLE : int = 1e4
MAX_NUM_SAMPLE : int = 1e8
DEFAULT_NUM_PARALLEL_THREAD : int = 1
MAX_NUM_PARALLEL_THREAD : int = 10
WAIT_TIME : float = 0.01

class ReverseInfluenceSampling(BaseSamplingMethod):
	threadList = {"mapping_thread": {}, "sampling_thread" : {}}
	lock_thread = None
	mappingQueue = None
	stopFlag = None
	totalSample = None
	sample = None
	cover = None
	def __init__(
		self,		
		model : Type[BaseSamplingModel],  ## require
		num_sample: int = DEFAULT_NUM_SAMPLE,
		num_parallel_thread: int = DEFAULT_NUM_PARALLEL_THREAD,
		reset: bool = True,
		**kwargs,
	) -> None:
		super.__init__(
			model = model,
			num_sample = num_sample,
			num_parallel_thread = num_parallel_thread
		)
		if reset:
			self.__reset()
	@classmethod
	def cInit(
		cls, 
		model : Type[BaseSamplingModel],  ## require
		num_sample: int = DEFAULT_NUM_SAMPLE,
		num_parallel_thread: int = DEFAULT_NUM_PARALLEL_THREAD,
		reset: bool = True,
		**kwargs
	) -> Type[BaseSamplingMethod]:
		obj = cls(
			model = model,
			num_sample = num_sample,
			num_parallel_thread = num_parallel_thread,
			reset = reset,
			**kwargs
		)
		return obj
	def sampling(self,) -> Callable[..., List]:
		return self.model.sampling
	def __reset(self,):
		self.mappingQueue = queue.Queue()
		self.RR = {}
		self.sample = {}
		self.cover = {}
		self.totalSample = 0
		self.stopFlag = False
		self.threadList = []
	@property
	def sample(self):
		return deepcopy(self.sample)
	@property
	def cover(self):
		return deepcopy(self.cover)
				## unlocked
	## threading loop function
	def mapping_multithread(self,) -> None:
		while not (self.mappingQueue.empty() and self.stopFlag):
			if self.mappingQueue.empty():
				time.sleep(WAIT_TIME) ## 1
				continue
			sampleID = self.mappingQueue.get()
			## mapping sample to cover
			while True:
				try:
					for nodeID in self.sample[sampleID]:
						if nodeID not in self.cover:
							self.cover[nodeID] = set()
						## add cover sample in to set of cover node u
						self.cover[nodeID].add(sampleID)
				except Exception as e:
					print(f"{str(e)}")
					time.sleep(WAIT_TIME)
				else:
					break
	## threading loop function
	def sampling_multithread(
		self,
		thread_name: Any = None,
		required: int = 1,
		print_per: int = 100,
	) -> None:
		for i in range(required):
			R = self.sampling() ## R = self.model.sampling()
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
	def run_multhithread(self, print_per: int = 100) -> None:
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
		self.cover = {}
		## create n sampling thread
		required_split = []
		__divideZ(n = self.num_sample, t = self.num_parallel_thread, z = required_split)
		if not 0 < print_per < MAX_NUM_SAMPLE:
			print_per = required_split[0]
		for thread_i in range(self.num_parallel_thread):
			samplingThread = threading.Thread(target = self.sampling_multithread, args = (thread_i, required_split[thread_i], print_per), daemon = True)
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
	def sampling_unithread(self,
		required: int = 1,
		print_per: int = 100,
	) -> None:
		for i in range(required):
			R = self.sampling() ## R = self.model.sampling()
			if R:
				sampleID = self.totalSample
				self.sample[sampleID] = R
				self.totalSample += 1
				for nodeID in self.sample[sampleID]:
						if nodeID not in self.cover:
							self.cover[nodeID] = set()
						## add cover sample in to set of cover node u
						self.cover[nodeID].add(sampleID)
				if print_per and self.totalSample % print_per == 0:
					print(f"sampleID '{sampleID}'")
	def run_unithread(self, print_per: int = 100) -> None:
		if not 0 < print_per < MAX_NUM_SAMPLE:
			print_per = self.num_sample
		self.sampling_unithread(
			required = self.num_sample,
			print_per = 100
		)
	def run(self,) -> None:
		if self.num_parallel_thread > 1:
			self.run_multithread()
		else:
			self.run_unithread()
		