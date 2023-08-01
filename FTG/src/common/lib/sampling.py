import random
import time
import queue
from copy import deepcopy
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar, Union
import threading

# MultipleThreading: not using

class RIS:
	threadList = {"mapping_thread": {}, "sampling_thread" : {}}
	lock_thread = None
	mappingQueue = None
	stopFlag = None
	totalSample = None
	sample = None
	cover = None
	##
	def __init__(
		self,
		graphNode : Dict = None,
		model: str = "IC",
		reset: bool = True,
	):
		self.graphNode = graphNode
		self.model = model
		if reset:
			self.reset()
	##
	def reset(self,):
		self.mappingQueue = queue.Queue()
		self.RR = {}
		self.sample = {}
		self.cover = {}
		self.totalSample = 0
		self.stopFlag = False
		self.threadList = []
	## 
	def run(
		self,
		num_sample: int = 100,
		num_thread: int = 1,
		reset: bool = True,
	) -> None:
		if not num_thread or num_thread <= 0:
			num_thread = 1
		if reset:
			self.reset()
		## create 1 maping thread
		mappingThread = threading.Thread(target = self.mapping_thread, args = (), daemon = True)
		mappingThread.start()
		self.lock_thread = threading.Lock()
		self.sample = {}
		self.cover = {}
		## create n sampling thread
		required_split = []
		self.divideZ(n = num_sample, t = num_thread, z = required_split)
		for thread_i in range(num_thread):
			samplingThread = threading.Thread(target = self.sampling_thread, args = (thread_i, required_split[thread_i],), daemon = True)
			self.threadList.append(samplingThread)
			samplingThread.start()
		for thread_i in range(num_thread):
			self.threadList[thread_i].join()
		self.lock_thread.acquire()
		print(f"Generated: {len(self.sample)} sample(s).")
		self.lock_thread.release()
		## empty thread list
		self.threadList = []
		## call stop for mapping thread
		self.stopFlag = True
		mappingThread.join()
	## threading loop function
	def sampling_thread(
		self,
		thread_name: Any = None,
		required: int = 1,
	) -> None:
		for i in range(required):
			# print("sampling")
			if self.model == "IC":
				R = self.sampling_IC()
			else:
				R = self.sapling_LT()
			if R:
				## lock for write
				self.lock_thread.acquire()
				sampleID = self.totalSample
				self.mappingQueue.put(sampleID)
				print(f"Thread name '{thread_name}': sampleID '{sampleID}'")
				self.sample[sampleID] = R
				self.totalSample += 1
				# if self.totalSample % 100 == 0:
					# print(f"Thread name '{name}': Topic [{topic_i}] - sample {sampleID}")
				self.lock_thread.release()
				## unlocked
	## threading loop function
	def mapping_thread(self,) -> None:
		# print("mapping on")
		while not (self.mappingQueue.empty() and self.stopFlag):
			# print("mapping")
			if self.mappingQueue.empty():
				wait = 0.5
				print(f"wait: {wait}")
				time.sleep(wait) ## 1
				continue
			sampleID = self.mappingQueue.get()
			## mapping to cover
			while True:
				try:
					for nodeID in self.sample[sampleID]:
						if nodeID not in self.cover:
							self.cover[nodeID] = set()
						## add cover sample in to set of cover node u
						self.cover[nodeID].add(sampleID)
				except Exception as e:
					print(f"{str(e)}")
					print(f"wait: {wait}")
					time.sleep(wait)
				else:
					break	
	## sampling model
	def sampling_LT(self,):
		## random source node
		rand_node = random.randint(0,len(self.graphNode)-1)
		Q = queue.Queue()
		R = []
		Q.put(rand_node)
		R.append(rand_node)
		## influence spread
		while not Q.empty():
			v = Q.get()
			totalProb = 0
			for u in self.graphNode[v]["adjList"]:
				if self.graphNode[v]["adjList"][u]["weight"]:
					prob = self.graphNode[v]["adjList"][u]["weight"]
				else:
					prob = random.random()
				if not u in R and totalProb >= prob:
					Q.put(u)
					R.append(u)
					break
				totalProb += prob
		## R sample
		return R
	# ## sampling model
	def sampling_IC(self,):
		rand_node = random.randint(0,len(self.graphNode)-1)
		Q = queue.Queue()
		R = []
		Q.put(rand_node)
		R.append(rand_node)
		## influence spread
		while not Q.empty():
			v = Q.get()
			for u in self.graphNode[v]["adjList"]:
				if u not in R:
					if len(self.graphNode[u]["adjList"]) == 0:
						prob = 0.9999
					else:
						prob = 1/len(self.graphNode[u]["adjList"])
					rand_prob = random.random()
					if rand_prob >= prob:
						Q.put(u)
						R.append(u)
						break
		## R sample
		return R
	##
	def get_cover(self,):
		return deepcopy(self.cover)
	def get_sample(self,):
		return deepcopy(self.sample)
	##
	def divideZ(self,n,t,z):
		if t == 0:
			return None
		if t == 1:
			z.append(int(n))
			return True
		z.append(int(n//t))
		self.divideZ(n-z[-1],t-1,z)