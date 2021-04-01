import threading
import time
import random
import socket
from rs import rs
#from ts import ts  

def client(rsHostname, rsListenPort, tsListenPort):
    # list that contains all queried hostnames
    hostnameList = []

    try:
        # create RS socket 
        csRS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # create TS socket 
        #csTS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # populate hostNameList with hostnames from 'PROJI-HNS.txt'(one line of the file = one element of hostnameList) 
    file = open('PROJI-HNS.txt', 'r')
    linesList = file.readlines()
    for line in linesList: 
        hostnameList.append(line)
    
    # get client's IP address
    localhost_addr = socket.gethostbyname(socket.gethostname())
    
    # iterate through each hostnameList to query each hostName and talk to servers
    for hostname in hostnameList:

        ''' connect to the RS server on local machine '''
        server_binding = (localhost_addr, rsListenPort)
        csRS.connect(server_binding)
        csRS.listen(100)

        # Get a connection request from RS
        rsSockid, addr = csRS.accept()
         
        # Send queried hostname to RS
        queriedHostname = hostname
        rsSockid.send(queriedHostname.encode('utf-8'))
        
        # receive RS's answer
        receivedString = csRS.recv(300)
        print("[Client]: Data received from RS: {}".format(receivedString.decode('utf-8')))
        word_list = receivedString.split()

        # if last word of receivedString is A, we found a match
        if(word_list[-1] == "A"):
            rs_output = open("ASH+VID-RESOLVED.txt", "w")
            n = rs_output.write(receivedString)
            rs_output.close()
            continue  # found a match so don't need to connect to TS, move onto next hostname
 
        '''
        # connect to the TS server on local machine 
        server_binding = (localhost_addr, tsListenPort)
        csTS.connect(server_binding)
        csTS.listen(100)

        # Get a connection request from TS
        tsSockid, addr = csTS.accept()
         
        # Send queried hostname to TS
        queriedHostname = hostname
        tsSockid.send(queriedHostname.encode('utf-8'))
        
        # receive TS's message
        receivedString = csTS.recv(100)
        print("[Client]: Data received from RS: {}".format(receivedString.decode('utf-8')))
        word_list = receivedString.split()

        # if last word of receivedString is A, we found a match
        if(word_list[-1] == "A"):
            # print("found in RS")
            ts_output = open("ASH+VID-RESOLVED.txt", "w")
            n = ts_output.write(receivedString)
            ts_output.close()
            continue  # we found a match so move onto next hostname (don't need to connect to TS)

        # connect to the TS server on local machine
        server_binding = (localhost_addr, tsListenPort)    
        csTS.connect(server_binding)

        # receiving TS's answer
        ts_output = open("ASH+VID-RESOLVED.txt", "w")
        n = ts_output.write(receivedString)
        ts_output.close()
        '''

    # close the client socket
    csRS.close()
    csTS.close()
    exit()


if __name__ == "__main__":
    rsHostname = "Anything"
    rsListenPort = 50007
    tsListenPort = 50008

    client(rsHostname, rsListenPort, tsListenPort)
    rs(rsListenPort)
    '''
    t1 = threading.Thread(name='server', target=rs) # launch a separate thread for the server
    t1.start()

    time.sleep(random.random() * 5) # sleep for some random amount of time
    t2 = threading.Thread(name='client', target=client) # launch another thread for the client
    t2.start()

    time.sleep(5) # sleep for a bit to give the threads time to complete
    print("Done.")
    '''