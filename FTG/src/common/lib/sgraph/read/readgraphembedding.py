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

GRAPH_LIST: List[str] = [
	"nodeembedding",
	"edgeembedding",
]

T_GRAPH_LIST = TypeVar("T_GRAPH_LIST", bound=GRAPH_LIST)

GRAPH_OBJECT: Dict[str, Dict[str, Any]] = {
    "graph": {
    	"nodeembedding" : "<any_val>",
	    "edgeembedding" : "<any_val>",
    }
}

T_GRAPH_OBJECT = TypeVar("T_GRAPH_OBJECT", bound=GRAPH_OBJECT)

GRAPH_EMBEDDING_TEMPLATE : Union[Type[T_GRAPH_LIST], Type[T_GRAPH_OBJECT]] = None

T_GRAPH_EMBEDDING_TEMPLATE = TypeVar("T_GRAPH_EMBEDDING_TEMPLATE", bound=GRAPH_EMBEDDING_TEMPLATE)

GRAPH_READ_FROM : Dict[str, Type[T_GRAPH_EMBEDDING_TEMPLATE]] = {
	".txt" : GRAPH_LIST,
	".json" : GRAPH_OBJECT,
	".csv" : GRAPH_LIST,
}

class ReadGraphEmbedding(BaseReadEmbedding):
	def __init__(
		self,
		file_path : str = None,
		**kwargs
	) -> None:
		self.data = None
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
		file_path: str,
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
				raise ValueError("Unsupported graph embedding file format.")
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
			if not self.check_file_format(
				template=GRAPH_READ_FROM[".txt"],
				data = header
			):
				raise Exception(f"Out of graph embedding format.")
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
				template=GRAPH_READ_FROM[".json"],
				data=data
			):
				raise Exception(f"Out of graph embedding format.")
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
			with open(file_path, 'r') as csvfile:
				csv_reader = csv.reader(csvfile)
				header = next(csv_reader)  # Read the first line as the header
				if not self.check_file_format(
					template=GRAPH_READ_FROM[".csv"],
					data=header
				):
					raise Exception(f"Out of graph embedding format.")
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
						if value == "<any_key>" or value == "<any_val>":
							continue
						if value not in data:
							raise Exception(f"Value '{value}' missing in data")
				elif isinstance(template, dict) and isinstance(data, dict):
					template_keys = template.keys()
					for key in template_keys:
						# Key can be any 
						if not key == "<any_key>":
							if key not in data.keys():
								raise Exception(f"Key '{key}' missing in data")
						template_value = template[key]
						if not template_value == "<any_val>":						
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
		template : Type[GRAPH_EMBEDDING_TEMPLATE],
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
		else:
			return True
