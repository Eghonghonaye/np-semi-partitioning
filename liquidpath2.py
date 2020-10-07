import header, task_generator
import read_tasks_from_file as rtff
import result_logging as lg

'''input set of tasks and set of cores'''

'''to check if overlap of two ranges'''
def overlap(start1, end1, start2, end2):
    """Does the range (start1, end1) overlap with (start2, end2)?"""
    return not (end1 < start2 or end2 < start1)


'''1. create jobs for all tasks'''
def init(task_list):
	hyperperiod = header.computeHyperperiod(task_list)
	for task in task_list:
		task.jobs_in_hyper_period = hyperperiod/task.period;
		for jobnum in range(0,int(task.jobs_in_hyper_period)):
			job = header.Job(ex_time=task.ex_time, arr_time = (jobnum*task.period), abs_deadline = ((jobnum*task.period) + task.rel_deadline), job_number=jobnum, task_number=task.number)
			task.task_joblist.append(job)

'''2. Sort tasks by largest period, descending order
gravel before stone policy'''

def sortTask(task_list):
	task_list.sort(key=lambda task: task.period, reverse=True)

'''find all possible positions that a job can fit in a core'''
def findPositions(core,job,est,lst,hyperperiod):
	'''append position index to positions list, use -1 if position is the head
	position signifies the predecessor of that job'''
	positions = []
	if core.path:
		for position in range(len(core.path)):
			if position == 0:
				#check if it can fit in before or after	
				if overlap(est,lst,0,core.path[position].lst):
					positions.append(-1)
				if  len(core.path)!= 1 and overlap(est,lst,core.path[position].end_time,core.path[position+1].lst):					
					positions.append(0)
			if position == len(core.path) - 1:
				if overlap(est,lst,core.path[position].end_time,hyperperiod):
					positions.append(position)
			else:
				if overlap(est,lst,core.path[position].end_time,core.path[position+1].lst):
					positions.append(position)
	else:
		positions.append(-1)
	return positions

'''pick a position according to heuristic and see if deadlines are allowed'''
def checkCoreFit(core,job,est,lst,hyperperiod,positions):
	'''if positions is empty, it means the job cannot fit anywhere on that core'''
	#print("possible positions are ", positions)
	if positions:
		position = positions[-1] #use the latest position ~ position = positions[0] to use the earliest posiitn
	else:
		return False
	'''compute start and end times '''
	if core.path:
		if position == -1:
			start_time = est
			end_time = start_time + job.ex_time
		else:
			start_time = max([core.path[position].end_time,est])
			end_time = start_time + job.ex_time
	else:
		start_time = est
		end_time = start_time + job.ex_time

	'''check if fit'''
	if position == len(core.path) - 1:
		if end_time < job.abs_deadline:
			pass
		else:
			return False
	else:
		if ((end_time < job.abs_deadline) and (end_time < core.path[position+1].lst)):
			pass
		else:
			return False
	updatePath(core,job,est,lst,hyperperiod,position,start_time,end_time)
	return True

'''if chosen position is succesfsul then update the path'''
def updatePath(core,job,est,lst,hyperperiod,position,start_time,end_time):
	'''create path item'''
	pathitem = header.PathItem(job_number=job.job_number, task_number=job.task_number, ex_time=job.ex_time, abs_deadline=job.abs_deadline, est=est)
	pathitem.start_time = start_time
	pathitem.end_time = end_time

	if core.path:
		if position == len(core.path) - 1:
			pathitem.lst = pathitem.abs_deadline - pathitem.ex_time
			core.path.insert(position+1,pathitem)	
			'''propagate last from tail of path'''
			for index,item in reversed(list(enumerate(core.path))):
				if index == (len(core.path) - 1):
					pass
				else:
					item.lst = min([core.path[index+1].lst - item.ex_time, item.abs_deadline - item.ex_time])
				
		else:
			pathitem.lst = min([core.path[position+1].lst - pathitem.ex_time, pathitem.abs_deadline - pathitem.ex_time])
			core.path[position+1].start_time = max([pathitem.end_time, core.path[position+1].est])
			core.path[position+1].end_time = core.path[position+1].start_time + core.path[position+1].ex_time
			core.path.insert(position+1,pathitem)	
			'''should also propagate start time and end time for the rest of the path'''
			for index in range(position+2,len(core.path)):
				core.path[index].start_time = max([core.path[index-1].end_time,core.path[index].est])
				core.path[index].end_time = core.path[index].start_time + core.path[index].ex_time	
			
	else:
		pathitem.lst = pathitem.abs_deadline - pathitem.ex_time
		core.path.insert(position,pathitem)

'''run the fitting steps for each job in the hp and break if any job fails'''
def jobFit(processor,task_list):
	hyperperiod = header.computeHyperperiod(task_list)
	for task in task_list:
		for job in task.task_joblist:
			# print("\n")
			# print("Checking job ", job.job_number, " of task ", job.task_number)

			est = job.arr_time
			lst = job.abs_deadline - job.ex_time
			for core in processor.cores:
				positions = findPositions(core,job,est,lst,hyperperiod)
				status = checkCoreFit(core,job,est,lst,hyperperiod,positions)
				# print("Core under check is ", core.number)
				# print (status)
				# print([(item.task_number, item.job_number, item.start_time, item.end_time) for item in core.path])
				if status:
					break
				else:
					if core.number == len(processor.cores) - 1:
						return False
	return True


def prepareForOffsetTuning(task_list,processor):
	task_list.sort(key=lambda task: task.number, reverse=False)
	for core in processor.cores:
		for item in core.path:
			task_list[item.task_number].task_joblist[item.job_number].starting_time = item.start_time
			task_list[item.task_number].task_joblist[item.job_number].core_number = core.number


def main(task_set,number_of_cores):
	init(task_set)
	sortTask(task_set)
	processor = header.Processor(num_cores = number_of_cores)
	status = jobFit(processor, task_set)

	prepareForOffsetTuning(task_set,processor)
	return status


if __name__ == '__main__':
	task_set = []

	task_set.append(task_generator.generateTask(0,10000,0.6796))
	task_set.append(task_generator.generateTask(1,10000,0.4074))
	task_set.append(task_generator.generateTask(2,2000,0.381))

	'''task_set.append(task_generator.generateTask(0, 1000, 0.8669207464643705))#, 866.9207464643705), 
	task_set.append(task_generator.generateTask(1, 200, 0.7838792955831181))#, 156.77585911662362), 
	task_set.append(task_generator.generateTask(2, 100, 0.24724443080396466))#, 24.724443080396465), 
	task_set.append(task_generator.generateTask(3, 200, 0.7629044722127165))#, 152.5808944425433), 
	task_set.append(task_generator.generateTask(4, 1000, 0.9390510549358302))#, 939.0510549358302)'''

	status = main(task_set,2)

	print("\n")
	for task in task_set:
		print([(job.task_number, job.job_number,job.starting_time) for job in task.task_joblist])

	print("Final status is ", status)