# Command and Telemetry Group

## Communication Protocol
The communication protcol is defined in the CommunicationProtocol.py file and outlines how communication between the flight and ground command and telemetry should occur.

## Subgroup Class
The SubgroupClass (defined in the SubgoupClass.py) represents, generically, how all the subgroups will behave. Each instance of this class will represent the 4 different subgroups. The purpose of this class is so that the implementation of how communication between each subgroup (via sockets) is abstracted to the rest of the project.  

## ThreadingClass
The ThreadingClass (defined in threadSocket.py) is a background thread that listens for messages sent to out group on a specific port. We chose to add this functionality as a thread so that the communication between the ground and flight command and telemetry is not blocked.

## How to Run
Within the Flight and Ground folder are single main files that iniitate the communication between itself and the other command and telemetry subgroup (either Flight or Ground). These files are the entry point to our project. 

To test the project, run `python3.7 main.py` in either the Flight or Ground folde. The expected output is "event loop running" to be printed to the console. When integrated with the rest of the subgroups, each event loop run will send messages received from the other subgroups. 
