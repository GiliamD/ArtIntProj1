############################################################
#
#   File name:  ISTravel.py
#               (Python version 3.5)
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

# Close files after reading
networkFile.close()
clientsFile.close()


####################################
#       NEW CODE BELOW
####################################

# Import heap queue module
import heapq


# Priority queue class

class PriorityQueue:
    """Generic priority queue using Python's heap queue module."""
    def __init__(self):
        self.elements = []

    def empty(self):
        """Returns True if queue is empty."""
        return not self.elements

    def add(self, item, priority):
        """Adds item to the queue with specified priority."""
        heapq.heappush(self.elements, (priority, item))

    def pop(self):
        """Returns item with highest priority (i.e. lowest priority value) and removes it from the queue."""
        return heapq.heappop(self.elements)[1]


# Informed search algorithm

def a_star(graph, start, goal, heuristic):
    """Searches the state space for the optimal path from the initial state to the goal state, minimizing the value
    function f(n) = g(n) + h(n), where g(n) is the cost from the initial node to the current node n and h(n) is the
    estimated cost to reach the goal state from the current node, i.e. the heuristic value."""

    # Initialize open list, closed list and path cost (estimate)
    open_list = PriorityQueue()
    open_list.add(start, 0)

    closed_list = {}
    current_best_cost = {}

    closed_list[start] = None
    current_best_cost[start] = 0

    # Run algorithm until no more nodes left to explore (i.e. until open list is empty)
    while not open_list.empty():

        # Get next node in priority queue and remove from the queue
        current = open_list.pop()

        # Check if current node is goal node
        if current == goal:
            return get_path(current, closed_list), current_best_cost

        # Let client expand current node according to specified constraints
        successors = client.expandNode(current)

        # Loop through successors to find the best next node
        for successor in successors:

            # Compute path cost (g value) from start to successor of current, via current
            new_cost = current_best_cost[current] + graph.link_cost(current, successor)

            # If successor node not visited yet or if the new path cost is better than the previously obtained cost,
            # set or update the current best cost for that node
            if successor not in current_best_cost or new_cost < current_best_cost[successor]:
                current_best_cost[successor] = new_cost

                # Set priority equal to value function f(n) = g(n) + h(n)
                priority = new_cost + heuristic(successor, goal)

                # Add successor to open list with specified priority
                open_list.add(successor, priority)

                # Add the current node to the closed list. Note that it was already removed from the open list
                closed_list[successor] = current

    # Return -1 if no path was found
    return -1


# Get path from start to current node (= goal)

def get_path(current, closed_list):
    """Traces path from current node back to start."""

    total_path = [current]
    while current in closed_list:
        current = closed_list[current]
        total_path.append(current)
    return total_path


# Uninformed search algorithm

def uniform_cost(graph, start, goal):
    """Searches the state space for the optimal path from the initial state to the goal state by selecting the node with
    the lowest path cost first."""

    # Initialize open list, closed list and path cost (estimate)
    open_list = PriorityQueue()
    open_list.add(start, 0)

    closed_list = {}
    current_best_cost = {}

    closed_list[start] = None
    current_best_cost[start] = 0

    # Run algorithm until no more nodes left to explore (i.e. until open list is empty)
    while not open_list.empty():

        # Get next node in priority queue and remove from the queue
        current = open_list.pop()

        # Check if current node is goal node
        if current == goal:
            return get_path(current, closed_list), current_best_cost

        # Let client expand current node according to specified constraints
        successors = client.expandNode(current)

        # Loop through successors to find the best next node
        for successor in successors:

            # Compute path cost (g value) from start to successor of current, via current
            new_cost = current_best_cost[current] + graph.link_cost(current, successor)

            # If successor node not visited yet or if the new path cost is better than the previously obtained cost,
            # set or update the current best cost for that node
            if successor not in current_best_cost or new_cost < current_best_cost[successor]:
                current_best_cost[successor] = new_cost

                # Set priority equal to the path cost g(n)
                priority = new_cost

                # Add successor to open list with specified priority
                open_list.add(successor, priority)

                # Add the current node to the closed list. Note that it was already removed from the open list
                closed_list[successor] = current

    # Return -1 if no path was found
    return -1


# # Search main loop
#
# results = []
#
# for client in clients:
#
#     # Uninformed search
#     [*UC_results] = uniform_cost(graph, start, goal)
#
#     # Informed search
#     [*AS_results] = a_star(graph, start, goal, heuristic)
#
#     # Check if results are the same
#     print('Algorithms found same solution: ', UC_results == AS_results)
#
#     # Save results
#     results.append(...)
#
# # Write results to output file. The the results from both algorithms should be the same, i.e. the optimal solution
# outputFile = open(cliFileName.strip('.cli')+'.sol','w')
# outputFile.writelines(results)
# outputFile.close()
