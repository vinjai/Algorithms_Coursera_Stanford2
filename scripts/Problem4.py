#!/usr/bin/env python

"""
In this assignment you will implement one or more algorithms for the all-pairs shortest-path problem. Here are data
files describing three graphs:

g1.txt
g2.txt
g3.txt
The first line indicates the number of vertices and edges, respectively. Each subsequent line describes an edge (the
first two numbers are its tail and head, respectively) and its length (the third number). NOTE: some of the edge
lengths are negative. NOTE: These graphs may or may not have negative-cost cycles.

Your task is to compute the "shortest shortest path". Precisely, you must first identify which, if any, of the three
graphs have no negative cycles. For each such graph, you should compute all-pairs shortest paths and remember the
smallest one (i.e., compute minu,v?Vd(u,v), where d(u,v) denotes the shortest-path distance from u to v).

If each of the three graphs has a negative-cost cycle, then enter "NULL" in the box below. If exactly one graph has no
negative-cost cycles, then enter the length of its shortest shortest path in the box below. If two or more of the
graphs have no negative-cost cycles, then enter the smallest of the lengths of their shortest shortest paths in the
box below.

OPTIONAL: You can use whatever algorithm you like to solve this question. If you have extra time, try comparing the
performance of different all-pairs shortest-path algorithms!
"""

__author__ = 'Vinayak'

from fileIO import readAsListOfDict,writeSingleToFile
from math import inf

def runFloydWarshallAlgorithm(vertexCount,edgeCount,edgeList):
    """returns the smallest shortest distance after running Floyd Warshall Algorithm"""

    #memoitization
    array=[ [ inf for j in range(1,vertexCount+2) ] for i in range(1,vertexCount+2) ]

    for i in range(1,vertexCount+1):
        array[i][i]=0

    for edge in edgeList:
        array[edge["tail"]][edge["head"]]=edge["cost"]

    for k in range(vertexCount+1):
        for i in range(1,vertexCount+1):
            for j in range(1,vertexCount+1):
                array[i][j]=min(array[i][j],array[i][k]+array[k][j])
                if i==j and array[i][j]<0:
                    return inf             #infinity signifies negative cycle

    return min(min(array,key=lambda v:min(v)))

if __name__=="__main__":
    inputListG1=readAsListOfDict('_6ff856efca965e8774eb18584754fd65_g1.txt','\s+',3,
                               ["tail","head","cost"],[int,int,int],0,1)
    vertexCountG1,edgeCountG1=[int(i) for i in inputListG1.pop(0).split(' ')]
    inputListG2=readAsListOfDict('_6ff856efca965e8774eb18584754fd65_g2.txt','\s+',3,
                               ["tail","head","cost"],[int,int,int],0,1)
    vertexCountG2,edgeCountG2=[int(i) for i in inputListG2.pop(0).split(' ')]
    inputListG3=readAsListOfDict('_6ff856efca965e8774eb18584754fd65_g3.txt','\s+',3,
                               ["tail","head","cost"],[int,int,int],0,1)
    vertexCountG3,edgeCountG3=[int(i) for i in inputListG3.pop(0).split(' ')]
    writeSingleToFile('Problem4.txt',min(runFloydWarshallAlgorithm(vertexCountG1,edgeCountG1,inputListG1),
                      runFloydWarshallAlgorithm(vertexCountG2,edgeCountG2,inputListG2),
                      runFloydWarshallAlgorithm(vertexCountG3,edgeCountG3,inputListG3)))