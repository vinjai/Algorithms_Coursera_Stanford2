#!/usr/bin/env python

"""
In this assignment you will implement one or more algorithms for the 2SAT problem. Here are 6 different 2SAT instances:

2sat1.txt
2sat2.txt
2sat3.txt
2sat4.txt
2sat5.txt
2sat6.txt

The file format is as follows. In each instance, the number of variables and the number of clauses is the same, and
this number is specified on the first line of the file. Each subsequent line specifies a clause via its two literals,
with a number denoting the variable and a "-" sign denoting logical "not". For example, the second line of the first
data file is "-16808 75250", which indicates the clause !x16808?x75250.

Your task is to determine which of the 6 instances are satisfiable, and which are unsatisfiable. In the box below,
enter a 6-bit string, where the ith bit should be 1 if the ith instance is satisfiable, and 0 otherwise. For example,
if you think that the first 3 instances are satisfiable and the last 3 are not, then you should enter the string
111000 in the box below.

DISCUSSION: This assignment is deliberately open-ended, and you can implement whichever 2SAT algorithm you want. For
example, 2SAT reduces to computing the strongly connected components of a suitable graph (with two vertices per
variable and two directed edges per clause, you should think through the details). This might be an especially
attractive option for those of you who coded up an SCC algorithm for my Algo 1 course. Alternatively, you can use
Papadimitriou's randomized local search algorithm. (The algorithm from lecture is probably too slow as stated,
so you might want to make one or more simple modifications to it --- even if this means breaking the analysis given
in lecture --- to ensure that it runs in a reasonable amount of time.) A third approach is via backtracking. In
lecture we mentioned this approach only in passing; see Chapter 9 of the Dasgupta-Papadimitriou-Vazirani book, for
example, for more details.
"""

__author__ = 'Vinayak'

from fileIO import readAsList,writeSingleToFile

def getStronglyConnectedComponents(edgesList):
    """Calculate Strongly connected components and return if two complements not found in same SCC"""

    graph=dict()
    graphRev=dict()
    finishTimes=list()
    for e in edgesList:
        if not e[0] in graph:
            graph[e[0]]={e[1]}
        else:
            graph[e[0]].add(e[1])
        if not e[1] in graphRev:
            graphRev[e[1]]={e[0]}
        else:
            graphRev[e[1]].add(e[0])

    t=0
    exploredNodes=set()

    def _DFS_on_Rev(i):
        nonlocal t
        nonlocal exploredNodes
        nonlocal finishTimes
        nonlocal graphRev

        if not i in exploredNodes:
            exploredNodes.add(i)
            if i in graphRev:
                for node in graphRev[i]:
                    if node not in exploredNodes:
                        _DFS_on_Rev(node)
            finishTimes.append(i)
            t+=1

    graphRevKeys=list(graphRev.keys())

    graphRevKeys.sort(reverse=True)

    for vertex in graphRevKeys:
        if not vertex in exploredNodes:
            _DFS_on_Rev(vertex)

    exploredNodes=set()

    def _DFS(i):
        nonlocal exploredNodes
        nonlocal graph
        nonlocal currentSCC
        nonlocal flag

        if not i in exploredNodes:
            exploredNodes.add(i)
            if i in graph:
                for node in graph[i]:
                    if node not in exploredNodes:
                        _DFS(node)

            if -i in currentSCC:
                flag=False
                return
            currentSCC.add(i)

    flag = True
    for i in reversed(finishTimes):
        if not i in exploredNodes:
            currentSCC=set()
            _DFS(i)
            if not flag:
                break

    return flag

def return2SATEdgeList(inputList):
    """return edgeList of 2-SAT problem"""

    inputList.pop(0)
    clauseList = [tuple(int(x) for x in line.split(' ')) for line in inputList ]
    edgeList=list()

    for clause in clauseList:
        edgeList.append({0:-clause[0],1:clause[1]})
        edgeList.append({0:-clause[1],1:clause[0]})

    return edgeList

if __name__=="__main__":
    inputFiles=['_02c1945398be467219866ee1c3294d2d_2sat1.txt'
                ,'_02c1945398be467219866ee1c3294d2d_2sat2.txt'
                ,'_02c1945398be467219866ee1c3294d2d_2sat3.txt'
                ,'_02c1945398be467219866ee1c3294d2d_2sat4.txt'
                ,'_02c1945398be467219866ee1c3294d2d_2sat5.txt'
                ,'_02c1945398be467219866ee1c3294d2d_2sat6.txt']

    resultList=[ getStronglyConnectedComponents(return2SATEdgeList(readAsList(fileName))) for fileName in inputFiles]
    writeSingleToFile("Problem6.txt","".join(('1' if result else '0' for result in resultList )))

