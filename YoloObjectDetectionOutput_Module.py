#!/usr/bin/env python
# coding: utf-8

# In[68]:


import re
import pandas as pd 
class YoloObjectDetectionOutput():
    def __init__(self,rawDatafile):
        with open (rawDatafile, 'rt') as rawData:
            self.contents = rawData.read()
        self.contents=re.sub(r'\n', ' ', self.contents)
        self.contents=re.sub(r'\t', ' ', self.contents)
        mylist= self.contents.split(' ')
        mylist_dropHeaderInfo = mylist[mylist.index('FPS:0.0'):]
        my_listToString = ' '.join(map(str, mylist_dropHeaderInfo))
        Data_preprocessed= my_listToString.replace("(","").replace(")","\n").split("\n")
        FPS=[]
        AVG_FPS=[]
        Flachhänger=[]
        left_x=[]
        top_y=[]
        width=[]
        height=[]
        for item in Data_preprocessed:
            try:
                FPS.append(re.search("FPS:(.*?)AVG_FPS:", item ).group(1).strip())
            except AttributeError:
                continue 
            try:
                AVG_FPS.append(re.search("AVG_FPS:(.*?)Objects:", item ).group(1).strip())
            except AttributeError:
                continue 
            try:
                 Flachhänger.append(re.search("Flachhänger:(.*?)left_x:",item).group(1).strip())
            except AttributeError:
                continue 
            try:
                left_x.append(re.search("left_x:(.*?)top_y:", item ).group(1).strip())
            except AttributeError:
                continue 
            try:
                top_y.append(re.search("top_y:(.*?)width:", item ).group(1).strip())
            except AttributeError:
                continue
            try:
                width.append(re.search("width:(.*?)height:", item ).group(1).strip())
            except AttributeError:
                continue
            try:
                height.append(re.search("height:(.*)", item ).group(1).strip())
            except AttributeError:
                continue
        ListOfYoloOutputs={'FPS':FPS,'AVG_FPS':AVG_FPS,'Flachhänger':Flachhänger,
                'left_x':left_x,'top_y':top_y,'width':width,'height':height}
        self.df = pd.DataFrame(ListOfYoloOutputs)
        self.df.to_csv('YoLoDataOutputProcessed.csv',index=False)
    def data_analysis(self):
        for index in ['FPS','AVG_FPS','left_x','top_y','width','height']:
            self.df[index]= pd.to_numeric(self.df[index]) 
        self.df=self.df.convert_dtypes()
        print('How many object detections the run contains, and othere information:')
        print(self.df.info())
        self.uniqueObject=self.df.groupby(['Flachhänger','left_x', 'top_y','width','height']).size()
        print('How many different objects was detected?, and othere information:')
        print(self.uniqueObject)


# In[69]:


df=YoloObjectDetectionOutput('pkg_dump.txt')


# In[70]:


df.data_analysis()


# In[ ]:




