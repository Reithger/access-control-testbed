import socket
import time
import re
import random
import _thread

''' List of tuples (ip_address, socket) representing live connections to other entities in the network '''
LIVE_CONNECTIONS = []
''' Default port to connect to '''
TCP_PORT = 5005
''' Type of this entity in the network '''
type = 'appliance'
''' Specific id of this entity, specifying its nature '''
id = 'oven'

'''
Main function that is called after all functions are defined; top-down code structure is preferred.
'''

def main():
  sock = make_socket()
  if(not bind_socket(sock, '', 12)):
    print("Failure to bind local socket, program shutting down.")
    return

  _thread.start_new_thread(listen, (sock,))

  while True:
    numWat = random.randint(0, 0)
    numElec = random.randint(0, 200)
    message = "w:" + str(numWat) + " e:" + str(numElec)
    print("Sending message: '" + message + "' to ips:")
    for hold in LIVE_CONNECTIONS:
      conn = hold[1]
      if(send(conn, message)):
        print("  Live: " + str(hold[0]))
      else:
        print("  Dead (Removed): " + str(hold[0]))
        close_socket(conn)
        LIVE_CONNECTIONS.remove(hold)
    time.sleep(5)

'''
Defines the functionality of this program to establish a listening socket which processes
received input accordingly.
'''

def listen (sock):
  while True:
    conn, address = sock.accept()
    conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    _thread.start_new_thread(process, (conn,))

'''
Defines the response to incoming messages once a connection has been established
'''

def process(sock):
  while True:
    info, addr = sock.recvfrom(1024)
    info = info.decode().split()
    if(len(info) < 1):
      continue
    print("Received Message: " + str(info) + " from: " + str(addr))
    if(authorize(info[0])):
      if(info[1] == "who"):
        send(sock, authenticate() + " " + type + " " + id)
      elif(info[1] == "new_ip"):
        send(sock, "Received")
        for ip in info[2:]:
          new_sock = make_socket()
          if(connect_socket(new_sock, ip) and sum([1 for x in LIVE_CONNECTIONS if x[0] == ip_address]) < 1):
            LIVE_CONNECTIONS.append((ip, new_sock,))
    else:
      send(sock, "Failed Authorization, Disconnecting")
      close_socket(sock);

#-------  Generic Below  ----------------------------------------------------------------------

'''
Manage the creation of a socket; setting initial values
Returns Socket
'''

def make_socket():
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  return sock

'''
Manage the closing of a socket; calling shutdown and then closing
'''

def close_socket(sock):
  try:
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
  except:
    print("Error in Socket Closing - Potentially non-fatal")

'''
Manage the binding of a socket to listen to a defined ip address ('' for universal) at a default port with
a specified number of live connections on that socket permitted.
Returns Boolean
'''

def bind_socket(sock, ip, num_connections):
  try:
    sock.bind((ip, TCP_PORT))
    sock.listen(num_connections)
    print("Successful binding of socket to: " + ip)
    return True
  except:
    print("Failure to bind local socket to: " + ip)
    return False

'''
Manage the connecting of a socket to a defined ip address and default port
Returns Boolean
'''

def connect_socket(sock, ip):
  try:
    sock.connect((ip, TCP_PORT))
    print("Successful connection to ip: " + ip)
    return True
  except:
    print("Failure to connect to ip: " + ip)
    return False

'''
Manage the sending of a message by a defined socket
Returns Boolean
'''

def send(sock, message):
  try:
    sock.send(message.encode())
    return True
  except:
    print("Failure to send message via socket at ip: " + str(re.findall("\d+\.\d+\.\d+\.\d+", str(sock))))
    return False

'''
Authorize authentification key received from a message
Returns Boolean
'''

def authorize(info):
  return info == "auth"

'''
Generate authentification key to send with messages
Returns String
'''

def authenticate():
  return "auth"

#----------------------------------------------------------------------------------------------

main()