#!/usr/bin/env python

"""
In this programming problem and the next you'll code up the clustering algorithm from lecture for computing a
max-spacing k-clustering.

Download the text file below.

clustering1.txt
This file describes a distance function (equivalently, a complete graph with edge costs). It has the following format:

[number_of_nodes]

[edge 1 node 1] [edge 1 node 2] [edge 1 cost]

[edge 2 node 1] [edge 2 node 2] [edge 2 cost]

...

There is one edge (i,j) for each choice of 1?i<j?n, where n is the number of nodes.

For example, the third line of the file is "1 3 5250", indicating that the distance between nodes 1 and 3 (equivalently,
the cost of the edge (1,3)) is 5250. You can assume that distances are positive, but you should NOT assume that they
are distinct.

Your task in this problem is to run the clustering algorithm from lecture on this data set, where the target number k
of clusters is set to 4. What is the maximum spacing of a 4-clustering?

ADVICE: If you're not getting the correct answer, try debugging your algorithm using some small test cases. And then
post them to the discussion forum!
"""

__author__ = 'Vinayak'

from fileIO import readAsListOfDict,writeSingleToFile

class UnionFind(object):
    """Implementation of Union Find Data Structure"""

    def __init__(self, nodeList):
        self._nodeLeaderList=dict()
        self._nodeList=nodeList
        self._nodeCount=len(nodeList)
        for node in nodeList:
            self._nodeLeaderList.update({node:node})

    def find(self, node):
        """Return leader of given node"""
        return self._nodeLeaderList[node]

    def union(self, node1, node2):
        """Union of tree containing node1 and tree containing node2"""
        leader1 = self._nodeLeaderList[node1]
        leader2 = self._nodeLeaderList[node2]

        if leader1==leader2:
            return

        tree1 = [node for node,leader in self._nodeLeaderList.items() if leader == leader1]
        tree2 = [node for node,leader in self._nodeLeaderList.items() if leader == leader2]

        if len(tree1)<len(tree2):
            for node in tree1:
                self._nodeLeaderList[node]=leader2
        else:
            for node in tree2:
                self._nodeLeaderList[node]=leader1

    def uniqueLeaders(self):
        return len(set([leader for node,leader in self._nodeLeaderList.items()]))


def kruskalClustering(edgeList, nodeCount, numberOfClusters):
    """Return cost of maximum spacing edge after kruskal clustering"""

    edgeList.sort(key = lambda v:v["cost"])

    UFObj = UnionFind(list(range(1,nodeCount+1)))

    while UFObj.uniqueLeaders() != numberOfClusters:
        edge = edgeList.pop(0)
        UFObj.union(edge["node1"],edge["node2"])

    maxSpacingEdge={}

    while edgeList:
        maxSpacingEdge = edgeList.pop(0)
        if(UFObj.find(maxSpacingEdge["node1"])!=UFObj.find(maxSpacingEdge["node2"])):
            break

    return maxSpacingEdge["cost"]

if __name__=='__main__':
    inputList = readAsListOfDict("_fe8d0202cd20a808db6a4d5d06be62f4_clustering1.txt",'\s+'
                           ,3,['node1','node2','cost'],[int,int,int],0,1)
    nodeCount = int(inputList.pop(0))
    writeSingleToFile("Problem2a.txt",kruskalClustering(inputList,nodeCount,4))

