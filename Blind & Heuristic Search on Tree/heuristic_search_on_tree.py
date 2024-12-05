# Cmput 455 sample code
# Treasure hunt with a heuristic
# With probability p, the heuristic gives a correct move
# which stays on the precomputed path to the goal.
# With prob. 1-p, and also in case the agent is already off the path, 
# it plays randomly.
# Written by Martin Mueller

import random
from collections import deque
from generate_tree import generateTree

def bernoulliExperiment(p):
    return random.random() < p

# depth-first search on tree
# returns (found, numNodesSearched)
def dfs(tree, node, treasure):
    numNodesSearched = 1
    if node == treasure:
        return True, [node], numNodesSearched
    for child in tree[node]:
        found, path, childNodes = dfs(tree, child, treasure)
        numNodesSearched += childNodes
        if found:
            return True, [node] + path, numNodesSearched
    return False, [], numNodesSearched



# Single random sample on tree
# returns (found, numNodesSearched)
def sampleRandomPath(tree, start, treasure, path, p):
    numNodesSearched = 1
    #print("searching root node", start)
    current = start
    if current == treasure:
        return True, numNodesSearched
    while tree[current]: # while current has children, pick one to go next
        #print(path)
        if path != [] and bernoulliExperiment(p):
            current = path[0]
        else:
            current = random.choice(tree[current])
        #print("searching node", current)
        numNodesSearched += 1
        if current == treasure:
            return True, numNodesSearched
        if path != []:
            if current == path[0]:
                path = path[1:]
            else:
                path = []
    return False, numNodesSearched

# Repeated random sampling on tree
# returns (found, numNodesSearched)
def sample(tree, start, treasure, path, p):
    totalNodesSearched = 0
    path = path[1:] # skip root
    for _ in range(1000):
        found, numNodesSearched = sampleRandomPath(tree, start, treasure, path, p)
        totalNodesSearched += numNodesSearched
        if found:
            return True, totalNodesSearched
    return False, totalNodesSearched

def doTest(tree, name, n, p):
    print ("Search with", name)
    print ("Heuristic accuracy", p)
    numSuccess = 0
    totalNodesSearched = 0
    for _ in range(n):
        # hide treasure in random node in tree
        treasure = random.choice(list(tree.keys()))
        _, path, _ = dfs(tree, 0, treasure)
        #print("path", path)
        found, numNodesSearched = sample(tree, 0, treasure, path, p)
        if found:
            numSuccess += 1
        totalNodesSearched += numNodesSearched
    print(n, "Runs",
          numSuccess, "Successes", 
          totalNodesSearched/n, "Average nodes searched")

tree, nuNodes = generateTree(3, 6)
print("Tree with", nuNodes, "Nodes.")
for p in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]: 
    doTest(tree, "Random sampling", 100, p)
