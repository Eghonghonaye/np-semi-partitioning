import jobset_generator as jg
import header
import os
import subprocess

def testSAGFP(task_set):
	folder = "JobSets"
	try:
		os.remove(folder + "/currentJobSet.csv")
	except:
		pass

	hyperperiod = header.computeHyperperiod(task_set)
	jg.create_jobs(task_set,hyperperiod)
	jg.write_jobs(task_set, "currentJobSet" ,folder, 0)

	testPath = 'np-schedulability-analysis/build/nptest'
	jobSetPath = folder + "/currentJobSet.csv"

	result = subprocess.run([testPath, '-t', 'dense', jobSetPath], stdout=subprocess.PIPE)
	result = result.stdout.decode("utf-8")
	result = result.replace(',', '')
	result = result.split()

	os.remove(folder + "/currentJobSet.csv")
	return int(result[1])

def testSAGCWEDF(task_set):
	folder = "JobSets"
	try:
		os.remove(folder + "/currentJobSet.csv")
	except:
		pass

	hyperperiod = header.computeHyperperiod(task_set)
	jg.create_jobs(task_set,hyperperiod)
	jg.write_jobs(task_set, "currentJobSet" ,folder)

	testPath = 'np-schedulability-analysis/build/nptest'
	jobSetPath = folder + "/currentJobSet.csv"

	result = subprocess.run([testPath, '-i', 'CW','-t', 'dense',  jobSetPath], stdout=subprocess.PIPE)
	result = result.stdout.decode("utf-8")
	result = result.replace(',', '')
	result = result.split()

	os.remove(folder + "/currentJobSet.csv")
	return int(result[1])