from readgraphembedding import ReadGraphEmbedding
from readnodeembedding import ReadNodeEmbedding
from readedgeembedding import ReadEdgeEmbedding

def test_read_graph():
	graphEmbedding = ReadGraphEmbedding(
		file_path="D:\\Research\\ComplexNetworks\\Complex-Networks-experiments\\FTG\\src\\common\\lib\\sgraph\\storegraph\\sample\\graphembedding\\sample_graph_graphembedding.json"
	)
	print(graphEmbedding.data)
	graphEmbedding = ReadGraphEmbedding(
		file_path="D:\\Research\\ComplexNetworks\\Complex-Networks-experiments\\FTG\\src\\common\\lib\\sgraph\\storegraph\\sample\\graphembedding\\sample_graph_graphembedding.txt"
	)
	print(graphEmbedding.data)
	graphEmbedding = ReadGraphEmbedding(
		file_path="D:\\Research\\ComplexNetworks\\Complex-Networks-experiments\\FTG\\src\\common\\lib\\sgraph\\storegraph\\sample\\graphembedding\\sample_graph_graphembedding.csv"
	)
	print(graphEmbedding.data)

def test_read_node():
	nodeEmbedding = ReadNodeEmbedding()
	nodeEmbedding.read(
		file_path="D:\\Research\\ComplexNetworks\\Complex-Networks-experiments\\FTG\\src\\common\\lib\\sgraph\\storegraph\\sample\\nodeembedding\\sample_graph_nodeembedding.csv",
	)
	print(nodeEmbedding.data)
	nodeEmbedding.read(
		file_path="D:\\Research\\ComplexNetworks\\Complex-Networks-experiments\\FTG\\src\\common\\lib\\sgraph\\storegraph\\sample\\nodeembedding\\sample_graph_nodeembedding.json"
	)
	print(nodeEmbedding.data)
	nodeEmbedding.read(
		file_path="D:\\Research\\ComplexNetworks\\Complex-Networks-experiments\\FTG\\src\\common\\lib\\sgraph\\storegraph\\sample\\nodeembedding\\sample_graph_nodeembedding.txt"
	)
	print(nodeEmbedding.data)
		
def test_read_edge():
	edgeEmbedding = ReadEdgeEmbedding()
	edgeEmbedding.read(
		file_path="D:\\Research\\ComplexNetworks\\Complex-Networks-experiments\\FTG\\src\\common\\lib\\sgraph\\storegraph\\sample\\edgeembedding\\edgelist\\sample_graph_edgelist_edgeembedding.csv",
		repr="edgelist"
	)
	edgeEmbedding.read(
		file_path="D:\\Research\\ComplexNetworks\\Complex-Networks-experiments\\FTG\\src\\common\\lib\\sgraph\\storegraph\\sample\\edgeembedding\\adjlist\\sample_graph_adjlist_edgeembedding.json",
		repr="adjlist"
	)
	edgeEmbedding.read(
		file_path="D:\\Research\\ComplexNetworks\\Complex-Networks-experiments\\FTG\\src\\common\\lib\\sgraph\\storegraph\\sample\\edgeembedding\\adjmatrix\\sample_graph_adjmatrix_edgeembedding.json",
		repr="adjlist"
	)
	edgeEmbedding.read(
		file_path="D:\\Research\\ComplexNetworks\\Complex-Networks-experiments\\FTG\\src\\common\\lib\\sgraph\\storegraph\\sample\\edgeembedding\\edgelist\\sample_graph_edgelist_edgeembedding.json",
		repr="edgelist"
	)
	edgeEmbedding.read(
		file_path="D:\\Research\\ComplexNetworks\\Complex-Networks-experiments\\FTG\\src\\common\\lib\\sgraph\\storegraph\\sample\\edgeembedding\\adjlist\\sample_graph_adjlist_edgeembedding.txt",
		repr="adjlist"
	)
	edgeEmbedding.read(
		file_path="D:\\Research\\ComplexNetworks\\Complex-Networks-experiments\\FTG\\src\\common\\lib\\sgraph\\storegraph\\sample\\edgeembedding\\adjmatrix\\sample_graph_adjmatrix_edgeembedding.txt",
		repr="adjmatrix"
	)
	edgeEmbedding.read(
		file_path="D:\\Research\\ComplexNetworks\\Complex-Networks-experiments\\FTG\\src\\common\\lib\\sgraph\\storegraph\\sample\\edgeembedding\\edgelist\\sample_graph_edgelist_edgeembedding.txt",
		repr="edgelist"
	)
	print(edgeEmbedding.data)

# test_read_graph()

test_read_node()

test_read_edge()

print()