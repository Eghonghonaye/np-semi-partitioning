import numpy as np, math
import task_generator, header
import read_tasks_from_file as rtff
import result_logging as lg

def init(task_list):
	#rate monotonic task priority assignment
	i = 0
	task_list.sort(key=lambda x: x.period,reverse=False)
	for task in task_list:
		task.priority = i
		task.blocking = 0
		task.WO = 0
		task.WCRT = 0
		i = i+1

	#for task in task_list:
	#	print (task.number, task.period, task.ex_time, task.priority)
	return task_list

def blocking(task_list):
	for task in task_list:
		#nobody blocks the lowest priority task eh
		if task.priority == max([other_task.priority for other_task in task_list]):
			task.blocking = 0
		else:
			task.blocking = max([other_task.ex_time for other_task in task_list if other_task.priority > task.priority])
	'''for task in task_list:
		print ([task.number, task.priority, task.WCRT, task.rel_deadline,task.blocking,task.ex_time])'''



def getLengthOfBusyPeriod(task_list,current_task):
	epsilon = 0.000000000000000000001
	w = current_task.ex_time
	while 1:
		rhs = current_task.blocking
		higher_prio_task = [higher_task for higher_task in task_list if higher_task.priority <= current_task.priority]
		for task in higher_prio_task:
			#print (math.ceil(w/task.period),task.ex_time)
			rhs = rhs + (math.ceil(w/task.period) * task.ex_time)
		#print(current_task.number,current_task.blocking,rhs)
		#print("rhs, w ",current_task.number, rhs,w)
		if rhs <= w :
			return rhs
		w = rhs + epsilon

def schedulabilityTestFPWC(task_list):
	#calculate blocking
	blocking(task_list)
	#calculte WCRT
	for task in task_list:
		epsilon = 0.000000000000000000001
		tM = getLengthOfBusyPeriod(task_list,task)
		qM = int(math.ceil(tM/task.period))
		#print("tM,qM ",task.number,tM,qM)
		respMax = -1
		for q in range(qM):
			#RTA analysis for the current job q:
			#starting value:
			t = task.blocking + task.ex_time*q
			while 1:
				rhs = task.blocking + q*task.ex_time
				#add interference
				for higher_task in [other_task for other_task in task_list if other_task.priority < task.priority]:
					rhs = rhs + ( (math.floor(t/higher_task.period)+1) * higher_task.ex_time)
				#print("q,w ",q,t,rhs,task.number)
				if rhs <= t:
					t = rhs
					break
				if (rhs - q * task.period + task.ex_time) > task.deadline:
					t = rhs
					break	
				t = rhs + epsilon

			#come out of while loop we have response time of that q
			resp = t - q* task.period + task.ex_time
			if resp > respMax:
				respMax = resp
			task.WCRT = respMax


def main(task_list):
	init(task_list)
	schedulabilityTestFPWC(task_list)
	for task in task_list:
		if task.WCRT > task.deadline:
			return False
	return True

if __name__ == '__main__':
	task_list = []

	'''task_list.append(task_generator.generateTask(0, 500, 0.07943275104355482))#, 39.71637552177741), 
	task_list.append(task_generator.generateTask(1, 10, 0.02589823696988874))#, 0.2589823696988874),
	task_list.append(task_generator.generateTask(2, 100, 0.12394618024647497))#, 12.394618024647496), 
	task_list.append(task_generator.generateTask(3, 1000, 0.012127272637004572))#, 12.127272637004571), 
	task_list.append(task_generator.generateTask(4, 100, 0.1585955591030769))#, 15.85955591030769)
	'''

	task_list.append(task_generator.generateTask(0, 2.5, 0.4))#, 39.71637552177741), 
	task_list.append(task_generator.generateTask(1, 3.5, 0.2857142857142857))#, 0.2589823696988874),
	task_list.append(task_generator.generateTask(2, 3.5, 0.2857142857142857))#, 12.394618024647496), 
	
	main(task_list)

	print ("[task.number, task.WCRT, task.rel_deadline, task.ex_time]")
	for task in task_list:
		print ([task.number, task.WCRT, task.rel_deadline,task.ex_time])
	

	'''all_task_sets = rtff.main()

	for task_set in all_task_sets:
		status = main(task_set)
		task_list = [(task.number, task.period, task.utilisation, task.ex_time) for task in task_set]
		results = [task_list,status]
		lg.log_results("davis_test", results)'''
		
