'''
Created on 2017/02/13

@author: 6516371656
'''
# coding: UTF-8

import pandas as pd
import numpy as np
from pandas import DataFrame
import datetime 
import scipy.stats as sp

dat = pd.read_csv('OnlineRetail_ver1.csv')
dat = dat[dat.ClusterID_S != 1]
dat = dat[dat.ClusterID_S != 7]
dat = dat[dat.ClusterID_C != 4]
dat = dat[dat.ClusterID_C != 5]
del dat['InvoiceMonth']
del dat['InvoiceHour']
del dat['ClusterID_C']
del dat['ClusterID_S']
 
dat['InvoiceDate'] = pd.to_datetime(dat['InvoiceDate'], format="%Y/%m/%d %H:%M:%S")
dat_s = dat[dat.Quantity > 0]
dat_r = dat[dat.Quantity < 0]
 
##Customer Analysis
dat_cid = dat_s.groupby('CustomerID')
##RFM
#Recency
dat_cid_recency = datetime.datetime(2011,12,9,23,59,59) - dat_cid.max().InvoiceDate
dat_cid_recency = dat_cid_recency.astype('timedelta64[D]')
dat_cid_recency_std = sp.stats.zscore(dat_cid_recency)
dat_cid_recency_std = pd.DataFrame(dat_cid_recency_std)
#Frequency
dat_cid_inv = dat_s.groupby(['CustomerID','InvoiceNo']).size().reset_index()
dat_cid_frequency = dat_cid_inv.groupby('CustomerID')['InvoiceNo'].size()
dat_cid_frequency_std = sp.stats.zscore(dat_cid_frequency)
dat_cid_frequency_std = pd.DataFrame(dat_cid_frequency_std)
#Monetary
dat_cid_sales = dat_cid.sum().Sales
dat_cid_sales_std = sp.stats.zscore(dat_cid_sales)
dat_cid_sales_std = pd.DataFrame(dat_cid_sales_std)
#R+F+M
dat_rfm_std = pd.concat([dat_cid_recency_std, dat_cid_frequency_std, dat_cid_sales_std], axis=1)
dat_rfm = pd.concat([dat_cid_recency, dat_cid_frequency, dat_cid_sales], axis=1)
  
##Cluster Analysis of RFM
from sklearn.cluster import KMeans
kmeans_model_rfm = KMeans(n_clusters=10, random_state=10).fit(dat_rfm_std)
labels_c = kmeans_model_rfm.labels_
dat_rfm['ClusterID_C']=labels_c
dat = pd.merge(dat, dat_rfm['ClusterID_C'].to_frame(), left_on='CustomerID', right_index=True)
# dat_rfm_result = pd.concat([dat_rfm[dat_rfm['ClusterID_C']==0].mean(), dat_rfm[dat_rfm['ClusterID_C']==1].mean(), dat_rfm[dat_rfm['ClusterID_C']==2].mean(), dat_rfm[dat_rfm['ClusterID_C']==3].mean(), dat_rfm[dat_rfm['ClusterID_C']==4].mean(), dat_rfm[dat_rfm['ClusterID_C']==5].mean(), dat_rfm[dat_rfm['ClusterID_C']==6].mean(), dat_rfm[dat_rfm['ClusterID_C']==7].mean(), dat_rfm[dat_rfm['ClusterID_C']==8].mean(), dat_rfm[dat_rfm['ClusterID_C']==9].mean()], axis=1)
# dat_rfm_result.to_csv('dat_rfm_result_2.csv')
dat = dat[dat.ClusterID_C != 1]
dat = dat[dat.ClusterID_C != 3]
dat = dat[dat.ClusterID_C != 4]
dat = dat[dat.ClusterID_C != 6]
dat.to_csv('OnlineRetail_ver2.csv')