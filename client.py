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

    # create RS socket 
    try:
        csRS = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    except socket.error as err:
        exit()

    # connect to RS server
    rsAddr = socket.gethostbyname(rsHostname)
    server_binding = (rsAddr, rsListenPort)
    csRS.connect(server_binding)

    # create TS socket 
    try:
        csTS = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    except socket.error as err:
        exit()

    # read last line of PROJI-DNSRS.txt to get TShostname
    with open("PROJI-DNSRS.txt", "r") as file:
        for lastLine in file:
            pass
    line = lastLine.split()
    tsHostname = line[0]

    # connect to TS server
    tsAddr = socket.gethostbyname(tsHostname)
    server_binding = (tsAddr, tsListenPort)
    csTS.connect(server_binding)

    # iterate through each hostName to talk to servers
    for hostname in hostnameList: 
        csRS.send(hostname.encode('utf-8'))  # send queried hostname to RS

        receivedString = csRS.recv(300) # receive RS's answer
        receivedString = receivedString.decode('utf-8').rstrip() 
        word_list = receivedString.split()

        # if flag of receivedString is A, we found a match, write this to RESOLVED.txt
        if(word_list[-1] == "A"):
            with open('RESOLVED.txt', 'a') as the_file:
                the_file.write(receivedString)
                the_file.write("\n")
            continue  # found a match so move onto next hostname

        # send queried hostname to TS
        csTS.send(hostname.encode('utf-8'))

        receivedString = csTS.recv(300)  # receive TS's answer
        receivedString = receivedString.decode('utf-8').rstrip() 

        # write to RESOLVED.txt file
        with open('RESOLVED.txt', 'a') as the_file:
            the_file.write(receivedString)
            the_file.write("\n")

    # if done going going through hostnames, tell TS and RS to close connection
    csRS.send("closeConnection".encode('utf-8'))
    csTS.send("closeConnection".encode('utf-8'))

    # close both sockets
    csRS.close()
    csTS.close()
    exit()

if __name__ == "__main__":
    rsHostname = ""      # type in hostname of machine that RS runs on
    rsListenPort = 50007
    tsListenPort = 50008
    
    client(rsHostname, rsListenPort, tsListenPort)

    