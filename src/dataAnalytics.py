
'''
************************************************************************************************************************************************************
File: dataAnalytics.py
Written By: Luke Burks
August 2017

Analysis of data comming from the wordCounter

Words are chosen from the infochimps simple english word list
on: http://www.infochimps.com/

Words are farther paired down to remove words with numbers,
resulting in the list used from: https://github.com/dwyl/english-words



************************************************************************************************************************************************************
'''
from __future__ import division
import linecache
from random import randint
import os
import h5py
import sys
import numpy as np
import signal
import matplotlib.pyplot as plt
from scipy.stats import norm

__author__ = "Luke Burks"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Luke Burks"
__email__ = "clburks9@gmail.com"
__status__ = "Development"



def grabData():
	f = h5py.File("../data/subjectData/luke1.hdf5",'r'); 
	pers = np.array(f['percentages']); 
	ans = np.array(f['answers']); 

	totalWords = 370101

	means = []; 
	confidenceBounds = []; 
	UB = []; 
	LB = []; 
	totalYes = 0; 
	totalNo = 0; 
	total = 0; 
	alpha = 0.05; 
	z = norm.ppf(1-.5*alpha)  

	for a in ans:
		total +=1; 
		if(int(a)==0):
			totalNo +=1; 
		if(int(a)==1):
			totalYes +=1; 
		mean = totalYes/total; 
		cbu = mean+z*np.sqrt((mean*(1-mean))/total); 
		cbl = mean-z*np.sqrt((mean*(1-mean))/total); 
		UB.append(cbu); 
		LB.append(cbl); 
		confidenceBounds.append([cbl,cbu]); 
		means.append(mean); 

	x = [i for i in range(0,len(ans))]; 

	plt.figure(); 
	plt.plot(x,means,'b');
	plt.plot(x,UB,'b--'); 
	plt.plot(x,LB,'b--'); 
	plt.fill_between(x,LB,UB,color='b',alpha=0.25);

	plt.ylim([0,1]); 
	plt.title('Percentage of words known with 95% confidence bounds')

	plt.show(); 






if __name__ == "__main__":

	grabData(); 