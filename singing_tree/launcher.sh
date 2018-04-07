#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/singing_tree
sudo python singing_tree_0_2.py
cd /

