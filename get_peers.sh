#! /bin/bash
sudo arp-scan -l --interface=wlp2s0 | grep -E "([0-9]{1,3}\.){3}[0-9]{1,3}"	 |cut -d$'\t' -f1,2 > peers.txt
python p2p.py