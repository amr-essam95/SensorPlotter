import socket
import struct
import random
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 6666        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    timeStamp = 0
    timeStampNano = 0
    with conn:
        print('Connected by', addr)
        while True:
            # data = conn.recv(1024)
            # # print("received data {}".format(data))
            # if not data:
            #     continue
            # rcvStruct = struct.unpack("?BB?100HHH",data)
            # print (rcvStruct)
            # # print (struct.calcsize("?BB?100HHH"))
            # print("Finished Parsing.\n\n")
            # time.sleep(2)
            time.sleep(10/1000)

            
            timeStampNano = timeStampNano + 10000000
            if timeStampNano > (1E9):
                timeStampNano = 0
                timeStamp = timeStamp + 1

            rsAngle = random.randint(0,36000)
            lsAngle = random.randint(0,36000)
            rtAngle = random.randint(0,36000)
            ltAngle = random.randint(0,36000)
            trunkAngle = random.randint(0,36000)
            rmEnc = 7644
            lmEnc = 7644
            # rmCurrentReadout = random.randint(0,65535)
            # lmCurrentReadout = random.randint(0,65535)
            # rmCurrentSent = random.randint(0,65535)
            # lmCurrentSent = random.randint(0,65535)
            rmCurrentReadout = random.randint(0,30000)
            lmCurrentReadout = random.randint(0,30000)
            rmCurrentSent = random.randint(0,30000)
            lmCurrentSent = random.randint(0,30000)
            # analog0 = random.randint(0,65535)
            # analog1 = random.randint(0,65535)
            # analog2 = random.randint(0,65535)
            # analog3 = random.randint(0,65535)
            analog0 = random.randint(0,30000)
            analog1 = random.randint(0,30000)
            analog2 = random.randint(0,30000)
            analog3 = random.randint(0,30000)
            syncIn = random.randint(0,1)
            syncOut = random.randint(0,1)
            usrButton = random.randint(0,1)
            leftEnable = random.randint(0,1)
            rightEnable = random.randint(0,1)
            dummy1 = 0
            dummy2 = 0

            # structData = struct.pack('iiiiiiihhHHHHHHHHBBBhhhh', timeStamp, timeStampNano, rsAngle, lsAngle, rtAngle, ltAngle, trunkAngle, rmEnc, lmEnc, rmCurrentReadout, lmCurrentReadout, rmCurrentSent, lmCurrentSent, analog0, analog1, analog2, analog3, syncIn, syncOut, usrButton, leftEnable, rightEnable, dummy1, dummy2)
            structData = struct.pack('iiiiiiihhHHHHHHHHBBBhh', timeStamp, timeStampNano, rsAngle, lsAngle, rtAngle, ltAngle, trunkAngle, rmEnc, lmEnc, rmCurrentReadout, lmCurrentReadout, rmCurrentSent, lmCurrentSent, analog0, analog1, analog2, analog3, syncIn, syncOut, usrButton, leftEnable, rightEnable)
            print("/n")
            print (len(structData))
            print(structData)
            print("/n")
            conn.sendall(structData)