#! /usr/bin/env python

import datetime
import hashlib
import logging
import os.path
import random
import string
import time
import sys
import pkgutil
import numpy as np
import pandas as pd
import pip

import platform
import json

from import_ulog import ulog_list_data, ulog_param, ulog_to_df
from list_param import Device, Kind, Position

logger = logging.getLogger("model")

# Local imports:


############################# DECORATOR #############################


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if "log_time" in kw:
            name = kw.get("log_name", method.__name__.upper())
            kw["log_time"][name] = int((te - ts) * 1000)
        else:
            logger.info("%r  %2.2f s" % (method.__name__, (te - ts)))
        return result

    return timed


############################# DEFINITIONS #############################


def id_generator(msize=6, chars=string.ascii_uppercase + string.digits):
    """ Generate a random ID .

    Parameters:
        msize (str): length of the random string.
        chars (list of string): the list of the possible characters

    :Returns:
        id_str(str): the random string   
    """

    id_str = "".join(random.choice(chars) for _ in range(int(msize)))
    return id_str


def sha256sum(filename):
    """ Compute the sha256 of the a file.
    Usefull to refind source file , or detect duplicate one

    Parameters:
        filename (str):The file path.

    :Returns:
        sha(str): tHe sha256 hars string   
    """
    # compute the SH256 of the file  to identify possible duplicated source file.
    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)
    with open(filename, "rb", buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

def getSystemInfo():
        try:
            info={}
            info['platform']=platform.system()
            info['platform-release']=platform.release()
            info['platform-version']=platform.version()
            info['architecture']=platform.machine()
            info['processor']=platform.processor()

            info['python version:'] =sys.version
            info['modules:']=list(sys.modules.keys())

            return json.dumps(info)
        except Exception as e:
            logging.exception(e)

############################# MAIN MODEL #############################


class Flight:
    def __repr__(self):
        return str(self.__dict__)

    def __init__(self):
        logger.info("initialise_flight ")

        self.id = id_generator()
        self.createdDate = time.time()

        self.manufacturer = None
        self.glider = None
        self.size = None
        self.modif = None
        self.pilot = None
        self.weight = None
        self.location = None
        self.laboratory = None

        self.data = []

        self.sections = []

        self.flight_version = 1  # version of the data model

    @timeit
    def add_data_file(self, mfilePath, mdevice, mposition):
        mData_File = Data_File(mfilePath, mdevice, mposition)
        mData_File.populate_df()
        mData_File.populated_device_param()

        self.data.append(mData_File)

    def add_info(self, mmanufacturer, mglider,msize, mmodif, mpilot, mweight, mlocation,mlabo):
        self.manufacturer = mmanufacturer
        self.glider = mglider
        self.size = msize
        self.modif = mmodif
        self.pilot = mpilot
        self.weight = mweight
        self.location = mlocation
        self.laboratory = mlabo


    def get_df_by_position(self, mposition):
        df_to_return = []
        for dataf in self.data:
            if dataf.position == mposition:
                df_to_return.append(dataf.df)
            
        return df_to_return

    def apply_section(self,uid,time_calibrate=5):

        mSection= self.section_by_id(uid)
        t_start,t_end = mSection.get_start_end()
        t_start,t_end =float(t_start),float(t_end)
        mdf = self.get_df_by_position(Position.PILOT)[0]
        df_plot = mdf.loc[mdf["lat"].notnull()]

        mSection.set_calibration(df_plot,t_start , t_start + time_calibrate)
        dict_calibration = mSection.get_calibration() 


        df_plot['pitch'] = df_plot['pitch'] - dict_calibration['pitch']
        df_plot['roll'] = df_plot['roll'] - dict_calibration['roll']

        mask = (df_plot["time0_s"] > t_start) & (df_plot["time0_s"] <= t_end)
        df_plot_sel = df_plot.loc[mask].copy()

        return df_plot_sel


    def add_general_section(self , time_min=None ,time_max=None ):

        if not len(self.data)==0:
            
            df=self.data[0].df   #TODO need to select the shorter one instead of the first one
            
            if time_min == None:
                time_min = df['time0_s'].min()
            if time_max == None:
                time_max = df['time0_s'].max()

            mSection= Sections(time_min,time_max,Kind.MISC)
            self.sections.append(mSection)
            
        else:
            logger.info("Impossible to create section, Data is empty")

    def delete_section(self, uid):
        self.sections = [i for i in self.sections if i.id!=uid]

    def section_by_id(self, uid):
        section_to_return = [i for i in self.sections if i.id == uid]
        return section_to_return[0]  




class Sections:
    def __repr__(self):
        return '%s (%s,%s) ' % (self.kind, self.start , self.end)

    def __init__(self, start = None , end=None , kind=None):

        self.id = id_generator()
        self.kind = kind
        self.start = start
        self.end = end
        self.version = 1  # version of the Sections model
        self.calibration = {"pitch" : 0 , "roll" :0 , "yaw" : 0 }

    def get_start_end(self):
        return (self.start, self.end)

    def set_calibration(self,df, t_start=0 ,t_end =5):
        mask = (df["time0_s"] > t_start) & (df["time0_s"] <= t_end)


        avg_pitch = df.loc[mask, 'pitch'].mean()
        avg_roll = df.loc[mask, 'roll'].mean()
        avg_yaw = df.loc[mask, 'yaw'].mean()

        if (avg_pitch == None or avg_roll == None or avg_yaw == None):
            logger.warning("Calibration failed section: " + self.__repr__)

        logger.info( " calibrating  from time0_s: " + str(t_start) + "s to : " + str(t_end) + " s" )
        logger.debug( ' avg_pitch :' + str(avg_pitch) + " rad so: " + str(np.rad2deg(avg_pitch)) + " deg")
        logger.debug( ' avg_roll :' + str(avg_roll) + " rad so: " + str(np.rad2deg(avg_roll)) + " deg")
        #logger.debug( ' avg_yaw :' + str(avg_yaw) + " rad so: " + str(np.rad2deg(avg_yaw)) + " deg" + " wanted (deg): "+ str(start_yaw_angle_deg))
        
        self.calibration = {"pitch" : avg_pitch , "roll" :avg_roll , "yaw" : avg_yaw }
        return {"pitch" : avg_pitch , "roll" :avg_roll , "yaw" : avg_yaw }
    
    def get_calibration(self):
        return self.calibration

        

class Data_File:


    def __init__(self, mfilePath, mdevice, mposition):
        logger.info("Data_File ")

        self.version = 1  # version of the Data_File model
        self.file_path = mfilePath
        self.file_date = None
        self.file_sha1 = None
        self.device = mdevice
        self.device_sn = None  # serial number of the devices
        self.device_param = None
        self.position = mposition  # serial number of the devices

        self.df = None

        self.file_sha1 = sha256sum(self.file_path)

        self.file_date = time.ctime(os.path.getctime(self.file_path))

    def __repr__(self):
        return '%s (%s) ' % (self.position, str(self.df.shape))

    def populate_df(self):
        logger.info("populate_df ")
        if self.device == Device.PIXRACER:
            self.df = ulog_to_df(self.file_path)

    def list_available_data(self):
        if self.device == Device.PIXRACER:
            return ulog_list_data(self.file_path)

    def populated_device_param(self):
        if self.device == Device.PIXRACER:
            self.device_param = ulog_param(self.file_path)

    def get_start_end_time(self):
        """
        return the start and end timestamp in s 
        """
        timestamp_start = (
            self.df[~self.df["time_utc_usec"].isnull()].iloc[0]["time_utc_usec"]
            / 10 ** 6
        )
        timestamp_end = (
            self.df[~self.df["time_utc_usec"].isnull()].iloc[-1]["time_utc_usec"]
            / 10 ** 6
        )

        return {"timestamp_start": timestamp_start, "timestamp_end": timestamp_end}

class Video_File:
    def __repr__(self):
        return '%s' % (self.device)

    def __init__(self, mfilePath, mdevice):
        logger.info("Data_File ")

        self.version = 1  # version of the Data_File model
        self.file_path = mfilePath
        self.file_date = None
        self.file_sha1 = None
        self.device = mdevice

        self.file_sha1 = sha256sum(self.file_path)

        self.file_date = time.ctime(os.path.getctime(self.file_path))