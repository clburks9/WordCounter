
'''
************************************************************************************************************************************************************
File: wordCounting.py
Written By: Luke Burks
August 2017

Intended to determine how many words in the english language
a test subject knows.

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

__author__ = "Luke Burks"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Luke Burks"
__email__ = "clburks9@gmail.com"
__status__ = "Development"



class WordCounter:

	def __init__(self):
		self.exitFlag = False; 

		signal.signal(signal.SIGINT, self.signal_handler);
		self.loadSubjectData(); 

	def loadSubjectData(self):
		#get user ID
		self.sID = str(raw_input("Please input your subject ID:")); 
		
		#Check if subject has an existing profile
		pathName = "../data/subjectData/{}.hdf5".format(self.sID);
		if(os.path.exists(pathName)):
			#If so, open that hdf5 file
			f = h5py.File(pathName);
			f.close(); 
			self.pathName = pathName; 
		else:
			#If not, ask if they'd like to create one
			answer = str(raw_input("Would you like to initialize a new subject profile? (Y/N)"));
			if(answer.lower() == "y"):
				#If so, create one
				f = h5py.File(pathName); 
				f.create_dataset("words",(0,),maxshape=(None,));
				f.create_dataset("indexes",(0,),maxshape=(None,)); 
				f.create_dataset("answers",(0,),maxshape=(None,));
				f.create_dataset("percentages",(0,),maxshape=(None,)); 
				f.close();
				self.pathName = pathName;  
			else:
				print("Exiting Experiment..."); 
				sys.exit(0); 
				#If not, exit


	def getWord(self):

		#generate random index
		index = randint(0,370101); 

		#Check that the index hasn't already been asked of the subject
		f = h5py.File(self.pathName,'r+');  
		askedAlready = np.array(f["indexes"]); 
		while(index in askedAlready):
			index = randint(0,370101); 

		#grabs a word from the file at the chosen index
		#without opening the whole thing
		#also cuts the endline off
		word = linecache.getline('../data/words_alpha.txt',index)[:-1]; 
		
		#returns the index and word
		return [index,word]; 
		


	def askWord(self,word):
		ans = 'n'; 
		try:
			ans = str(raw_input(word + ('\n'))); 
		except(RuntimeError):
			self.experimentStopper(); 
		print(""); 
		print("");
		if(ans.lower() == 'y' or ans == '.'):
			return True; 
		else:
			return False; 


	def findPer(self,ans):
		f = h5py.File(self.pathName,'r+');  
		answers = np.array(f['answers']);
		f.close(); 
		numTrue = 0; 
		numFalse = 0; 
		total = len(answers)+1;
		if(ans == True):
			numTrue += 1; 
		else:
			numFalse +=1; 
		for a in answers:
			if(a == True):
				numTrue+=1; 
			else:
				numFalse+=1; 

		#basically each word is a draw from a hyper geometric distribution
		#use the hypergeometric test for significance
		per = numTrue/total; 
		return per; 

	def runTest(self):
		while(self.exitFlag == False):
			#get a word
			[index,word] = self.getWord();

			#ask the subject if they know that word
			ans = self.askWord(word); 
			
			#do the statistical analysis
			per = self.findPer(ans); 

			#write all the data to the file
			f = h5py.File(self.pathName,'r+');
			words = np.array(f["words"]);  
			indexes = np.array(f['indexes']); 
			answers = np.array(f['answers']);
			percentages = np.array(f['percentages']);  
			 

			os.remove(self.pathName); 

			words = np.append(words,word); 
			indexes = np.append(indexes,index); 
			answers = np.append(answers,ans); 
			percentages = np.append(percentages,per); 

			print(words); 

			f = h5py.File(self.pathName,'w'); 

			f.create_dataset('words',data=words);
			f.create_dataset("indexes",data = indexes); 
			f.create_dataset("answers",data = answers);
			f.create_dataset("percentages",data = percentages); 
			f.close();


	def signal_handler(self,signal, frame):
		if(self.exitFlag==False):
			answer = raw_input("Would you like to stop the experiment?"); 
			if(answer.lower()=='y'):
				print("Stopping word generation and saving results..."); 
				self.exitFlag = True; 
		else:
			print("Overriding Proper Stop Protocol. Shutting down now...")
			sys.exit();

	def experimentStopper(self):
		print("Stopping word generation and saving results..."); 
		sys.exit();


if __name__ == "__main__": 
	tester = WordCounter(); 
	tester.runTest(); 

	# f = h5py.File("../data/subjectData/luke.hdf5",'r');
	# print(np.array(f['words']));
	# print(np.array(f['answers']));
	# print(np.array(f['indexes']));
	# print(np.array(f['percentages']));



