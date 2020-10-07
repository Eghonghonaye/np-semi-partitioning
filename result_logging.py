import csv


def log_results(experiment_number, results):
	#file = "JobSets/experiment_log_" + str(experiment_number) + ".csv"
	file = str(experiment_number) + ".csv"

	with open(file, 'a') as writeFile:
		writer = csv.writer(writeFile)
		writer.writerow(results)