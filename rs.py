import threading
import time
import random
import socket

def rs(rsListenPort): 
    dnsTable = [] # list of arrays [ [hostname1, ip1, flag1], [hostname2, ip2, flag2],...]
    currInfo = [] # current line's info [hostname1,ip1,flag1]
    print("does the program reach here??")
    # populating the table while reading the file
    file = open('PROJI-DNSRS.txt', 'r')
    linesList = file.readlines()
    for line in linesList: # outer loop for each line
        for word in line.split(): # inner loop that reads until it hits a space, go on to the next thing
            currInfo.append(word) # (hostname,ipaddress,flag)
        dnsTable.append(currInfo)
        currInfo = []
    
    tsHostName = dnsTable[-1][0]  

    try:
        rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket (AF_INET -> IPV4 and SOCKET_STREAM -> TCP transport protocol)
        print("[S]: RS socket created") # creating socket was successful
    except socket.error as err: 
        print('socket open error: {}\n'.format(err)) # creating socket was not successful
        exit()
    
    server_binding = ('', rsListenPort)
    rs.bind(server_binding) # bind the socket to the port we want to use
    rs.listen(1) # start listening for connections (1 tells you how many connections ur allowed to have in queue)

    csockid, addr = rs.accept()
    
    # Receive queried hostname from the client
    data_from_client = csockid.recv(300)
    print("Data received from the client: {}".format(data_from_client.decode('utf-8')))
    
    encoding = 'utf-8'
    data_from_client = data_from_client.decode(encoding).rstrip()

    # data_from_client = data_from_client.decode('utf-8')
    print("data_from_client: ", data_from_client)

    string = ""
    hasMatched = False
    # searching the table for hostname that the client is requesting
    for info in dnsTable:
        # check first element (hostname) of each list stored in DNSTable 
        if(info[0] == data_from_client):
            # there's a match! send "Hostname IPaddress A" to client
            string = "" + info[0] + " " + info[1] + " " + info[2]
            hasMatched = True
            break

    if(hasMatched is False):
        string = dnsTable[-1]

    print("string being sent to client: ", string)
    # send string to the client.  
    csockid.send(string.encode('utf-8'))
    
    # Close the server socket
    rs.close()
    

if __name__ == "__main__":
    rsListenPort = 50007
    rs(rsListenPort)

