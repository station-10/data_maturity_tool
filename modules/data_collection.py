from modules.linkedin_scraper import linkedIn_scraper
from modules.linkedin_nlp import linkedIn_NLP
from modules.network_logs_scraper import network_log_scraper


def collect_data(input_url):

	linkedin_data = linkedIn_NLP(linkedIn_scraper(input_url))
	network_data = network_log_scraper(input_url)

	#data = linkedin_data + network_data

	return linkedin_data,network_data