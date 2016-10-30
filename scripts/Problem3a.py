#!/usr/bin/env python

"""
In this programming problem and the next you'll code up the knapsack algorithm from lecture.

Let's start with a warm-up. Download the text file below.

knapsack1.txt
This file describes a knapsack instance, and it has the following format:

[knapsack_size][number_of_items]

[value_1] [weight_1]

[value_2] [weight_2]

...

For example, the third line of the file is "50074 659", indicating that the second item has value 50074 and size 659,
respectively.

You can assume that all numbers are positive. You should assume that item weights and the knapsack capacity are
integers.

In the box below, type in the value of the optimal solution.

ADVICE: If you're not getting the correct answer, try debugging your algorithm using some small test cases. And
then post them to the discussion forum!
"""

__author__ = 'Vinayak'

from fileIO import readAsListOfDict,writeSingleToFile

def calculateOptimalKnapsack(itemList, size, count):
    """Returns optimal value when items from itemList are scheduled on knapsack of size size"""

    # Sub-problems Array
    knapsackValues = [[0 for i in range(size+1)] for j in range(count)]

    for c in range(1,count):
        for s in range(size+1):
            if itemList[c]["weight"] > s:
                knapsackValues[c][s]=knapsackValues[c-1][s]
            else:
                knapsackValues[c][s] = max(knapsackValues[c-1][s],knapsackValues[c-1][s-itemList[c]["weight"]] +
                                           itemList[c]["value"])

    return knapsackValues[count-1][size]

if __name__=='__main__':
    inputList = readAsListOfDict("_6dfda29c18c77fd14511ba8964c2e265_knapsack1.txt",'\s+'
                           ,2,['value','weight'],[int,int],0,1)
    knapsackSize, itemCount = [int(value) for value in  inputList.pop(0).split(' ')]
    writeSingleToFile("Problem3a.txt",calculateOptimalKnapsack(inputList, knapsackSize, itemCount))
