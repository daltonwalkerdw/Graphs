from room import Room
from player import Player
from world import World


import random
from ast import literal_eval

# Load world
world = World()

class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


def find_unexplored(room):
    for direction in room:
        if room[direction] == '?':
            return direction
    return None


def find_direction(current_room, target_room_id):
    for direction in current_room:
        if current_room[direction] == target_room_id:
            return direction
    return None


def move_map(player):
    path = []
    starting_room = player.current_room.id
    graph = {}
    unexplored_paths = 0

    graph[starting_room] = {}
    for e in player.current_room.get_exits():
        graph[starting_room][e] = '?'
        unexplored_paths += 1

    reverse_directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

    while unexplored_paths > 0:
        current_room = player.current_room.id

        # check if current room has unexplored paths
        if '?' in graph[current_room].values():
            # if so,
            # find an unexplored direction from current room
            direction = find_unexplored(graph[current_room])
            player.travel(direction)
            next_room = player.current_room.id
            # add direction to path
            path.append(direction)
            graph[current_room][direction] = player.current_room.id
            if not next_room in graph:
                graph[next_room] = {}
                for e in player.current_room.get_exits():
                    graph[next_room][e] = '?'
                    unexplored_paths += 1
            graph[next_room][reverse_directions[direction]] = current_room
            unexplored_paths -= 2

        else:
            # if no paths left,
            # perform a bfs to find nearest room with unexplored path

            q = Queue()

            q.enqueue([current_room])

            visited = set()

            while q.size() > 0:

                p = q.dequeue()

                room = p[-1]

                direction = find_unexplored(graph[room])

                # check if room has any unexplored exits
                if direction is not None:

                    for i in range(len(p) - 1):
                        d = find_direction(graph[p[i]], p[i + 1])

                        path.append(d)
                        # move player
                        player.travel(d)

                    break

                if room not in visited:

                    # mark as visited
                    visited.add(room)
                    # enqueue paths to neighboring rooms
                    for e in graph[room]:
                        p_copy = p.copy()
                        p_copy.append(graph[room][e])
                        q.enqueue(p_copy)

    return path


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = move_map(player)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")