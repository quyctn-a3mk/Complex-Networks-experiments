import sys
import argparse
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Type, TypeVar, Union

from common.lib.sgraph import SGraph
from utils.basealgo import BaseAlgorithm

# from utils.ftg import FTG_MC, FTG_R
from utils.tg import GreedyMCSC as G_MCSC, GreedyRevenue as G_R

ALGO: Dict[str, List[Type[BaseAlgorithm]]] = {
	# "1" : FTG_MC,
	# "2" : FTG_R,
	"3" : G_MCSC,
	"4" : G_R,
}

def argumentParse():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"-i",
		"--inFile", 
		type=str, 
		required=True,
		help = "File input formated, a file path."
	)
	parser.add_argument(
		"-o",
		"--outFile", 
		type=str, 
		default="",
		required=False,
		help = "File output writing result of algorithm process (text data), a file path."
	)
	parser.add_argument(
		"-s",
		"--seedFile", 
		type=str, 
		default="",
		required=False,
		help = "File output contain the seed set lists was found, a file path."
	)
	parser.add_argument(
		"-c",
		"--chartFile", 
		type=str, 
		default="",
		required=False,
		help = "File output display as table for chart design, a file path."
	)		
	parser.add_argument(
		"--algo",
		type = str,
		default = "1",
		required = False,
		choices=list(ALGO.keys()),
		help = f"FTG Expriment version Algorithm: '1'('ftg') - '2'('greedy')",
	)
	parser.add_argument(
		"--algo-kwargs",
		type=str, 
		nargs=argparse.REMAINDER,
		help="Optional keyword argument to pass to the FTG algorithm",
	)
	return parser

def main(sys_argv) -> None:
	args, unknown_args = argumentParse().parse_known_args(args=sys_argv)
	## inFile
	inFile = args.inFile ## need to check inFile isExist and isFilePath.
	if not inFile:
		print("There is no input file.")
		return False
	##
	outFile = args.outFile
	if not outFile:
		extSplit = inFile.split(".")
		outFile = extSplit[-2] + ".out"
	##
	seedFile = args.seedFile	
	if not seedFile:
		extSplit = inFile.split(".")
		seedFile = extSplit[-2] + ".seed"
	##
	chartFile = args.chartFile
	if not chartFile:
		extSplit = inFile.split(".")
		chartFile = extSplit[-2] + ".chart"
	## ====RUN====
	sgraph = SGraph.cReadFile_GraphFormatted(path = inFile)
	## Process unknown_args to remove '--algo-kwargs' from the list
	if "--algo-kwargs" in unknown_args:
		unknown_args.remove("--algo-kwargs")
	args.algo_kwargs = unknown_args
	##
	algo = args.algo
	algo_kwargs = args.algo_kwargs
	for algorithm in ALGO[algo]:
		instance = algorithm.load(graph = sgraph, sys_argv = algo_kwargs)
	seed_set = instance.run()
	print(seed_set)

if __name__ == "__main__":
	main(sys.argv[1:])