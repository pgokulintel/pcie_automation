#*********************************************************************************************#
#                                PCIe Automation                                              #
#            This script automate PCIe Tests based on Test Suite, Test line                   #
#*********************************************************************************************#

# importing libraries
import xml.etree.ElementTree as ET
import sys
import argparse
from xml.dom.minidom import parse, parseString
import subprocess
import os
import platform

def runCommand(command):
    """
    Prints and then runs shell command.
    """
    print(f'> running: {command}')
    stream = subprocess.Popen(command, shell=True,env=os.environ)
    (result_data, result_error) = stream.communicate()
    print(f'{result_data}, {result_error}')

# Prerequisite scripts
svos_prerequisite ='''#svos package_update
apt-get update
apt-get dist-upgrade
sudo apt-get -y install git
sudo apt-get -y install git-gui
sudo apt-get -y install git-lfs
sudo apt-get -y install gitk
sudo git config --global http.proxy http://proxy-chain.intel.com:911
sudo git lfs install
sudo apt-get install kate
sudo apt-get -y install gdb
sudo apt-get -y install git-gui
sudo apt-get -y install meld
apt-get install -y libtornado-dev libsv-dev python3-distutils osv-tornado-solarlib-dev libgecode49 libgecodegist49 libgecode-dev
apt-get install -y libospm-dev
apt-get install -y libparse-dev
apt-get install -y libmedpg-dev
apt-get install -y libnetlib-dev
sudo apt-get install -y bison
sudo apt-get install -y build-essential cmake
#Perspec setup
cd /root/
[! -d maestro ] || mv maestro maestro_bp
sudo git clone https://github.com/intel-restricted/frameworks.validation.maestro.maestro.git maestro
wget http://ubit-artifactory-or.intel.com/artifactory/maestro-local/Tools/svos/svos_perspec_<svos_perspec_ver>.tar.gz
tar -pxvzf <svos_perspec_ver>.tar.gz
cd install
./perspec_svos_install.sh <svos_perspec_ver>
#Maestro Environment setup
export $MAESTRO_REPO_PATH=/root/maestro
export CADENCE_INSTALL_ROOT=/opt/cad
cd $MAESTRO_REPO_PATH
source $MAESTRO_REPO_PATH/perspec/scripts/environment/setup.env
export PERSPEC_VERSION=<svos_perspec_ver>
#unsetenv CDS_LIC_FILE
export CDS_LIC_FILE=5280@cadence03p.elic.intel.com:5280@cadence20p.elic.intel.com
#compilation setup
export CONTENT_TYPE=LINUX
export SITECODE=il
#git checkout integration
#source ./utils/setup.env
#git setup
git config --global diff.tool meld
git config --global merge.tool meld
git config --global --add difftool.prompt false	
export PATH=/opt/cad/perspec/21.09.001-s/tools/perspec/bin:$PATH
export CADENCE_INSTALL_ROOT=/opt/cad
'''

# Class for Perspec

class PerspecTestLine:
  def __init__(self):
    self.maestro_home            = '$MAESTRO_REPO_PATH'
    self.psf_path                = '$MAESTRO_REPO_PATH/perspec/targets/adl_sil/'
    self.ps_test_path            = '$MAESTRO_REPO_PATH/perspec/targets/adl_sil/models/pcie/tests/'
    self.pcie_num_ctrls          = 1
    self.content_regression_flag = 'TRUE'
    self.f                       = self.psf_path+'adl_sil_tornado.psf'
    self.pcie_ctrl               = 'PEG10'
    self.pcie_test_ctrls         = 'PEG10'
    self.sln                     = self.ps_test_path+'liad_tc.sln'
    self.top_action              = 'pcie_aspm_pre_link_speed_L1_1_EP_EXIT_Gen4'
    #self.csv_name                = 'liad_test_table.csv'
    #self.table_name              = 'pcie_aspm_pre_link_speed'
    self.generate_test_table     = self.ps_test_path+'liad_test_table.csv'+'::'+'pcie_aspm_pre_link_speed'
    self.ps_cmd                  = None

  def set_generate_test_table(self, csv_name, table_name):
    self.generate_test_table     = self.ps_test_path+csv_name+'::'+table_name

  def set_sln(self,sln_name):
    self.sln                     = self.ps_test_path+sln_name

  def set_content_regression_flag(self,crf):
    self.content_regression_flag = crf

  def set_top_action(self, top_action):
    self.top_action = top_action

  def  set_pcie_ctrl(self, pcie_ctrl):
    self.pcie_ctrl               = pcie_ctrl
    self.pcie_test_ctrls         = pcie_ctrl

  def get_ps_cmd(self):
    self.ps_cmd = 'perspec generate -define PCIE_NUM_CTRLS {0} -define PCIE_TEST_CTRL {1} -define CONTENT_REGRESSION_FLAG {2} -define PCIE_TEST_CTRLS {3} -f {4} -sln {5}\
    -top_action {6} -generate_test_table {7} -target_dir {8}'.format(self.pcie_num_ctrls, self.pcie_test_ctrls, self.content_regression_flag, self.pcie_test_ctrls,\
                                                    self.f, self.sln, self.top_action, self.generate_test_table, self.top_action)
    self.ps_cmd1 ='MAESTRO_FRAMEWORK=UNIFIED CONTENT_TYPE=LINUX DEBUG=TRUE make -Bj TAGS=skl.qa -C ./{0}'.format(self.top_action)
    self.ps_cmd2 = '$MAESTRO_REPO_PATH/build/content/linux/root/maestro/{0}/{1}'.format(self.top_action, self.top_action)
    return [self.ps_cmd,self.ps_cmd1,self.ps_cmd2]

  def prerequisite(self):
    printf('Not implemented')
	
  def package_update(self,svos_perspec_version = None):
    #print(svos_prerequisite)
    svos_prereq = svos_prerequisite.replace("<svos_perspec_ver>",svos_perspec_version)
    with open('./svos_setup.bash','w') as rsh:
        rsh.write('#!/bin/bash\n')
        rsh.write(svos_prereq)
    print('prerequisite shell script AutoGenerated : Please run the cmd ''source svos_prerequsite.bash''')
    #runCommand(svos_prerequisite)

    #subprocess.Popen('/root/maestro/perspec/scripts/environment/setup.env /root/maestro')
#    print('Generated svos_setup.bash, please run source ./svos_setup.bash')
# Class for PCIe Automation

class PCIeAutomation():
  def __init__(self):
    self.args = None
    self.run_testlines     = []
    self.run_testsuites    = []
    self.prereq            = []
    self.vt_framework      = 'perspec'
    self.root              = None
    self.tree              = None
    self.ps_tstline        = None
    self.exec              = "yes"
    self.rp                = ["PEG10"]
    self.speed             = ["4"]
    self.linkwidth         = ["8"]
    self.parse_init_done   = self.parser_init()
    
  def parser_init(self):

    # Argument Parser
    parser = argparse.ArgumentParser(description='Perspec Argument Parser')
    # Add arguments
    parser.add_argument('--xml', dest='xml', type=str, help='xml Names of tests')
    parser.add_argument('--testgroup', dest='testgroup', type=str, help='PCIe Test Group (Set of Test Suite)')
    parser.add_argument('--testsuite', dest='testsuite', type=str, help='PCIe Test Suite (Set of Test lines)')
    parser.add_argument('--testline', dest='testline', type=str, help='PCIe Test lines')
    parser.add_argument('--prerequisite', dest='prerequisite', type=str, help='PCIe Tests prerequisite')
    parser.add_argument('--print', dest='print', type=str, help='Print all PCie tests details')
    parser.add_argument('--speed', dest='speed', type=str, help='Provide PCIe Gen speed (1,2,3,4,5)')
    parser.add_argument('--linkwidth', dest='linkwidth', type=str, help='Provide PCIe Linkwidth')
    parser.add_argument('--rp', dest='rp', type=str, help='Provide PCIe Root Port Name')
    parser.add_argument('--execute', dest='execute', type=str, help='Control Execution')
    #parser.add_argument('--help', dest='help', type=str, help='Usage')

    self.args = parser.parse_args()
    
    # Default Values if arguments not passed
    if(self.args.xml == None):
      self.inFile='vt_pcie.xml' # Default xml file
      #print('XML File not Providing, Taking Default one : {0}'.format(self.inFile))
    else:
      self.inFile = self.args.xml
    if(self.args.testline != None):
      self.run_testlines = self.args.testline.split(',')
    if(self.args.testsuite != None):
      self.run_testsuites = self.args.testsuite.split(',')
    if(self.args.prerequisite != None):
        self.prereq = self.args.prerequisite.split(',')
    if(self.args.speed != None):
      self.speed = self.args.speed.split(',')
    if(self.args.prerequisite != None):
      self.linkwidth = self.args.linkwidth.split(',')
    if(self.args.rp != None):
      self.rp = self.args.rp.split(',')
    if(self.args.execute != None):
       if(self.args.execute == "No" or self.args.execute == "no" or self.args.execute == "NO"):
          self.exec   = "no"
       print(self.args.execute)
       print(self.exec)

    return 1
    
  def print_all_registered_tests(self):

    self.group = self.get_xml_tree().getroot()
    nts = 0
    ntl = 0
    for suite in self.group:
      nts = nts +1
      for line in suite:
        ntl = ntl + 1
    print("************************************************************************")
    print("Printing all Registered Tests...from {0}".format(self.inFile))
    print("Found {0} Test Suites, {1} Test Lines".format(nts, ntl))
    print('Group Name : ' + self.group.get('name'))
    for suite in self.group:
      print('  Suite Name :' + suite.get('name'))
      print('    TestLine Name :')
      for line in suite:
        print('      '+line.get('name')),
    print("************************************************************************")

  def perspec_execute(self):
      #************************* perspec commands **************************#
      output = ''
      
      self.group = self.get_xml_tree().getroot()
      # Extract from xml to ps_tstline and run
      self.ps_tstline = PerspecTestLine()
      #print("************************************************************************")
      cnt=0
      k=0
      with open('perspec_tests.sh', 'w') as f:
        f.write('#!/bin/bash\n')
        for suite in self.group:
          for line in suite:
            if(len(self.run_testsuites) != 0):
              if suite.get('name') not in self.run_testsuites:
                continue
            if(line.get('skip') == 'true'):
              continue
            if(line.get('name') == "svos_config"):
              #print('Prerequisite : {0}'.format(str(self.prereq)))
              ps = PerspecTestLine()
              ps.package_update(svos_perspec_version=line.find('svos_perspec_ver').text)
              continue                  
            for rp in self.rp:
              if(rp not in line.get('name')):
                continue
              else:
                for speed in self.speed:
                  for lw in self.linkwidth:
                    cnt=cnt+1
                    self.ps_tstline.set_generate_test_table(line.find('csv_name').text+'.csv',line.find('table_name').text)
                    self.ps_tstline.set_sln(line.find('sln_name').text+'.sln')
                    self.ps_tstline.set_top_action(line.find('action').text)
                    self.ps_tstline.set_pcie_ctrl(line.find('ctlr').text)

                    [psgenerate,pscompile,psexecute] = self.ps_tstline.get_ps_cmd()  
                    f.write("\necho \"{0}.Running {1}.{2}...\"\n".format(cnt,suite.get('name'),line.get('name')))
                    f.write("echo \"Parameters: {0}, {1}, {2}, {3}\n\"".format(line.find('ctlr').text,line.find('action').text,
                                                                         line.find('table_name').text, line.find('csv_name').text,
                                                                         line.find('sln_name').text))
                    f.write('\n'+psgenerate+'\n')                 
                    f.write(pscompile+'\n')
                    f.write(psexecute+'\n')
                    f.write('echo \"Completed\"'+'\n')

                    if(self.exec == "yes"):
                      if(platform.system() == 'Windows'):
                          k=k+1
                          if(k==1):
                              print('Perspec test can be run on Linux...')
                          continue
                      # create perspec command and Execute
                      print("Running {0}.{1}...".format(suite.get('name'),line.get('name')))
                      print("Parameters: {0}, {1}, {2}, {3}".format(line.find('ctlr').text,line.find('action').text,
                                                                    line.find('table_name').text, line.find('csv_name').text,
                                                                    line.find('sln_name').text))
                                         
                      #Enable below lines while executing the command
                      #temp = subprocess.Popen('dir')
                      #output.join(str(temp.communicate()))
                      temp = subprocess.Popen(psgenerate,stdout = subprocess.PIPE, shell=True)
                      output.join(str(temp.communicate()))
                      temp = subprocess.Popen(pscompile, stdout = subprocess.PIPE, shell=True)
                      output.join(str(temp.communicate()))
                      temp = subprocess.Popen(psexecute, stdout = subprocess.PIPE, shell=True)
                      output.join(str(temp.communicate()))
                      print('Completed.\n')
                      output = output.split("\n")
                      output = output[0].split('\\')
                      res = []
                      for line in output:
                        res.append(line)
                      
                      # print the output
                      for i in range(1, len(res) - 1):
                        print(res[i])
                        return res
                    
  def get_xml_tree(self):
    #************************* XML Parser **************************#
    return ET.parse(self.inFile)

    # Parsing XML Test Lines to create Perspec Command
    #- Execute Perspec Test Lines
  def execute(self):
#    self.parse_xml()
    if(self.vt_framework == 'perspec'):
      self.perspec_execute()
    elif (self.vt_framework) == 'osbv':
      print('yet to Implemented')

  #for country in root.findall('pcie_automation'):
  #  print(country)
  #  rank = country.find('pcie_sln_name').text
  #  name = country.get('name')
  #  print(name, rank)

  def prerequisite(self):
    if('tornadosetup' in self.prereq):
      print('Running tornadosetup')
      subprocess.Popen(psgenerateself.ps_tornadosetup)
      
def main():
    print("************************************************************************")
    print("*                       PCIe Automation Ver 1.0                        *")
    print("*    (Developed by iVE CVI PCIe Team for standalone Regression)        *")
    print("************************************************************************")
    PCIeauto = PCIeAutomation()
    PCIeauto.print_all_registered_tests()
    PCIeauto.execute()  
  
# Using the special variable 
# __name__
if __name__=="__main__":
    main()
