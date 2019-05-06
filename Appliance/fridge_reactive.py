import socket
import time
import random
import subprocess
import re

UDP_IP = "0.0.0.0"
UDP_PORT = 5005
id = 'appliance'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

while True:
  data, addr = sock.recvfrom(1024)  #let's pretend the format is: [type], [request], [information list]
  components = data.split()
  #some kind of verification
  switch(components[0]):
    case 'arbiter':
      switch(components[1]):
        case 'new_ip':
          for x in range(2, len(components)):
            os.environ['ips'] = os.environ['ips'] + ' ' + x
        case 'remove_ip':
          ip_list = os.environ['ips'].split()
          for x in range(2, len(components)):
            ip_list.remove(x)
          new_ips = ''
          for x in ip_list:
            new_ips += ' ' + x
          os.environ['ips'] = new_ips