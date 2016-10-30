#!/usr/bin/env python

"""
This problem also asks you to solve a knapsack instance, but a much bigger one.

Download the text file below.

knapsack_big.txt
This file describes a knapsack instance, and it has the following format:

[knapsack_size][number_of_items]

[value_1] [weight_1]

[value_2] [weight_2]

...

For example, the third line of the file is "50074 834558", indicating that the second item has value 50074 and size
834558, respectively. As before, you should assume that item weights and the knapsack capacity are integers.

This instance is so big that the straightforward iterative implemetation uses an infeasible amount of time and space.
So you will have to be creative to compute an optimal solution. One idea is to go back to a recursive implementation,
solving subproblems --- and, of course, caching the results to avoid redundant work --- only on an "as needed" basis.
Also, be sure to think about appropriate data structures for storing and looking up solutions to subproblems.

In the box below, type in the value of the optimal solution.

ADVICE: If you're not getting the correct answer, try debugging your algorithm using some small test cases.
And then post them to the discussion forum!
"""

__author__ = 'Vinayak'

from fileIO import readAsListOfDict,writeSingleToFile

def calculateOptimalKnapsack(itemList, size, count):
    """Returns optimal value when items from itemList are scheduled on knapsack of size size"""

    # Sub-problems Array
    knapsackValues = [0 for i in range(size+1)]

    for c in range(count):
        for s in range(size,0,-1):
            if itemList[c]["weight"] <= s:
                knapsackValues[s] = max(knapsackValues[s],knapsackValues[s-itemList[c]["weight"]] +
                                           itemList[c]["value"])
            else:
                break

    return knapsackValues[size]

if __name__=='__main__':
    inputList = readAsListOfDict("_6dfda29c18c77fd14511ba8964c2e265_knapsack_big.txt",'\s+'
                           ,2,['value','weight'],[int,int],0,1)
    knapsackSize, itemCount = [int(value) for value in  inputList.pop(0).split(' ')]
    writeSingleToFile("Problem3b.txt",calculateOptimalKnapsack(inputList, knapsackSize, itemCount))
