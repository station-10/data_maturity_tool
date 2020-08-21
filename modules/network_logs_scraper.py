from seleniumwire import webdriver
import pandas as pd
import urllib
import time
import re
from datetime import datetime
import logging


js_libraries_dict = {"2.21.0":"24-06-2020",
"2.20.0":"05-03-2020",
"2.19.0":"21-02-2020",
"2.18.0":"13-02-2020",
"2.17.0":"23-08-2019",
"2.16.0":"15-08-2019",
"2.15.0":"15-07-2019",
"2.14.0":"21-05-2019",
"2.13.0":"10-04-2019",
"2.12.0":"22-02-2019",
"2.11.0":"11-02-2019",
"2.10.0":"20-09-2018",
"2.9.0":"24-05-2018"
    }


def network_log_scraper(input_url):
    driver = webdriver.Chrome()
    driver.get(input_url)
    time.sleep(60)
    response_list = []

    for request in driver.requests:
        if request.response:
            case = {'path': request.path, 'status': request.response.status_code, 'headers':request.response.headers}
            response_list.append(case)
    df = pd.DataFrame(response_list)

    network_log_variables = {}
    # b/ss
    if len(df['path'][df['path'].str.contains('b/ss')]) > 0:
        bss_list = urllib.parse.unquote(df['path'][df['path'].str.contains('b/ss')].iloc[0]).split('&')
        network_log_variables['has_adobe_analytics'] = True
        network_log_variables['custom_request_domain'] = (lambda x: True if "smetrics" in x else False)(str(bss_list[0]))
        network_log_variables['latest_js_library'] = (lambda x: True if x == "2.21.0" else False)(bss_list[0].split('/')[7].split('-')[1])
        try:
            network_log_variables['days_since_js_update'] = (lambda x: datetime.strptime(js_libraries_dict.get("2.21.0"), '%d-%m-%Y').date() - x)(datetime.strptime(js_libraries_dict.get(bss_list[0].split('/')[7].split('-')[1]), '%d-%m-%Y').date())
        except:
            network_log_variables['days_since_js_update'] = "> 3 years"
        network_log_variables['has_experience_cloud_id'] = (lambda x: True if 'mid' in str(x) else False)(bss_list)
        network_log_variables['count_of_evars'] = len(re.findall(r'v[0-9][0-9]?[0-9]?', urllib.parse.unquote(df['path'][df['path'].str.contains('b/ss')].iloc[0])))
        network_log_variables['count_of_props'] = len(re.findall(r'c[0-9][0-9]?[0-9]?',urllib.parse.unquote(df['path'][df['path'].str.contains('b/ss')].iloc[0])))
        network_log_variables['count_of_listvars'] = len(re.findall(r'l[0-9][0-9]?[0-9]?',urllib.parse.unquote(df['path'][df['path'].str.contains('b/ss')].iloc[0])))

    else:
        network_log_variables['has_adobe_analytics'] = False
    # ga
    if len(df['path'][df['path'].str.contains('https://www.google-analytics.com/')]) > 0:
        ga_list = df['path'][df['path'].str.contains('https://www.google-analytics.com/')]
        network_log_variables['has_google_analytics'] = True
        network_log_variables['ga_tag_uptodate'] = (lambda x: True if "analytics.js" in x else False)(str(ga_list.iloc[0]))
    else:
        network_log_variables['has_google_analytics'] = False
    # ga collect
    if len(df['path'][df['path'].str.contains('google.analytics.com/r/collect?')]) > 0:
        ga_collect_list = urllib.parse.unquote(df['path'][df['path'].str.contains('google.analytics.com/r/collect?')].iloc[0]).split('&')
        network_log_variables['has_google_analytics_collect'] = True
        network_log_variables['using_custom_dimensions'] = (lambda x: True if re.search('cd[0-9]*', x) else False)(urllib.parse.unquote(df['path'][df['path'].str.contains('google.analytics.com/r/collect?')].iloc[0]))
        if network_log_variables['using_custom_dimensions'] == True:
            network_log_variables['more_than_20_cd'] = max([int(s) for s in list(("").join(re.findall('cd[0-9]*',urllib.parse.unquote(df['path'][df['path'].str.contains('google.analytics.com/r/collect?')].iloc[0])))) if    s.isdigit()]) > 19
    else:
        network_log_variables['has_google_analytics_collect'] = False
    # is it possible to have ga but not collect? what would this mean?

        # google optimize
    if len(df['path'][df['path'].str.contains('optimize.')]) > 0:
        network_log_variables['has_google_optimize'] = True
    else:
        network_log_variables['has_google_optimize'] = False   

    # adobe target
    if len(df['path'][df['path'].str.contains('target.')]) > 0:
        network_log_variables['has_adobe_target'] = True
    else:
        network_log_variables['has_adobe_target'] = False      

    # optimizely
    if len(df['path'][df['path'].str.contains('optimizely')]) > 0:
        network_log_variables['has_optimizely'] = True
    else:
        network_log_variables['has_optimizely'] = False    

    return network_log_variables




