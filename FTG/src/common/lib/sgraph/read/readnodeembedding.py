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

class ReadNodeEmbedding(BaseReadEmbedding):
	def __init__(
		self,
		file_path : str = None,
	) -> None:
		self.node = None
		if file_path:
			if not self.read(file_path=file_path):
				print("Something went wrong")
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
				raise ValueError("Unsupported graph_embedding file format.")
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
		file_path: str,
		key : str = "node"
	):
		try:
			with open(file_path, 'r') as txtfile:
				lines = txtfile.readlines()
			## first line for header
			header = lines[0].strip().split()
			if len(header) >= len(lines):
				raise Exception(f"Not enough line")
			if key not in header:
				raise Exception(f"No {key} has found")
			node_list = lines[1].strip().split()
			# Split each element of the list by space to get the values
			values = [row.strip().split() for row in lines[2:]]
			data = {node_list[i]:{header[j]:values[j-1][i] for j in range(1, len(header))} for i in range(len(node_list))}	
			print()
		except IOError as e:
			print(f"{str(e)}")
			return False
		except Exception as e:
			print(f"{str(e)}")
			return False
		else:
			self.node = data
			return True
	def read_embedding_json(
		self,
		file_path: str,
		key: str = "node",
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
			self.node = data
			return True
	def read_embedding_csv(
		self,
		file_path: str,
		key: str = "node"
	):
		try:
			data = {}
			with open(file_path, 'r') as csvfile:
				csv_reader = csv.reader(csvfile)
				header = next(csv_reader)  # Read the first line as the header
				if key not in header:
					raise Exception(f"No {key} has found")
				for row in csv_reader:
					node = row[0]
					node_atts = {
						header[i]: row[i] for i in range(1, len(header))  # Create a dictionary for the node data
					}
					data[node] = node_atts
		except IOError as e:
			print(f"{str(e)}")
			return False
		except Exception as e:
			print(f"{str(e)}")
			return False
		else:
			self.node = data
			return True
		
def test():
	nodeEmbedding = ReadNodeEmbedding()
	nodeEmbedding.read(
		# file_path="D:\\Research\\ComplexNetworks\\Complex-Networks-experiments\\FTG\\src\\common\\lib\\sgraph\\storegraph\\sample\\nodeembeding\\sample_graph_nodeembeding.csv"
		# file_path="D:\\Research\\ComplexNetworks\\Complex-Networks-experiments\\FTG\\src\\common\\lib\\sgraph\\storegraph\\sample\\nodeembeding\\sample_graph_nodeembeding.json"
		file_path="D:\\Research\\ComplexNetworks\\Complex-Networks-experiments\\FTG\\src\\common\\lib\\sgraph\\storegraph\\sample\\nodeembeding\\sample_graph_nodeembeding.txt"
	)
	print(nodeEmbedding.node)

# test()