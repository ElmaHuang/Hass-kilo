#test-05

from collections import Counter
from prettytable import PrettyTable
from datetime import datetime
import xmlrpclib
import sys
import ConfigParser
import os
import time

from Recovery import Recovery
from Recovery import Cluster

environment_node = ["testNode1", "testNode2", "testNode3", "testNode4"]
listen_port = str(61209)

cwd = os.path.dirname(os.path.abspath(__file__))
#sys.stdout = open(os.path.join(cwd,"log/","test-01_%s" %(time.strftime('%Y-%m-%d-%H.%M.%S'))),'w')


# ----------------------------Test Data-------------------------
correct_auth = "http://user:0000@127.0.0.1:" + listen_port
no_auth = "http://127.0.0.1:" + listen_port
wrong_auth = "http://auth:fail@127.0.0.1:" + listen_port

cluster_name = "testCluster"

correct_nodeList = ["testNode1", "testNode4"]
duplicate_nodeList = ["testNode1", "testNode3"]
wrong_nodeList = ["testNode4", "testNode5"]
correct_nodeName = "testNode1"
wrong_nodeName = "testNode5"
wrong_clusterId = "1a2b3c4d-5678-9101-2b3c-zxcvb987654a"

test_instanceId = "0e4011a4-3128-4674-ab16-dd1b7ecc126e"
duplicate_instanceId = "0e4011a4-3128-4674-ab16-dd1b7ecc126e"
wrong_instanceId = "1a2b3c4d-5678-9101-2b3c-zxcvb987654a"


# --------------------------------------------------------------

class ShowResult():
    def __init__(self):
        self.OK = '\033[92m' + "PASS!" + '\033[0m'
        self.ERROR = '\033[91m' + "FAIL!" + '\033[0m'

    def ok(self, case, time):
        print case + "(" + str(time.microseconds) + "ms) : " + self.OK

    def error(self, case, time):
        print case + "(execution time:" + str(time.microseconds) + "ms) : " + self.ERROR

           
class TestNode():
    def __init__(self):
        self.printer = ShowResult()
        self.case_counter = 0
        self.pass_case = 0
        self.fail_case = 0

    # test-05
    def test_add_correctList(self):
        case = "Add nodes to HA cluster with correct node list"
        self.case_counter += 1
        testRM = Recovery(test=True)
        test_clusterId = testRM.createCluster(cluster_name)["clusterId"]

        start_time = datetime.now()
        result = testRM.addNode(test_clusterId, correct_nodeList, hostList=environment_node)
        exec_time = datetime.now() - start_time
        if result["code"] == "0":
            self.pass_case += 1
            self.printer.ok(case, exec_time)
        else:
            self.fail_case += 1
            self.printer.error(case, exec_time)
     #test-05
    def test_add_wrongClusterId(self):
        case = "Add nodes to HA cluster with wrong cluster ID"
        self.case_counter += 1
        testRM = Recovery(test=True)
        test_clusterId = testRM.createCluster(cluster_name)["clusterId"]

        start_time = datetime.now()
        result = testRM.addNode(wrong_clusterId, correct_nodeList, hostList=environment_node)
        exec_time = datetime.now() - start_time
        if result["code"] == "1":
            self.pass_case += 1
            self.printer.ok(case, exec_time)
        else:
            self.fail_case += 1
            self.printer.error(case, exec_time)
    #test-05
    def test_add_duplicateList(self):
        case = "Add nodes to HA cluster with duplicate node list"
        self.case_counter += 1
        testRM = Recovery(test=True)
        test_clusterId = testRM.createCluster(cluster_name)["clusterId"]
        testRM.addNode(test_clusterId, correct_nodeList, hostList=environment_node)

        start_time = datetime.now()
        result = testRM.addNode(test_clusterId, duplicate_nodeList, hostList=environment_node)
        exec_time = datetime.now() - start_time
        if result["code"] == "1":
            if "overlapping node" in result["message"]:
                self.pass_case += 1
                self.printer.ok(case, exec_time)
            else:
                self.fail_case += 1
                self.printer.error(case, exec_time)
        else:
            self.fail_case += 1
            self.printer.error(case, exec_time)
    #test-05
    def test_add_wrongList(self):
        case = "Add nodes to HA cluster with wrong node list"
        self.case_counter += 1
        testRM = Recovery(test=True)
        test_clusterId = testRM.createCluster(cluster_name)["clusterId"]

        start_time = datetime.now()
        result = testRM.addNode(test_clusterId, wrong_nodeList, hostList=environment_node)
        exec_time = datetime.now() - start_time
        if result["code"] == "1":
            self.pass_case += 1
            self.printer.ok(case, exec_time)
        else:
            self.fail_case += 1
            self.printer.error(case, exec_time)

    def output_resultlog(self):
        
        Str= "test05\n"

        if self.pass_case==4:
            if self.fail_case==0:
                with open('./log/sucess.log','a') as f:
                    f.write(Str)
                    f.close()
            else:
                with open('./log/fail.log','a') as f:
                    f.write(Str)
                    f.close()           
     


def main():

    sys.stdout = open(os.path.join(cwd,"log/","test-05_%s" %(time.strftime('%Y-%m-%d-%H.%M.%S'))),'w')
	
    print "Test Start!"
   # auth_tester = TestClientAuth()
    node_tester=TestNode()
    print "------------------------------------------------------------------------------------"
    print "[HAaaS-TC-05]"
    node_tester.test_add_correctList()
    node_tester.test_add_wrongClusterId()
    node_tester.test_add_duplicateList()
    node_tester.test_add_wrongList()
    node_tester.output_resultlog()
    print "------------------------------------------------------------------------------------"

    print "Test Finish!"

    def percentage(part, whole):
        list = [node_tester.pass_case,  node_tester.fail_case]
         # return str(result) + "%"
        return list
 #   total_case = auth_tester.case_counter + cluster_tester.case_counter + node_tester.case_counter + instance_tester.case_counter
  #  pass_case = auth_tester.pass_case + cluster_tester.pass_case + node_tester.pass_case + instance_tester.pass_case
   # fail_case = auth_tester.fail_case + cluster_tester.fail_case + node_tester.fail_case + instance_tester.fail_case

   # reportTable = PrettyTable()
   # reportTable.field_names = ["Total Case", "Pass Case", "Fail Case", "Pass Rate"]
   # reportTable.add_row([total_case, pass_case, fail_case, percentage(pass_case, total_case)])
   # print
   # reportTable


if __name__ == "__main__":
    main()
