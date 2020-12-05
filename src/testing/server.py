import socket
import struct
import random

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 6666        # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            # print("received data {}".format(data))
            if not data:
                continue
            print(struct.unpack("?BB?100HHH",data))
            print("Finished Parsing.\n\n")

            timeStamp = 10
            timeStampNano = 10
            rsAngle = 18000
            lsAngle = 24000
            rtAngle = 5000
            ltAngle = 7000
            trunkAngle = 12000
            rmEnc = 7644
            lmEnc = 7644
            rmCurrentReadout = 2000
            lmCurrentReadout = 3000
            rmCurrentSent = 5000
            lmCurrentSent = 6000
            analog0 = 10000
            analog1 = 20000
            analog2 = 40000
            analog3 = 60000
            syncIn = random.randint(0,1)
            syncOut = random.randint(0,1)
            usrButton = random.randint(0,1)
            leftEnable = random.randint(0,1)
            rightEnable = random.randint(0,1)
            dummy1 = 0
            dummy2 = 0

            structData = struct.pack('iiiiiiihhhhhhHHHHBBBhhhh', timeStamp, timeStampNano, rsAngle, lsAngle, rtAngle, ltAngle, trunkAngle, rmEnc, lmEnc, rmCurrentReadout, lmCurrentReadout, rmCurrentSent, lmCurrentSent, analog0, analog1, analog2, analog3, syncIn, syncOut, usrButton, leftEnable, rightEnable, dummy1, dummy2)

            conn.sendall(structData)