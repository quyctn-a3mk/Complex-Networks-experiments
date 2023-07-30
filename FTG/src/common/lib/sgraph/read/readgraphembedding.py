from copy import deepcopy
from typing import Any, Callable, Dict, Set, List, Optional, Tuple, Type, TypeVar, Union
import json
import csv
import os

from basegraphread import BaseReadEmbedding

FILEEXT : Set[str] = [
	".csv",
	".json",
	".txt",
	# "tsv",
	# "pkl",
]

class ReadGraphEmbedding(BaseReadEmbedding):
	def __init__(
		self,
		file_path : str = None,
		**kwargs
	) -> None:
		self.graph = None
		if file_path:
			if not self.read(file_path=file_path):
				print("Something went wrong")
	@classmethod
	def cInit(
		cls,
		**kwargs
	) -> BaseReadEmbedding: 
		return cls(**kwargs)
	@property
	def get(self):
		return self.graph
	def read(
		self,
		file_path: str
	) -> bool:
		try:
			if os.path.exists(file_path):
				_ , file_ext = os.path.splitext(file_path)
			else:
				raise Exception(f"File path not exist")
			if file_ext not in FILEEXT:
				raise Exception(f"File extension has not supported")
			if file_ext == ".txt":
				return self.read_embedding_txt(file_path = file_path)
			elif file_ext == ".json":
				return self.read_embedding_json(file_path = file_path)
			elif file_ext == ".csv":
				return self.read_embedding_csv(file_path = file_path)
			else:
				raise ValueError("Unsupported node_embedding file format.")
		except ValueError as e:
			print(f"{str(e)}")
			return False
		except Exception as e:
			print(f"{str(e)}")
			return False
	'''
	interface
	'''
	def read_embedding_txt(
		self,
		file_path: str
	):
		try:
			with open(file_path, 'r') as txtfile:
				lines = txtfile.readlines()
			data = {}
			## first line for header
			header = lines[0].strip().split()
			if len(header) >= len(lines):
				raise Exception(f"Not enough line")
			for i in range(0, len(header)):
				key = header[i].strip()
				value = lines[i+1].strip()
				data[key] = value
			# Convert boolean values for "directed" and "multigraph"
			if "directed" in data:
				data["directed"] = data["directed"].lower() == "true"
			if "multigraph" in data:
				data["multigraph"] = data["multigraph"].lower() == "true"		
		except IOError as e:
			print(f"{str(e)}")
			return False
		except Exception as e:
			print(f"{str(e)}")
			return False
		else:
			self.graph = data
			return True
	def read_embedding_json(
		self,
		file_path: str,
		key: str = "graph",
	):
		try:
			with open(file_path, "r") as json_file:
				data = json.load(json_file)
			if isinstance(data,dict) and key in data:
				data = data[key]
		except IOError as e:
			print(f"{str(e)}")
			return False
		except Exception as e:
			print(f"{str(e)}")
			return False
		else:
			self.graph = data
			return True
	def read_embedding_csv(
		self,
		file_path: str
	):
		try:
			with open(file_path, 'r') as csvfile:
				csv_reader = csv.reader(csvfile)
				header = next(csv_reader)  # Read the first line as the header
				data = next(csv_reader)	# Read the second line as the data
			# Convert the data to a dictionary using the header as keys
			data = dict(zip(header, data))
			# Convert boolean values for "directed" and "multigraph"
			data["directed"] = data["directed"].lower() == "true"
			data["multigraph"] = data["multigraph"].lower() == "true"
		except IOError as e:
			print(f"{str(e)}")
			return False
		except Exception as e:
			print(f"{str(e)}")
			return False
		else:
			self.graph = data
			return True
		
def test():
	graphEmbedding = ReadGraphEmbedding(
		# file_path="D:\Research\ComplexNetworks\Complex-Networks-experiments\FTG\src\common\lib\sgraph\storegraph\sample\graphembeding\sample_graph_graphembeding.json"
		file_path="D:\Research\ComplexNetworks\Complex-Networks-experiments\FTG\src\common\lib\sgraph\storegraph\sample\graphembeding\sample_graph_graphembeding.txt"
		# file_path="D:\Research\ComplexNetworks\Complex-Networks-experiments\FTG\src\common\lib\sgraph\storegraph\sample\graphembeding\sample_graph_graphembeding.csv"
	)
	print(graphEmbedding.graph)

# test()