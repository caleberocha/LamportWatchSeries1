#!/bin/bash
# You need to copy the supernode and edge executables (https://github.com/ntop/n2n) to the user directory (/home/ec2_user) before running this 

err_report() {
    echo "Error on line $1"
    exit 1
}

trap 'err_report $LINENO' ERR

REPO=https://github.com/caleberocha/LamportWatchSeries1.git
HOSTS="172.31.89.166 172.31.87.254 172.31.81.175 172.31.83.104 172.31.93.72"
VHOSTS="192.168.1.1 192.168.1.2 192.168.1.3 192.168.1.4 192.168.1.5"
SUPERNODE=172.31.89.166:1200

HOST_IDX=0
for h in $HOSTS 00000000; do
  HOST_IDX=$(($HOST_IDX+1))
  ip addr | grep $h/ >/dev/null && break
done
if [ $HOST_IDX -eq 6 ]; then
  echo "Host not found"
  exit 1
fi


chmod 755 edge

if [ $HOST_IDX -eq 1 ]; then
  echo "Starting supernode"
  chmod 755 supernode
  pgrep supernode >/dev/null || ./supernode -l 1200 &
fi

echo "Checking packages"
which python3 >/dev/null || sudo yum install python3 -y
which git >/dev/null || sudo yum install git -y

echo "Cloning repository"
git clone $REPO || echo "Repository already exists" >&2

echo "Setting config"
echo "$HOSTS" | awk '{for(i=1;i<=NF;i++) print i,$i,50000,0.2}' >LamportWatchSeries1/config.txt

ip link del edge0 || echo "edge0 not found, creating" >&2
./edge -l $SUPERNODE -c pd -a 192.168.1.$HOST_IDX -d edge0 -E
route add -net 224.0.0.0 netmask 240.0.0.0 dev edge0

chmod 755 -R LamportWatchSeries1
cd LamportWatchSeries1

clear
echo "python3 run.py config.txt $HOST_IDX"
python3 run.py config.txt $HOST_IDX
