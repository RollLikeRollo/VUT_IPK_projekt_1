#!/usr/bin/env python3.8

# //////////////////////////////
# Project no. 1
# IPK, 4th sem.
# Jan Zboril
# xzbori20
# Simple FSP client 
# //////////////////////////////

# TODO co delat, kdyz je NSP server vypnuty

import argparse
import parser
import socket as sock
import re
import sys
# ----------------------------------------------------------------------
    # Make FSP request
    # func recvall from user https://stackoverflow.com/users/7406945/zamkot 
    # at https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data
def recvall(sock):
    BUFF_SIZE = 4096
    data = bytearray()
    while True:
        packet = sock.recv(BUFF_SIZE)
        if not packet:  # Important!!
            break
        data.extend(packet)
    return data
# -----------------------------------------------------
# communication with FTP server and file manager
def FTP():
    socketFTP = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
    socket.setblocking(False)
    socketFTP.connect((address,port))
    socketFTP.sendall(request.encode())
    data = recvall(socketFTP)

    # Wrong answers from server handling
    data_split = str(data)
    data_split = data.split()
    if data_split[1].decode() == 'Success':
        pass
    elif data_split[1].decode() == 'Bad':
        sys.exit("Wrong FTP request format. Exiting.") 
    elif data_split[1].decode() == 'Not':
        sys.exit("File could not have been found. Exiting.") 
    elif data_split[1].decode() == 'Server':
        sys.exit("Other server error occured. Exiting.") 

    # formatting output - deleting HTTP header
    data = re.sub(b'^FSP/1.0 Success\r\n',b'',data)
    data = re.sub(b'^.*\r\n\r\n',b'',data)

    # writing into new local file
    file_name = re.search('[\w.]*$', file_path)
    file_name = file_name.group(0)
    f = open(file_name, "wb")
    f.write(data)
    f.close()

    # TODO make all files in folder work
#---------------------------------------------------

# ----------------------------
# CLI argument parsing
parser = argparse.ArgumentParser(description='Simple FSP client')
parser.add_argument('-n', metavar='name_server', type=str, required=True,
                    help="Nameserver's IP address and port number")
parser.add_argument('-f', metavar='surl', type=str, required=True,
                    help="SURL of file designated to be downloaded. Protocol have to be FSP")

args = parser.parse_args()

# checking input address
v = vars(args)
name_server = str(v["f"])
surl = str(v["n"])

surl_IP = re.search('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',surl)
surl_PORT = re.search('\:[0-9]{1,5}$', surl)
surl_PORT = re.search('[0-9]{1,5}$', surl)

if surl_IP is None:
    sys.exit("Input IP address has wrong format. Exiting.")  
if surl_PORT is None: 
    sys.exit("Input Port Number has wrong format. Exiting.") 

# print(surl_PORT.group(0))
# print(surl_IP.group(0))

# regex match to string
surl_IP = surl_IP.group(0)
surl_PORT = surl_PORT.group(0)
surl_PORT = int(surl_PORT)

# name_server_name = re.search('^fsp://[a-zA-Z._-]+', name_server)
name_server_name = re.search('\/\/[a-zA-Z._-]+', name_server)

if name_server_name is None: 
    sys.exit("Input Name Server has wrong format. Exiting.") 

name_server_name = name_server_name.group(0)
name_server_name = re.search('[a-zA-Z._-]+', name_server_name)
name_server_name = str(name_server_name.group(0))
to_send = "WHEREIS " + name_server_name
to_send = str(to_send)

# ----------------------------------------------------------------------
# Sending request to NSP server
socket = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
socket.connect((surl_IP,surl_PORT))
socket.sendall(to_send.encode())
NSP_answer = socket.recv(4096)

NSP_answer = str(NSP_answer.decode())
NSP_answer = NSP_answer.split()
if NSP_answer[0] == 'OK':
    # print(NSP_answer[1])
    pass
elif NSP_answer[1] == 'Not':
    sys.exit("Domain Name does not exist. Exiting.") 
else:
    sys.exit("Wrong NSP request format.") 

# if NSP request success
# Address formatting and request making
NSP_answer_string = str(NSP_answer[1])
address = re.search('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',NSP_answer_string)
address = address.group(0)
port = re.search('[0-9]{1,7}$', NSP_answer_string)
port = port.group(0)
port = int(port)

# re.sub(regex_search_term, regex_replacement, text_before)
file_path = re.sub('^fsp:\/\/[a-zA-Z._-]+\/','',name_server)
request = "GET " + file_path + " FSP/1.0\r\n"
request += "Hostname: " + name_server_name + "\r\n"
request += "Agent: xzbori20\r\n\r\n"

# download all files from server
download_all = False
if(file_path == '*'):
    download_all = True
    file_path = re.sub('^fsp:\/\/[a-zA-Z._-]+\/','',name_server)
    request = "GET " + "index" + " FSP/1.0\r\n"
    request += "Hostname: " + name_server_name + "\r\n"
    request += "Agent: xzbori20\r\n\r\n"
    FTP()
else: 
    FTP()
