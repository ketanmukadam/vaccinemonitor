import json
import requests
import datetime
import pandas as pd
import os
import logging
from gmail import body

######### Cowin APIs ##########
cowin_api_url = "https://cdn-api.co-vin.in/api/v2/"
cowin_get_states_url = cowin_api_url+"admin/location/states"
cowin_base_url = cowin_api_url+"admin/location/districts/"
cowin_vacc_base_url = cowin_api_url+"appointment/sessions/public/calendarByDistrict?district_id={}&date={}"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) " 
           "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 " 
           "Safari/537.36"}

def get_url_data(url):
    try:
        logging.info(url)
        rsp = requests.get(url, headers=headers)
        rsp.raise_for_status()
        logging.debug(rsp)
        return rsp
    except:
        logging.error("GET error - %s", url)
        return None


def show_states():
    logging.info(cowin_get_states_url)
    cowin_data = json.loads(get_url_data(cowin_get_states_url).text)
    for s in cowin_data['states']:
        print (s['state_id'],s['state_name'])

def show_dists(state_num, log):
    dist_list = []
    cowin_url = cowin_base_url+"{}".format(state_num)
    cowin_data = json.loads(get_url_data(cowin_url).text)
    if not cowin_data["districts"]:
        logging.error("Input invalid - incorrect name") 
    for d in cowin_data["districts"]:
        if log: print (d['district_id'],d['district_name'])
        dist_list.append(d['district_name'])
    return dist_list

def state2id(state_name):
    logging.info(cowin_get_states_url)
    cowin_data = json.loads(get_url_data(cowin_get_states_url).text)
    for s in cowin_data['states']:
        if s['state_name'] == state_name:
            return s['state_id']

def dist2id(state_name, dist_name):
    cowin_url = cowin_base_url+"{}".format(state2id(state_name))
    cowin_data = json.loads(get_url_data(cowin_url).text)
    for d in cowin_data["districts"]:
        if d['district_name'] == dist_name:
            return d['district_id']

def show_vacc(dist_id, numdays):
    global body
    if not dist_id : 
        logging.error("Incorrect District/State")
        exit(1)
    free_vac = 0
    paid_vac = 0
    body = "\n\nHey, Here is an update on vaccine!! \n\n"
    date_list = [datetime.datetime.today() + datetime.timedelta(days=x) for x in range(numdays)]
    for datestr in date_list :
        logging.info("Date:{} ...".format(datestr.strftime("%d-%m-%Y")))
        cowin_url = cowin_vacc_base_url.format(dist_id, datestr.strftime("%d-%m-%Y"))
        rsp = get_url_data(cowin_url)
        if rsp.ok :
            try :
                jdata = json.loads(rsp.text)
            except ValueError:
                logging.error('Json decoding failed %s', cowin_url)
                continue
            if not jdata['centers'] : continue #Empty data
            vdata = pd.json_normalize(
                         jdata['centers'], 
                         record_path =['sessions'],
                         meta=['center_id', 'name', 'block_name', 'fee_type'],
                         errors='ignore'
                         )
            logging.debug('\t'+vdata[['name','fee_type', 'vaccine']].to_string().replace('\n', '\n\t'))
            if vdata.empty: continue
            first_cols = ['name','block_name','fee_type','vaccine', 'date',
                    'available_capacity', 'min_age_limit',
                    'available_capacity_dose1', 'available_capacity_dose2']
            last_cols = [col for col in vdata.columns if col not in first_cols]
            vdata = vdata[first_cols+last_cols]
            logging.debug('Total entries = %s',str(len(vdata)))
            freevac = vdata[vdata['fee_type'] == 'Free']
            if (len(freevac) == 0 or
                len(freevac[freevac['available_capacity_dose1'] == 0]) or 
                len(freevac[freevac['available_capacity_dose2'] == 0]) ) :
                     logging.debug("\tNo Free dose available")
                     pass
            paidvac = vdata[vdata['fee_type'] == 'Paid']
            if (len(paidvac) == 0 or 
                len(paidvac[paidvac['available_capacity_dose1'] == 0]) or 
                len(paidvac[paidvac['available_capacity_dose2'] == 0]) ) :
                     logging.debug("\tNo Paid dose available")
                     pass
            else :
                     paid_vac = 1 
                     pv1 = paidvac[paidvac['available_capacity_dose1'] != 0]
                     pv2 = paidvac[paidvac['available_capacity_dose2'] != 0]
                     body = body + pv1[['name', 'block_name', 'date', 'fee_type', 'vaccine',
                               'available_capacity_dose1', 'min_age_limit']].to_string(index=False)
                     logging.debug(body)
        else : 
            logging.error("Error in fetching")
            print("Err in fetching")

    body = body + ("\n\n Thanks")
    logging.info(body)
    return paid_vac

