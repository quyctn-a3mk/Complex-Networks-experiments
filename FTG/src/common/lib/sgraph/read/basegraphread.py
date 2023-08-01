import time
import queue
from copy import deepcopy
import argparse
from typing import Any, Callable, Dict, Set, List, Optional, Tuple, Type, TypeVar, Union
import threading
import argparse
import json
import csv
import os

SelfBaseReadEmbedding = TypeVar("SelfBaseReadEmbedding", bound="BaseReadEmbedding")

STORETYPE : Dict[str, str] = {
	"AL" : "adjacency-list",
	"AM" : "adjacency-matrix",
	"EL" : "edge-list",
	"XX" : "others",
}

FILEEXT : Set[str] = [
	".csv",
	".json",
	# ".txt",
	# ".tsv",
	# ".pkl",
]

class BaseReadEmbedding:
	def __init__(
		self,
	) -> None:
		self.data = None
	'''
	interface
	'''
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
		file_path: str
	):
		pass
	def read_embedding_json(
		self,
		file_path: str
	):
		pass
	def read_embedding_csv(
		self,
		file_path: str
	):
		pass