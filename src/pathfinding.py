import heapq
import math
import R
import libtcodpy as libtcod

__author__ = 'Emily'

STRAIGHT = 2
DIAG = STRAIGHT + STRAIGHT

GRASS = 15
MOUNTAIN = 40
PATH = 5


class PathNode:
    OPEN = 0
    CLOSED = 1

    def __init__(self, grid, cost, parentNode=None, endNode=None):
        self.grid = grid #location
        self.cost = cost #cost of journey to this node so far.
        # self.cost = 0 #cost of  and estimate for distance left
        self.open = self.OPEN

        self.parent_node = parentNode
        self.end_node = endNode

        # if self.end_node != None:
        #     self.cost = self.direct_cost + self.find_heuristic(self.grid, self.end_node.grid)

    def __str__(self):
        return str(self.grid)

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    def __eq__(self, other):
        return hash(str(self)) == hash(str(other))

    def find_heuristic(self, start, end):
        return heuristic(start, end)

    def is_equal_to_node(self, node):
        if node.grid == self.grid:
            return True

        if node.grid[0] == self.grid[0] and node.grid[1] == self.grid[1]:
            return True

        return False


class Pather:
    OPEN = 0
    CLOSED = 1

    STRAIGHT = STRAIGHT  #
    DIAG = DIAG

    def __init__(self):
        self.node_status = {}

        self.node_costs = {}
        self.open_list = []  # # the HIGHEST cost is at the LOWEST index number.
        self.frontier = PriorityQueue()
        self.end = None
        self.start = None
        self.largest_cost = 0
        self.heuristic_cost = 0
        self.actual_cost = 0

    def check_blocked(self, point):
        x = point[0]
        y = point[1]

        if 0 > x or x >= len(self.tiles) or 0 > y or y >= len(self.tiles[0]) or self.tiles[x][y].blocked:
            return True

        return False

    def replace_node(self, possible_node):
        old_grid = possible_node.grid
        old_cost = self.node_costs[old_grid]
        if self.node_status.has_key(old_grid) and self.node_status[old_grid] == self.OPEN:
            # index = self.get_node_binary(old_cost, old_grid)
            # if index != -1:
            self.open_list.remove(possible_node)
            # del self.open_list[index]
            self.add_node(possible_node)
        else:
            print "already been removed from lists. ADDING"
            self.add_node(possible_node)


            # del self.node_status[old_node]
            #self.open_list.remove()

    def new_find_path(self, start, end, tiles=[]):
        t0 = libtcod.sys_elapsed_seconds()

        if len(tiles) == 0:
            self.tiles = R.tiles
        else:
            self.tiles = tiles
        if self.check_blocked(start) and self.check_blocked(end):
            return None
        if self.tiles[start[0]][start[1]].continent != self.tiles[end[0]][end[1]].continent:
            print "not on same continent"
            return None

        self.frontier = PriorityQueue()
        self.node_costs = {}
        self.node_status = {}
        self.came_from = {}
        self.largest_cost = 0

        self.end = end_node = PathNode(end, 0)
        self.start = start_node = PathNode(start, 0, endNode=end_node)

        self.heuristic_cost = heuristic_straightline(start,end)

        self.frontier.put(start_node, 0)
        self.node_costs[start_node] = 0

        while not self.frontier.empty():
            current = self.frontier.get()

            if current.is_equal_to_node(end_node) and current == end_node:
                t1 = libtcod.sys_elapsed_seconds()
                path = self.reconstruct_path(self.came_from, start_node, end_node)
                print "path of length: ", len(path), " succeeded in %s" % (t1 - t0), "explored ", len(self.node_costs.keys())

                print "heuristic_cost:", self.heuristic_cost, " Actual cost:", self.node_costs[end_node]
                # return current #TODO: reconstruct path.
                path.reverse()
                return path
            else:
                for neighbour in self.find_neighbours(current, end_node):
                    new_cost = neighbour.cost
                    # if self.node_costs.has_key(neighbour):
                    if new_cost < self.node_costs.get(neighbour, float("inf")):
                        if self.largest_cost < new_cost:
                            self.largest_cost = new_cost
                        self.node_costs[neighbour] = new_cost
                        self.frontier.put(neighbour, new_cost + heuristic_straightline(neighbour.grid, end_node.grid))
                        self.came_from[neighbour] = current

    def find_path(self, start, end, tiles=[]):

        t0 = libtcod.sys_elapsed_seconds()
        if len(tiles) == 0:
            self.tiles = R.tiles
        else:
            self.tiles = tiles

        if len(tiles) <= 0 or start[0] < 0 or start[1] < 0 or end[0] < 0 or end[1] < 0:
            print "FALSE"
            return None

        if self.check_blocked(start) and self.check_blocked(end):
            print str(start[0]), "/", str(start[1]), "to" + str(end[0]), "/", str(end[1]) + " tile was not traversable."
            return None

        if self.tiles[start[0]][start[1]].continent != self.tiles[end[0]][end[1]].continent:
            print "not on same continent"
            return None

        self.open_list = []
        self.node_costs.clear()
        self.node_status.clear()
        self.largest_cost = 0

        self.end = end_node = PathNode(end, 0)
        self.start = start_node = PathNode(start, 0, endNode=end_node)
        # print "weeee let's go."
        self.add_node(start_node)

        while len(self.open_list) > 0:
            current_node = self.open_list[len(self.open_list) - 1]  #putting this to 0 is cool.
            #check to see if the end has been reached.
            if current_node.is_equal_to_node(end_node):# and current_node == self.open_list[0]: #why does this need to be 0?
                best_path = []
                while current_node != None:
                    best_path.insert(0, current_node.grid)
                    current_node = current_node.parent_node
                #return the path of grid points.
                t1 = libtcod.sys_elapsed_seconds()
                print "path of length: ", len(best_path), " succeeded in %s" % (t1 - t0), "explored ", \
                    len(self.node_costs.keys()), "and open nodes left: " + str(len(self.open_list))
                # print "open_list is " + str(len(self.open_list)) + " long"
                # print "path succeeded in %s" % (t1 - t0)
                t0 = t1
                return best_path
            else:
                if current_node.is_equal_to_node(end_node) and current_node != self.open_list[0]:
                    current_node = self.open_list[len(self.open_list) - 2]
                #do this
                if current_node.grid[0] < 0 or current_node.grid[1] < 0:
                    print "uh-oh somehow it's a minus!"
                    return None

                self.open_list.remove(current_node)
                self.node_status[current_node.grid] = self.CLOSED
                if self.node_costs[current_node.grid] != current_node.cost:
                    print "for some reason, the current grid costs don't match the dictionary.... fixing.."
                    self.node_costs[current_node.grid] = current_node.cost

                #                 if self.node_costs.has_key(current_node.grid):
                #                     #node_costs is used to track the nodes. so this NEEDS to be removed.
                #                     self.node_costs.pop(current_node.grid, 0)
                #                 else:
                #                     print "NODE WAS NOT IN NODE_COSTS"
                #                     continue

                for neighbour in self.find_adjacent_nodes_3(current_node, end_node):
                    if self.node_status.has_key(neighbour.grid):
                        if self.node_status[neighbour.grid] == self.CLOSED:
                            continue
                        if self.node_status[neighbour.grid] == self.OPEN or neighbour.cost < self.node_costs[
                            neighbour.grid]:
                            if neighbour.cost >= self.node_costs[neighbour.grid]:
                                continue
                            else:
                                self.replace_node(neighbour)
                    else:
                        self.add_node(neighbour)
                        if self.largest_cost < neighbour.cost:
                            self.largest_cost = neighbour.cost
                self.node_status[current_node.grid] = self.CLOSED
                # current_node = None

        print "failed", len(self.open_list), start[0], start[1], " --- > ", end[0], end[1]
        t1 = libtcod.sys_elapsed_seconds()
        print "path failed in %s" % (t1 - t0)
        t0 = t1
        return None

    def add_node(self, node):
        cost = node.cost
        index = self.add_to_open_list_(cost, node)
        self.open_list.insert(index, node)
        self.node_costs[node.grid] = cost
        self.node_status[node.grid] = node.open

    def add_to_open_list(self, node):
        index = 0
        cost = node.cost

        while len(self.open_list) > index and cost < self.open_list[index].cost:
            index += 1

        self.open_list.insert(index, node)
        self.node_status[node.grid] = node.open
        self.node_costs[node.grid] = node.cost

    def get_node_binary(self, cost, grid, high=-1, low=0):
        # TODO: finish this.
        #NOT FINISHED
        length = len(self.open_list)
        index = -1

        if high == -1:
            high = length - 1

        mid = (high + low) / 2

        if (length <= 0):
            return -1
        else:
            if length == 1:
                if self.open_list[0].cost == cost:
                    return 0
                else:
                    print "bloop"
                    return -1

            elif length == 2:
                if self.open_list[0].cost == cost:
                    return 0
                elif self.open_list[1].cost == cost:
                    return 1
                else:
                    return 2
            else:
                if self.open_list[high].cost == cost:
                    if self.open_list[high].grid[0] == grid[0] and self.open_list[high].grid[1] == grid[1]:
                        #print "returning as it's the same."
                        return high
                    else:
                        #need to cycle through any that cost the same.
                        print "not returning as not the same grid"
                        return -1
                elif self.open_list[mid].cost == cost:
                    if self.open_list[mid].grid[0] == grid[0] and self.open_list[mid].grid[1] == grid[1]:
                        #print "returning as it's the same."
                        return mid
                    else:
                        print "not returning as not the same grid"
                        return -1
                elif self.open_list[low].cost == cost:
                    if self.open_list[low].grid[0] == grid[0] and self.open_list[low].grid[1] == grid[1]:
                        #print "returning as it's the same."
                        return low
                    else:
                        print "not repturning as not the same grid"
                        return -1
                else:
                    if cost < self.open_list[low].cost and cost > self.open_list[high].cost:
                        if self.open_list[mid].cost >= cost:
                            index = self.get_node_binary(cost, grid, mid, low)
                        elif self.open_list[mid].cost < cost:
                            index = self.get_node_binary(cost, grid, high, mid)
                    else:
                        #print "didn't find in open list"
                        return -1

        return index

    def add_to_open_list_(self, cost, node, high=-1, low=0):
        index = -1
        length = len(self.open_list)
        if high == -1:
            high = length - 1
        mid = (high + low) / 2
        if (length <= 0):
            return 0
        else:
            if length == 1:
                if self.open_list[0].cost > cost:
                    return 1
                elif self.open_list[0].cost <= cost:
                    return 0
            elif length == 2:
                if self.open_list[0].cost <= cost:
                    return 0
                elif self.open_list[1].cost <= cost:
                    return 1
                else:
                    return 2
            else:
                if mid == length - 1:
                    if self.open_list[mid].cost > cost:
                        index = mid + 1
                    elif self.open_list[mid].cost <= cost:
                        index = mid
                elif mid == 0:
                    if self.open_list[0].cost > cost:
                        index = 1
                    elif self.open_list[0].cost <= cost:
                        index = 0
                else:
                    if self.open_list[mid].cost > cost and self.open_list[mid + 1].cost < cost:
                        return mid + 1
                    elif self.open_list[0].cost < cost and self.open_list[mid - 1].cost > cost:
                        return mid
                    elif self.open_list[0].cost > cost:
                        index = self.add_to_open_list_(cost, node, high, mid + 1)
                    elif self.open_list[0].cost < cost:
                        index = self.add_to_open_list_(cost, node, mid - 1, low)
        return index

    def find_adjacent_nodes_2(self, current, end):
        nodes = []
        X = current.grid[0]
        Y = current.grid[1]
        # distance = current.diag_heuristic(current.grid, end.grid)
        # distance = current.find_heuristic(current.grid, end.grid)
        # distance *= (1.0 + 1 / 1000)  # agh
        # distance = distance + (distance * 0.1) #current distance + 10% so that it excludes directly away from the target.
        length_x = len(self.tiles) - 1
        length_y = len(self.tiles[0]) - 1

        #Orthogonal directions
        point = (X - 1, Y)  #left

        if X > 0 and not self.check_blocked(point) :
            nodes.append(PathNode(point, self.get_cost(point) + current.cost , current, end))
        point = (X + 1, Y)  #right

        if X < length_x and not self.check_blocked(point):
            nodes.append(PathNode(point, self.get_cost(point) + current.cost , current, end))
        point = (X, Y - 1)  #Up

        if Y > 0 and not self.check_blocked(point):
            nodes.append(PathNode(point, self.get_cost(point) + current.cost , current, end))
        point = (X, Y + 1)  #Down

        if Y < length_y and not self.check_blocked(point):
            nodes.append(PathNode(point, self.get_cost(point) + current.cost , current, end))

        #Diagonal directions.
        point = (X - 1, Y - 1)  #upleft

        if X > 0 and Y > 0 and not self.check_blocked(point) :
            nodes.append(PathNode(point, self.get_cost(point) + current.cost, current, end))
        point = (X - 1, Y + 1)  #down left

        if X > 0 and Y < length_y and not self.check_blocked(point) :
            nodes.append(PathNode(point, self.get_cost(point) + current.cost, current, end))
        point = (X + 1, Y - 1)  #up-right

        if X < length_x and Y > 0 and not self.check_blocked(point) :
            nodes.append(PathNode(point, self.get_cost(point) + current.cost, current, end))
        point = (X + 1, Y + 1)  #down-right

        if X < length_x and Y < length_y and not self.check_blocked(point) :
            nodes.append(PathNode(point, self.get_cost(point) + current.cost, current, end))

        return nodes

    def find_adjacent_nodes_3(self, current, end):
        nodes = []
        X = current.grid[0]
        Y = current.grid[1]
        # distance = current.diag_heuristic(current.grid, end.grid)
        distance = current.find_heuristic(current.grid, end.grid)
        distance *= (1.0 + 1 / 1000)  # agh
        # distance = distance + (distance * 0.1) #current distance + 10% so that it excludes directly away from the target.
        length_x = len(self.tiles) - 1
        length_y = len(self.tiles[0]) - 1

        #Orthogonal directions
        point = (X - 1, Y)  #left
        new_distance = current.find_heuristic(point, end.grid)
        if X > 0 and not self.check_blocked(point) and new_distance < distance:
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.STRAIGHT, current, end))
        point = (X + 1, Y)  #right
        new_distance = current.find_heuristic(point, end.grid)
        if X < length_x and not self.check_blocked(point) and new_distance < distance:
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.STRAIGHT, current, end))
        point = (X, Y - 1)  #Up
        new_distance = current.find_heuristic(point, end.grid)
        if Y > 0 and not self.check_blocked(point)  and new_distance < distance:
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.STRAIGHT, current, end))
        point = (X, Y + 1)  #Down
        new_distance = current.find_heuristic(point, end.grid)
        if Y < length_y and not self.check_blocked(point) and new_distance < distance:
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.STRAIGHT, current, end))

        #Diagonal directions.
        point = (X - 1, Y - 1)  #upleft
        new_distance = current.find_heuristic(point, end.grid)
        if X > 0 and Y > 0 and not self.check_blocked(point) and new_distance < distance:
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.DIAG, current, end))
        point = (X - 1, Y + 1)  #down left
        new_distance = current.find_heuristic(point, end.grid)
        if X > 0 and Y < length_y and not self.check_blocked(point) and new_distance < distance:
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.DIAG, current, end))
        point = (X + 1, Y - 1)  #up-right
        new_distance = current.find_heuristic(point, end.grid)
        if X < length_x and Y > 0 and not self.check_blocked(point) and new_distance < distance:
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.DIAG, current, end))
        point = (X + 1, Y + 1)  #down-right
        new_distance = current.find_heuristic(point, end.grid)
        if X < length_x and Y < length_y and not self.check_blocked(point) and new_distance < distance:
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.DIAG, current, end))

        return nodes

    def get_cost(self, point):
        # gets the cost of tile-movement.
        cost = self.tiles[point[0]][point[1]].cost
        return cost

    def find_neighbours(self, current, end_node):
        neighbours = []
        for dirx in xrange(-1, 2):
            for diry in xrange(-1, 2):
                if not (dirx == 0 and diry == 0):
                    x = current.grid[0] + dirx
                    y = current.grid[1] + diry
                    if not self.check_blocked((x,y)):
                        if dirx == 0 or diry == 0: #orthogonal
                            neighbours.insert(0, PathNode((x,y),
                                                        self.get_cost((x,y)) + current.cost, # + self.STRAIGHT,,
                                                        current,
                                                        end_node))
                        else: #diagonal
                            neighbours.append(PathNode((x,y),
                                                        self.get_cost((x,y)) + current.cost + 1, # + self.STRAIGHT,,
                                                        current,
                                                        end_node))


        # if (current.grid[0] + current.grid[1]) % 2 == 0: neighbours.reverse() # aesthetics
        return neighbours

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = [current.grid]
        while current != start:
            current = came_from[current]
            path.append(current.grid)

        return path

class Graph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def neighbours(self, id):
        return self.edges[id]

    def add_edge(self, node, neighbours = []):
        self.nodes[tuple(node.location)] = node
        self.edges[tuple(node.location)] = neighbours

    def add_connection(self, node, new_neighbours):
        if self.edges.has_key(tuple(node.location)):
            (self.edges[tuple(node.location)].append(neighbour) for neighbour in new_neighbours)

    def cost(self, a, b):
        return self.nodes.get(a).cost(self.nodes.get(b))


class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = [] #impassable
        self.weights = {}

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbours(self, id):
      (x, y) = id
      # results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)] #orthogonal only
      results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1), (x+1, y+1), (x-1, y-1), (x-1, y+1), (x-1, y+1)] #all directions
      if (x + y) % 2 == 0: results.reverse() # aesthetics
      results = filter(self.in_bounds, results)
      results = filter(self.passable, results)
      return results

    def cost(self, a, b):
        c = self.weights.get(b, 1)
        return c


class PriorityQueue:
   def __init__(self):
      self.elements = []

   def empty(self):
      return len(self.elements) == 0

   def put(self, item, priority):
      heapq.heappush(self.elements, (priority, item))

   def get(self):
      return heapq.heappop(self.elements)[1]


class PathFinder():
    def __init__(self):
        self.frontier = PriorityQueue()
        self.came_from = {}
        self.node_costs = {}
        self.largest_cost = 0


    def dijkstra_search(self, graph, start, goal):
        #todo: factor in the technology - can the ship travel the distances between nodes?
        #todo: possibly havea seperate function that constructs a graph of reachable nodes to use for this.
        self.frontier = PriorityQueue()
        self.frontier.put(start, 0)

        self.came_from = {}
        self.node_costs = {}
        self.came_from[start] = None
        self.node_costs[start] = 0

        while not self.frontier.empty():
            current = self.frontier.get()

            if current == goal:
                break

            for next in graph.neighbours(current):
                new_cost = self.node_costs[current] + graph.cost(current, next)
                if next not in self.node_costs or new_cost < self.node_costs[next]:
                    self.node_costs[next] = new_cost  #cost
                    priority = new_cost
                    self.frontier.put(next, priority)
                    self.came_from[next] = current

        return self.came_from, self.node_costs


    def find_path(self, world, start, goal):

        if world.tiles[start[0]][start[1]].continent != world.tiles[goal[0]][goal[1]].continent:
            print "not on same continent"
            return None
        t0 = libtcod.sys_elapsed_seconds()
        graph = SquareGrid(R.MAP_WIDTH, R.MAP_HEIGHT)
        graph.walls = world.blocked
        graph.weights = world.weights
        came_from, costs = self.a_star(graph, start, goal)
        path = self.reconstruct_path(came_from, start, goal)
        path.reverse()
        t1 = libtcod.sys_elapsed_seconds()
        print "path found in ", (t1-t0), " explored ", len(self.node_costs)
        return path

    def a_star(self, graph, start, goal):
        #todo: factor in the technology - can the ship travel the distances between nodes?
        #todo: possibly have a seperate function that constructs a graph of reachable nodes to use for this.
        self.frontier = PriorityQueue()
        self.frontier.put(start, 0)

        self.came_from = {}
        self.node_costs = {}
        self.largest_cost = 0
        self.came_from[start] = None
        self.node_costs[str(start)] = 0

        while not self.frontier.empty():
            current = self.frontier.get()

            if current == goal:
                break

            for next in graph.neighbours(current):
                new_cost = self.node_costs[str(current)] + graph.cost(current, next)
                if str(next) not in self.node_costs or new_cost < self.node_costs[str(next)]:
                    self.node_costs[str(next)] = new_cost
                    #cost, plus distance to end.
                    priority = new_cost + heuristic(goal, next)
                    self.frontier.put(next, priority)
                    self.came_from[next] = current
                    if new_cost > self.largest_cost:
                        self.largest_cost = new_cost

        return self.came_from, self.node_costs


    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = [current]
        while current != start:
            current = came_from[current]
            path.append(current)

        return path


class Node():
    def __init__(self, name, location, cost): #parent=None, end=None):
        self.name = name
        self.location = location #tuple?
        self.direct_cost = cost #cost of entering node
        #
        # self.cost = self.direct_cost

    def cost(self, node):
        """

        :param node: other node
        :return: direct cost of entry of other node plus distance.
        """
        return node.direct_cost + heuristic(self.location, node.location)

    def __str__(self):
        return str(self.location)

    def __hash__(self):
        # print(hash(str(self)))
        return hash(str(self))

    def __eq__(self, other):
        return hash(str(self)) == hash(str(other))





def heuristic(a, b):
   (x1, y1) = a
   (x2, y2) = b
   return abs(x1 - x2) + abs(y1 - y2)


def heuristic_straightline(node, end):
    return math.sqrt((end[0] - node[0]) ** 2 + (end[1] - node[1]) ** 2)


# def diag_heuristic( start, end):
#     # dx = abs(start[0] - end[0])
#     #         dy = abs(start[1] - end[1])
#     #         return 10 * max(dx, dy)
#
#     dx = abs(start[0] - end[0])
#     dy = abs(start[1] - end[1])
#     beep = STRAIGHT * (dx + dy) + (DIAG - 2 * STRAIGHT) * min(dx, dy)  #+ (dx + dy)* GRASS
#     return beep
#
# def manhattan_distance( (x1,y1), (x2, y2)):
#     return abs(x1 - x2) + abs(y1 - y2)
#
# def heuristic( node, end):
#     return math.sqrt((end[0] - node[0]) ** 2 + (end[1] - node[1]) ** 2)
#
# def linear_cost():
#     dx = self.end_node.grid[0] - self.grid[0]
#     dy = self.end_node.grid[1] - self.grid[1]
#
#     dx = abs(dx)
#     dy = abs(dy)
#
#     tempCost = 10 * min(dx, dy) + 10 * (max(dx, dy) - min(dx, dy))
#     return tempCost
#
# def LinearCost( point):
#     dx = point[0] - self.grid[0]
#     dy = point[1] - self.grid[1]
#
#     dx = abs(dx)
#     dy = abs(dy)
#
#     tempCost = 10 * min(dx, dy) + 10 * (max(dx, dy) - min(dx, dy))
#     return tempCost