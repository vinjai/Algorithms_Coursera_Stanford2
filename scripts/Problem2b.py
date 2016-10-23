#!/usr/bin/env python

"""
In this question your task is again to run the clustering algorithm from lecture, but on a MUCH bigger graph. So big,
in fact, that the distances (i.e., edge costs) are only defined implicitly, rather than being provided as an explicit
list.

The data set is below.

clustering_big.txt
The format is:

[# of nodes] [# of bits for each node's label]

[first bit of node 1] ... [last bit of node 1]

[first bit of node 2] ... [last bit of node 2]

...

For example, the third line of the file "0 1 1 0 0 1 1 0 0 1 0 1 1 1 1 1 1 0 1 0 1 1 0 1" denotes the 24 bits
associated with node #2.

The distance between two nodes u and v in this problem is defined as the Hamming distance--- the number of differing
bits --- between the two nodes' labels. For example, the Hamming distance between the 24-bit label of node #2 above
and the label "0 1 0 0 0 1 0 0 0 1 0 1 1 1 1 1 1 0 1 0 0 1 0 1" is 3 (since they differ in the 3rd, 7th, and 21st bits).

The question is: what is the largest value of k such that there is a k-clustering with spacing at least 3? That is,
how many clusters are needed to ensure that no pair of nodes with all but 2 bits in common get split into different
clusters?

NOTE: The graph implicitly defined by the data file is so big that you probably can't write it out explicitly, let
alone sort the edges by cost. So you will have to be a little creative to complete this part of the question. For
example, is there some way you can identify the smallest distances without explicitly looking at every pair of nodes?
"""


__author__ = 'Vinayak'

from fileIO import readAsList,writeSingleToFile
from itertools import combinations
import re


class UnionFind(object):
    """Implementation of Union Find Data Structure"""

    def __init__(self, nodeList):
        self._nodeLeaderList=dict()
        self._leaderSets = dict()
        self._nodeList=nodeList
        self._nodeCount=len(nodeList)
        for node in nodeList:
            self._leaderSets.update({node:{node}})
            self._nodeLeaderList.update({node:node})

    def find(self, node):
        """Return leader of given node"""
        return self._nodeLeaderList[node]

    def union(self, node1, node2):
        """Union of tree containing node1 and tree containing node2"""
        leader1 = self.find(node1)
        leader2 = self.find(node2)

        if leader1==leader2:
            return

        tree1 = self._leaderSets[leader1]
        tree2 = self._leaderSets[leader2]

        if len(tree1)<len(tree2):
            for node in tree1:
                self._nodeLeaderList[node]=leader2
            self._leaderSets[leader2]=self._leaderSets[leader2].union(self._leaderSets[leader1])
            del self._leaderSets[leader1]
        else:
            for node in tree2:
                self._nodeLeaderList[node]=leader1
            self._leaderSets[leader1]=self._leaderSets[leader1].union(self._leaderSets[leader2])
            del self._leaderSets[leader2]

    def uniqueLeaders(self):
        return len(self._leaderSets)

def calculateMasks(bitCount, maxCombinations):
    """Create swap masks in the form tuples with numbers indicating which bits to swap."""

    masks = []
    for i in range(1,maxCombinations):
        masks=masks+[ c for c in combinations(range(bitCount), i) ]

    return masks

def swapByMask(nodeLabel, mask):
    """Swap bits in label according to a mask"""

    modNodeLabel = [ c for c in nodeLabel ]

    for bitNum in mask:
        if modNodeLabel[bitNum] == '0':
            modNodeLabel[bitNum] = '1'
        elif modNodeLabel[bitNum] == '1':
            modNodeLabel[bitNum] = '0'

    return "".join(modNodeLabel)

def generateIntegerLabels(nodeList):
    """Returns Dictionary of labels for nodes"""
    d = dict()
    for node in nodeList:
        d.update({node:int(node,2)})
    return d

def maskClustering(nodeList, maxSpacing, bitCount):
    """Return the number of clusters formed when maxSpacing is achieved"""

    swapMasks = calculateMasks(bitCount,maxSpacing)
    labels = generateIntegerLabels(nodeList)

    UFObj = UnionFind([value for key, value in labels.items() ])

    for node in nodeList:
        currentLabel=labels[node]
        for mask in swapMasks:
            modNodeLabel = swapByMask(node,mask)
            if modNodeLabel in labels:
                UFObj.union(labels[modNodeLabel],currentLabel)

    return UFObj.uniqueLeaders()



if __name__=='__main__':
    inputList = readAsList("_fe8d0202cd20a808db6a4d5d06be62f4_clustering_big.txt")
    nodeCount, bitCount = [int(value) for value in inputList.pop(0).split(' ')]
    inputList = [re.sub('\s+','',string) for string in inputList]
    writeSingleToFile("Problem2b.txt",maskClustering(inputList,3,bitCount))

