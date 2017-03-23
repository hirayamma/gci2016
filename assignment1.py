'''
Created on 2017/02/04

@author: 6516371656
'''
import pandas as pd
import numpy as np
from pandas import DataFrame
import datetime
#from pylab import *
#import matplotlib
#import matplotlib.pyplot as plt

dat_origin = pd.read_csv('OnlineRetail.csv')
dat_origin['Sales'] = dat_origin['Quantity'] * dat_origin['UnitPrice']

##Hidsuke
dat_origin['InvoiceDate'] = pd.to_datetime(dat_origin['InvoiceDate'], format="%Y/%m/%d %H:%M:%S")
dat_origin['InvoiceMonth'] = dat_origin['InvoiceDate'].dt.month.astype(int)
dat_origin['InvoiceHour'] = dat_origin['InvoiceDate'].dt.hour.astype(int)

#Henkin to wakeru
dat = dat_origin[dat_origin.Quantity > 0]
dat_return = dat_origin[dat_origin.Quantity < 0]


##Customer
dat_cid = dat.groupby('CustomerID')
dat_return_cid = dat_return.groupby('CustomerID')
##Purchase size groupby
dat_cid_size = dat_cid.size()
dat_return_cid_size = dat_return_cid.size()
#dat_cid_size = dat_cid_size.sort_values(ascending=False)
#dat_cid_size_10 = dat_cid_size[dat_cid_size > 999]
#print(dat_cid_size_10.size)
#print(dat_cid_size.mean())
#dat_cid_size.plot.hist(bins=100) ##Histgram of Purchase size
#plt.show()
##Purchase Order
#dat_cid_sales = dat_cid.sum().Sales
#dat_cid_sales = dat_cid_sales.sort_values(ascending=False)
#print(dat_cid_sales)
##Customer Data
dat_cid_sales = dat_cid.sum().Sales
dat_cid_return = dat_return_cid.sum().Sales
dat_cid_unit_sales = dat_cid.mean().Sales
dat_cid_unit_return = dat_return_cid.mean().Sales
dat_cid_month = dat_cid.median().InvoiceMonth
dat_cid_hour = dat_cid.median().InvoiceHour
dat_cid_stock = dat.groupby(['CustomerID','StockCode']).sum().Quantity
dat_cid_stock = dat_cid_stock.reset_index() #without this not pivot
dat_cid_stock_pivot = pd.pivot_table(dat_cid_stock, index='CustomerID', columns='StockCode', fill_value=0)
dat_cid_country = dat.groupby(['CustomerID','Country']).size()
dat_cid_country = dat_cid_country.reset_index() #without this not pivot
dat_cid_country_pivot = pd.pivot_table(dat_cid_country, index='CustomerID', columns='Country', fill_value=0)
dat_c = pd.concat([dat_cid_sales, dat_cid_size, dat_cid_unit_sales, dat_cid_return, dat_return_cid_size, dat_cid_unit_return, dat_cid_month, dat_cid_hour, dat_cid_stock_pivot,dat_cid_country_pivot], axis=1)
dat_c = dat_c.fillna(0)
#print(dat_c)

##Cluster Analysis of Customer
from sklearn.cluster import KMeans
kmeans_model_c = KMeans(n_clusters=10, random_state=10).fit(dat_c)
labels_c = kmeans_model_c.labels_
dat_c['ClusterID']=labels_c
dat_c_result = pd.concat([dat_c[dat_c['ClusterID']==0].mean(), dat_c[dat_c['ClusterID']==1].mean(), dat_c[dat_c['ClusterID']==2].mean(), dat_c[dat_c['ClusterID']==3].mean(), dat_c[dat_c['ClusterID']==4].mean(), dat_c[dat_c['ClusterID']==5].mean(), dat_c[dat_c['ClusterID']==6].mean(), dat_c[dat_c['ClusterID']==7].mean(), dat_c[dat_c['ClusterID']==8].mean(), dat_c[dat_c['ClusterID']==9].mean()], axis=1)
dat_c_result.to_excel('dat_c_result.xlsx')
# writer = pd.ExcelWriter('dat_c.xlsx')
# dat_c[dat_c['ClusterID']==0].to_excel(writer,'0')
# dat_c[dat_c['ClusterID']==1].to_excel(writer,'1')
# dat_c[dat_c['ClusterID']==2].to_excel(writer,'2')
# dat_c[dat_c['ClusterID']==3].to_excel(writer,'3')
# dat_c[dat_c['ClusterID']==4].to_excel(writer,'4')
# dat_c[dat_c['ClusterID']==5].to_excel(writer,'5')
# dat_c[dat_c['ClusterID']==6].to_excel(writer,'6')
# dat_c[dat_c['ClusterID']==7].to_excel(writer,'7')
# dat_c[dat_c['ClusterID']==8].to_excel(writer,'8')
# dat_c[dat_c['ClusterID']==9].to_excel(writer,'9')
# writer.save()
# dat_c_0_a = dat_c['ClusterID']
#print(dat_c)


##Purchase date
##Purchase date groupby
#dat_date = dat.groupby([dat['InvoiceDate'].dt.year, dat['InvoiceDate'].dt.month, dat['InvoiceDate'].dt.hour])
#dat_date_size = dat_date.size()
#dat_date_size.to_csv('dat_date_size.csv')

# #original no table naosu
# dat_origin = pd.merge(dat_origin, dat_c_0_a.to_frame(), left_on='CustomerID', right_index=True)
# dat = dat_origin[dat_origin.Quantity > 0]
# dat_return = dat_origin[dat_origin.Quantity < 0]

##Country
#dat_cont = dat.groupby('Country')
#dat_cont_size = dat_cont.size()
#dat_cont_size = dat_cont_size.sort_values(ascending=False)
#dat_cont_size.to_csv('dat_cont_size.csv')
#print(dat_cont_size)

##Stock
#dat_stock = dat.groupby([dat['InvoiceDate'].dt.year, dat['InvoiceDate'].dt.month, 'StockCode','Description'])
# dat_stock = dat.groupby(['StockCode'])
# dat_return_stock = dat_return.groupby(['StockCode'])
# dat_stock_size = dat_stock.size()
# dat_return_stock_size = dat_return_stock.size()
# #dat_stock_size.to_csv('dat_stock_size.csv')
# dat_stock_sales = dat_stock.sum().Sales
# dat_stock_return = dat_return_stock.sum().Sales
# dat_stock_unit_sales = dat_stock.mean().Sales
# dat_stock_unit_return = dat_return_stock.mean().Sales
# dat_stock_quantity = dat_stock.sum().Quantity
# dat_stock_tanka = dat_stock_sales / dat_stock_quantity
# dat_stock_month = dat_stock.median().InvoiceMonth
# dat_stock_hour = dat_stock.median().InvoiceHour
# dat_stock_cluster = dat.groupby(['StockCode','ClusterID']).sum().Quantity
# dat_stock_cluster = dat_stock_cluster.reset_index() #without this not pivot
# dat_stock_cluster_pivot = pd.pivot_table(dat_stock_cluster, index='StockCode', columns='ClusterID', fill_value=0)
# dat_stock_country = dat.groupby(['StockCode','Country']).size()
# dat_stock_country = dat_stock_country.reset_index() #without this not pivot
# dat_stock_country_pivot = pd.pivot_table(dat_stock_country, index='StockCode', columns='Country', fill_value=0)
# dat_s = pd.concat([dat_stock_sales, dat_stock_size, dat_stock_unit_sales, dat_stock_return, dat_return_stock_size, dat_stock_unit_return, dat_stock_quantity, dat_stock_tanka, dat_stock_month, dat_stock_hour, dat_stock_cluster_pivot, dat_stock_country_pivot], axis=1)
# dat_s = dat_s.fillna(0)

##Cluster Analysis of Stock
# from sklearn.cluster import KMeans
# kmeans_model_s = KMeans(n_clusters=10, random_state=10).fit(dat_s)
# labels_s = kmeans_model_s.labels_
# dat_s['ClusterID']=labels_s
# dat_s_result = pd.concat([dat_s[dat_s['ClusterID']==0].mean(), dat_s[dat_s['ClusterID']==1].mean(), dat_s[dat_s['ClusterID']==2].mean(), dat_s[dat_s['ClusterID']==3].mean(), dat_s[dat_s['ClusterID']==4].mean(), dat_s[dat_s['ClusterID']==5].mean(), dat_s[dat_s['ClusterID']==6].mean(), dat_s[dat_s['ClusterID']==7].mean(), dat_s[dat_s['ClusterID']==8].mean(), dat_s[dat_s['ClusterID']==9].mean()], axis=1)
# dat_s_result.to_excel('dat_s_result.xlsx')
# writer = pd.ExcelWriter('dat_s.xlsx')
# dat_s[dat_s['ClusterID']==0].to_excel(writer,'0')
# dat_s[dat_s['ClusterID']==1].to_excel(writer,'1')
# dat_s[dat_s['ClusterID']==2].to_excel(writer,'2')
# dat_s[dat_s['ClusterID']==3].to_excel(writer,'3')
# dat_s[dat_s['ClusterID']==4].to_excel(writer,'4')
# dat_s[dat_s['ClusterID']==5].to_excel(writer,'5')
# dat_s[dat_s['ClusterID']==6].to_excel(writer,'6')
# dat_s[dat_s['ClusterID']==7].to_excel(writer,'7')
# dat_s[dat_s['ClusterID']==8].to_excel(writer,'8')
# dat_s[dat_s['ClusterID']==9].to_excel(writer,'9')
# writer.save()
print(dat_c['ClusterID'].value_counts())
# print(dat_s['ClusterID'].value_counts())

# #Assign ClusterIDs to dat_origin
# dat_s_l = dat_s['ClusterID']
# dat_origin = pd.merge(dat_origin, dat_s_l.to_frame(), left_on='StockCode', right_index=True)
# dat = dat_origin[dat_origin.Quantity > 0]
# dat_return = dat_origin[dat_origin.Quantity < 0]
# dat_origin.to_csv('OnlineRetail_ver1.csv')

