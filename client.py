import time
import random
import socket

def client(rsHostname, rsListenPort, tsListenPort):
    # list that contains all queried hostnames
    hostnameList = []

    # populate hostNameList with hostnames from 'PROJI-HNS.txt'(one line of the file = one element of hostnameList) 
    file = open('PROJI-HNS.txt', 'r')
    linesList = file.readlines()
    for line in linesList: 
        hostnameList.append(line.lower())

    ''' create RS socket '''
    try:
        # create RS socket
        csRS = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    except socket.error as err:
        #print('socket open error: {} \n'.format(err))
        exit()

    ''' connect to the RS server'''
    rsAddr = socket.gethostbyname(rsHostname)
    server_binding = (rsAddr, rsListenPort)
    csRS.connect(server_binding)

    ''' create TS socket '''
    try:
        # create TS socket
        csTS = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    except socket.error as err:
        #print('socket open error: {} \n'.format(err))
        exit()

    # read last line of PROJI-DNSRS.txt to get tsHostname
    with open("PROJI-DNSRS.txt", "r") as file:
        for lastLine in file:
            pass
    line = lastLine.split()
    tsHostname = line[0]
    #print("tsHostname", tsHostname)

    ''' connect to the TS server'''
    tsAddr = socket.gethostbyname(tsHostname)
    server_binding = (tsAddr, tsListenPort)
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

    #tell ts and rs to close connection
    csRS.send("closeConnection".encode('utf-8'))
    csTS.send("closeConnection".encode('utf-8'))

    # close the client socket
    csRS.close()
    csTS.close()

if __name__ == "__main__":
    #rsHostname = "cray1.cs.rutgers.edu"
    rsHostname = ""
    rsListenPort = 50007
    tsListenPort = 50008
    
    client(rsHostname, rsListenPort, tsListenPort)

    