'''
Created on 2017/02/14

@author: 6516371656
'''

import pandas as pd
import numpy as np
from pandas import DataFrame
import datetime 
import scipy.stats as sp
import matplotlib
import matplotlib.pyplot as plt

plt.style.use('ggplot') 
font = {'family' : 'meiryo'}
matplotlib.rc('font', **font)

dat = pd.read_csv('OnlineRetail_ver2.csv')

##Hidsuke
dat['InvoiceDate'] = pd.to_datetime(dat['InvoiceDate'], format="%Y/%m/%d %H:%M:%S")
dat['InvoiceMonth'] = dat['InvoiceDate'].dt.month.astype(int)
dat['InvoiceYear'] = dat['InvoiceDate'].dt.year.astype(int)


dat_c_up = dat.groupby(['ClusterID_C','InvoiceYear','InvoiceMonth']).mean().UnitPrice
dat_c_up = dat_c_up.reset_index() #without this not pivot
dat_c_up_pivot = pd.pivot_table(dat_c_up, index=['InvoiceYear','InvoiceMonth'], columns='ClusterID_C', fill_value=0)

dat_good = dat[(dat.ClusterID_C== 0) | (dat.ClusterID_C== 5) | (dat.ClusterID_C== 7)]
dat_good_c_up = dat_good.groupby(['ClusterID_C','InvoiceYear','InvoiceMonth']).mean().UnitPrice
dat_good_c_up = dat_good_c_up.reset_index() #without this not pivot
dat_good_c_up_pivot = pd.pivot_table(dat_good_c_up, index=['InvoiceYear','InvoiceMonth'], columns='ClusterID_C', fill_value=0)
dat_good_c_up_pivot.plot()
plt.show()