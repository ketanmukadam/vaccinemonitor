#!/usr/bin/env python3

import logging
import argparse
from cowin import show_dists, show_vacc, state2id, dist2id
from gmail import send_gmail, countdown

state_name=""
dist_name=""
inloop=True
loglevel='debug'

def check_arguments():
    if not dist_name or not state_name:
        logging.error('Invalid State or District names')
        return 1

def parse_arguments():
    global state_name
    global dist_name
    global inloop
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action='store', default='',
                                dest='state_name', help='State Name')
    parser.add_argument('-d', action='store', default='',
                                dest='dist_name',help='District Name')
    parser.add_argument('-l', action='store_false', default=True,
                                dest='loop', help='dont run in loop')
    results = parser.parse_args()
    state_name=results.state_name
    dist_name=results.dist_name
    inloop=results.loop
    logging.info('Arguments =  %s', results)

def main():
    nlevel = getattr(logging, loglevel.upper(), None)
    if not isinstance(nlevel, int):
            raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(filename='vacinfo.log', filemode="w", level=nlevel, 
            format='%(asctime)s %(levelname)s:%(message)s')
    parse_arguments()
    numdays = 7 
    if check_arguments(): exit(1)
    try:
        while True:
            if show_vacc(dist2id(state_name, dist_name), numdays):
                send_gmail()
            if not inloop: break
            countdown(300) # Wait 5 minutes
    except:
        logging.error('Exited Waiting')

if __name__ == "__main__":
    main()
