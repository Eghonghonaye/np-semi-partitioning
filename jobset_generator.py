import csv, task_generator
import ast, header
import sys
import result_logging as lg
import os

def read_tasks(path):
	#path = "/home/eghonghonaye/Desktop/tasks.csv"
	task_list = []
	all_task_sets = []
	with open(path) as csv_file:
	    csv_reader = csv.reader(csv_file, delimiter=',')
	    for row in csv_reader:
	    	task_set = ast.literal_eval(row[0])
	    	print(task_set)
	    	for task in task_set:
	    		number = task[0]
	    		period = task[1]
	    		util = task[2]
	    		task_list.append(task_generator.generateTask(number, period, util))#, 15.85955591030769)
	    	all_task_sets.append(task_list)
	    	task_list = []
	return (all_task_sets)

def setPriority(task_set):
	task_set.sort(key=lambda x: x.period, reverse=False)
	i = 0
	for task in task_set:
		task.priority = i
		i = i+1


def create_jobs(task_set,hyperperiod):
	setPriority(task_set)
	for task in task_set:
		number_of_jobs = int(hyperperiod/task.period)
		for job_number in range(number_of_jobs):
			job = header.Job(ex_time=task.ex_time, arr_time = (job_number*task.period), 
				abs_deadline = ((job_number*task.period) + task.rel_deadline), 
				job_number=job_number, task_number=task.number,
				task_priority = task.priority)
			task.task_joblist.append(job)

def write_jobs(task_set,tasksetcount,folder,edf=1):
	heading = ["Task ID","Job ID","Arrival min","Arrival max","Cost min","Cost max","Deadline","Priority"]
	lg.log_results(folder + "/" + str(tasksetcount), heading)
	for task in task_set:
		for job in task.task_joblist:
			if edf:
				results = [job.task_number+1,job.job_number+1,job.arr_time,job.arr_time,0,job.ex_time,job.abs_deadline,job.abs_deadline]
			else:
				results = [job.task_number+1,job.job_number+1,job.arr_time,job.arr_time,0,job.ex_time,job.abs_deadline,task.priority]
			lg.log_results(folder + "/" + str(tasksetcount), results)

