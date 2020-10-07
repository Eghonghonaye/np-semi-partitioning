# Non-preemptive (semi)-partitioning solutions
The tool takes a set of tasks and a schedulability test and returns the number of cores used for each partitioning solution for that task set except for the semi-partitioning solution which return TRUE or FALSE for if a schedule found or not. At the moment, it runs tests for first fit using a variety of schedulability tests and liquid path semi partitioning.

## Input
The input is the collection of task sets saved in the TaskSet folder. They are for tasks on 4 and 8 cores with number of tasks in the set {2m, 3m, 4m} where m is the number of cores.

## Output
The tool outputs the number of cores used for each solution for each task set and saves it to a csv file

## How to run
python3 runExp.py $numberOfCores $numberOfTasks $sched_test

The numbers for which task sets have been generated are: {(4,8),(4,12),(4,16),(8,16),(8,24),(8,32)}
The tool recognises schedulability tests from the set {CWEDF, RMFP, davis, DBF, jeffay, cwedfSAG, fpSAG]}, otherwise it fails with an "unknown scheduler" error.

## Dependencies
To use the schedule abstraction graph tests, clone this repository (https://github.com/brandenburg/np-schedulability-analysis) and edit the correct path in SAG_tests.py 
