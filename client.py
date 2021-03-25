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
        # create first socket here
        csRS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # create a second socket here
        csTS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # print("[C]: Client socket created")
    except socket.error as err:
        print('socket open error: {} \n'.format(err))
        exit()

    # populating hostnameList while reading the file
    file = open('PROJI-HNS.txt', 'r')
    linesList = file.readlines()
    for line in linesList: # for each entry
        hostnameList.append(line)
    
    # get client's IP address
    localhost_addr = socket.gethostbyname(socket.gethostname())
    
    
    # iterate through each hostnameList to talk to servers
    for hostname in hostnameList:
        # talking to RS
        # connect to the RS server on local machine
        server_binding = (localhost_addr, rsListenPort)
        csRS.connect(server_binding)

        # Got a connection request from rs
        rsSockid, addr = csRS.accept()
         
        # Send message to rs
        msg = hostname
        rsSockid.send(msg.encode('utf-8'))

        # receiving RS's answer
        receivedString = "s A"
        word_list = receivedString.split()

        # if last word is A
        if(word_list[-1] == "A"):
            # print("found in RS")
            rs_output = open("ASH+VID-RESOLVED.txt", "w")
            n = rs_output.write(receivedString)
            rs_output.close()
            continue
            
        # talking to ts
        # connect to the TS server on local machine
        server_binding = (localhost_addr, tsListenPort)    
        csTS.connect(server_binding)

        # receiving TS's answer
        ts_output = open("ASH+VID-RESOLVED.txt", "w")
        n = ts_output.write(receivedString)
        ts_output.close()

'''
    # Receive data from the server
    data_from_server=cs.recv(100)
    print("[C]: Data received from server: {}".format(data_from_server.decode('utf-8')))

    # close the client socket
    cs.close()
    exit()
    '''

if __name__ == "__main__":
    #rsHostname = 
    #rsListenPort = 50007
    #tsListenPort = 

    client(rsHostname, rsListenPort, tsListenPort)
   
    # rs(rsListenPort, "google.com")
  
    t1 = threading.Thread(name='server', target=rs) # launch a separate thread for the server
    t1.start()

    time.sleep(random.random() * 5) # sleep for some random amount of time
    t2 = threading.Thread(name='client', target=client) # launch another thread for the client
    t2.start()

    time.sleep(5) # sleep for a bit to give the threads time to complete
    print("Done.")
    