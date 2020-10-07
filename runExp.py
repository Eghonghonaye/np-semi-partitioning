import sys
import liquidpath2 as lp2
import read_tasks_from_file as rtff
import first_fit, first_fit_meta as FFM
import result_logging as lg
import m_necessary_test as necTest


def main():
	number_of_cores = int(sys.argv[1])
	number_of_tasks = int(sys.argv[2])
	sched_test = sys.argv[3]

	print ("Running tests for " + str(number_of_tasks) + "tasks on " + str(number_of_cores) + " cores w/ partitioning test " + sched_test)
	for utilisation in [90,80,70,60,50,40,30,20,10]:
		path = "TaskSets/" + str(number_of_cores) + "Cores" + str(number_of_tasks) + "Tasks" + str(utilisation) + ".csv"
		resultPath = "Partitioning" + str(number_of_cores) + "Cores" + str(number_of_tasks) + "Tasks"

		all_task_sets = rtff.main(path)
		for task_set in all_task_sets:
			liq = lp2.main(task_set,number_of_cores)
			len_p_ff_period_cwedf, p_ff_period_cwedf = FFM.main(task_set, number_of_cores, "period",sched_test)
			len_p_ff_period_cwedf_meta, p_ff_period_cwedf_meta = first_fit.main(task_set, "period",sched_test)	
			min_cores = necTest.main(task_set)

			lg.log_results(resultPath, [utilisation,liq,len_p_ff_period_cwedf,len_p_ff_period_cwedf_meta,min_cores])


if __name__ == '__main__':
	main()