# Cmput 455 sample code
# Generate a tree of depth d and uniform branching factor b
# Written by Martin Mueller

_counter = 0

# Creates a tree of depth d and uniform branching factor b 
# in a depth-first manner.
# Nodes are numbered depth-first as well. The root is 0
# returns dictionary with the tree in adjacency list form, and number of nodes
def generateTree(b, d):
    global _counter
    _counter = 0
    tree = {}
    _generateRecursively(tree, 0, b, d)
    return tree, _counter + 1

# traverse depth-first, collect all children, store in tree
def _generateRecursively(tree, level, b, d):
    global _counter
    current = _counter
    children = []
    if level < d:
        for _ in range(b):
            _counter += 1
            child = _generateRecursively(tree, level + 1, b, d)
            children.append(child)
    tree[current] = children
    return current
