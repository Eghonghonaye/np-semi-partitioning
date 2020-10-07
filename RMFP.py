import numpy as np
import task_generator, header

def init(task_list, hyper_period):
	#rate monotonic task priority assignment
	i = 0
	task_list.sort(key=lambda x: x.period,reverse=False)
	for task in task_list:
		task.next_job_number = 0
		task.jobs_in_hyper_period = hyper_period/task.period
		task.priority = i
		i = i+1

	#for task in task_list:
	#	print (task.number, task.period, task.ex_time, task.priority)
	return task_list
	

def scheduler(task_list, hyper_period, ready_jobs,next_ready_jobs, busy_time):
	job_to_run = None
	highest_priority = len(task_list)

	for job in ready_jobs:				
		if job.task_priority <= highest_priority:
			highest_priority = job.task_priority 
			#handle edge case of two jobs of same task
			if (job_to_run and (job_to_run.task_number == job.task_number)):
				job_to_run = min([job_to_run,job], key=lambda x: x.job_number)
			else:
				job_to_run = job
	if job_to_run:			
		#try to run this job and check the proposed finishing time of the job
		if busy_time < job_to_run.arr_time:
			finishing_time = job_to_run.arr_time + job_to_run.ex_time
		else:
			finishing_time = busy_time + job_to_run.ex_time
			#check if this core can run the job without deadline miss

		#keep busy time....job can ony run after busy time eh?

		if finishing_time > job_to_run.abs_deadline:
			status = False
		else:
			busy_time = finishing_time
			ready_jobs.remove(job_to_run)
			status = True
	else:
		status = "idle"

	return busy_time,status



def releaseTask(time,ready_jobs, next_ready_jobs,task_list):
	for task in task_list:
		#print("task", task.number, "next_job_number is", task.next_job_number)
		if task.next_job_number < task.jobs_in_hyper_period:
			if (task.period*task.next_job_number) <= time:
				job = header.Job(ex_time=task.ex_time, arr_time = (task.next_job_number*task.period), 
					abs_deadline = ((task.next_job_number*task.period) + task.rel_deadline), 
					job_number=task.next_job_number, task_number=task.number,
					task_priority = task.priority)
				ready_jobs.append(job)
				task.next_job_number = task.next_job_number + 1


def runScheduler(task_list, hyper_period):

	ready_jobs = []
	next_ready_jobs = []

	busy_time = 0
	time = 0
	
	#print ("start time is", time)
	task_list = init(task_list, hyper_period)
	while (time < hyper_period):
		releaseTask(time,ready_jobs,next_ready_jobs, task_list)
		busy_time, status = scheduler(task_list, hyper_period, ready_jobs, next_ready_jobs, busy_time)

		if not status:
			return False

		if (ready_jobs and status != "idle"):
			time = busy_time
		else:
			next_earliest_arrival = hyper_period
			for task in task_list:
				if (task.next_job_number < task.jobs_in_hyper_period) and ((task.next_job_number*task.period) < next_earliest_arrival):
					next_earliest_arrival = task.next_job_number*task.period
			time = next_earliest_arrival

	if (ready_jobs):
		return False

	else:
		return True


def testRMFP(task_list):
	hyper_period = header.computeHyperperiod(task_list)
	status = runScheduler(task_list, hyper_period)
	return status


if __name__ == '__main__':

	task_list = []

	task_list.append(task_generator.generateTask(0,256, 0.3515625))#90
	task_list.append(task_generator.generateTask(1,512, 0.21484375))#110
	task_list.append(task_generator.generateTask(4,512, 0.13671875))#70
	task_list.append(task_generator.generateTask(5,1024, 0.05859375))#60

	status = testRMFP(task_list)
	print (status)

	for task in task_list:
		print (task.number, task.period, task.ex_time, task.priority)