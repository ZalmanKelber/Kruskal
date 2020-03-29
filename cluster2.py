#solve for the maximum number of clusters we can have in order for the maximum spanning distance to be 3

f = open("BigClusters.txt", "r")
nodes = []
i = 0
for line in f:
    string_entries = line.split()
    row = [int(n) for n in string_entries]
    nodes.append([row, i])
    i += 1

"""

nodes = [[[8, 24], 0], [[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 1],
        [[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0], 2],
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 3],
        [[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 4],
        [[0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], 5],
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0], 6],
        [[0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0], 7],
        [[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0], 8]]
"""


#find number of nodes and number of bits
N = nodes[0][0][0]
BITS = nodes[0][0][1]


#get rid of first entry in nodes
nodes[0] = nodes.pop()


#sort nodes by first bit
nodes.sort()

#check if two nodes are equal except for the last [distance] number of bits (which must all be unequal)
def close(node1, node2, bits, distance):
    for i in range(bits - distance):
        if node1[i] != node2[i]:
            return False
    for i in range(bits - distance, bits):
        if node1[i] == node2[i]:
            return False
    return True

#initialize list of edges
edge_list = []

#define the function that goes through a sorted list and adds close nodes to edge list
#note that there may be non-adjacent nodes that the function misses when there are consecutive nodes
#with the same value, but extracting the adjacent pairs alone will be enough to make sure that all nodes
#separated by [distance] are connected in our eventual clusters
def add_to_edge_list(edge_list, nodes, bits, distance):
    for i in range(1, len(nodes)):     
        if close(nodes[i - 1][0], nodes[i][0], bits, distance):
            edge = [distance, nodes[i - 1][1], nodes[i][1]]
            edge_list.append(edge)
           

#define the function that changes the order of a certain number of bits in each node
#this is done so that the nodes can be sorted to compare values at different positions
def swap (nodes, num_list, bits):
    for i in range(len(nodes)):
        for j in range(len(num_list)):
            nodes[i][0][num_list[j]], nodes[i][0][bits - j - 1] = nodes[i][0][bits - j - 1], nodes[i][0][num_list[j]]

def swap_reverse (nodes, num_list, bits):
    for i in range(len(nodes)):
        for j in range(len(num_list)):
            nodes[i][0][num_list[j]], nodes[i][0][bits - len(num_list) + j] = nodes[i][0][bits - len(num_list) + j], nodes[i][0][num_list[j]]


#add to the edge list the edges of length 0
add_to_edge_list(edge_list, nodes, BITS, 0)

#for each sorted nodes list with a different bit in the final position, add the edges of distance 1
for i in range(BITS):
    swap(nodes, [i], BITS)
    nodes.sort()
    add_to_edge_list(edge_list, nodes, BITS, 1)
    swap(nodes, [i], BITS)

#now do the same but with distance 2, sorting the list by all possible pairs of positions
for i in range(BITS - 1):
    for j in range(i + 1, BITS):
        swap(nodes, [j, i], BITS)
        nodes.sort()
        add_to_edge_list(edge_list, nodes, BITS, 2)
        swap_reverse(nodes, [i, j], BITS)

#the rest of the program mostly replicates the code of cluster1.py
 
#create list of vertices, with each list entry in the form [leader, size of cluster (if leader), [list of connected nodes]]
#initialize each entry, i, to [i, 1, []]
#create unused entry in index 0 so that nodes are in the index that corresponds to their number, starting with 1
vertices = [None] * (N + 1)
for i in range(1, N + 1):
    vertices[i] = [i, 1, []]

#set the pointer that will keep track of which edge is the next minimum, and initialize it to 0
counter = 0

#define the function that finds the next edge to add to our graph, returning a list of the form [edge, new value of counter]
#if we've run out of edges, return [[-1, -1, -1], -1]
def next_edge(v_table, costs, counter):
    if counter == len(costs):
        return [[-1, -1, -1], -1]
    edge = costs[counter]
    #find leaders of the two vertices
    l1, l2 = v_table[edge[1]][0], v_table[edge[2]][0]
    #if they're equal, they belong to the same cluster and we need to try again
    while l1 == l2:
        counter += 1
        if counter == len(costs):
            return [[-1, -1, -1], -1]
        edge = costs[counter]
        l1, l2 = v_table[edge[1]][0], v_table[edge[2]][0]
    #now that l1 and l2 are unequal, we can return the edge and new position of the counter
    return [edge, counter + 1]

#initialize found_list to use for vertices search in breadth-first-search algorithm
found_vertices = [False] * len(vertices)

#use breadth-first search to find all vertices connected to a vertex in the graph so far
def find_cluster(v_table, vertex, found_vertices):
    #create a list of all the vertices to keep track of which ones we've found
    cluster = []
    #create a queue and add the vertex to it, and set its value in the found_vertices table to true
    found_vertices[vertex] = True
    q = [vertex]
    #for each item in the queue, find its children and, if they haven't been found, add them to a temp queue and then
    #add them to the main queue after transfering the main queue's items to the cluster list
    while len(q) > 0:
        tempq = []
        for i in range(len(q)):
            parent = q[i]
            for j in range(len(v_table[parent][2])):
                new_v = v_table[parent][2][j]
                #see if new node hasn't been found
                if found_vertices[new_v] == False:
                    found_vertices[new_v] = True
                    tempq.append(new_v)
        #transfer the parent vertices we've already searched to the cluster list and add the new vertices to the queue
        cluster += q.copy()
        q = tempq.copy()
    #set the value of all the found_vertices entries we changed back to False so the next breadth-first search can use it again
    for i in range(len(cluster)):
        found_vertices[cluster[i]] = False
    #return the found vertices
    return cluster 

#define the function that will add a new edge to the graph, and update the clusters:
def add_to_graph(v_table, costs, counter, found_vertices):
    #first, find the next edge to add find its leaders, and then determine which of the two clusters is smaller
    edge_and_counter = next_edge(v_table, costs, counter)
    edge, new_counter = edge_and_counter[0], edge_and_counter[1]
    if new_counter == -1:
        return new_counter
    a, b = edge[1], edge[2]
    l1, l2 = v_table[a][0], v_table[b][0]
    smaller, bigger = l1, l2
    if v_table[l2][1] < v_table[l1][1]:
        smaller, bigger = l2, l1
    #increase the size of the bigger leader by the size of the smalelr (note: only the size of leaders will be accurate in v_table, which is
    #fine for our purposes)
    v_table[bigger][1] += v_table[smaller][1]
    #now find all of the vertices in the smaller cluster
    small_cluster = find_cluster(v_table, smaller, found_vertices)
    #change the leader of all the vertices in the smaller cluster to the leader of the bigger cluster
    for i in range(len(small_cluster)):
        v_table[small_cluster[i]][0] = bigger
    #now update the graph by adding the edge to it
    v_table[a][2].append(b)
    v_table[b][2].append(a)
    #finally, return the new counter
    return new_counter

#find the number of edges we've added to our graph:
num_edges = 0
while counter >= 0:
    counter = add_to_graph(vertices, edge_list, counter, found_vertices)
    if counter >= 0:
        num_edges += 1

#the number of clusters left is equal to the number of nodes minus the number of edges we've added
answer = N - num_edges
print(N)
print(num_edges)
print(answer)

