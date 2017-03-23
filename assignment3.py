'''
Created on 2017/02/14

@author: 6516371656
'''

import pandas as pd
import numpy as np
from pandas import DataFrame
import datetime 
import scipy.stats as sp

dat_origin = pd.read_csv('OnlineRetail_ver2.csv')

##Hidsuke
dat_origin['InvoiceDate'] = pd.to_datetime(dat_origin['InvoiceDate'], format="%Y/%m/%d %H:%M:%S")

#Henkin to wakeru
dat = dat_origin[dat_origin.Quantity > 0]
dat_return = dat_origin[dat_origin.Quantity < 0]

##Customer
dat_cid = dat.groupby('CustomerID')
dat_return_cid = dat_return.groupby('CustomerID')
#Recency
dat_cid_recency = datetime.datetime(2011,12,9,23,59,59) - dat_cid.max().InvoiceDate
dat_cid_recency = dat_cid_recency.astype('timedelta64[D]')
dat_cid_recency_std = sp.stats.zscore(dat_cid_recency)
#Frequency
dat_cid_inv = dat.groupby(['CustomerID','InvoiceNo']).size().reset_index()
dat_cid_frequency = dat_cid_inv.groupby('CustomerID')['InvoiceNo'].size()
dat_cid_frequency_std = sp.stats.zscore(dat_cid_frequency)
#Monetary
dat_cid_sales = dat_cid.sum().Sales
dat_cid_sales_std = sp.stats.zscore(dat_cid_sales)
##Customer Data
dat_cid_s_q = dat_cid.sum().Quantity
dat_cid_r_q = dat_return_cid.sum().Quantity
dat_cid_return = dat_cid_r_q / dat_cid_r_q
dat_cid_unitprice = dat_cid.mean().UnitPrice
dat_cid_id = dat_cid.mean().ClusterID_C
dat_cid_stock = dat.groupby(['CustomerID','StockCode']).sum().Quantity
dat_cid_stock = dat_cid_stock.reset_index() #without this not pivot
dat_cid_stock_pivot = pd.pivot_table(dat_cid_stock, index='CustomerID', columns='StockCode', fill_value=0)
dat_cid_country = dat.groupby(['CustomerID','Country']).size()
dat_cid_country = dat_cid_country.reset_index() #without this not pivot
dat_cid_country_pivot = pd.pivot_table(dat_cid_country, index='CustomerID', columns='Country', fill_value=0)
dat_c = pd.concat([dat_cid_recency, dat_cid_frequency, dat_cid_sales, dat_cid_return, dat_cid_unitprice, dat_cid_id, dat_cid_stock_pivot,dat_cid_country_pivot], axis=1)
dat_c = dat_c.fillna(0)
dat_c_result = pd.concat([dat_c[dat_c['ClusterID_C']==0].mean(), dat_c[dat_c['ClusterID_C']==2].mean(), dat_c[dat_c['ClusterID_C']==5].mean(), dat_c[dat_c['ClusterID_C']==7].mean(), dat_c[dat_c['ClusterID_C']==8].mean(), dat_c[dat_c['ClusterID_C']==9].mean()], axis=1)
dat_c_result.to_excel('dat_c_result_ver2.xlsx')
