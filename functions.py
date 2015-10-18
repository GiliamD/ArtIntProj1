def heuristics(client, startNode, goalNode):
    [*heu_results] = uniform_cost(client, graph, startNode, goalNode, ifHeuristics = True)
    # do something with results and return proper value (you can check if it's total time or cost in 'client' object)