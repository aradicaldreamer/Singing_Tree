#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/singing_tree
sudo python singing_tree_0_3.py
cd /


# Add this shell script to /etc/rc.local to run the program at startup like this
# sudo bash /home/pi/singing_tree/launcher.sh &
