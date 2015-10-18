# Class definitions file

import heapq


# Tries to return integer equivalent of input, if input is not convertible, returns input

def try_int(x):
    """Tries to convert argument to type int."""
    try:
        return int(x)
    except ValueError:
        return x


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


class InputData:
    """Structures the input data."""

    def __init__(self, network, clients):

        # Network configuration
        network_data = [line.rstrip().split() for line in network]
        self.nCities = try_int(network_data[0][0])
        self.nConnections = try_int(network_data[0][1])
        self.networkData = [[try_int(network_data[lst][elem]) for elem in range(len(network_data[lst]))] for lst in
                        range(1, len(network_data))]

        # Client requests
        client_data = [line.rstrip().split() for line in clients]
        self.nClients = try_int(client_data[0][0])
        self.clData = [[try_int(client_data[lst][elem]) for elem in range(len(client_data[lst]))] for lst in
                        range(1, len(client_data))]


class Node:
    """Stores a number of city the agent can jump to with the value of travelling (time or cost)."""

    def __init__(self, cityNo, vehicle, time, cost, optimCrit):
        self.cityNo = cityNo    # city number
        self.vehicle = vehicle  # vehicle used
        self.time = time        # travel time
        self.cost = cost        # travel cost
        if optimCrit == 'tempo': self.value = self.time     # self.value is a duplicate of either self.time or self.cost
        elif optimCrit == 'custo': self.value = self.cost   # it is constructed that way in order to be used
                                                            # by the generic search algorithm
                                                            # (which does not know the minimization criterion)

    def __repr__(self):
        return "<city: %2d, vehicle: %9s, time: %4d, cost: %3d, value: %4d>" % (self.cityNo, self.vehicle, self.time, self.cost, self.value)


class Edge:
    """Stores a connection between two cities along with all information provided."""

    def __init__(self, edge):
        self.cities = [edge[0], edge[1]]    # cities, which are connected by this edge
        self.vehicle = edge[2]      # vehicle used
        self.time = edge[3]         # travel time
        self.cost = edge[4]         # travel cost
        self.firstDep = edge[5]     # time of first departure
        self.noMoreDepTime = edge[6]   # time after no departure is performed in present day
        self.depInterval = edge[7]  # time between departures

    def __repr__(self):
        return "<cities: %2d %2d, vehicle: %9s, time: %4d, cost: %3d, first: %4d, border: %4d, interval: %4d>" % (self.cities[0], self.cities[1], self.vehicle, self.time, self.cost, self.firstDep, self.noMoreDepTime, self.depInterval)

class Graph:
    """Stores a set of all possible connections on the map."""
    def __init__(self, networkData, nCities, nConnections):    # initializes the network using networkData raw data list
        self.nCities = nCities
        self.nConnections = nConnections
        self.network = []
        for edgeData in networkData:
            self.network.append(Edge(edgeData))

    def __repr__(self):
        for edge in self.network:
            print(edge)


class Client:
    """Stores client preferences"""

    def __init__(self, clData):     # initializes the client using clData raw data list

        # these two constraints are for main search function
        self.maxTotalTime = float("inf")    # initially there is no limit for whole travel time
        self.maxTotalCost = float("inf")    # initially there is no limit for whole travel cost

        # these three constraints are for node generating
        self.forbiddenVehicle = 'none'      # initially all transport types are available
        self.maxConnTime = float("inf")     # initially there is no limit for single connection time
        self.maxConnCost = float("inf")     # initially there is no limit for single connection cost

        self.clientNo = clData[0]       # put client number in appropriate variable
        self.startCity = clData[1]      # put client starting location in appropriate variable
        self.goalCity = clData[2]       # put client goal location in appropriate variable
        self.timeAvailable = clData[3]  # put client time of availability in appropriate variable
        self.optimCrit = clData[4]      # put client optimality criterion in appropriate variable
        if clData[5] > 0:               # if there are some constraints
            if   clData[6] == 'A1': self.forbiddenVehicle = clData[7]
            elif clData[6] == 'A2': self.maxConnTime = clData[7]
            elif clData[6] == 'A3': self.maxConnCost = clData[7]
            elif clData[6] == 'B1': self.maxTotalTime = clData[7]
            elif clData[6] == 'B2': self.maxTotalCost = clData[7]
            if clData[5] == 2:
                if   clData[8] == 'A1': self.forbiddenVehicle = clData[9]
                elif clData[8] == 'A2': self.maxConnTime = clData[9]
                elif clData[8] == 'A3': self.maxConnCost = clData[9]
                elif clData[8] == 'B1': self.maxTotalTime = clData[9]
                elif clData[8] == 'B2': self.maxTotalCost = clData[9]

    def expandNode(self, nodeNo, currTime, graph, ifHeuristics = False):    # expands given node using client's constraints
        nodes=[]    # initialize nodes list to return later
        for edge in graph.network:    # loop through all edges (connections)
            if edge.cities[0] == nodeNo or edge.cities[1] == nodeNo:      # if current city found in connection
                if edge.vehicle != self.forbiddenVehicle or (ifHeuristics and self.optimCrit == 'custo'):    # if vehicle is not forbidden (but when we are calculating heuristic cost value, this constraint should be omitted)
                    if edge.time <= self.maxConnTime or (ifHeuristics and self.optimCrit == 'custo'):       # if connection travel time does not exceed desired value (as above for cost heuristics)
                        if edge.cost <= self.maxConnCost:     # if connection travel cost does not exceed desired value
                            tmpTime = edge.firstDep          # initialize tmpTime
                            noMoreDepTime = edge.noMoreDepTime     # initialize noMoreDepTime
                            while True:
                                if tmpTime > noMoreDepTime:     # if we are after last departure
                                    tmpTime = edge.firstDep + 1440    # set the first departure of next day
                                    noMoreDepTime += 1440       # set the noMoreDepTime for the next day
                                    continue
                                elif tmpTime >= currTime and tmpTime >= self.timeAvailable: # if we found next departure
                                    if ifHeuristics and self.optimCrit == 'tempo': time = edge.time    # calculate heuristic time (travelling)
                                    else: time = tmpTime-currTime+edge.time     # calculate total time (waiting + travelling)
                                    cost = edge.cost                            # assign cost

                                    if edge.cities[0] == nodeNo: destinationCity = edge.cities[1]     # check to which city are we
                                    else: destinationCity = edge.cities[0]                     # actually going

                                    nodes.append(Node(destinationCity, edge.vehicle, time, cost, self.optimCrit))# append
                                    break                                                 # new node to 'nodes' variable
                                tmpTime += edge.depInterval
        from operator import attrgetter     # for easier sorting
        if self.optimCrit == 'tempo':
            nodes = sorted(nodes, key = attrgetter('cost'))    # sort by cost
            nodes = sorted(nodes, key = attrgetter('time'))    # sort by time
        elif self.optimCrit == 'custo':
            nodes = sorted(nodes, key = attrgetter('time'))    # sort by time
            nodes = sorted(nodes, key = attrgetter('cost'))    # sort by cost
        nodes = sorted(nodes, key = attrgetter('cityNo'))   # and then by cityNo; possible because sorted() is stable
        for i in range(len(nodes)-1, 0, -1):    # iterate backward from the end to second (therefore node[1]) element
            if nodes[i].cityNo == nodes[i-1].cityNo:    # if node before has the same city
                nodes.pop(i)    # delete current one, because it has higher value
        return nodes
