# -- coding: utf-8 --
#import sys
#sys.stdout.buffer.write(chr(9986).encode('utf8'))
import matplotlib.pyplot as plt
import http.client
from urllib.parse import urlencode
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
print(callerId,timestamp,"wKalNs1fMuymxyXtN9wPwEypXpwtVWA3JT4uepf8",unique)
hashstr = sha1((callerId+timestamp+"YOUR_PRIVATE_KEY"+unique).encode('utf-8')).hexdigest()
kvmPriceMonth=[]
kvmSizeMonth=[]
dateArray = [
             #'20150101',
             #'20150201',
             #'20150301',
             #'20150401',
             #'20150501',
             #'20150601',
             #'20150701',
             #'20150801',
             #'20150901',
             #'20151001',
             #'20151101',
             #'20151201',
             '20160101',
             '20160201',
             '20160301',
             '20160401',
             '20160501',
             '20160601',
             '20160701',
             '20160801',
             '20160901',
             ]
             
area = 'gr%C3%B6ndal'
print(area)      
for i in range(len(dateArray)-1):
    print(dateArray[i])
    url = ("/sold?q="+area+"&"
            "minSoldDate="+dateArray[i]+"&"
            "maxSoldDate="+dateArray[i+1]+"&"
            "minLivingArea=40&"
            "maxLivingArea=70&"
            "limit=10000&"
            "callerId="+callerId+"&time="+timestamp+"&unique="+unique+"&hash="+hashstr)
    connection = http.client.HTTPConnection("api.booli.se")
    connection.request("GET", url)
    response = connection.getresponse()
    data = response.read().decode('utf8')
    connection.close()
    time.sleep(1)
    if response.status != 200:
        print("fail")
        kvmPriceMonth.append(0)
        kvmSizeMonth.append(0)
    else:
        result = json.loads(data)
        with open('data.txt', 'w') as outfile:
            json.dump(data, outfile)
        count = result['totalCount']
        print("Nr: ",str(count))
        
        kvmPrice=[]
        kvmSize=[]
        for i in range(count):
            try:
                kvmPrice.append(result['sold'][i]['soldPrice']/result['sold'][i]['livingArea'])
                kvmSize.append(result['sold'][i]['livingArea'])
            except:
                print("info missing")
        nrObjects = count
        kvmSizeMonth.append(np.mean(kvmSize))
        kvmPriceMonth.append(np.mean(kvmPrice))
    
x = range(len(kvmSizeMonth))
df = pd.DataFrame(kvmPriceMonth,index=pd.to_datetime(dateArray[0:-1]),columns=['kvm_price'])

df.plot()
