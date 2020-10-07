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

def coreSearch(task_order,processor,scheduler):

	header.processor_init(processor)
	remaining_tasks = task_order.copy()

	test = testDict.get(scheduler)
	if not test:
		print ("unkown scheduler")
		return

	for task in task_order:
		'''add utilisation based core assignment'''
		for core in range(processor.num_cores):
			'''needed for tests'''
			task_list = []
			task_list = [item for item in processor.core_tasklist[core]]
			task_list.append(task)
			
			init(task_list)
			
			if ((processor.core_utilisation[core] + task.utilisation) <= 1.0   and  (test(task_list))):
				processor.assign_task_to_core(core,task)
				remaining_tasks.remove(task)
				break
			else:
				if(core == (processor.num_cores-1)):
					header.processor_extend(processor)
					processor.assign_task_to_core((core+1),task)
					remaining_tasks.remove(task)		

	return processor.num_cores


def firstFit(task_set,criteria=None, scheduler=None):
	
	hyper_period = header.computeHyperperiod(task_set)
	'''task_order_list = permutations(task_set)'''
	'''takes too long just do rate monotonic task order'''
	if criteria == "extime":
		task_order_list = sorted(task_set, key=lambda x: x.ex_time)
	elif criteria == "utilisation":
		task_order_list = sorted(task_set, key=lambda x: x.utilisation)
	else:
		task_order_list = sorted(task_set, key=lambda x: x.period)

	processor_to_fit = header.Processor(num_cores = 1)
	core_search = coreSearch(task_order_list, processor_to_fit, scheduler)

	return core_search, processor_to_fit.core_tasklist



def main(task_set,criteria=None, scheduler=None, processor=None):

	if processor is None:
		number_of_cores, partition_list = firstFit(task_set,criteria,scheduler)
		partition_task_list = [[task.number for task in item] for item in partition_list]
		return number_of_cores, partition_task_list
	

def printPartitions(task_set):
	for task in task_set:
		for job in task.task_joblist:
			print(job.job_number, job.starting_time) 
	print(len_partitions,partitions)


if __name__ == '__main__':
	task_set = []

	task_set.append(task_generator.generateTask(0, 100, 0.16))#, 16), 
	task_set.append(task_generator.generateTask(1, 200, 0.895))#, 179), 
	task_set.append(task_generator.generateTask(2, 200, 0.25))#, 50), 
	task_set.append(task_generator.generateTask(3, 200, 0.085))#, 17), 
	task_set.append(task_generator.generateTask(4, 100, 0.18))#, 18), 
	task_set.append(task_generator.generateTask(5, 200, 0.015))#, 3)]

	'''task_set.append(task_generator.generateTask(0, 100, 0.9))#, 16), 
	task_set.append(task_generator.generateTask(1, 200, 0.895))#, 179), 
	task_set.append(task_generator.generateTask(2, 200, 0.5))#, 50), 
	task_set.append(task_generator.generateTask(3, 200, 0.5))#, 17), 
	task_set.append(task_generator.generateTask(4, 100, 0.9))#, 18), 
	task_set.append(task_generator.generateTask(5, 200, 0.8))#, 3)]'''

	for test in ["CWEDF","RMFP","davis","DBF","jeffay"]:
		print("\n test " + test)
		len_partitions, partitions = main(task_set, "period",test)	
		printPartitions(task_set)



	

