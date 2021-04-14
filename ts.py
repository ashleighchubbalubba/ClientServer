import time
import random
import socket

def ts(tsListenPort): 
    dnsTable = [] # list of arrays [ [hostname1, ip1, flag1], [hostname2, ip2, flag2],...]
    currInfo = [] # current line's info [hostname1,ip1,flag1]

    # populate the table while reading the file
    file = open('PROJI-DNSTS.txt', 'r')
    linesList = file.readlines()
    for line in linesList: 
        for word in line.split(): 
            currInfo.append(word) 
        dnsTable.append(currInfo)
        currInfo = []
   
    try:
        ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    except socket.error as err: 
        exit()
    
    server_binding = ('', tsListenPort)
    ts.bind(server_binding) 
    ts.listen(1)  
    csockid, addr = ts.accept()
    
    while True:
        # receive queried hostname from the client
        queriedHostname = csockid.recv(300).decode('utf-8').rstrip()

        # if client finished sending all hostnames, close socket
        if queriedHostname == "closeConnection":
			break

        string = ""
        hasMatched = False

        # search dnsTable for queried hostname 
        for info in dnsTable:
            replacement = info[0].lower()
            # check hostname of each list stored in DNSTable 
            if(replacement == queriedHostname):
                # there's a match! send "Hostname IPaddress A" to client
                string = "" + info[0] + " " + info[1] + " " + info[2]
                hasMatched = True
                break

        # no match, send 'Hostname - Error:HOST NOT FOUND'
        if(hasMatched is False):
            string = "" + queriedHostname + " - Error:HOST NOT FOUND"

        # send string to the client.  
        csockid.send(string.encode('utf-8'))

    # Close the server socket
    ts.close() 
    exit()   

if __name__ == "__main__":
    tsListenPort = 50008
    ts(tsListenPort)

