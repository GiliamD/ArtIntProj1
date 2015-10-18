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
from classes import *

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

# client = Client(rawData.clData[1]) # just example - to show that it works - you can change this [1] to change the client number (should be deleted)
# nodes = client.expandNode(5, 0, graph)  # also example - client.expandNode(nodeNo, currentTime, graph)
# for nod in nodes: print(nod)            # just prints what came out


# Informed search algorithm

def a_star(graph, start, goal, heuristic):
    """Searches the state space for the optimal path from the initial state to the goal state, minimizing the value
    function f(n) = g(n) + h(n), where g(n) is the value from the initial node to the current node n and h(n) is the
    estimated value to reach the goal state from the current node, i.e. the heuristic value."""

    # Initialize open list, closed list and path value (estimate)
    open_list = PriorityQueue()
    open_list.add(start, 0)

    closed_list = {}
    current_best_value = {}

    # Note: closed list contains nodes and means of transportation used to get to the nodes
    closed_list[start] = (None, None)
    current_best_value[start] = 0

    # Initialize total time and cost. Note that one of these is a duplicate of path value, depending on whether the
    # optimization criterion is time or cost
    totalTime = {}
    totalTime[start] = 0
    totalCost = {}
    totalCost[start] = 0

    # Run algorithm until no more nodes left to explore (i.e. until open list is empty)
    while not open_list.empty():

        # Get next node in priority queue and remove from the queue
        current = open_list.pop()

        # Check if current node is goal node
        if current == goal:
            return get_path(current, closed_list), totalTime[current], totalCost[current]

        # Let client expand current node according to specified constraints
        successors = client.expandNode(current, totalTime[current], graph)

        # Loop through successors to find the best next node
        for successor in successors:

            # Compute path value (g value) from start to successor of current, via current
            new_value = current_best_value[current] + successor.value

            # If successor node not visited yet or if the new path value is better than the previously obtained value,
            # set or update the current best value for that node
            if successor not in current_best_value or new_value < current_best_value[successor]:
                current_best_value[successor.cityNo] = new_value

                # Set priority equal to value function f(n) = g(n) + h(n)
                priority = new_value + heuristic(successor, goal)

                # Add successor to open list with specified priority
                open_list.add(successor.cityNo, priority)

                # Add the current node to the closed list. Note that it was already removed from the open list
                closed_list[successor.cityNo] = (current, successor.vehicle)

                # Compute and store total time and cost for successor node
                totalTime[successor.cityNo] = totalTime[current] + successor.time
                totalCost[successor.cityNo] = totalCost[current] + successor.cost

    # Return -1 if no path was found
    return -1


# Get path from start to goal

def get_path(current, closed_list):
    """Traces path from current node back to start."""

    total_path = [current]
    while current in closed_list:
        total_path.append(closed_list[current][1])
        total_path.append(closed_list[current][0])
        current = closed_list[current][0]

    # Reverse order and get rid of None (the parent of the start node)
    return total_path[::-1][2:]


# Uninformed search algorithm

def uniform_cost(graph, start, goal):
    """Searches the state space for the optimal path from the initial state to the goal state by selecting the node with
    the lowest path value first."""

    # Initialize open list, closed list and path value, which can be either cost or time
    open_list = PriorityQueue()
    open_list.add(start, 0)

    closed_list = {}
    current_best_value = {}

    # Note: closed list contains nodes and means of transportation used to get to the nodes
    closed_list[start] = (None, None)
    current_best_value[start] = 0

    # Initialize total time and cost. Note that one of these is a duplicate of path value, depending on whether the
    # optimization criterion is time or cost
    totalTime = {}
    totalTime[start] = 0
    totalCost = {}
    totalCost[start] = 0

    # Run algorithm until no more nodes left to explore (i.e. until open list is empty)
    while not open_list.empty():

        # Get next node in priority queue and remove from the queue
        current = open_list.pop()

        # Check if current node is goal node
        if current == goal:
            return get_path(current, closed_list), totalTime[current], totalCost[current]

        # Let client expand current node according to specified constraints
        successors = client.expandNode(current, totalTime[current], graph)

        # Loop through successors to find the best next node
        for successor in successors:

            # Compute path value (g value) from start to successor of current, via current
            new_value = current_best_value[current] + successor.value

            # If successor node not visited yet or if the new path value is better than the previously obtained value,
            # set or update the current best value for that node
            if successor.cityNo not in current_best_value or new_value < current_best_value[successor.cityNo]:
                current_best_value[successor.cityNo] = new_value

                # Set priority equal to the path value g(n)
                priority = new_value

                # Add successor to open list with specified priority
                open_list.add(successor.cityNo, priority)

                # Add the current node to the closed list. Note that it was already removed from the open list
                closed_list[successor.cityNo] = (current, successor.vehicle)

                # Compute and store total time and cost for successor node
                totalTime[successor.cityNo] = totalTime[current] + successor.time
                totalCost[successor.cityNo] = totalCost[current] + successor.cost

    # Return -1 if no path was found
    return -1


# Search main loop

results = []

for clientNo in range(rawData.nClients):

    client = Client(rawData.clData[clientNo])

    # Uninformed search
    UC_result = [clientNo+1]
    UC_result.append(uniform_cost(graph, client.startCity, client.goalCity))
    UC_result = ''.join(c for c in str(UC_result) if c not in '[](),\'')

    # Informed search
    AS_result = [clientNo+1]
    AS_result.append(a_star(graph, client.startCity, client.goalCity))
    AS_result = ''.join(c for c in str(AS_result) if c not in '[](),\'')

    print(UC_result == AS_result)

    results.append(UC_result+'\n')

# Write results to output file. The the results from both algorithms should be the same, i.e. the optimal solution
outputFile = open(cliFileName.strip('.cli')+'.sol','w')
outputFile.writelines(results)
outputFile.close()