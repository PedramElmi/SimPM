import numpy as np
import pandas as pd
import bisect
import scipy.stats as st
import matplotlib.pyplot as plt
'''
**************************************
*********distribution*****************
**************************************
'''

def fit_dist(data,distType):
        try:
            data=np.concatenate(data).ravel()
        except:
            pass
        if distType=='triang':
            distType='triang'
            params=st.triang.fit(data)
            dist=st.triang(params[0],loc=params[1],scale=params[2])
            a=triang(0,1,2)
            a.dist=dist
            return a
        if distType=='norm' :
            distType='norm'
            params=st.norm.fit(data)
            dist=st.norm(loc=params[0],scale=params[1])
            a=norm(0,1)
            a.dist=dist
            return a
        if distType=='beta' :
            distType='beta'
            params=st.beta.fit(data)
            dist=st.beta(params[0],params[1],loc=params[2],scale=params[3])
            a=beta(1,1,0,1)
            a.dist=dist
            return a
        if distType=='trapz' :
            distType='trapz'
            params=st.trapz.fit(data)
            print(params)
            dist=st.trapz(params[0],params[1],loc=params[2],scale=params[3])
            a=trapz(1,2,3,4)
            a.dist=dist
            return a

    
class Distribution():
    def __init__(self):
        self.params=None
        self.distType=None
        self.dist=None
        self.params=None

    def sample(self):
        return self.dist.rvs()
        
    def plot_pdf(self):
        low=0.00001
        high=.99999
        if self.distType=='uniform' or self.distType=='triang' or self.distType=='trapz':
            low=0
            high=1
        x=np.linspace(self.dist.ppf(low),self.dist.ppf(high),101)
        y=self.dist.pdf(x)
        plt.plot(x,y,'r')
        plt.show()

    def plot_cdf(self):
        low=0.00001
        high=.99999
        if self.distType=='uniform' or self.distType=='triang' or self.distType=='trapz':
            low=0
            high=1
        x=np.linspace(self.dist.ppf(low),self.dist.ppf(high),101)
        y=self.dist.cdf(x)
        plt.plot(x,y,'b')
        plt.show()

    def percentile(self,q):
        return self.dist.ppf(q)

    def pdf(self,x):
        return self.dist.pdf(x)

    def cdf(self,x):
        return self.dist.cdf(x)
        
class uniform(Distribution):
    def __init__(self,a,b):
        self.distType='uniform'
        Loc=a
        Scale=b-a
        self.params=[Loc,Scale]
        self.dist=st.uniform(loc=Loc,scale=Scale)
    
class norm(Distribution):
    def __init__(self,mean,std):
        self.distType='norm'
        self.params=[mean,std]
        self.dist=st.norm(loc=mean,scale=std)
class triang(Distribution): 
    def __init__(self,a,b,c):
        self.distType='triang'
        Loc=a
        Scale=c-a
        c=(b-a)/Scale
        self.params=[c,Loc,Scale]
        self.dist=st.triang(c,loc=Loc,scale=Scale)
    
class trapz(Distribution): 
    def __init__(self,a,b,c,d):

        self.distType='trapz'
        Loc=a
        Scale=d-a
        C=(b-a)/(d-a)
        D=(c-a)/(d-a)
       
        self.params=[C,D,Loc,Scale]
        self.dist=st.trapz(C,D,loc=Loc,scale=Scale)   
class beta(Distribution): 
    def __init__(self,a,b,minp,maxp):
        self.distType='beta'
        Loc=minp
        Scale=maxp-minp
        self.params=[a,b,Loc,Scale]
        self.dist=st.beta(a,b,loc=Loc,scale=Scale)  
class expon(Distribution): 
    def __init__(self,mean):
        self.distType='expon'
        Scale=mean
        self.params=[Scale]
        self.dist=st.expon(scale=Scale)

class emperical(Distribution):
    def __init__(self,data):
        try:
            data=np.concatenate(data).ravel()
        except:
            pass
        self.distType='emperical'
        self.params=None
        self.dist=None
        self.data=np.sort(data)

    def plot_cdf(self):
        print('here')
        unique, counts = np.unique(self.data, return_counts=True)
        c=np.cumsum(counts)
        print(c)
        c=c/c[-1]
        plt.step(unique,c)
        plt.show()

    def plot_pdf(self):
        bins=int(2*len(self.data)**(1/3))
        value,BinList=np.histogram(self.data,bins)
        value=value/len(self.data)
        l=BinList[-1]-BinList[0]
        n=len(BinList)
        width=l/(n)
        value=value/width
        BinList=BinList[:-1]+np.diff(BinList)[1]/2
        plt.bar(BinList,value,width)
        plt.show()

    def pdf(self,x):
        bins=int(2*len(self.data)**(1/3))
        value,BinList=np.histogram(self.data,bins)
        if x<BinList[0] or x>BinList[-1]:
            return 0
        i=0
        bl=len(BinList)
        while x>=BinList[i] and i<bl:
            i+=1
        r=value[i-1]/len(self.data)
        l=BinList[-1]-BinList[0]
        n=len(BinList)
        width=l/(n)
        r=r/width
        return r
       
    def cdf(self,x):
        if x>self.data[-1]:
            return 1
        i=0
        while x>=self.data[i]:
            i+=1
        return i/len(self.data)
 
    def percentile(self,q):
        return np.quantile(self.data,q)

    def sample(self):
        return np.quantile(self.data,np.random.random())
        
    def discrete_sample(self):
        return np.random.choice(self.data)
        
'''
*****************************
********future works*********
*****************************
'''