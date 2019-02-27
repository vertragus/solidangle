
# coding: utf-8

# In[1]:

#set up 3 folders 'panel','vp','output'  
#the former 2 containing the input csv with the same filename as in file
#######
#bring all geometry close to origin to improve quality of data output
#the input csv should be, for panels: 'x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4', without headers. 
#x,y,z coordinates of vertexes 1,2,3,(4). vertex 4 should be coincident with vertex 3 in case panels are triangular.
#######
#the input csv should be, for viewpoints: 'xvp,yvp,zvp', without headers.

import pandas as pd
import numpy as np

#set directory and file 
file='prova'
panel_dir="C:/Users/florio/Desktop/prova/sa/panel/"
vp_dir='C:/Users/florio/Desktop/prova/sa/vp/'
output_dir='C:/Users/florio/Desktop/prova/sa/output/'
print('input panel dir: '+panel_dir+file+'.csv')
print('viewpoints dir: '+vp_dir+file+'.csv')
print('output mean solid angle per panel across viewpoints dir: '+output_dir+file+'.res')

#read csv and extract vertex coordinates column
tile=pd.read_csv(panel_dir+file+'.csv',header=None)
coord=tile #subset CSV table if needed
#print(coord)


# In[2]:

#split coordinates into x y and z values
splitted_coord=coord
#label columns
cols=['x1','y1','z1','x2','y2','z2','x3','y3','z3','x4','y4','z4']
splitted_coord.columns=cols
print(splitted_coord)


# In[3]:

#read viewpoints csv
viewpoints=pd.read_csv(vp_dir+file+'.csv',header=None)
viewpoints.columns=['xvp','yvp','zvp']
vpid=viewpoints.index.values
print(viewpoints)


# In[18]:

#create empty matrix to host solid angles, panels in rows and viewpoints in columns
sa_matrix=np.empty((splitted_coord.shape[0],viewpoints.shape[0]))
#calculate solid angle between viewpoint and panels
import time
import datetime
start_time = time.time()
for nvp, vp in viewpoints.iterrows():
    a=np.array([splitted_coord['x1']-vp['xvp'],splitted_coord['y1']-vp['yvp'],splitted_coord['z1']-vp['zvp']]).T.tolist()
    b=np.array([splitted_coord['x2']-vp['xvp'],splitted_coord['y2']-vp['yvp'],splitted_coord['z2']-vp['zvp']]).T.tolist()
    c=np.array([splitted_coord['x3']-vp['xvp'],splitted_coord['y3']-vp['yvp'],splitted_coord['z3']-vp['zvp']]).T.tolist()
    d=np.array([splitted_coord['x4']-vp['xvp'],splitted_coord['y4']-vp['yvp'],splitted_coord['z4']-vp['zvp']]).T.tolist()   
    vectors=pd.DataFrame({'veca':a,'vecb':b,'vecc':c,'vecd':d})
    def ab(row):
        return np.dot(row['veca'],row['vecb'])  
    def ac(row):
        return np.dot(row['veca'],row['vecc'])
    def bc(row):
        return np.dot(row['vecb'],row['vecc'])
    def bxc(row):
        return np.cross(row['vecb'],row['vecc']).tolist()
    def ad(row):
        return np.dot(row['veca'],row['vecd'])
    def cd(row):
        return np.dot(row['vecc'],row['vecd'])
    def cxd(row):
        return np.cross(row['vecc'],row['vecd']).tolist()
    vectors['ab']=vectors.apply(ab,axis=1)
    vectors['ac']=vectors.apply(ac,axis=1)
    vectors['bc']=vectors.apply(bc,axis=1)
    vectors['bxc']=vectors.apply(bxc,axis=1)
    vectors['ad']=vectors.apply(ad,axis=1)
    vectors['cd']=vectors.apply(cd,axis=1)
    vectors['cxd']=vectors.apply(cxd,axis=1)
    def sa(row):
        return np.abs(2*np.arctan(np.dot(row['veca'],row['bxc'])/(np.linalg.norm(row['veca'])*np.linalg.norm(row['vecb'])*np.linalg.norm(row['vecc'])+row['ab']*np.linalg.norm(row['vecc'])+row['ac']*np.linalg.norm(row['vecb'])+row['bc']*np.linalg.norm(row['veca']))))+np.abs(2*np.arctan(np.dot(row['veca'],row['cxd'])/(np.linalg.norm(row['veca'])*np.linalg.norm(row['vecd'])*np.linalg.norm(row['vecc'])+row['ad']*np.linalg.norm(row['vecc'])+row['ac']*np.linalg.norm(row['vecd'])+row['cd']*np.linalg.norm(row['veca']))))
    vectors['sa']=vectors.apply(sa,axis=1)
    sa_matrix[:,nvp]=vectors['sa']
    print ('\r'+str(round(nvp/len(viewpoints)*100,2))+' % complete', end='')
elapsed=(time.time() - start_time)
print("--- %s seconds ---" % elapsed)
print(str(datetime.timedelta(seconds=elapsed)))


# In[15]:

#check matrix
print(sa_matrix)
print(sa_matrix.shape)


# In[16]:

#calculate mean of values per row (panel) across the different columns (viewpoints)
#calculate sum of row values, i.e. the total solid angle subtended by all panels
sa_mean = np.mean(sa_matrix,axis=1)
sa_sum=np.sum(sa_matrix,axis=0)
print('average solid angle: '+str(sa_mean))
print('average solid angle array shape: '+str(sa_mean.shape))
print('total solid angle of different panels: '+str(sa_sum))


# In[50]:

#export as textfiles
sa_mean_pd=pd.DataFrame({'sa_mean_per_vp':sa_mean})
sa_mean_pd.to_csv(output_dir+file+".res")
print("export complete")


# In[ ]:



