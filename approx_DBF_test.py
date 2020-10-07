def main(task_list):
	'''first fit appends the task under consideration to task_list hence it'll be at the end'''
	new_task = task_list[-1]
	DBF = 0
	for task in task_list:
		if new_task.deadline < task.deadline:
			DBF = DBF + 0
		else:
			DBF = DBF + task.ex_time + task.utilisation*(new_task.deadline-task.deadline)

	'''says maximum execution time of tasks in the whole set in the paper 
	I am using maximum execution time of tasks in the current partition here'''
	RHS = new_task.ex_time + max([task.ex_time for task in task_list])
	LHS = new_task.deadline - DBF
	if RHS < LHS:
		return True
	else:
		return False