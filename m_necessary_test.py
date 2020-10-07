import networkx as nx
from networkx.algorithms.approximation import clique
import matplotlib.pyplot as plt
import result_logging as lg
from itertools import combinations
import numpy as np
import task_generator, header, CWEDF
import read_tasks_from_file as rtff

def buildTaskGraph(task_set):
	adjacency_matrix = [ [0 for i in range(len(task_set))] for j in range(len(task_set))]
	for task in task_set:
		for item in task_set:
			if task.number != item.number:
				#add an edge if the necessary condition is not satisfied
				if task.ex_time > 2*(item.period-item.ex_time):
					adjacency_matrix[task.number][item.number] = 1
				elif task.utilisation + item.utilisation > 1:
					adjacency_matrix[task.number][item.number] = 1
	np.array(adjacency_matrix).view()
	G = nx.from_numpy_matrix(np.array(adjacency_matrix), parallel_edges=False,create_using=nx.DiGraph)
	for node in G.nodes():
		G.node[node]['weight'] = task_set[node].utilisation
	return G

def findLargestClique(G):
	'''finds all maximal cliques in the graph '''
	G2 = G.to_undirected()
	'''because we cannot find cliques ina digraph using this api'''
	cliques = list(nx.find_cliques(G2))
	'''return the largest clique'''
	cliquesize = 0
	#print ("cliques are", cliques)
	for clique in cliques:
		if len(clique) > cliquesize:
			cliquesize = len(clique)
	return cliquesize


def drawGraph(G):
	node_labels = {node:node for node in G.nodes()}
	nx.draw(G,labels=node_labels)
	plt.show()
	return G

def main(task_set):
	G = buildTaskGraph(task_set)
	cliquesize = findLargestClique(G)
	return cliquesize

if __name__ == '__main__':
	task_set = []
	
	task_set.append(task_generator.generateTask(0, 1000, 0.8669207464643705))#, 866.9207464643705), 
	task_set.append(task_generator.generateTask(1, 200, 0.7838792955831181))#, 156.77585911662362), 
	task_set.append(task_generator.generateTask(2, 100, 0.24724443080396466))#, 24.724443080396465), 
	task_set.append(task_generator.generateTask(3, 200, 0.7629044722127165))#, 152.5808944425433), 
	task_set.append(task_generator.generateTask(4, 1000, 0.9390510549358302))#, 939.0510549358302)


	main(task_set)



