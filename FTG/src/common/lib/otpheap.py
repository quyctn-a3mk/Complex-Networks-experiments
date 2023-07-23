## option Heap

class OptHeap:
	__heap = __keyList  = __keyFlag  = __attSize = __heapify = __empty = None
	#======init==================================
	def __init__(self):		# 0 agrument
		self.__heap = []
		self.__heapify = None
		self.__empty = True
		self.__resetKey()
	def __init__(self, keyList = [0], keyFlag = [1], heapNode = []):	# 0-3 agruments
		self.__heap = []
		for node in heapNode:
			self.push(node)
		if len(self.__heap)>0:
			self.__empty = False
		else:
			self.__empty = True
		self.__checkKey(keyList,keyFlag)
		self.__updateKey(keyList,keyFlag)
	#======set attibutes=========================
	def __resetKey(self):
		self.__attSize = 1
		self.__keyList = [0]
		self.__keyFlag = [1]
	def __updateKey(self,keyList,keyFlag):
		self.__attSize = max(self.__attSize,len(keyList))
		self.__keyList = keyList
		self.__keyFlag = keyFlag
	#=====heap private method====================
	def __checkHeapNode(self,node):
		self.__attSize = max(self.__attSize,len(node))
		if len(node)<len(self.__keyList):
			node+=[0 for i in range(len(self.__keyList)-len(node))]
		# return node
	def __checkKey(self,keyList,keyFlag):
		self.__attSize = 1
		self.__attSize = max(self.__attSize,len(keyList))
		if len(keyFlag)<len(keyList):
			keyFlag+=[1 for i in range(max(self.attSize-len(keyFlag),0))]
		else:
			keyFlag = keyFlag[:len(keyList)]
		i = 0
		while i<len(keyList):
			if keyList[i]<0 or keyList[i]>=self.__attSize:
				keyList.pop(i)
				keyFlag.pop(i)
				continue
			if keyFlag[i] not in [-1,1]:
				keyFlag[i]=1
			i+=1
	def __compareHeapNode(self, a, b):	# list
		for i in range(0,len(self.__keyList)):
			if a[self.__keyList[i]]*self.__keyFlag[i] > b[self.__keyList[i]]*self.__keyFlag[i]:
				return True
		return False
	def __upHeap(self,childPos, childVal):	#sub 
		if childPos==0 or self.__compareHeapNode(childVal, self.__heap[(childPos-1)>>2]):
			return
		self.__heap[childPos],self.__heap[(childPos-1)>>2] = self.__heap[(childPos-1)>>2],self.__heap[childPos]
		self.__upHeap((childPos-1)>>2,childVal)
	def __downHeap(self, root):
		key = self.__heap[root]
		size = len(self.__heap)
		while root*2+1<size:
			childPos = root*2+1
			if childPos+1<size and self.__compareHeapNode(self.__heap[childPos+1],self.__heap[childPos]):
				childPos+=1
			if self.__compareHeapNode(key,self.__heap[childPos]):
				break
			self.__heap[root] = self.__heap[childPos]
			root = childPos
		self.__heap[root] = key
	#=====heap method============================
	def heapify(self):
		self.__heapify = True
		for node in self.__heap:
			self.__checkHeapNode(node)
		for i in reversed(range(len(self.__heap)//2)):
			self.__attSize = max(self.__attSize,len(self.__heap[i]))
			self.__downHeap(i)
	def push(self,node,upHeap = False):
		self.__checkHeapNode(node)
		self.__heap.append(node)
		self.__empty = False
		if upHeap:
			self.__upHeap(len(self.__heap)-1)
	def pop(self):
		if self.__empty:
			return None
		if len(self.__heap)==1:
			self.__empty = True
			return self.__heap.pop()
		top = self.__heap[0]
		self.__heap[0] = self.__heap.pop() # heap[-1]
		self.__downHeap(0)
		return top
	def top(self):
		return self.__heap[0]
	def isHeapify(self):
		return self.__heapify
	def isEmpty(self):
		return self.__empty
	def findAtts(self,attsList, attsVal):
		index = []
		for i in range(len(self.__heap)):
			for j in range(len(attsList)):
				if self.__heap[i][attsList[j]] == attsVal[j]:
					index.append(i)
		return index
	def updateHeapNode(self, attsList, attsVal, newHeapNode, heapify = False):
		index = self.findAtts(attsList, attsVal)
		self.__checkHeapNode(newHeapNode)
		for i in index:
			self.__heap[i] = newHeapNode
		if heapify:
			self.heapify()
		return heapify
	def updateAttsHeapNode(self, attsList, attsVal, updateAttsList, updateAttsVal , heapify = False):
		# if tuple => const
		index = self.findAtts(attsList, attsVal)
		for i in index:
			for j in range(len(updateAttsList)): 
				if j<0 or j>=self.__attSize:
					# return None
					continue
				self.__heap[i][updateAttsList[j]] = updateAttsVal[j]
		if heapify:
			self.heapify()
		return heapify
	def print(self):
		print(self)
		print("attSize: ", self.__attSize)
		print("keyList: ", self.__keyList)
		print("keyFlag: ", self.__keyFlag)
		print("size: ", len(self.__heap))
		print(self.__heap)
		if not self.__empty:
			print("root: ", self.__heap[0])		