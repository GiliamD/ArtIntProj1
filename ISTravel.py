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
    print('Specify input files (.map and .cli)!')
    quit()
except FileNotFoundError:
    print('Specified file was not found!')
    quit()

rawData = InputData(networkFile.readlines(), clientsFile.readlines())   # data variable initialization. It contains
                                                                        # raw, splitted and stripped integers
                                                                        # or strings

# Close files after reading
networkFile.close()
clientsFile.close()

graph = Graph(rawData.networkData, rawData.nCities, rawData.nConnections)    # graph variable initialization

# Search main loop

results = []

for clientNo in range(rawData.nClients):

    client = Client(rawData.clData[clientNo])

    # Uninformed search
    UC_result = [clientNo+1]
    UC_result.append(uniform_cost(client, graph))
    UC_result = ''.join(c for c in str(UC_result) if c not in '[](),\'')

    # Informed search
    AS_result = [clientNo+1]
    AS_result.append(a_star(client, graph))
    AS_result = ''.join(c for c in str(AS_result) if c not in '[](),\'')

    print(UC_result == AS_result)

    # results.append(UC_result+'\n')
    results.append(AS_result+'\n')

# Write results to output file. The the results from both algorithms should be the same, i.e. the optimal solution
outputFile = open(cliFileName.strip('.cli')+'.sol','w')
outputFile.writelines(results)
outputFile.close()



# # comparing with teacher's
# our=open(cliFileName.strip('.cli')+'.sol','r')
# teacher=open(cliFileName.strip('.cli')+'.solx','r')
#
# ourData=our.readlines()
# teacherData=teacher.readlines()
#
# ourDataSplitted = [line.rstrip().split() for line in ourData]
# teacherDataSplitted = [line.rstrip().split() for line in teacherData]
#
# for line in ourDataSplitted:
#     line.pop(len(line)-2)
#
# for line in teacherDataSplitted:
#     line.pop(len(line)-2)
#
# for i in range(len(ourDataSplitted)):
#     print('Client ',i+1,' the same: ',ourDataSplitted[i] == teacherDataSplitted[i])
#
# print('\n\nAll OK: ',ourDataSplitted == teacherDataSplitted)