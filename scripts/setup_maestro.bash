#!/bin/bash
#svos package_update
echo "This Setup script to update all the required package to install Maestro and Perspec and set environment Variables"

#Perspec setup
PERSPEC_VERSION=24.03.001

#Proxy Settings
sudo git config --global http.proxy http://proxy-chain.intel.com:911
sudo git config --global http.proxy http://proxy-dmz.intel.com:912
sudo git config --global https.proxy https://proxy-dmz.intel.com:912
export http_proxy=http://proxy-dmz.intel.com:911
export https_proxy=http://proxy-dmz.intel.com:912
export ftp_proxy=http://proxy-dmz.intel.com:911
export socks_proxy=http://proxy-us.intel.com:1080
export no_proxy=intel.com,.intel.com,localhost,127.0.0.1,10.0.0.0/8,192.168.0.0/16,172.16.0.0/12
export MAESTRO_REPO_PATH=/root/maestro

#Install Packages
apt-get update
apt-get dist-upgrade
sudo apt-get -y install git
sudo apt-get -y install git-gui
sudo apt-get -y install git-lfs
sudo apt-get -y install gitk
sudo git lfs install
sudo apt-get install kate
sudo apt-get -y install gdb
sudo apt-get -y install git-gui
sudo apt-get -y install meld
apt-get install -y libtornado-dev libsv-dev librocket-dev python3-distutils osv-tornado-solarlib-dev libgecode49 libgecodegist49 libgecode-dev
apt-get install -y libospm-dev
apt-get install -y libparse-dev
apt-get install -y libmedpg-dev
apt-get install -y libnetlib-dev
sudo apt-get install -y bison
sudo apt-get install -y build-essential cmake
apt install -y acpica-tools apt-file apt-utils autoconf autogen automake autotools-dev bc bison cmake csh curl debhelper dh-acc dnsutils doxygen dpkg-repack expect g++ gcc gdb git git-lfs htop kmod ksh libelf-dev libgecode-dev libmedpg-dev libncurses5-dev libnetlib-dev libospm-dev libparse-dev libpci-dev libpcietc-dev librocket-dev libsv-dev libtool libtornado-dev lsb-release lshw lsof make man nano ncdu ninja-build osv-scc osv-hostsmanager osv-tornado-solarlib-dev parted pcietctests python3-distutils python3-full python3-pip python3-virtualenv ripgrep rsync software-properties-common svdefs-modules-dev svos-pcie svos-pcietcrand svos-prerelease-kernel-headers svos-released-kernel-headers svos-released-kernels tldr traceroute tree ucf-modules-dev valgrind vim wget zip
apt install libpcietc-datagen-dev libpcietc-dev

cd /root/
# prompting for choice
read -p "Do you want to install Maestro. (y)Yes/(n)No :- " choice
# giving choices there tasks using
case $choice in
[yY]* )
echo "Installing Maestro... if maestro folder is there moving as backup" 
[! -d maestro ] || mv maestro maestro_bp
sudo git clone https://github.com/intel-restricted/frameworks.validation.maestro.maestro.git maestro ;;
[nN]* ) echo "Maestro Not installed" ;;
*) exit ;;
esac
# prompting for choice
read -p "Do you want to install Perspec. (y)Yes/(n)No :- " choice
# giving choices there tasks using
case $choice in
[yY]* )
echo "Installing $PERSPEC_VERSION, Please update this script to install any latest version"
wget https://af01p-or-app04.devtools.intel.com/artifactory/maestro-local/Tools/svos/svos_perspec_$PERSPEC_VERSION.tar.gz
tar -pxvzf svos_perspec_$PERSPEC_VERSION.tar.gz
cd install
./perspec_svos_install.sh $PERSPEC_VERSION.tgz ;;
[nN]* ) echo "Perspec Not installed" ;;
*) exit ;;
esac
export PERSPEC_VERSION=$PERSPEC_VERSION
export CADENCE_INSTALL_ROOT=/opt/cad
#unsetenv CDS_LIC_FILE
export CDS_LIC_FILE=5280@cadence03p.elic.intel.com:5280@cadence20p.elic.intel.com
#compilation setup
export CONTENT_TYPE=LINUX
export SITECODE=il
export PATH=/opt/cad/perspec/$PERSPEC_VERSION/tools/perspec/bin:$PATH
export CADENCE_INSTALL_ROOT=/opt/cad

#git checkout integration
#source ./utils/setup.env
#git setup
git config --global diff.tool meld
git config --global merge.tool meld
git config --global --add difftool.prompt false
#Maestro Environment setup
cd $MAESTRO_REPO_PATH
bash
source $MAESTRO_REPO_PATH/perspec/scripts/environment/setup.env
