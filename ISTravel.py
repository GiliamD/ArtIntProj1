############################################################
#
#   File name:  ISTravel.py
#               (Python version 3.5)
#   Authors:    Maciek Przydatek & Giliam Datema
#   Created:    10/10/2015
#
#   Course:     Artificial Intelligence & Decision Systems
#   Assignment: 1
#
#   IST Lisboa
#
############################################################

# Import libraries
import sys
from functions import *

# Read input files
try:
    netFileName = sys.argv[1]
    cliFileName = sys.argv[2]
    networkFile = open(netFileName, 'r')
    clientsFile = open(cliFileName, 'r')
except IndexError:
    print('Specify input files (.map and .cli)')
    quit()
except FileNotFoundError:
    print('Specified file was not found')
    quit()

try:
    if sys.argv[3] == 'informed':
        searchStrategy = 'informed'
    elif sys.argv[3] == 'uninformed':
        searchStrategy = 'uninformed'
    else:
        print('Third argument (optional): ''uninformed'' (default) or ''informed''.')
        quit()
except IndexError:
    searchStrategy = 'uninformed'

rawData = InputData(networkFile.readlines(), clientsFile.readlines())   # data variable initialization. It contains
                                                                        # raw, splitted and stripped integers
                                                                        # or strings

# Close files after reading
networkFile.close()
clientsFile.close()

graph = Graph(rawData.networkData, rawData.nCities, rawData.nConnections)    # graph variable initialization

# Search main loop

results = []

for clientNo in range(rawData.nClients):    # loop through clients

    client = Client(rawData.clData[clientNo])   # initialize new client

    if searchStrategy == 'uninformed':
        # Uninformed search
        print("Performing uninformed search for client %d. Please wait..." % (clientNo+1))
        UC_result = [clientNo+1]
        UC_result.append(uniform_cost(client, graph))
        UC_result = ''.join(c for c in str(UC_result) if c not in '[](),\'')
        results.append(UC_result+'\n')
    else:
        # Informed search
        print("Performing informed search for client %d. Please wait..." % (clientNo+1))
        AS_result = [clientNo+1]
        AS_result.append(a_star(client, graph))
        AS_result = ''.join(c for c in str(AS_result) if c not in '[](),\'')
        results.append(AS_result+'\n')

# Write results to output file. The the results from both algorithms should be the same, i.e. the optimal solution
outputFileName = cliFileName.strip('.cli')+'.sol'
outputFile = open(outputFileName,'w')
outputFile.writelines(results)
outputFile.close()

print("\nFinished. Results stored in %s" % (outputFileName))