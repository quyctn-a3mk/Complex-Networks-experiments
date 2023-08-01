from copy import deepcopy
from typing import Any, Callable, Dict, Set, List, Optional, Tuple, Type, TypeVar, Union
import json
import csv
import os

from basegraphread import BaseReadEmbedding

FILEEXT : List[str] = [
	".csv",
	".json",
	".txt",
	# "tsv",
	# "pkl",
]

NODE_LIST: List[str] = [
	"node",
]

T_NODE_LIST = TypeVar("T_NODE_LIST", bound=NODE_LIST)

NODE_OBJECT: Dict[str, Dict[Any, Any]] = {
    "node": {
        "<any_key>" : "<any_val>"
    }
}

T_NODE_OBJECT = TypeVar("T_NODE_OBJECT", bound=NODE_OBJECT)

NODE_EMBEDDING_TEMPLATE : Union[Type[T_NODE_LIST], Type[T_NODE_OBJECT]] = None

T_NODE_EMBEDDING_TEMPLATE = TypeVar("T_NODE_EMBEDDING_TEMPLATE", bound=NODE_EMBEDDING_TEMPLATE)

NODE_READ_FROM : Dict[str, Type[T_NODE_EMBEDDING_TEMPLATE]] = {
	".txt" : NODE_LIST,
	".json" : NODE_OBJECT,
	".csv" : NODE_LIST,
}

class ReadNodeEmbedding(BaseReadEmbedding):
	def __init__(
		self,
		file_path : str = None,
		**kwargs
	) -> None:
		self.data = None
		if file_path:
			if not self.read(
				file_path = file_path
			):
				print("Something went wrong")
	@classmethod
	def cInit(
		cls,
		**kwargs
	) -> BaseReadEmbedding: 
		return cls(**kwargs)
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
				raise ValueError("Unsupported node embedding file format.")
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
			## first line for header
			header = lines[0].strip().split()
			if len(header) >= len(lines):
				raise Exception(f"Not enough line")
			if not self.check_file_format(
				template=NODE_READ_FROM[".txt"],
				data=header
			):
				raise Exception(f"Out of node embedding format.")
			# if key not in header:
			# 	raise Exception(f"No {key} has found")
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
			self.data = data
			return True
	def read_embedding_json(
		self,
		file_path: str
	):
		try:
			with open(file_path, "r") as json_file:
				data = json.load(json_file)
			if not self.check_file_format(
				template=NODE_READ_FROM[".csv"],
				data=data
			):
				raise Exception(f"Out of node embedding format.")
			# if isinstance(data,dict) and key in data:
			# 	data = data[key]
		except IOError as e:
			print(f"{str(e)}")
			return False
		except Exception as e:
			print(f"{str(e)}")
			return False
		else:
			self.data = data
			return True
	def read_embedding_csv(
		self,
		file_path: str	
	):
		try:
			data = {}
			with open(file_path, 'r') as csvfile:
				csv_reader = csv.reader(csvfile)
				header = next(csv_reader)  # Read the first line as the header
				if not self.check_file_format(
					template=NODE_READ_FROM[".csv"],
					data=header
				):
					raise Exception(f"Out of node embedding format.")
				# if key not in header:
				# 	raise Exception(f"No {key} has found")
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
			self.data = data
			return True
	def check_file_format(
		self,
		template : Type[NODE_EMBEDDING_TEMPLATE],
		data: Any
	) -> bool:
		if isinstance(template, list) and isinstance(data, list):
			# Check if the data is a list and each element in the data is a string
			return all(isinstance(item, str) for item in data)
		if isinstance(template, dict) and isinstance(data, dict):
			for key, val in template.items():
				# Skip the <any_key> and <any_val> checks
				if key == "<any_key>" or val == "<any_val>":
					continue
				if key not in data or not isinstance(data[key], type(val)):
					return False

				if isinstance(val, dict) and not self.check_file_format(val, data[key]):
					return False
				
			# Check if all keywords in the template exist in the data dictionary
			template_keys_set = set(template.keys()) - {"<any_key>", "<any_val>"}
			data_keys_set = set(data.keys())
			return template_keys_set.issubset(data_keys_set)
		## else
		return False