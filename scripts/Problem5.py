#!/usr/bin/env python

"""
In this assignment you will implement one or more algorithms for the traveling salesman problem, such as the dynamic
programming algorithm covered in the video lectures. Here is a data file describing a TSP instance.

tsp.txt
The first line indicates the number of cities. Each city is a point in the plane, and each subsequent line indicates
the x- and y-coordinates of a single city.

The distance between two cities is defined as the Euclidean distance --- that is, two cities at locations (x,y) and
(z,w) have distance (x?z)2+(y?w)2???????????????? between them.

In the box below, type in the minimum cost of a traveling salesman tour for this instance, rounded down to the nearest
integer.

OPTIONAL: If you want bigger data sets to play with, check out the TSP instances from around the world here. The
smallest data set (Western Sahara) has 29 cities, and most of the data sets are much bigger than that. What's the
largest of these data sets that you're able to solve --- using dynamic programming or, if you like, a completely
different method?

HINT: You might experiment with ways to reduce the data set size. For example, trying plotting the points. Can you
infer any structure of the optimal solution? Can you use that structure to speed up your algorithm?
"""

__author__ = 'Vinayak'

from fileIO import readAsList, writeSingleToFile
import math
import heapq
from itertools import combinations
import dbm
import pickle

euclidean = lambda i, j: math.sqrt(math.pow(cities[i][0] - cities[j][0], 2) + math.pow(cities[i][1] - cities[j][1], 2))

pickleDump = lambda x : pickle.dumps(x)
pickleLoad = lambda x : pickle.loads(x)

def returnMinTSP(adjMatrix, cityCount):
    """return min distance after running TSP on adjacency matrix"""

    adjMatrix = [ [math.inf if r==c else adjMatrix[r][c] for c in range(cityCount)] for r in range(cityCount)]

    costMatrix=[]
    matrixDictionary={}

    combinationsCompleted = []

    def _computeCost(adjMatrix,cityCount):
        """Computes cost for branch and bound technique and returns cost as well as new adjacency matrix"""

        def _rowReduction(matrix,size):
            """s row reduction on the matrix"""

            cost=0

            for i in range(size):
                minR = min(matrix[i])
                if minR != 0 and minR!=math.inf:
                    cost+=minR
                    matrix[i] = [matrix[i][j] - minR for j in range(size)]

            return matrix,cost

        def _colReduction(matrix,size):
            """performs column reduction on the matrix"""

            #take transpose
            matrix = [list(i) for i in zip(*matrix)]
            matrix,cost = _rowReduction(matrix,size)
            matrix = [list(i) for i in zip(*matrix)]
            return matrix,cost

        row_cost,col_cost = 0,0
        matrix,row_cost = _rowReduction(adjMatrix.copy(),cityCount)
        matrix,col_cost = _colReduction(matrix.copy(),cityCount)

        return matrix,row_cost+col_cost

    matrix,cost=_computeCost(adjMatrix,cityCount)

    heapq.heappush(costMatrix,(cost,tuple([0])))
    matrixDictionary.update({tuple([0]):pickleDump(matrix)})

    cityIndexList = list(range(cityCount))

    costParent = -1
    while True:
        costParent, permParent = heapq.heappop(costMatrix)
        if permParent in matrixDictionary:
            if set(permParent) in combinationsCompleted:
                del matrixDictionary[permParent]
                continue
            print(costParent,permParent)
            if len(permParent) == cityCount:
                break
            matrixParent = pickleLoad(matrixDictionary[permParent])
            remCities = set(cityIndexList).difference(set(permParent))
            listParents = list(permParent)
            lastParent = listParents[-1]

            for remIndex in remCities:
                # edgeCostInReducedMatrix = matrixParent[lastParent][remIndex]
                matrix = matrixParent.copy()

                matrix[lastParent] = [math.inf for _ in range(cityCount)]
                matrix = [list(i) for i in zip(*matrix)]
                matrix[remIndex] = [math.inf for _ in range(cityCount)]
                matrix = [list(i) for i in zip(*matrix)]

                matrix[remIndex][lastParent]=math.inf

                matrixChild,cost=_computeCost(matrix,cityCount)
                # matrixChild,cost=_computeCost(matrix,len(remIndex))

                costChild = costParent+cost+matrixParent[lastParent][remIndex]

                permChild = tuple(listParents+[remIndex])

                if set(permChild) in combinationsCompleted:
                    continue

                heapq.heappush(costMatrix,(costChild,permChild))
                matrixDictionary.update({permChild:pickleDump(matrixChild)})

            del matrixDictionary[permParent]
            combinationsCompleted.append(set(permParent))
    return costParent


    # A, B = dict(), dict()
    # for k in range(1, cityCount):
    #     A[pickleDump((1 << k, k))] = adjMatrix[0][k]
    #
    # for m in range(2, cityCount):
    #     B = dict()
    #     for subset in combinations(range(1, cityCount), m):
    #         bits = 0
    #         for bit in subset:
    #             bits |= (1 << bit)
    #         print(bits)
    #         for j in subset:
    #             prev = bits & ~(1 << j)
    #             subsetToCheck=list(subset)
    #             if 0 in subsetToCheck:
    #                 subsetToCheck.remove(0)
    #             if j in subsetToCheck:
    #                 subsetToCheck.remove(j)
    #             # print(prev,j,A,pickleDump((4,2)))
    #             B[pickleDump((bits, j))] = min([A[pickleDump((prev, k))] + adjMatrix[k][j] for k in subsetToCheck])
    #     A = B.copy()
    #     print("subset size :",m)
    #
    # bits = (2 ** cityCount - 1) - 1
    #
    # return min([A[pickleDump((bits, j))] + adjMatrix[j][0] for j in range(2, cityCount)])



    # with dbm.open('TSPCache','n') as db:
    #     for k in range(1, cityCount):
    #         db[(str(1 << k)+ " " + str(k))] = str(adjMatrix[0][k])
    #     for m in range(2, cityCount):
    #         # B = dict()
    #         for subset in combinations(range(1, cityCount), m):
    #             bits = 0
    #             for bit in subset:
    #                 bits |= (1 << bit)
    #             for j in subset:
    #                 prev = bits & ~(1 << j)
    #                 subsetToCheck=list(subset)
    #                 if 0 in subsetToCheck:
    #                     subsetToCheck.remove(0)
    #                 if j in subsetToCheck:
    #                     subsetToCheck.remove(j)
    #                 db[str(bits) + " "+ str(j)] = str(min([float(db[str(prev) + " " + str(k)]) + adjMatrix[k][j]
    #                                                          for k in subsetToCheck]))
    #         # A = B.copy()
    #         print(m)
    #
    #     bits = (2 ** cityCount - 1) - 1
    #
    #     return min([float(db[str(bits) + " " + str(j)]) + adjMatrix[j][0] for j in range(2, cityCount)])


    # A, B = dict(), dict()
    # for k in range(1, cityCount):
    #     A[(1 << k, k)] = adjMatrix[0][k]
    #
    # for m in range(2, cityCount):
    #     B = dict()
    #     for subset in combinations(range(1, cityCount), m):
    #         bits = 0
    #         for bit in subset:
    #             bits |= (1 << bit)
    #         print(bits)
    #         for j in subset:
    #             prev = bits & ~(1 << j)
    #             subsetToCheck=list(subset)
    #             if 0 in subsetToCheck:
    #                 subsetToCheck.remove(0)
    #             if j in subsetToCheck:
    #                 subsetToCheck.remove(j)
    #             B[(bits, j)] = min([A[(prev, k)] + adjMatrix[k][j] for k in subsetToCheck])
    #     A = B.copy()
    #     print(m)
    #
    # bits = (2 ** cityCount - 1) - 1
    #
    # return min([A[(bits, j)] + adjMatrix[j][0] for j in range(2, cityCount)])

    # adjMatrix = [ [math.inf if r==c else adjMatrix[r][c] for c in range(cityCount)] for r in range(cityCount)]
    #
    # costMatrix=[]
    # matrixDictionary={}
    #
    # def _computeCost(adjMatrix,cityCount):
    #     """Computes cost for branch and bound technique and returns cost as well as new adjacency matrix"""
    #
    #     def _rowReduction(matrix,size):
    #         ""s row reduction on the matrix"""
    # ""
    #
    #         cost=0
    #
    #         for i in range(size):
    #             minR = min(matrix[i])
    #             if minR != 0:
    #                 cost+=minR
    #                 matrix[i] = [matrix[i][j] - minR for j in range(size)]
    #
    #         return matrix,cost
    #
    #     def _colReduction(matrix,size):
    #         """performs column reduction on the matrix"""
    #
    #         #take transpose
    #         matrix = [list(i) for i in zip(*matrix)]
    #         matrix,cost = _rowReduction(matrix,size)
    #         matrix = [list(i) for i in zip(*matrix)]
    #         return matrix,cost
    #
    #     row_cost,col_cost = 0,0
    #     matrix,row_cost = _rowReduction(adjMatrix.copy(),cityCount)
    #     matrix,col_cost = _colReduction(matrix.copy(),cityCount)
    #
    #     return matrix,row_cost+col_cost
    #
    # matrix,cost=_computeCost(adjMatrix,cityCount)
    #
    # heapq.heappush(costMatrix,(cost,tuple([0])))
    # matrixDictionary.update({tuple([0]):matrix})
    #
    # cityIndexList = list(range(cityCount))
    #
    # costParent = -1
    # while True:
    #     costParent, permParent = heapq.heappop(costMatrix)
    #     print(costParent,permParent)
    #     if permParent in matrixDictionary:
    #         if len(permParent) == cityCount:
    #             break
    #         matrixParent = matrixDictionary[permParent]
    #         remCities = set(cityIndexList).difference(set(permParent))
    #         listParents = list(permParent)
    #         lastParent = listParents[-1]
    #
    #         for remIndex in remCities:
    #             # edgeCostInReducedMatrix = matrixParent[lastParent][remIndex]
    #             matrix = matrixParent.copy()
    #
    #             matrix[lastParent] = [math.inf for j in range(cityCount)]
    #             matrix = [list(i) for i in zip(*matrix)]
    #             matrix[remIndex] = [math.inf for j in range(cityCount)]
    #             matrix = [list(i) for i in zip(*matrix)]
    #
    #             matrix[remIndex][lastParent]=math.inf
    #
    #             # matrixChild,cost=_computeCost(matrix,cityCount)
    #             matrixChild,cost=_computeCost(matrix,len(remIndex))
    #
    #             costChild = costParent+cost+matrixParent[lastParent][remIndex]
    #
    #             permChild = tuple(listParents+[remIndex])
    #             heapq.heappush(costMatrix,(costChild,permChild))
    #             matrixDictionary.update({permChild:matrixChild})
    #
    # return costParent

    # A,B=dict(),dict()
    # A[((0,),0)]=0
    # for m in range(1,cityCount):
    #     B = dict()
    #     for subset in combinations(range(1,cityCount),m):
    #         subset=tuple([0]+list(subset))
    #         for j in subset:
    #             if j != 0:
    #                 listWithOutJ = list(subset)
    #                 listWithOutJ.remove(j)
    #                 B[(subset,j)] =min([ math.inf if k==0 and (tuple(listWithOutJ),k) not in A  else A[(tuple(
    #                     listWithOutJ),k)] + adjMatrix[k][j] for k in list(subset) if k != j  ])
    #     A=B.copy()
    #     print(m)
    # return min([ A[(range(25),j)] + adjMatrix[j][0] for j in range(1,cityCount) ])


if __name__ == "__main__":
    inputList = readAsList("_f702b2a7b43c0d64707f7ab1b4394754_tsp.txt")
    # inputList = readAsList("test.txt")
    cityCount = int(inputList.pop(0))
    cities = {i: tuple(float(point) for point in plotStr.split(' ')) for i, plotStr in enumerate(inputList)}
    # generate adjacency matrix
    adjMatrix = [[euclidean(i, j) for j in range(cityCount)] for i in range(cityCount)]
    x=returnMinTSP(adjMatrix, cityCount)
    writeSingleToFile("Problem5.txt",math.floor(x))
    print(math.floor(x),x)
