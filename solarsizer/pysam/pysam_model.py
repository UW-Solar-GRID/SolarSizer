#!/usr/bin/env python
# coding: utf-8

import os
import numpy as np
import pandas as pd
import PySAM.Pvsamv1 as pv
import matplotlib.pyplot as plt
import urllib.request
from pysam.pysam_utils import run_pvmodel

def pysam_model():
    
    print('started running')

    ## Running single scenario to get an estimate of the array size 
    pv_guess, our_load_profile = run_pvmodel.execute_pvmodel(2, 1, n_inverters=1)
    
    print('calculating uptime_hours')
    
    uptime_hours = np.count_nonzero(
        (np.array(pv_guess.Outputs.system_to_load) + 
         np.array(pv_guess.Outputs.batt_to_load) - 
         np.tile(our_load_profile, 25)  # repeat load profile for 25 years
        ) == 0 
    )
    
    print('calculating panel_number_estimate')
    
    panel_number_estimate = (1/(uptime_hours/(365 * 24 * 25)))/1.5 #, uptime_hours  # percent uptime for 25 years
    
    print('panel_number_estimate', panel_number_estimate)


    # Now, we will evaluate multiple scenarios - we will look at a range of modules numbers and a range of strings to find minimum system requirements that satisfy maximum uptime

    pvmodels_param = []
    pvmodels = []
    
    print('testing multiple scenarios')

    for m in range(2,8): # m is no of modules
        for n in range(1,30): # n is no of strings
            print('m', m)
            print('n', n)
            if m*n >=panel_number_estimate:  
                print('m*n is greater than panel_number_estimate') 
                z, our_load_profile = run_pvmodel.execute_pvmodel(m,n,m)
                pvmodels_param.append([m, n, n])
                pvmodels.append(z) 
                print('z', z)
                print('scenario ran')
                
#    if len(pvmodels) == 0:
#    #error for system cant match load profile
#        pass
    
    uptime_percent = []
    pvmodel_analysis = []
    system_analysis = []
    
    print('pvmodels', pvmodels)

    for i in range(len(pvmodels)):
        uptime_hours = np.count_nonzero(
            (np.array(pvmodels[i].Outputs.system_to_load) + 
             np.array(pvmodels[i].Outputs.batt_to_load) - 
             np.tile(our_load_profile, 25)  # repeat load profile for 25 years
            ) == 0 
        )
        
        print('uptime_hours', uptime_hours)
    
        uptime_percent.append(uptime_hours/(365 * 24 * 25))
        print('uptime_percent', uptime_percent)
        pvmodel_analysis = pvmodels_param[i]
        print('pvmodel_analysis', pvmodel_analysis)
        pvmodel_analysis.append(uptime_percent[i])
        print('pvmodel_analysis', pvmodel_analysis)
        system_analysis.append(pvmodel_analysis)
        print('system_analysis', system_analysis)

    print('out of loop')
    df_system_array = pd.DataFrame(system_analysis,columns = ['Panels in Strings','Strings','Inverters','Uptime_Percent'])
          
    print('df_system_array', df_system_array)
    #df_uptime_met = df_system_array[df_system_array.Uptime_Percent>0.95] 
    
    print('finished running')
    
    return df_system_array