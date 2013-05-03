#!/usr/bin/python
##
## Corosync/Pacemaker cluster monitor for Ganeti
## 
## (c) 2013 Giuseppe Paterno' <gpaterno@gpaterno.com>
##
## This is pre-alpha software, use at your own risk.
## After using this code, my cousin eat a banana split and 
## an hot dog and he sat in the toilet for two days.
##

import sys
import os
import re
import subprocess
import logging
import time

## Global variable
NODES = dict()

##
## This routine parses corosync crm status
## and return a dict with the status of the nodes
##

def getCorosyncNodeStatus():
   cmd = subprocess.Popen(["crm", "status"], stdout=subprocess.PIPE)
   cluster_status = cmd.communicate()[0]


   online_regex  = re.compile("Online:\s+\[(.*)\]", re.MULTILINE)
   offline_regex = re.compile("OFFLINE:\s+\[(.*)\]", re.MULTILINE)
   standby_regex = re.compile("Node\s+(\w+): standby", re.MULTILINE)
   offline_standby_regex = re.compile("Node\s+(\w+): OFFLINE \(standby\)", re.MULTILINE)

   online_list_nodes = online_regex.search(cluster_status)
   offline_list_nodes = offline_regex.search(cluster_status)
   offline_standby_list_nodes = offline_standby_regex.search(cluster_status)
   standby_list_nodes = standby_regex.search(cluster_status)

   if online_list_nodes != None:
      for node in re.split("\s+", online_list_nodes.group(1).strip()):
         NODES[node] = 'online'
         logging.debug("Node %s is online" % node)

   if standby_list_nodes != None:
      for node in re.split("\s+", standby_list_nodes.group(1).strip()):
         NODES[node] = 'standby'
         logging.debug("Node %s is in standby" % node)

   if offline_list_nodes != None:
      for node in re.split("\s+", offline_list_nodes.group(1).strip()):
         NODES[node] = 'offline'
         logging.debug("Node %s is offline" % node)

   if offline_standby_list_nodes != None:
      for node in re.split("\s+", offline_standby_list_nodes.group(1).strip()):
         NODES[node] = 'offline'
         logging.debug("Node %s is offline and standby" % node)




## Main routine
if __name__ == '__main__':
   logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG)

   while True:
      getCorosyncNodeStatus()
      time.sleep(30)
