#!/usr/bin/env python

"""
In this programming problem you'll code up Prim's minimum spanning tree algorithm.

Download the text file below.

edges.txt
This file describes an undirected graph with integer edge costs. It has the format

[number_of_nodes] [number_of_edges]

[one_node_of_edge_1] [other_node_of_edge_1] [edge_1_cost]

[one_node_of_edge_2] [other_node_of_edge_2] [edge_2_cost]

...

For example, the third line of the file is "2 3 -8874", indicating that there is an edge connecting vertex #2
and vertex #3 that has cost -8874.

You should NOT assume that edge costs are positive, nor should you assume that they are distinct.

Your task is to run Prim's minimum spanning tree algorithm on this graph. You should report the overall cost of
a minimum spanning tree --- an integer, which may or may not be negative --- in the box below.

IMPLEMENTATION NOTES: This graph is small enough that the straightforward O(mn) time implementation of Prim's
algorithm should work fine. OPTIONAL: For those of you seeking an additional challenge, try implementing a
heap-based version. The simpler approach, which should already give you a healthy speed-up, is to maintain
relevant edges in a heap (with keys = edge costs). The superior approach stores the unprocessed vertices in
the heap, as described in lecture. Note this requires a heap that supports deletions, and you'll probably need
to maintain some kind of mapping between vertices and their positions in the heap.
"""

__author__ = 'Vinayak'

from fileIO import readAsListOfDict,writeSingleToFile
import heapq
import collections

def prim(inputList, nodeCount):
    """Returns Prim's MST on graph given in the form of edge list"""

    edgeList=[(edge['cost'],[edge['node1'],edge['node2']]) for edge in inputList]
    heapq.heapify(edgeList)

    exploredNodes = set()
    unexploredNodes = set.union({edge['node1'] for edge in inputList},{edge['node2'] for edge in inputList})
    edgesInMST = set()
    MSTCost = 0

    startNode = edgeList[0][1][0]
    exploredNodes.add(startNode)
    unexploredNodes.remove(startNode)

    while len(unexploredNodes) != 0:

        edgeHeap=list(filter(lambda e:e[1][0] in exploredNodes or e[1][1] in exploredNodes,edgeList))
        heapq.heapify(edgeHeap)
        edge=heapq.heappop(edgeHeap)
        cost,node1,node2=edge[0],edge[1][0],edge[1][1]

        if node1 not in exploredNodes:
            exploredNodes.add(node1)
            unexploredNodes.remove(node1)

        if node2 not in exploredNodes:
            exploredNodes.add(node2)
            unexploredNodes.remove(node2)

        MSTCost+=cost
        edgesInMST.add((node1,node2,cost))

        edgeList=list(filter(lambda e:e[1][0] in unexploredNodes or e[1][1] in unexploredNodes,edgeList))

    return edgesInMST, MSTCost


if __name__=="__main__":
    inputList=readAsListOfDict('_d4f3531eac1d289525141e95a2fea52f_edges.txt','\s+'
                           ,3,['node1','node2','cost'],[int,int,int],0,1)
    nodeCount,edgeCount=[int(i) for i in inputList[0].split(' ')]
    del inputList[0]
    writeSingleToFile("Problem1c.txt",prim(inputList,nodeCount)[1])
