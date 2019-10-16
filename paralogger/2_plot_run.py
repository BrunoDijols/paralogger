#! /usr/bin/env python
"""
Created plot for visualising ulog

Fred
12/10/2019
"""

#%% import

import sys
import time
import math
import pickle

import pandas as pd 
import numpy as np

from model.model import Flight
from model.list_param import Device , Position

import logging
from logging.handlers import RotatingFileHandler


#%% Config logger
logger = logging.getLogger()
#logging.basicConfig(filename='1_import.log',level=logging.DEBUG)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(module)s :: %(funcName)s ::  %(message)s')
file_handler = RotatingFileHandler('plot_run.log', 'a', 1000000, 1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Redirect log on console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logger.addHandler(stream_handler)


#%%  functions and decorator
###  DECORATOR ####

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()       
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f s' % \
                  (method.__name__, (te - ts) ))
        return result    
    return timed

### FUNCTIONS  ####

def timer(start,end):
    hours, rem = divmod(end-start, 3600)
    minutes, seconds = divmod(rem, 60)
    return ("{:0>2} h {:0>2} min {:05.2f} s".format(int(hours),int(minutes),seconds))


#%% PARAMETERS 
gravity = 9.80665 #m·s-2


name_saved_file= 'mflight_plot.pkl'


#%%  Prepare file 
logger.info(" --- Start ----")


#Load file from pickle
logger.info("Reading : " + name_saved_file)
with open(name_saved_file , 'rb') as f:
    mflight = pickle.load(f)

# Print the input Dataframe. 
print(mflight )

logger.info(" --- END ----")

print("END")


#%%