import pandas as pd
import re

def linkedIn_NLP(data):

	jobs = data
	jobs['title'] = jobs['title'].str.lower()
	for i in range(len(jobs['title'])):
		for k in jobs['title'].iloc[i].split("\n"):
				jobs['title'].iloc[i] = re.sub(r"[^a-zA-Z0-9]+", ' ', k)
	jobs['title'] = jobs['title'].str.split(" at ",n=1,expand=True)

	linkedin_variables = {}

	employee_count = len(jobs['title'])
	linkedin_variables['employee_count'] = len(jobs['title'])
	data_related_roles = len(jobs[jobs['title'].str.contains("data")])
	linkedin_variables['percentage_data_roles'] = "{0:.0%}".format((data_related_roles / employee_count))
	linkedin_variables['count_data_scientists'] = len(jobs[jobs['title'].str.contains("data scientist")])

	return linkedin_variables