sudo yum -y groupinstall "Development Tools"
curl -o ./Python-3.9.15.tgz https://www.python.org/ftp/python/3.9.15/Python-3.9.15.tgz
tar xvf Python-3.9.15.tgz
cd Python-*/
./configure --enable-optimizations
sudo make altinstall

add to path
/usr/local/bin
source .bash_profile