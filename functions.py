# Function definitions file

from classes import *


# Returns heuristic value of cost from current node to goal node

def heuristic(client, graph, start, goal):
    [*heu_results] = uniform_cost(client, graph, ifHeuristics=True)
    if client.optimCrit == 'tempo':
        # return total time for relaxed problem
        return heu_results[-2]
    else:
        # return total cost for relaxed problem
        return heu_results[-1]


# Get path from start to goal

def get_path(current, start, closed_list):
    """Traces path from current node back to start."""

    total_path = [current]
    while current in closed_list and current != start:
        total_path.append(closed_list[current][1])
        total_path.append(closed_list[current][0])
        current = closed_list[current][0]

    # Reverse order and get rid of None (the parent of the start node)
    return total_path[::-1][2:]


# Uninformed search algorithm

def uniform_cost(client, graph, ifHeuristics=False):
    """Searches the state space for the optimal path from the initial state to the goal state by selecting the node with
    the lowest path value first."""

    start = client.startCity
    goal = client.goalCity

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
            return get_path(current, start, closed_list), totalTime[current] - client.timeAvailable, totalCost[current]

        # Let client expand current node according to specified constraints
        successors = client.expandNode(current, totalTime[current], graph, ifHeuristics)

        # Loop through successors to find the best next node
        for successor in successors:

            # Compute path value (g value) from start to successor of current, via current
            new_value = current_best_value[current] + successor.value

            # Compute total time and cost for successor
            tmpTotalTime = totalTime[current] + successor.time
            tmpTotalCost = totalCost[current] + successor.cost

            # Discard if total time or total cost exceeds constraints
            if tmpTotalTime - client.timeAvailable > client.maxTotalTime or tmpTotalCost > client.maxTotalCost:
                continue

            # If successor node not visited yet or if the new path value is better than the previously obtained value,
            # set or update the current best value for that node
            elif successor.cityNo not in current_best_value or new_value < current_best_value[successor.cityNo]:
                current_best_value[successor.cityNo] = new_value

                # Set priority equal to the path value g(n)
                priority = new_value

                # Add successor to open list with specified priority
                open_list.add(successor.cityNo, priority)

                # Add the current node to the closed list. Note that it was already removed from the open list
                closed_list[successor.cityNo] = (current, successor.vehicle)

                # Store total time and cost for successor node
                totalTime[successor.cityNo] = tmpTotalTime
                totalCost[successor.cityNo] = tmpTotalCost

    # Return -1 if no path was found
    return -1


# Informed search algorithm

def a_star(client, graph):
    """Searches the state space for the optimal path from the initial state to the goal state, minimizing the value
    function f(n) = g(n) + h(n), where g(n) is the value from the initial node to the current node n and h(n) is the
    estimated value to reach the goal state from the current node, i.e. the heuristic value."""

    start = client.startCity
    goal = client.goalCity

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
            return get_path(current, start, closed_list), totalTime[current] - client.timeAvailable, totalCost[current]

        # Let client expand current node according to specified constraints
        successors = client.expandNode(current, totalTime[current], graph)

        # Loop through successors to find the best next node
        for successor in successors:

            # Compute path value (g value) from start to successor of current, via current
            new_value = current_best_value[current] + successor.value

            # Compute total time and cost for successor
            tmpTotalTime = totalTime[current] + successor.time
            tmpTotalCost = totalCost[current] + successor.cost

            # Discard if total time or total cost exceeds constraints
            if tmpTotalTime - client.timeAvailable > client.maxTotalTime or tmpTotalCost > client.maxTotalCost:
                continue

            # If successor node not visited yet or if the new path value is better than the previously obtained value,
            # set or update the current best value for that node

            if successor not in current_best_value or new_value < current_best_value[successor]:
                current_best_value[successor.cityNo] = new_value

                # Set priority equal to value function f(n) = g(n) + h(n)
                priority = new_value + heuristic(client, graph, start, goal)

                print(successor)
                print(heuristic(client, graph, start, goal))

                # Add successor to open list with specified priority
                open_list.add(successor.cityNo, priority)

                # Add the current node to the closed list. Note that it was already removed from the open list
                closed_list[successor.cityNo] = (current, successor.vehicle)

                # Compute and store total time and cost for successor node
                totalTime[successor.cityNo] = tmpTotalTime
                totalCost[successor.cityNo] = tmpTotalCost

    # Return -1 if no path was found
    return -1
