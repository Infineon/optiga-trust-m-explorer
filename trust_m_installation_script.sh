#!/bin/sh

FILE="0001-trust_m_lib.patch"
LINUX_TOOLS_PATH="Python_TrustM_GUI/linux-optiga-trust-m/"
TRUSTM_LIB_PATH="${LINUX_TOOLS_PATH}trustm_lib/"
CURRENT_DIR="${PWD}"
PATCH="${PWD}/${FILE}"


sudo apt update 
sudo apt -y install awscli git gcc libssl-dev python-wxtools python3-pubsub
pip install PyPubSub

echo $PATCH
echo $TRUSTM_LIB_PATH
echo $LINUX_TOOLS_PATH

cp $PATCH $LINUX_TOOLS_PATH
cd $LINUX_TOOLS_PATH
echo "-----> Entering ${PWD}"
git apply $FILE
rm $FILE
set -e
echo "-----> Build Trust M Linux Tools"
sudo make uninstall
make -j5
sudo make install
echo "-----> Build Protected Update Set tool"
cd ex_protected_update_data_set/Linux/
make clean
make -j5
sudo make install
 
#~cd $CURRENT_DIR
echo "-----> Installation completed. Back to ${PWD}"



