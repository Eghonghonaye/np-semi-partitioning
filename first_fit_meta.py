import header, CWEDF, RMFP, task_generator, math
import davisTest, jeffaysTest
import result_logging as lg
from itertools import permutations
import numpy as np
import SAG_tests as sag
import approx_DBF_test as approxDBF

	
testDict = {
  "CWEDF": CWEDF.testCWEDF,
  "RMFP": RMFP.testRMFP,
  "davis":davisTest.main,
  "DBF": approxDBF.main,
  "jeffay":jeffaysTest.main,
  "cwedfSAG": sag.testSAGCWEDF,
  "fpSAG": sag.testSAGFP
}

'''clear up task list for next call'''
def init(task_list):
	for task in task_list:
		task.task_joblist = []

def coreSearch(task_order,processor,scheduler, n_depth=0):

	avail_cores = processor.num_cores
	#print("starting core search",[task.number for task in task_order])

	header.processor_init(processor)
	remaining_tasks = task_order.copy()

	test = testDict.get(scheduler)
	if not test:
		print ("unkown scheduler")
		return

	for task in task_order:
		'''add utilisation based core assignment'''
		for core in range(processor.num_cores):
			'''needed for CWEDF test'''
			task_list = [item for item in processor.core_tasklist[core]]
			task_list.append(task)
			init(task_list)
			
			if ((processor.core_utilisation[core] + task.utilisation) <= 1.0   and  (test(task_list))):
				processor.assign_task_to_core(core,task)
				remaining_tasks.remove(task)
				break
			else:
				if core >= avail_cores-1:
					'''this has failed
					try the meta heuristic - reshuffle task set and call core search with new task order 
					recursive so when we reach depth of trials....break and return failed'''
					if n_depth == len(task_order): #recursion base case
						return 999 #return ~ infinte number of processors
								
					'''reshuffle tak order and increment depth'''
					task_order.remove(task) 
					task_order.insert(n_depth, task) 
					n_depth += 1

					fitstatus = coreSearch(task_order, processor, scheduler, n_depth)
					if fitstatus == 999:
						return fitstatus
					else:
						return processor.num_cores

	return processor.num_cores


def firstFit(task_set, number_of_cores, criteria=None, scheduler=None):
	
	hyper_period = header.computeHyperperiod(task_set)
	'''task_order_list = permutations(task_set)'''
	'''takes too long just do rate monotonic task order'''
	if criteria == "extime":
		task_order_list = sorted(task_set, key=lambda x: x.ex_time)
	elif criteria == "utilisation":
		task_order_list = sorted(task_set, key=lambda x: x.utilisation)
	else:
		task_order_list = sorted(task_set, key=lambda x: x.period)

	processor_to_fit = header.Processor(num_cores = number_of_cores)
	core_search = coreSearch(task_order_list, processor_to_fit, scheduler)
	if core_search == 999:
		return 999, processor_to_fit.core_tasklist
	else:
		return core_search, processor_to_fit.core_tasklist



def main(task_set, number_of_cores, criteria=None, scheduler=None, processor=None):

	if processor is None:
		number_of_cores, partition_list = firstFit(task_set,number_of_cores, criteria,scheduler)
		partition_task_list = [ [task.number for task in item] for item in partition_list]
		return number_of_cores, partition_task_list
	
def printPartitions(task_set):
	for task in task_set:
		for job in task.task_joblist:
			print(job.job_number, job.starting_time) 
	print(len_partitions, partitions)


if __name__ == '__main__':

	number_of_cores = 4
	task_set = []

	task_set.append(task_generator.generateTask(0, 100, 0.9))#, 16), 
	task_set.append(task_generator.generateTask(1, 200, 0.895))#, 179), 
	task_set.append(task_generator.generateTask(2, 200, 0.5))#, 50), 
	task_set.append(task_generator.generateTask(3, 200, 0.5))#, 17), 
	task_set.append(task_generator.generateTask(4, 100, 0.9))#, 18), 
	task_set.append(task_generator.generateTask(5, 200, 0.8))#, 3)]

	'''task_set.append(task_generator.generateTask(0, 100, 0.16))#, 16), 
	task_set.append(task_generator.generateTask(1, 200, 0.895))#, 179), 
	task_set.append(task_generator.generateTask(2, 200, 0.25))#, 50), 
	task_set.append(task_generator.generateTask(3, 200, 0.085))#, 17), 
	task_set.append(task_generator.generateTask(4, 100, 0.18))#, 18), 
	task_set.append(task_generator.generateTask(5, 200, 0.015))#, 3)]'''

	for test in ["CWEDF","RMFP","davis","DBF","jeffay","cwedfSAG","fpSAG"]:
	#for test in ["CWEDF","RMFP","davis","DBF","jeffay"]:
		print("\n test " + test)
		len_partitions, partitions = main(task_set, number_of_cores, "period", test)	
		printPartitions(task_set)

