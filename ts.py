# import threading
# import time
# import random
# import socket

# def ts(tsListenPort):
'''
    dnsTable = [] # list of arrays [ [hostname1,ip1,flag1], [hostname1,ip1,flag1]]
    currInfo = [] # current line's info [hostname1,ip1,flag1]

    # populating the table while reading the file
        file = open('PROJI-DNSRS.txt', 'r')
        linesList = file.readlines()
        for line in linesList: # outer loop for each line
            for word in line.split(): # inner loop that reads until it hits a space, go on to the next thing
                currInfo.append(word) # (hostname,ipaddress,flag)
            dnsTable.append(currInfo)

            for i in range(3):
                print(currInfo[i], ", " , end =" ")
            print()
'''
#     try:
#         ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket (AF_INET -> IPV4 and SOCKET_STREAM -> TCP transport protocol)
#         print("[S]: Server socket created") # creating socket was successful
#     except socket.error as err: 
#         print('socket open error: {}\n'.format(err)) # creating socket was not successful
#         exit()

#     server_binding = ('', 50007)
#     ss.bind(server_binding) # bind the socket to the port we want to use (port 50007 in this case)
#     ss.listen(1) # start listening for connections (1 tells you how many connections ur allowed to have in queue)
#     host = socket.gethostname()
#     print("[S]: Server host name is {}".format(host))
#     localhost_ip = (socket.gethostbyname(host))
#     print("[S]: Server IP address is {}".format(localhost_ip))
#     csockid, addr = ss.accept()
#     print ("[S]: Got a connection request from a client at {}".format(addr))

#     # send a intro message to the client.  
#     msg = "Welcome to CS 352!"
#     csockid.send(msg.encode('utf-8'))

#     # Close the server socket
#     ss.close()
#     exit()