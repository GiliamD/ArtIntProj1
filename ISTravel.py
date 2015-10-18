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
import classes

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

data = classes.InputData(networkFile.readlines(), clientsFile.readlines())

graph=classes.Graph(data.networkData, data.nCities, data.nConnections)

client = classes.Client(data.clData[6])
nodes = client.expandNode(1, 0, graph)
for nod in nodes: print(nod)
# Search algorithm
