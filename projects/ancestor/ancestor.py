def earliest_ancestor(ancestors, starting_node):
    # Turn the ancestors list into an adjacency list
    adjacency_list = {}

    for ancestor_pair in ancestors:
        # add both vertices to adjacency_list
        if ancestor_pair[0] not in adjacency_list:
            adjacency_list[ancestor_pair[0]] = set()
        if ancestor_pair[1] not in adjacency_list:
            adjacency_list[ancestor_pair[1]] = set()
        # add the edge between the two vertices
        adjacency_list[ancestor_pair[1]].add(ancestor_pair[0])

    print(adjacency_list)

    # Create a queue
    queue = [ [starting_node] ]
    # create a visited set of vertices
    visited = set()

    max_path_length = 1
    current_earliest_ancestor = -1

    while len(queue) > 0:
        # dequeue the current path + vertex
        current_path = queue.pop(0)
        # get the current vertex out of the path
        current_vertex = current_path[-1]

        # if the vertex has not been visited
        if current_vertex not in visited:
            # add the vertex to the visited set
            visited.add(current_vertex)

            print(current_path)
            if len(current_path) > max_path_length or len(current_path) >= max_path_length and current_vertex < current_earliest_ancestor:
                max_path_length = len(current_path)
                current_earliest_ancestor = current_vertex
            # explore the neighbors
            # add the neighbor vertices to the queue (make sure to build the new paths)
            for neighbor in adjacency_list[current_vertex]:
                # copy the current path
                new_path = list(current_path)
                # add the neighbor to it
                new_path.append(neighbor)
                queue.append(new_path)

    return current_earliest_ancestor