"""
input_costs = [9, 
                [1, 2, 2], [1, 3, 200], [1, 4, 200], [1, 5, 5], [1, 6, 200], [1, 7, 200], [1, 8, 200], [1, 9, 200],
                [2, 3, 50], [2, 4, 3], [2, 5, 10], [2, 6, 200], [2, 7, 200], [2, 8, 200], [2, 9, 200],
                [3, 4, 75], [3, 5, 200], [3, 6, 200], [3, 7, 200], [3, 8, 200], [3, 9, 200],
                [4, 5, 1], [4, 6, 200], [4, 7, 200], [4, 8, 200], [4, 9, 200],
                [5, 6, 200], [5, 7, 200], [5, 8, 100], [5, 9, 200],
                [6, 7, 3], [6, 8, 200], [6, 9, 200],
                [7, 8, 200], [7, 9, 200],
                [8, 9, 200]]

"""

#define the function that finds the next edge to add to our graph, returning a list of the form [edge, new value of counter]
def next_edge(v_table, costs, counter):
    edge = costs[counter]
    #find leaders of the two vertices
    l1, l2 = v_table[edge[1]][0], v_table[edge[2]][0]
    #if they're equal, they belong to the same cluster and we need to try again
    while l1 == l2:
        counter += 1
        edge = costs[counter]
        l1, l2 = v_table[edge[1]][0], v_table[edge[2]][0]
    #now that l1 and l2 are unequal, we can return the edge and new position of the counter
    return [edge, counter + 1]

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


def read_input_costs(filename):
    input_costs = []
    with open(filename,"r") as f:
        for line in f:
            string_entries = line.split()
            row = [int(n) for n in string_entries]
            input_costs.append(row)

    return input_costs

def main():
    #solve for the maximum spanning distance with k = 4 clusters

    input_costs = read_input_costs("SmallClusters.txt")

    #find number of vertices
    n = input_costs[0][0]

    #define the number of clusters we want
    K = 4

    #create list of vertices, with each list entry in the form [leader, size of cluster (if leader), [list of connected nodes]]
    #initialize each entry, i, to [i, 1, []]
    #create unused entry in index 0 so that nodes are in the index that corresponds to their number, starting with 1
    vertices = [[i,1,[]] for i in range(n+1) ]

    #next, sort the list of edges by using the existing input_costs array, removing the first element,
    #reordering the entries for each edge so that cost apears first and then using the python sort() method
    input_costs[0] = input_costs.pop()
    for i in range(len(input_costs)):
        input_costs[i][0], input_costs[i][1], input_costs[i][2] = input_costs[i][2], input_costs[i][0], input_costs[i][1]
    input_costs.sort()

    #the pointer that will keep track of which edge is the next minimum
    counter = 0

    #initialize found_list to use for vertices search in breadth-first-search algorithm
    found_vertices = [False] * len(vertices)

    for i in range(n - K):
        counter = add_to_graph(vertices, input_costs, counter, found_vertices)


    #after finishing Kruskal's algorithm, the next edge in our list will have length equal to the 
    #maximum spanning distance
    print(next_edge(vertices, input_costs, counter))


if __name__=="__main__":
    main()

