# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#!/usr/bin/env python
 

import socket
import struct

HOST = '192.168.7.2'  # The server's hostname or IP address
PORT = 6666        # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = s.recv(56)
        if not data: break
        print (data)
        # print(struct.unpack("iiiiiiihhhhhhhhhhBBBhh",data))