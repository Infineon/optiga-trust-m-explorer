#!/bin/sh

FILE="0001-trust_m_lib.patch"
LINUX_TOOLS_PATH="Python_TrustM_GUI/linux-optiga-trust-m/"
TRUSTM_LIB_PATH="${LINUX_TOOLS_PATH}trustm_lib/"
CURRENT_DIR="${PWD}"
AWS_DIR_PATH="Python_TrustM_GUI/aws_trustm/sample_apps/eHealthTrustM/"
PATCH="${PWD}/${FILE}"


sudo apt update 
sudo apt -y install awscli git gcc libssl-dev python-wxtools
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

cd $CURRENT_DIR
cd $AWS_DIR_PATH
architecture=$(dpkg --print-architecture)
echo "System architecture: $architecture"
# Check if the architecture is 64-bit or 32-bit
if [ "$architecture" = "armhf" ];
then
    cp eHealthDevice_32 $CURRENT_DIR/Python_TrustM_GUI/eHealthDevice 
else
    cp eHealthDevice $CURRENT_DIR/Python_TrustM_GUI/eHealthDevice 
fi

#~cd $CURRENT_DIR
echo "-----> Installation completed. Back to ${PWD}"



