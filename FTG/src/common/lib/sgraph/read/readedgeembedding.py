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

REPR : List[str] = [
	"adjlist",
	"edgelist",
	"adjmatrix",
]

SOURCE_TARGET_LIST : List[str] = [
	"source",
	"target"
]

T_SOURCE_TARGET_LIST = TypeVar("T_SOURCE_TARGET_LIST", bound=SOURCE_TARGET_LIST)

EDGE_LIST_TARGET: Dict[str, List[ Dict[str, List]]] = {
    "edge": {
		"target" : ["<any_val>"]
	}
}

T_EDGE_LIST_TARGET = TypeVar("T_EDGE_LIST_TARGET", bound=EDGE_LIST_TARGET)

EDGE_OBJECT_TARGET: Dict[str, Dict[Any, List[Dict[str, Any]]]] = {
    "edge": {
        "<any_key>": [{
			"target": "<any_val>"
		}]
    }
}

T_EDGE_OBJECT_TARGET = TypeVar("T_EDGE_OBJECT_TARGET", bound=EDGE_OBJECT_TARGET)

EDGE_LIST_SOURCE_TARGET: Dict[str, List[ Dict[str, Any]]] = {
    "edge": [{
		"source" : "<any_val>",
		"target" : "<any_val>"
	}]
}

T_EDGE_LIST_SOURCE_TARGET = TypeVar("T_EDGE_LIST_SOURCE_TARGET", bound=EDGE_LIST_SOURCE_TARGET)

EDGE_EMBEDDING_TEMPLATE : Union[Type[T_SOURCE_TARGET_LIST], Type[T_EDGE_LIST_TARGET], Type[T_EDGE_OBJECT_TARGET], Type[T_EDGE_LIST_SOURCE_TARGET]] = None

T_EDGE_EMBEDDING_TEMPLATE = TypeVar("T_EDGE_EMBEDDING_TEMPLATE", bound=EDGE_EMBEDDING_TEMPLATE)

EDGE_READ_FROM : Dict[Tuple[str,str], Type[T_EDGE_EMBEDDING_TEMPLATE]] = {
	("adjlist", ".txt") : SOURCE_TARGET_LIST,
	("adjlist",  ".json") : EDGE_OBJECT_TARGET,
	("adjmatrix", ".json") : EDGE_LIST_TARGET,
	("adjmatrix", ".txt") : SOURCE_TARGET_LIST,
	("edgelist" , ".csv") : SOURCE_TARGET_LIST,
	("edgelist", ".json") : EDGE_LIST_SOURCE_TARGET,
	("edgelist", ".txt") : SOURCE_TARGET_LIST,
}

class ReadEdgeEmbedding(BaseReadEmbedding):
	def __init__(
		self,
		file_path : str = None,
		repr: str = "edgelist",
		**kwargs
	) -> None:
		self.data = None
		if file_path:
			if not self.read(
				file_path = file_path,
				repr = repr
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
		file_path: str,
		repr: str = "edgelist"
	) -> bool:
		try:
			if os.path.exists(file_path):
				_ , file_ext = os.path.splitext(file_path)
			else:
				raise Exception(f"File path not exist")
			if file_ext not in FILEEXT:
				raise Exception(f"File extension has not supported")
			if file_ext == ".txt":
				return self.read_embedding_txt(
					file_path = file_path,
					repr = repr
				)
			elif file_ext == ".json":
				return self.read_embedding_json(
					file_path = file_path,
					repr = repr
				)
			elif file_ext == ".csv":
				return self.read_embedding_csv(
					file_path = file_path,
					repr = repr
				)
			else:
				raise ValueError("Unsupported edge embedding file format.")
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
		repr: str = "adjlist"
	):
		try:
			if not repr or repr not in REPR:
				print("Try to read in edgelist representation")
				return self.read_embedding_txt_edgelist(file_path = file_path)
			if repr == "edgelist":
				return self.read_embedding_txt_edgelist(file_path = file_path)
			elif repr == "adjlist":
				return self.read_embedding_txt_adjlist(file_path = file_path)
			elif repr == "adjmatrix":
				return self.read_embedding_txt_adjmatrix(file_path = file_path)
			else:
				raise ValueError("Unsupported edge embedding representation.")
		except IOError as e:
			print(f"{str(e)}")
			return False
		except Exception as e:
			print(f"{str(e)}")
			return False
	def read_embedding_txt_edgelist(
		self,
		file_path: str
	) -> bool:
			try:
				data = []
				with open(file_path, 'r') as txtfile:
					lines = txtfile.readlines()
				header = lines[0].strip().split()
				if len(header) >= len(lines):
					raise Exception(f"Not enough line")
				if not self.check_file_format(
					template=EDGE_READ_FROM[("edgelist",".txt")],
					data=header
				):
					raise Exception(f"Out of edge embedding format.")
				# Create the data dictionary from the lines
				for i in range(1, len(lines)):
					row = lines[i].strip().split()
					data.append(dict(zip(header, row)))
			except Exception as e:
				print(f"{str(e)}")
				return False
			else:
				self.data = data
				return True
	def read_embedding_txt_adjlist(
		self,
		file_path: str
	) -> bool:
			try:
				data = {}
				with open(file_path, 'r') as txtfile:
					lines = txtfile.readlines()
				header = lines[0].strip().split()
				if len(header) >= len(lines):
					raise Exception(f"Not enough line")
				if not self.check_file_format(
					template=EDGE_READ_FROM[("adjlist",".txt")],
					data=header
				):
					raise Exception(f"Out of edge embedding format.")
				# Create the data dictionary from the lines
				for i in range(1, len(lines), len(header)):
					node = lines[i].strip()[0]
					data[node] = {header[j]:lines[i+j].strip().split() for j in range(1,len(header))}
			except Exception as e:
				print(f"{str(e)}")
				return False
			else:
				self.data = data
				return True
	def read_embedding_txt_adjmatrix(
		self,
		file_path: str
	) -> bool:
			try:
				data = {}
				with open(file_path, 'r') as txtfile:
					lines = txtfile.readlines()
				header = lines[0].strip().split()
				if len(header) >= len(lines):
					raise Exception(f"Not enough line")
				if not self.check_file_format(
					template=EDGE_READ_FROM[("adjmatrix",".txt")],
					data=header
				):
					raise Exception(f"Out of edge embedding format.")
				node_list = lines[1].strip().split()
				data = {node:{} for node in node_list}
				# Create the data dictionary from the lines
				att_i = 1
				for i in range(2, len(lines), len(node_list)): ## 2-6-10
					att = header[att_i]
					for j in range(len(node_list)):	## 0-1-2-3
						node = node_list[j]
						data[node][att] = lines[i+j].strip().split()
					att_i+=1
			except Exception as e:
				print(f"{str(e)}")
				return False
			else:
				self.data = data
				return True
	def read_embedding_json(
		self,
		file_path: str,
		repr: str = "adjlist"
	) -> bool:
		try:
			if not repr or repr not in REPR:
				print("Try to read in edgelist representation")
				return self.read_embedding_json_edgelist(file_path = file_path)
			if repr == "edgelist":
				return self.read_embedding_json_edgelist(file_path = file_path)
			elif repr == "adjlist":
				return self.read_embedding_json_adjlist(file_path = file_path)
			elif repr == "adjmatrix":
				return self.read_embedding_json_adjmatrix(file_path = file_path)
			else:
				raise ValueError("Unsupported edge embedding representation.")
		except IOError as e:
			print(f"{str(e)}")
			return False
		except Exception as e:
			print(f"{str(e)}")
			return False
	def read_embedding_json_edgelist(
		self,
		file_path : str
	) -> bool:
		try:
			with open(file_path, "r") as json_file:
				data = json.load(json_file)
			if not self.check_file_format(
				template=EDGE_READ_FROM[("edgelist",".json")],
				data=data
			):
				raise Exception(f"Out of edge embedding format.")
			if "edge" in data:
				data = data["edge"]
		except IOError as e:
			print(f"{str(e)}")
			return False
		except Exception as e:
			print(f"{str(e)}")
			return False
		else:
			self.data = data
			return True
	def read_embedding_json_adjlist(
		self,
		file_path : str
	) -> bool:
		try:
			with open(file_path, "r") as json_file:
				data = json.load(json_file)
			if not self.check_file_format(
				template=EDGE_READ_FROM[("adjlist",".json")],
				data=data
			):
				raise Exception(f"Out of edge embedding format.")
			if "edge" in data:
				data = data["edge"]
		except IOError as e:
			print(f"{str(e)}")
			return False
		except Exception as e:
			print(f"{str(e)}")
			return False
		else:
			self.data = data
			return True
	def read_embedding_json_adjmatrix(
		self,
		file_path : str
	) -> bool:
		try:
			with open(file_path, "r") as json_file:
				data = json.load(json_file)
			if not self.check_file_format(
				template=EDGE_READ_FROM[("adjmatrix",".json")],
				data=data
			):
				raise Exception(f"Out of edge embedding format.")
			# if isinstance(data,dict) and key in data:
			if "edge" in data:
				data = data["edge"]
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
		file_path: str,
		repr : str = "adjlist"
	):
		try:
			if not repr or repr not in REPR:
				print("Try to read in edgelist representation")
				return self.read_embedding_csv_edgelist(file_path = file_path)
			if repr == "edgelist":
				return self.read_embedding_csv_edgelist(file_path = file_path)
			elif repr == "adjlist":
				return self.read_embedding_csv_adjlist(file_path = file_path)
			elif repr == "adjmatrix":
				return self.read_embedding_csv_adjmatrix(file_path = file_path)
			else:
				raise ValueError("Unsupported edge embedding representation.")
		except IOError as e:
			print(f"{str(e)}")
			return False
		except Exception as e:
			print(f"{str(e)}")
			return False
	def read_embedding_csv_edgelist(
		self,
		file_path: str,
	):
		try:
			data = {}
			with open(file_path, 'r') as csvfile:
				csv_reader = csv.reader(csvfile)
				header = next(csv_reader)  # Read the first line as the header
				if not self.check_file_format(
					template=EDGE_READ_FROM[("edgelist",".csv")],
					data=header
				):
					raise Exception(f"Out of node embedding format.")
				for row in csv_reader:
					edge = row[0]
					edge_atts = {
						header[i]: row[i] for i in range(1, len(header))  # Create a dictionary for the edge data
					}
					data[edge] = edge_atts
		except IOError as e:
			print(f"{str(e)}")
			return False
		except Exception as e:
			print(f"{str(e)}")
			return False
		else:
			self.data = data
			return True
	def read_embedding_csv_adjlist(
		self,
		file_path: str,
	):
		try:
			data = {}
			with open(file_path, 'r') as csvfile:
				csv_reader = csv.reader(csvfile)
				header = next(csv_reader)  # Read the first line as the header
				if not self.check_file_format(
					template=EDGE_READ_FROM[("adjlist",".csv")],
					data=header
				):
					raise Exception(f"Out of node embedding format.")
				for row in csv_reader:
					edge = row[0]
					edge_atts = {
						header[i]: row[i] for i in range(1, len(header))  # Create a dictionary for the edge data
					}
					data[edge] = edge_atts
		except IOError as e:
			print(f"{str(e)}")
			return False
		except Exception as e:
			print(f"{str(e)}")
			return False
		else:
			self.data = data
			return True
	def read_embedding_csv_adjmatrix(
		self,
		file_path: str,
	):
		try:
			data = {}
			with open(file_path, 'r') as csvfile:
				csv_reader = csv.reader(csvfile)
				header = next(csv_reader)  # Read the first line as the header
				if not self.check_file_format(
					template=EDGE_READ_FROM[("adjmatrix",".csv")],
					data=header
				):
					raise Exception(f"Out of node embedding format.")
				for row in csv_reader:
					edge = row[0]
					edge_atts = {
						header[i]: row[i] for i in range(1, len(header))  # Create a dictionary for the edge data
					}
					data[edge] = edge_atts
		except IOError as e:
			print(f"{str(e)}")
			return False
		except Exception as e:
			print(f"{str(e)}")
			return False
		else:
			self.data = data
			return True
	def deep_type_value(
		self,
		template: Any,
		data: Any
	) -> bool:
			try:
				if not data:
					raise Exception(f"data was empty")
				if not template:
					raise Exception(f"template was empty")
				if not type(data) == type(template):
					raise Exception(f"data and template have different types.")
				if isinstance(template, list) and isinstance(data, list):
					for value in template:
						if isinstance(value, str):
							if value == "<any_key>" or value == "<any_val>":
								continue
							if value not in data:
								raise Exception(f"Value '{value}' missing in data")
						elif isinstance(value, dict):
							for data_value in data:
								if not self.deep_type_value(
									template=value,
									data=data_value
								):
									raise Exception(f"Value '{template_value}' maybe has wrong format in data")
				elif isinstance(template, dict) and isinstance(data, dict):
					template_keys = template.keys()
					for key in template_keys:
						# Key can be any 
						if not key == "<any_key>":
							if key not in data.keys():
								raise Exception(f"Key '{key}' missing in data")
						template_value = template[key]
						if not template_value == "<any_val>":
							if key == "<any_key>":
								# get the only key
								data_value = data[next(iter(data.keys()))]
							else:
								data_value = data[key]
							## value can be empty object
							if not data_value:
								return None
							if not isinstance(data_value, type(template_value)):
								raise Exception(f"Data value not instance with template")
							if isinstance(template_value, str) and isinstance(data_value, str):
								if not template_value == data_value:
									raise Exception(f"Value '{template_value} missing in data")
								else:
									return True
							if not self.deep_type_value(
								template=template_value,
								data=data_value
							):
								raise Exception(f"Value '{template_value}' maybe has wrong format in data")
				else:
					raise Exception(f"Data in wrong type format")
			except Exception as e:
				print(f"{str(e)}")
				return False
			else:
				return True		
	def check_file_format(
		self,
		template : Type[T_EDGE_EMBEDDING_TEMPLATE],
		data: Any
	) -> bool:
		try:
			if not data:
				raise Exception(f"data was empty")
			if not template:
				raise Exception(f"template was empty")
			if not type(data) == type(template):
				raise Exception(f"data and template have different types.")
			return self.deep_type_value(
				template=template,
				data=data
			)
		except Exception as e:
			print(f"{str(e)}")
			return False