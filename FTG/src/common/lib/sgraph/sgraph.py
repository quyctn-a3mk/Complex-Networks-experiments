import sys
import random
from copy import *
# import queue
import time

class SGraph:
	__graphName = None
	__numNode = __numEdge = None
	__graphNodeLabel = None
	__graphNode = None
	## getter
	@property
	def graphName(self):
		return self.__graphName
	@property
	def numNode(self):
		return self.__numNode
	@property
	def numEdge(self):
		return self.__numEdge
	@property
	def graphNodeLabel(self):
		return self.__graphNodeLabel
	@property
	def graphNode(self):
		return deepcopy(self.__graphNode)
	## constructor(s)
	def __init__(self, attsList = None):
		if not attsList:
			attsList = SGraph.sAttsList()
		self.__graphName = attsList["graphName"]
		self.__numNode = attsList["numNode"]
		self.__numEdge = attsList["numEdge"]
		self.__graphNodeLabel = attsList["graphNodeLabel"]
		self.__graphNode = attsList["graphNode"]
	## object instance initialize
	@classmethod
	def cInit(cls, attsList = None):
		sg = cls(attsList)
		return sg
	## default attributes list
	@staticmethod
	def sAttsList(graphName = None, numNode = 0, numEdge = 0, graphNodeLabel = [], graphNode = {}):
		return {
			"graphName" : str(graphName),
			"numNode" : int(numNode),
			"numEdge" : int(numEdge),
			"graphNodeLabel" : tuple(graphNodeLabel),
			"graphNode" : graphNode
		}
	## create default graph node
	@staticmethod
	def sGraphNode(adjList = {}):
		return {
			"adjList" : adjList,
			"cost" : 1.0,
		}
	## add graphnode attribute
	def addGraphNodeAtt(self, nodeID: int, att_name: str, att_value: None, replace = False):
		if att_name not in self.graphNode[nodeID] or replace:
			self.graphNode[nodeID][att_name] = att_value
			return True
		return False
	## load graph dataset from file
	@staticmethod
	def sParseGraph(path, graphName = None, numThread = 1):
		print(f"Load graph input dataset...")
		lines = readFile_ParseLine(path,numThread)
		if not lines:
			print(lines)	## debugging: result flag
			return False
		try:
			## parse header line and graph nodes label: line[0] = "numNode numEdge", line[1] = "graphNodeLabel"
			attsList = SGraph.sAttsList(graphName,*lines[0],lines[1])
			##
			# initial graph node list
			if len(lines) < 2 + int(attsList["numNode"]):
				print(f"Error: Unable to parse graph, file format does not contain enough lines.")
				return False
			attsList["graphNode"] = {nodeID:SGraph.sGraphNode() for nodeID in range(attsList["numNode"])}
			pointer_1 = 2	## start read from pointer line
			## muitlthread (?)
			## n lines for adjacency reverse list
			for nodeID in range(attsList["numNode"]):
				if len(lines[pointer_1+nodeID]) == 0 or not lines[pointer_1+nodeID][0].isnumeric():
					attsList["graphNode"][nodeID]["adjList"] = {}
				else:
					# attsList["graphNode"][nodeID]["adjList"] = set(map(int,lines[pointer_1+nodeID]))
					for nei in lines[pointer_1+nodeID]:
						attsList["graphNode"][nodeID]["adjList"][int(nei)] = {"weight": None}
			pointer_2 = pointer_1 + attsList["numNode"]
			if pointer_2 + attsList["numNode"] <= len(lines):
				## n lines for adjacency reverse weight list
				for nodeID in range(attsList["numNode"]):
					for weight_i in range(len(lines[pointer_2+nodeID])):
						attsList["graphNode"][nodeID]["adjList"][int(lines[pointer_1+nodeID][weight_i])]["weight"] = float(lines[pointer_2+nodeID][weight_i])
			# print(attsList)
		except:
			print("Error: Unable to parse graph, file format missing does not right.")
			return False
		else:
			print(f"Done parsing graph dataset.")
			return attsList
	## object instance initialize with graph dataset
	@classmethod
	def cReadFile_GraphFormatted(cls, path, graphName = None, numThread = 1):
		return cls.cInit(SGraph.sParseGraph(path, graphName, numThread))
	## re-init object with graph dataset
	def readFile_GraphFormatted(self, path, graphName = None, numThread = 1):
		self(SGraph.sParseGraph(path, graphName, numThread))
	## object print
	def prettyprint(self, detail = False):
		print(self)
		print(f"Graph name: {self.graphName}")
		print(f"Graph num node: {self.numNode}")
		print(f"Graph num edge: {self.numEdge}")
		if detail:
			## for debugging
			print(f"Graph nodes label: {self.graphNodeLabel}")
			print(f"Graph nodes: {self.graphNode}")
	##
	def assign_graph_cost(self,):
		graphNode = self.graph.__graphNode.keys()
		for nodeID in graphNode:
			# cost = 0.9
			# cost = random.random()
			cost = random.uniform(0.0001, 0.5)
			if cost == 0:
				cost = 0.0001
			if cost == 1:
				cost = 0.9999
			self.__graphNode[nodeID]["cost"] = cost
			# self.addGraphNodeAtt(nodeID=nodeID, att_name="cost", att_value=cost, replace=True)	
			print(nodeID, cost)

####
	
def readFile_ParseLine(path, numThread = 1):
	def __parseLine(string):
		# string = string.strip()
		lines = string.split("\n")
		if not lines:
			return None
		for i in range(len(lines)):
			lines[i] = lines[i].strip()
			lines[i] = lines[i].split(" ")	## regex?
		return lines
	start = time.perf_counter()
	print(f"Reading file: {path}")
	try:
		## type of file: "r","rb"
		with open(path,"r") as file:
			## multithread (?)
			data = file.read()
			print(f"Read file in: {time.perf_counter() - start}")
		file.close()
	except IOError: 
		print("Error: File does not appear to exist.")
		return False
	else:
		lines = __parseLine(data)
		if not lines:
			print(f"Error: File does not contain any readable data.")
			return None
		print(f"Success reading file.")
		return lines
	return None

