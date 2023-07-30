from copy import deepcopy
from typing import Any, Callable, Dict, Set, List, Optional, Tuple, Type, TypeVar, Union
import json
import csv
import os

from sgraph.read.basegraphread import BaseGraphRead

FILEEXT : Set[str] = [
	".csv",
	".json",
	".txt",
	# "tsv",
	# "pkl",
]

REPR : Set[str] = [
	"adjlist",
	"edgelist",
	"adjmatrix",
]

class ReadEdgeEmbedding(BaseGraphRead):
	edge : Dict
	def __init__(
		self,
	) -> None:
		self.edge = None
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
		rerp: str = "adjlist"
	):
		def __parseLine(string: str) -> List:
			# string = string.strip()
			lines = string.split("\n")
			if not lines:
				return None
			for i in range(len(lines)):
				lines[i] = lines[i].strip()
				lines[i] = lines[i].split(" ")	## regex?
			return lines
		##
		try:
			if not repr or repr not in REPR:
				print("Try to read in edgelist representation")
				return self.read_embedding_txt_edgelist(file_path = file_path)
			if repr == "edgelist":
				return self.read_embedding_txt_edgelist(file_path = file_path)
			elif rerp == "adjlist":
				return self.read_embedding_txt_adjlist(file_path = file_path)
			elif rerp == "adjmatrix":
				return self.read_embedding_txt_adjmatrix(file_path = file_path)
		except IOError as e:
			print(f"{str(e)}")
			return False
		except Exception as e:
			print(f"{str(e)}")
			return False
		else:
			return True
	def read_embedding_txt_edgelist(
		self,
		file_path: str
	) -> bool:
			data = {}
			with open(file_path, 'r') as txtfile:
				lines = txtfile.readlines()
			# Create the data dictionary from the lines
			for i in range(0, len(lines)):
				key = lines[i].strip()  # Remove any leading/trailing whitespace or newline
				value = lines[i + 1].strip()
				data[key] = value
			self.edge = data
	def read_embedding_txt_adjlist(
		self,
		file_path: str
	) -> bool:
			data = {}
			with open(file_path, 'r') as txtfile:
				lines = txtfile.readlines()
			# Create the data dictionary from the lines
			for i in range(0, len(lines)):
				key = lines[i].strip()  # Remove any leading/trailing whitespace or newline
				value = lines[i + 1].strip()
				data[key] = value
			self.edge = data
	def read_embedding_txt_adjmatrix(
		self,
		file_path: str
	) -> bool:
			data = {}
			with open(file_path, 'r') as txtfile:
				lines = txtfile.readlines()
			# Create the data dictionary from the lines
			for i in range(0, len(lines)):
				key = lines[i].strip()  # Remove any leading/trailing whitespace or newline
				value = lines[i + 1].strip()
				data[key] = value
			self.edge = data
	def read_embedding_json(
		self,
		file_path: str,
		key: str = "edge",
	) -> bool:
		try:
			with open(file_path, "r") as json_file:
				data = json.load(json_file)
			if isinstance(data,dict) and key in data:
				self.edge = data[key]
			else:
				raise Exception(f"something")
		except IOError as e:
			print(f"{str(e)}")
			return False
		except Exception as e:
			print(f"{str(e)}")
			return False
		else:
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
				for row in csv_reader:
					edge = row[0]
					edge_atts = {
						header[i]: row[i] for i in range(1, len(header))  # Create a dictionary for the edge data
					}
					data[edge] = edge_atts
			self.edge = data
		except IOError as e:
			print(f"{str(e)}")
			return False
		except Exception as e:
			print(f"{str(e)}")
			return False
		else:
			return True