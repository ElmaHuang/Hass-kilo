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
# sys.stdout = open(os.path.join(cwd,"log/","test-01_%s" %(time.strftime('%Y-%m-%d-%H.%M.%S'))),'w')


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
        #self.sucessNo=0
        self.OK = '\033[92m' + "PASS!" + '\033[0m'
        self.ERROR = '\033[91m' + "FAIL!" + '\033[0m'


    def ok(self, case, time):
        print case + "(" + str(time.microseconds) + "ms) : " + self.OK
        #self.sucess+=1

    def error(self, case, time):
        print case + "(execution time:" + str(time.microseconds) + "ms) : " + self.ERROR

class TestClientAuth():
    def __init__(self):
        self.printer = ShowResult()
        self.clientUrl = "127.0.0.1:" + listen_port
        self.case_counter = 0
        self.pass_case = 0
        self.fail_case = 0

    def test_correctAuth(self):
        case = "Authenticate client with correct username and password"
        self.case_counter += 1
        start_time = datetime.now()
        server = xmlrpclib.ServerProxy(correct_auth)
        try:
            resp = server.test_auth_response()
            exec_time = datetime.now() - start_time
            if resp == "auth success":
                self.pass_case += 1
                self.printer.ok(case, exec_time)
            else:
                self.fail_case += 1
                self.printer.error(case, exec_time)

        except xmlrpclib.ProtocolError:
            exec_time = datetime.now() - start_time
            self.fail_case += 1
            self.printer.error(case, exec_time)

    def test_wrongAuth(self):
        case = "Authenticate client with wrong username and password"
        self.case_counter += 1
        start_time = datetime.now()
        server = xmlrpclib.ServerProxy(wrong_auth)

        try:
            server.test_auth_response()
            exec_time = datetime.now() - start_time
            self.fail_case += 1
            self.printer.error(case, exec_time)
        except xmlrpclib.ProtocolError:
            exec_time = datetime.now() - start_time
            self.pass_case += 1
            self.printer.ok(case, exec_time)

    def test_withoutAuth(self):
        case = "Authenticate client without username and password"
        self.case_counter += 1
        start_time = datetime.now()
        server = xmlrpclib.ServerProxy(no_auth)

        try:
            server.test_auth_response()
            exec_time = datetime.now() - start_time
            self.fail_case += 1
            self.printer.error(case, exec_time)
        except xmlrpclib.ProtocolError:
            exec_time = datetime.now() - start_time
            self.pass_case += 1
            self.printer.ok(case, exec_time)

    def output_resultlog(self):
        Str= "test01\n"

        if self.pass_case==3:
            if self.fail_case==0:
                with open('./log/sucess.log','a') as f:
                    f.write(Str)
                    f.close()
            else:
                with open('./log/fail.log','a') as f:
                    f.write(Str)
                    f.close()           


def main():

    sys.stdout = open(os.path.join(cwd, "log/", "test-01_%s" % (time.strftime('%Y-%m-%d-%H.%M.%S'))), 'w')

    print "Test Start!"
    auth_tester = TestClientAuth()
    print "------------------------------------------------------------------------------------"
    print "[HAaaS-TC-01]"
    auth_tester.test_correctAuth()
    auth_tester.test_wrongAuth()
    auth_tester.test_withoutAuth()
    auth_tester.output_resultlog()
    print "------------------------------------------------------------------------------------"

    print "Test Finish!"


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