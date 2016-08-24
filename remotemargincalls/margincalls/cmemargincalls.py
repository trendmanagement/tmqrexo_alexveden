import os
import requests
import time
from lxml import etree
from configparser import ConfigParser

#this is the main function to call
def main_make_margin_call_cme_core(xml_file):
    config_vars = get_setup_config_variables()

    margin_id = post_margin_call_cme_core(xml_file, config_vars)

    return get_margin_call_cme_core(margin_id, config_vars)

#gets the cme core config variables
def get_setup_config_variables():

    config_vars = {'baseurl': '', 'username': '', 'password':''}

    config = ConfigParser()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    #print(dir_path)
    config.read(dir_path + '\\app.ini')
    config_vars['baseurl'] = config.get('CME_CORE_SETUP', 'baseurl')
    config_vars['username'] = config.get('CME_CORE_SETUP', 'username')
    config_vars['password'] = config.get('CME_CORE_SETUP', 'password')

    return config_vars


#get the id out of the xml content of the cme core message used for get
def __read_xml_margin_id(xmlData):

    try:
        tree = etree.fromstring(xmlData)
        child = tree.find('margin')
        marginId = child.attrib['id']
    except:
        marginId = ''

    return str(marginId)


#get the status code about margin calc at cme core
def __read_xml_cme_core_status_code(xmlData):

    try:
        root = etree.fromstring(xmlData)
        cme_core_status_code = root.attrib['status']
    except:
        cme_core_status_code = 'ERROR'

    #print('__read_xml_cme_core_status_code ' + cme_core_status_code)

    return cme_core_status_code

#reads the xml file for initial and maintenance margin
def __read_xml_cme_core_margin(xmlData, margin):

    #margin = {'init': 0, 'maint' : 0}

    try:
        root = etree.fromstring(xmlData)
        margin_child = root.find('margin')
        amounts_child = margin_child.find('amounts')

        margin['init'] = amounts_child.attrib['init']
        margin['maint'] = amounts_child.attrib['maint']
    finally:
        return margin


#posts the margin request to cme core
def post_margin_call_cme_core(xml_file, config_vars):
    url = config_vars['baseurl'] + '?complete=true'
    header = {'username': config_vars['username'],
              'password': config_vars['password'],
              'content-type': 'application/xml'}

    #r = requests.post(url, headers=header, data=xml_file, stream=True)

    r = requests.post(url, headers=header, data=xml_file)

    return __read_xml_margin_id(r.content)

#makes a get request with the id from the post for the margin values
def get_margin_call_cme_core(margin_id, config_vars):
    url = config_vars['baseurl'] + '/' + margin_id
    header = {'username': config_vars['username'],
              'password': config_vars['password'],
              'content-type': 'application/xml'}

    continue_check_cme_get = 0

    margin = {'status':'ERROR', 'init': 0, 'maint': 0}

    while(continue_check_cme_get < 10):
        time.sleep(1)

        r = requests.get(url, headers=header)

        #print(r.content)

        if __read_xml_cme_core_status_code(r.content).upper() == 'SUCCESS':
            margin['status'] = 'SUCCESS'
            break

        continue_check_cme_get+=1

    return __read_xml_cme_core_margin(r.content, margin)