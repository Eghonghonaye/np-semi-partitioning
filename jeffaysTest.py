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
		i = i+1
	return task_list


def schedulabilityJeffay(task_list):
	for task in task_list:
		h_tasks = [h_task for h_task in task_list if h_task.priority<=task.priority]
		lhs = h_tasks[0].period
		while(lhs<h_tasks[-1].period):
			rhs = task.ex_time + sum([math.floor((lhs-1)/h_task.period)*h_task.ex_time for h_task in h_tasks[:-1]])
			#print(task.number, lhs,rhs)
			lhs+=1
			if lhs<rhs:
				return False
	return True


def main(task_list):
	init(task_list)
	status = schedulabilityJeffay(task_list)
	#print(status)
	return status

if __name__ == '__main__':
	task_list = []

	task_list.append(task_generator.generateTask(0, 500, 0.07943275104355482))#, 39.71637552177741), 
	task_list.append(task_generator.generateTask(1, 10, 0.02589823696988874))#, 0.2589823696988874),
	task_list.append(task_generator.generateTask(2, 100, 0.12394618024647497))#, 12.394618024647496), 
	task_list.append(task_generator.generateTask(3, 1000, 0.012127272637004572))#, 12.127272637004571), 
	task_list.append(task_generator.generateTask(4, 100, 0.1585955591030769))#, 15.85955591030769)
	
	main(task_list)

	print ("[task.number, task.WCRT, task.rel_deadline, task.ex_time]")
	for task in task_list:
		print ([task.number, task.WCRT, task.rel_deadline,task.ex_time])
	
		
