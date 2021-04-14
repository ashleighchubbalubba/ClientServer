import time
import random
import socket

def rs(rsListenPort): 
    dnsTable = [] # list of arrays [ [hostname1, ip1, flag1], [hostname2, ip2, flag2],...]
    currInfo = [] # current line's info [hostname1,ip1,flag1]

    # populate the table while reading the file
    file = open('PROJI-DNSRS.txt', 'r')
    linesList = file.readlines()
    for line in linesList: 
        for word in line.split(): 
            currInfo.append(word) 
        dnsTable.append(currInfo)
        currInfo = []

    try:
        rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    except socket.error as err: 
        exit()
    
    server_binding = ('', rsListenPort)
    rs.bind(server_binding) 
    rs.listen(1) 
    csockid, addr = rs.accept()
    
    while True:
       # Receive queried hostname from the client
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

        # no match, send "TShostname - NS" to client
        if(hasMatched is False):
            string = "" + dnsTable[-1][0] + " " + dnsTable[-1][1] + " " + dnsTable[-1][2]

        # send string to the client
        csockid.send(string.encode('utf-8'))
    
    # close socket
    rs.close()
    exit() 

if __name__ == "__main__":
    rsListenPort = 50007
    rs(rsListenPort)

