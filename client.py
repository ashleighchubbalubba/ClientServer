import threading
import time
import random
import socket
from rs import rs
from ts import ts  

def client(rsHostname, rsListenPort, tsListenPort):
    # list that contains all queried hostnames
    hostnameList = []

    # populate hostNameList with hostnames from 'PROJI-HNS.txt'(one line of the file = one element of hostnameList) 
    file = open('PROJI-HNS.txt', 'r')
    linesList = file.readlines()
    for line in linesList: 
        hostnameList.append(line.lower())
    
    # get client's IP address
    addr = socket.gethostbyname(rsHostname)

    try:
        # create RS socket
        csRS = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    except socket.error as err:
        #print('socket open error: {} \n'.format(err))
        exit()

    ''' connect to the RS server'''
    server_binding = (addr, rsListenPort)
    csRS.connect(server_binding)

    try:
        # create TS socket
        csTS = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    except socket.error as err:
        #print('socket open error: {} \n'.format(err))
        exit()

    ''' connect to the TS server'''
    server_binding = (addr, tsListenPort)
    csTS.connect(server_binding)

    # iterate through each hostName to talk to servers
    for hostname in hostnameList: 
        # send queried hostname to RS 
        csRS.send(hostname.encode('utf-8'))

        # receive RS's answer
        receivedString = csRS.recv(300)
        receivedString = receivedString.decode('utf-8').rstrip() 
        #print("string received from RS: ", receivedString)
        word_list = receivedString.split()

        # if last word of receivedString is A, we found a match
        #print("word_list RS", word_list)
        if(word_list[-1] == "A"):
            with open('RESOLVED.txt', 'a') as the_file:
                the_file.write(receivedString)
                the_file.write("\n")
            continue  # found a match so don't need to connect to TS, move onto next hostname
    
        ''' connect to the TS server '''
        # send queried hostname to RS 
        csTS.send(hostname.encode('utf-8'))

        # receive TS's answer
        receivedString = csTS.recv(300)
        receivedString = receivedString.decode('utf-8').rstrip() 

        #print("receivedString TS", receivedString)
        with open('RESOLVED.txt', 'a') as the_file:
            the_file.write(receivedString)
            the_file.write("\n")

    # close the client socket
    csRS.close()
    csTS.close()
    exit()


if __name__ == "__main__":
    #rsHostname = "LAPTOP-8NUTDG7L"
    rsHostname = "Ashleighs-MacBook-Pro.local"
    rsListenPort = 50007
    tsListenPort = 50008
    
    client(rsHostname, rsListenPort, tsListenPort)

    