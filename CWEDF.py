import numpy as np
import task_generator, header
import read_tasks_from_file as rtff
import result_logging as lg

def init(task_list, hyper_period):
	for task in task_list:
		task.next_job_number = 0
		task.jobs_in_hyper_period = hyper_period/task.period
		task.task_joblist = []


def scheduler(task_list, hyper_period, ready_jobs,next_ready_jobs, busy_time):
	job_to_run = None
	earliest_deadline = hyper_period
	current_ready_tasks = []

	'''pick earliest deadline ready job'''
	for job in ready_jobs:
		current_ready_tasks.append(job.task_number)
		if job.abs_deadline <= earliest_deadline:
			earliest_deadline = job.abs_deadline
			job_to_run = job

	'''build list of next ready jobs'''
	if job_to_run:
		next_ready_jobs = []
		for task in task_list:
			if task.next_job_number < task.jobs_in_hyper_period:
				if task.number not in current_ready_tasks:
					job = header.Job(ex_time=task.ex_time, arr_time = (task.next_job_number*task.period), abs_deadline = ((task.next_job_number*task.period) + task.rel_deadline), job_number=task.next_job_number, task_number=task.number)
					next_ready_jobs.append(job)
		next_ready_jobs.sort(key=lambda job: job.abs_deadline, reverse=True)

		'''calculate latest start time'''
		latest_start_time = hyper_period
		for job in next_ready_jobs:
			if latest_start_time >= job.abs_deadline:
				latest_start_time = job.abs_deadline - job.ex_time
			else:
				latest_start_time = latest_start_time - job.ex_time

		'''try to run this job and check the proposed finishing time of the job'''
		if busy_time < job_to_run.arr_time: 
			finishing_time = job_to_run.arr_time + job_to_run.ex_time
		else:
			finishing_time = busy_time + job_to_run.ex_time
			

		'''keep busy time....job can ony run after busy time eh?'''
		if (finishing_time > latest_start_time):
			status = "idle"
		else:
			'''check if this core can run the job without deadline miss'''
			if finishing_time > job_to_run.abs_deadline:
				job_to_run.finishing_time = finishing_time
				job_to_run.starting_time = finishing_time - job_to_run.ex_time
				schedule_order.append(job_to_run)
				status = False
			else:
				busy_time = finishing_time
				ready_jobs.remove(job_to_run)
				job_to_run.finishing_time = finishing_time
				job_to_run.starting_time = finishing_time - job_to_run.ex_time
				schedule_order.append(job_to_run)
				status = True
	else:
		status = "idle"

	return busy_time,status



def releaseTask(time,ready_jobs, next_ready_jobs,task_list):

	for task in task_list:
		if task.next_job_number < task.jobs_in_hyper_period:
			if (task.period*task.next_job_number) <= time:
				job = header.Job(ex_time=task.ex_time, arr_time = (task.next_job_number*task.period), abs_deadline = ((task.next_job_number*task.period) + task.rel_deadline), job_number=task.next_job_number, task_number=task.number)
				ready_jobs.append(job)
				task.task_joblist.append(job)
				task.next_job_number = task.next_job_number + 1


def runScheduler(task_list, hyper_period):
	global schedule_order
	schedule_order = []
	ready_jobs = []
	next_ready_jobs = []

	busy_time = 0
	time = 0
	
	init(task_list, hyper_period)
	while (time < hyper_period):
		#print("time is ",time)
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

	return True


def testCWEDF(task_list):
	hyper_period = header.computeHyperperiod(task_list)
	status = runScheduler(task_list, hyper_period)
	return status



if __name__ == '__main__':

	'''all_task_sets = rtff.main(path = "experiment_log_uniprocessor_test.csv")

	for task_set in all_task_sets:
		hyper_period = header.computeHyperperiod(task_set)
		status = testCWEDF(task_set,hyper_period)
		task_list = [(task.number, task.period, task.utilisation, task.ex_time) for task in task_set]
		results = [task_list, status]
		lg.log_results("CWEDF-uniprocessor", results)'''

	task_list = []

	task_list.append(task_generator.generateTask(0, 500, 0.07943275104355482))#, 39.71637552177741), 
	task_list.append(task_generator.generateTask(1, 10, 0.02589823696988874))#, 0.2589823696988874),
	task_list.append(task_generator.generateTask(2, 100, 0.12394618024647497))#, 12.394618024647496), 
	task_list.append(task_generator.generateTask(3, 1000, 0.012127272637004572))#, 12.127272637004571), 
	task_list.append(task_generator.generateTask(4, 100, 0.1585955591030769))#, 15.85955591030769)

	for task in task_list:
		print (task.number, task.period, task.ex_time)

	status = testCWEDF(task_list)
	for job in schedule_order:
		print(job.task_number, job.job_number, job.starting_time, job.finishing_time)
	print (status)
