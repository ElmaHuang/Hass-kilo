from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
from base64 import b64decode
from prettytable import PrettyTable

import ConfigParser
import logging
import os
import sys
import time
#sys.path.append("../Desktop/HASS-Project-master")

#cwd = os.path.dirname(os.path.abspath(__file__))

class RunTestCase():	
		
	def execute_testcase(self,testcase_Type,testcasetimes):

		testcase_times=int(testcasetimes)
		
		if testcase_Type is None:
			print "there is no test case"
			
		elif testcasetimes is None:
			print "there is no times" 

		elif testcase_times is 0:
			print "the times cannot be 0"			

		else:
			run=TestcaseResult()
			self.testcase=run.caculate_testcaseresult(testcase_Type)
			self.run_testcase(self.testcase,testcase_times)

	#	output into log
	def run_testcase(self,testcase_type,testcase_time):
		#inty=int(testcase_time)	
		#print "inty:%i" %(i) 
	
		for j in range(0,testcase_time):
			#print "j:%i" %(i)
			time.sleep(float(3))
			os.system("python %s.py" %testcase_type)	
			print "%s finish" %testcase_type

	def clearlog(self):
		with open('./log/fail.log', 'w'): pass	
		with open('./log/sucess.log', 'w'): pass	


class TestcaseResult():

	def __init__(self):
		self.total_case=0
		self.total_sucesscase=0

		self.test01=[0,0,0]
		self.test02=[0,0,0]
		self.test03=[0,0,0]
		self.test04=[0,0,0]
		self.test05=[0,0,0]
		self.test06=[0,0,0]
		self.test07=[0,0,0]
		self.test08=[0,0,0]
		self.test09=[0,0,0]
		self.test10=[0,0,0]

		self.List={"test01":self.test01,"test02":self.test02,"test03":self.test03,"test04":self.test04,"test05":self.test05,"test06":self.test06,"test07":self.test07,"test08":self.test08,"test09":self.test09,"test10":self.test10}


	def caculate_resultList(self):
		with open('./log/sucess.log','r') as fs:
			for line in fs:
				self.tempe=self.caculate_testcaseresult(line)
				self.List[self.tempe][0]+=1

		fs.close()

		with open('./log/fail.log','r') as ff:
			for lines in ff:
				self.tempe=self.caculate_testcaseresult(line)
				self.List[self.tempe][1]+=1

		ff.close()
		


			
	def caculate_testcaseresult(self,test_String):

		self.tempe=str(test_String)

		if self.tempe in ["test01","test01\n","test-01","test1"]:
			return "test01"

		elif self.tempe in ["test02","test02\n","test-02","test2"]:
			return "test02"
			
		elif self.tempe in ["test03","test03\n","test-03","test3"]:
			return "test03"

			
		elif self.tempe in ["test04","test04\n","test-04","test4"]:
			return "test04"
			
			
		elif self.tempe in ["test05","test05\n","test-05","test5"]:
			return "test05"

			
		elif self.tempe in ["test06","test06\n","test-06","test6"]:
			return "test06"

			
		elif self.tempe in ["test07","test07\n","test-07","test7"]:
			return "test07"

		elif self.tempe in ["test08","test08\n","test-08","test8"]:
			return "test08"
			
		elif self.tempe in ["test09","test09\n","test-09","test9"]:
			return "test09"

			
		elif self.tempe in ["test10","test10\n","test-10","test10"]:
			return "test10"		

		else:
			print "No this test case"
		

	def show_report(self,testcase_list):
		self.reportTable = PrettyTable()
		self.reportTable.field_names = ["Test Case Name", "Number of Sucess Case", "Number of Fail Case", "Sucess Rate"]
		#print "test10= %s"%(self.test10)
		for j in range(0,len(testcase_list)):
			self.ln=str(testcase_list[j])
			self.temp=self.caculate_testcaseresult(self.ln)

			if self.List[self.temp][2]< 1 :
				self.List[self.temp][2]+=1

				self.total_sucesscase+=int(self.List[self.temp][0])
				self.total_case+=int(self.List[self.temp][0]+self.List[self.temp][1])
				self.reportTable.add_row([self.temp,self.List[self.temp][0],self.List[self.temp][1],str(100*float(self.List[self.temp][0])/float(int(self.List[self.temp][0])+int(self.List[self.temp][1])))+"%"])
			#print "test10[0]= %i"%(self.test10[0])
		print self.reportTable 	

		self.totalreport=PrettyTable()	
		self.totalreport.field_names = ["Total Number of Test Case", "Total Sucess Rate"]
		self.totalreport.add_row([self.total_case,str(100*float(self.total_sucesscase)/float(self.total_case))+"%"])
		print self.totalreport



def main():
	#read config
	runtest=RunTestCase()
	testresult=TestcaseResult()
	testcaselist=[]
	print "Start Test System"
	
	config = ConfigParser.RawConfigParser()
	config.read('testcaseconfig.cfg')
	
	#with open('./log/sucess.log', 'w'): pass
	runtest.clearlog()

	for i in range(1,11):
		#case="case%i" %(i)
		time.sleep(float(10))

		testcase_name=config.get('test case', 'case%i' %(i)) 
		times=config.get('time','case%i_time' %(i))

		testcaselist.append(testcase_name)
		
		#print testcaselist

		runtest.execute_testcase(testcase_name,times)
	
	testresult.caculate_resultList()
	testcaselist.sort()
	testresult.show_report(testcaselist)

if __name__ == "__main__":
	main()
