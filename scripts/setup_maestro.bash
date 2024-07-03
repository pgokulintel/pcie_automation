#!/bin/bash
#svos package_update
apt-get update
apt-get dist-upgrade
sudo apt-get -y install git
sudo apt-get -y install git-gui
sudo apt-get -y install git-lfs
sudo apt-get -y install gitk
sudo git config --global http.proxy http://proxy-chain.intel.com:911
sudo git config --global http.proxy http://proxy-dmz.intel.com:912
sudo git config --global https.proxy https://proxy-dmz.intel.com:912
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
export PERSPEC_VERSION=24.03.001
echo Installing $PERSPEC_VERSION, Please update this script to install any latest version
cd /root/
#[! -d maestro ] || mv maestro maestro_bp
#sudo git clone https://github.com/intel-restricted/frameworks.validation.maestro.maestro.git maestro
wget https://af01p-or-app04.devtools.intel.com/artifactory/maestro-local/Tools/svos/svos_perspec_$PERSPEC_VERSION.tar.gz
tar -pxvzf svos_perspec_$PERSPEC_VERSION.tar.gz
cd install
./perspec_svos_install.sh $PERSPEC_VERSION.tgz
#Maestro Environment setup
export MAESTRO_REPO_PATH=/root/maestro
export CADENCE_INSTALL_ROOT=/opt/cad
cd $MAESTRO_REPO_PATH
source $MAESTRO_REPO_PATH/perspec/scripts/environment/setup.env
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
export PATH=/opt/cad/perspec/$PERSPEC_VERSION/tools/perspec/bin:$PATH
export CADENCE_INSTALL_ROOT=/opt/cad
