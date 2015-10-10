############################################################
#
#   File name:  ISTravel.py
#   Authors:    Maciek Przydatek & Giliam Datema
#   Date:       10/10/2015
#
#   Course:     Artificial Intelligence & Decision Systems
#   Assignment: 1
#
#   IST Lisboa
#
############################################################

# Import libraries
import sys


# Function definitions
def try_int(x):
    """Tries to convert argument to type int."""
    try:
        return int(x)
    except ValueError:
        return x


# Class definitions
class InputData:
    """Structures the input data."""
    def __init__(self, network, clients):

        # Network configuration
        network_data = [line.rstrip().split() for line in network]
        self.nCities = int(network_data[0][0])
        self.nConnections = int(network_data[0][1])
        self.network = [[try_int(network_data[lst][elem]) for elem in range(len(network_data[lst]))] for lst in
                        range(1, len(network_data))]

        # Client requests
        client_data = [line.rstrip().split() for line in clients]
        self.nClients = int(network_data[0][0])
        self.clients = [[try_int(client_data[lst][elem]) for elem in range(len(client_data[lst]))] for lst in
                        range(1, len(client_data))]


# Read input files
try:
    netFileName = sys.argv[1]
    cliFileName = sys.argv[2]
    networkFile = open(netFileName, 'r')
    clientsFile = open(cliFileName, 'r')
except IndexError:
    print('Specify input files (.map and .cli)!')
    quit()
except FileNotFoundError:
    print('Specified file was not found!')
    quit()

networkData = networkFile.readlines()
clientsData = clientsFile.readlines()

data = InputData(networkData, clientsData)


# Search algorithm
