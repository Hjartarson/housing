# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import httplib
import time
from hashlib import sha1
import random
import string
import json
import numpy as np
import seaborn as sb
import numpy as np
import pandas as pd

callerId = "YOUR_CALLER_ID"
timestamp = str(int(time.time()))
unique = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(16))
hashstr = sha1(callerId+timestamp+"YOUR_PRIVATE_KEY"+unique).hexdigest()

kvmPriceMonth=[]
kvmSizeMonth=[]
dateArray = [
             '20150101',
             '20150201',
             '20150301',
             '20150401',
             '20150501',
             '20150601',
             '20150701',
             '20150801',
             '20150901',
             '20151001',
             '20151101',
             '20151201',
             '20160101',
             '20160201',
             '20160301',
             '20160401',
             '20160501',
             '20160601',
             '20160701',
             '20160801',
             ]
             
for i in range(len(dateArray)-1):
    print dateArray[i]
    url = ("/sold?q=gröndal&"
            "minSoldDate="+dateArray[i]+"&"
            "maxSoldDate="+dateArray[i+1]+"&"
            #"minLivingArea=40&"
            #"maxLivingArea=70&"
            "limit=10000&"+
            "callerId="+callerId+"&time="+timestamp+"&unique="+unique+"&hash="+hashstr)
   
   
    connection = httplib.HTTPConnection("api.booli.se")
    connection.request("GET", url)
    response = connection.getresponse()
    data = response.read()
    connection.close()
    time.sleep(1)
    if response.status != 200:
        print "fail"
        kvmPriceMonth.append(0)
        kvmSizeMonth.append(0)
    else:
        result = json.loads(data)
        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)
        count = result['totalCount']
        print "Nr: "+str(count)
        
        kvmPrice=[]
        kvmSize=[]
        for i in range(count):
            try:
                kvmPrice.append(result['sold'][i]['soldPrice']/result['sold'][i]['livingArea'])
                kvmSize.append(result['sold'][i]['livingArea'])
            except:
                print "info missing"
        nrObjects = count
        kvmSizeMonth.append(np.mean(kvmSize))
        kvmPriceMonth.append(np.mean(kvmPrice))
    
x = range(len(kvmSizeMonth))
df = pd.DataFrame(kvmPriceMonth,index=pd.to_datetime(dateArray[0:-1]),columns=['kvm_price'])




res = json.loads(data)
size = []
price = []
for i in range(res['count']):
    try:
        price.append(res['sold'][i]['soldPrice'])
        size.append(res['sold'][i]['livingArea'])
        #date.append(res['sold'][i]['livingArea'])
    except:
        print i
    
tag=np.ones(len(price))
sb.plt.rcParams['figure.figsize']=(16,10) 
data = {'price': pd.Series(price),'size': pd.Series(size),'tag':pd.Series(tag)}
#data2 = {'price':[3800000],'size':[52],'tag':[2]}
df = pd.DataFrame(data)
#df2 = pd.DataFrame(data2)
#df = df.append(df2)
df.plot(kind='scatter',x='size',y='price',title='Grondal 20150101-20160416')
#,xticks=np.arange(0,200,10),yticks=np.arange(0,12000000,400000)

#df[df.tag!=2].plot(kind='scatter',x='size',y='price',title='Grondal 20150101-20160416',xticks=np.arange(0,200,10),yticks=np.arange(0,12000000,400000))


