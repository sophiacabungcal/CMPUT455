# Cmput 455 sample code
# Treasure hunt with blind search
# builds a tree and hides the treasure in a random node.
# Then runs several blind search algorithms repeatedly
# and prints statistics about their success, and nodes searched.
# Written by Martin Mueller

import random
from collections import deque
from generate_tree import generateTree

# depth-first search on tree
# returns (found, numNodesSearched)
def dfs(tree, node, treasure):
    numNodesSearched = 1
    if node == treasure:
        return True, numNodesSearched
    for child in tree[node]:
        found, childNodes = dfs(tree, child, treasure)
        numNodesSearched += childNodes
        if found:
            return True, numNodesSearched
    return False, numNodesSearched


# breadth-first search on tree
# returns (found, numNodesSearched)
def bfs(tree, start, treasure):
    numNodesSearched = 0
    queue = deque()
    queue.append(start)
    while len(queue) > 0:
        node = queue.popleft();
        numNodesSearched += 1
        if node == treasure:
            return True, numNodesSearched
        for child in tree[node]:
            queue.append(child)
    return False, numNodesSearched

# Single random sample on tree
# returns (found, numNodesSearched)
def sampleRandomPath(tree, start, treasure):
    numNodesSearched = 1
    current = start
    if current == treasure:
        return True, numNodesSearched
    while tree[current]: # while current has children, pick one to go next
        current = random.choice(tree[current])
        numNodesSearched += 1
        if current == treasure:
            return True, numNodesSearched
    return False, numNodesSearched

# Repeated random sampling on tree
# returns (found, numNodesSearched)
def sample(tree, start, treasure):
    totalNodesSearched = 0
    for _ in range(1000):
        found, numNodesSearched = sampleRandomPath(tree, start, treasure)
        totalNodesSearched += numNodesSearched
        if found:
            return True, totalNodesSearched
    return False, totalNodesSearched

def doTest(tree, name, search, n):
    print ("Search with", name)
    numSuccess = 0
    totalNodesSearched = 0
    for _ in range(n):
        # hide treasure in random node in tree
        treasure = random.choice(list(tree.keys())) 
        found, numNodesSearched = search(tree, 0, treasure)
        if found:
            numSuccess += 1
        totalNodesSearched += numNodesSearched
    print(n, "Runs",
          numSuccess, "Successes", 
          totalNodesSearched/n, "Average nodes searched")

tree, nuNodes = generateTree(3, 6)
print("Tree with", nuNodes, "Nodes.")
doTest(tree, "Dfs", dfs, 1000)
doTest(tree, "Bfs", bfs, 1000)
doTest(tree, "Random sampling", sample, 1000)
