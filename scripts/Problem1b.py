#!/usr/bin/env python

"""
For this problem, use the same data set as in the previous problem.

Your task now is to run the greedy algorithm that schedules jobs (optimally) in decreasing order of the ratio
(weight/length). In this algorithm, it does not matter how you break ties. You should report the sum of weighted
completion times of the resulting schedule --- a positive integer --- in the box below.
"""

__author__ = 'Vinayak'

from fileIO import readAsListOfDict,writeSingleToFile
from itertools import accumulate

def calculateWeightedCompleteTime(jobs):
    """Schedule jobs based on difference (weight - length) and return weighted total time."""

    jobs.sort(key=lambda v:v['weight']/v['length'],reverse=True)
    finishTime = list(accumulate([0]+jobs,lambda s,v:s+v['length']))
    weightedCompletedTime = sum((jobs[i]['weight']*finishTime[i+1] for i in range(len(jobs))))
    return weightedCompletedTime

if __name__=="__main__":
    jobList=readAsListOfDict('_642c2ce8f3abe387bdff636d708cdb26_jobs.txt','\s+',
                             2,['weight','length'],[int,int],1)
    writeSingleToFile("Problem1b.txt",calculateWeightedCompleteTime(jobList))
    pass