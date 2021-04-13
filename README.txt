README file
-----------

0. Please write down the full names and netids of both your team members.
    Ashleigh Chung (atc101)
    Vidya Mannava (vm479)
    
1. Briefly discuss how you implemented your iterative client functionality.
    First, we populated an array with the given hostnames from PROJ1-HNS.txt. 
    Then we created the RS socket and connected it to the RS server. 
    Before handling TS, we read the last line of the PROJ1-DNSRS.txt 
    to find and record the TSHostname so we can repeat the process of 
    connecting to the TS socket/server. For the iterative functionality, we 
    iterated through each hostname in our array and send it to RS one at a time.
    If RS sends us a confirmation that it has it, client prints the hostname to 
    RESOLVED.txt and moves onto the next hostname. If not, then client sends hostname to TS. 
    After TS's responds, client writes TS's response to RESOLVED.txt (whether it is an 
    error message or 'found' message). Once RESOLVED.txt is complete, client sends a close
    message to both RS and TS, and client itself closes.

2. Are there known issues or functions that aren't working currently in your
   attached code? If so, explain.
    - None
    - Before running the program, just manually type in RS's hostname in line 80 of client.py
    
3. What problems did you face developing code for this project?
    1) Closing RS and TS when RESOLVED.txt is complete 
       - we fixed this by making client send a close message to both RS and TS
         so that RS and TS can exit outside of their while loops and close
    2) Not understanding what 'localhost' from PROJ1-DNRS.txt is and
       realizing it was just a placeholder for TS's hostname once we run on 3 different machines
    3) Not using 'rsHostname' properly (line 22 of client.py)
    
4. Reflect on what you learned by working on this project.
    We better understand how to send and receive data back-and-forth between a client and server. 
    We also have a clear idea of what bind(), listen(), accept(), connect(), and close() do. 
    We know how to solve different socket errors such as "Connection refused," "Broken pipe," and "Only one 
    usage of each socket address is normally permitted." We learned how to use rsHostname and allow 
    client() to communicate with rs() and ts() when the 3 programs run on different machines. 
    