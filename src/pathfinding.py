import math
import R

__author__ = 'Emily'



STRAIGHT = 5
DIAG = math.sqrt(2*STRAIGHT)*STRAIGHT


GRASS = 15
MOUNTAIN = 40
PATH = 5

class Pather:
    OPEN = 0
    CLOSED = 1

    STRAIGHT = STRAIGHT#
    DIAG = DIAG

    def __init__(self):
        self.node_status = {}
        self.node_costs = {}
        self.open_list = [] ## the HIGHEST cost is at the LOWEST index number.


    def check_blocked(self,point):
        x = point[0]
        y = point[1]

        if self.tiles[x][y].blocked:
            return True

        return False


    def replace_node(self, possible_node):
        old_grid = possible_node.grid
        old_cost = self.node_costs[old_grid]
        if self.node_status.has_key(old_grid) and self.node_status[old_grid] == self.OPEN:
            index = self.get_node_binary(old_cost, old_grid)
            if index != -1:
                del self.open_list[index]
                self.add_node(possible_node)
        else:
            print "already been removed from lists. ADDING"
            self.add_node(possible_node)


        #del self.node_status[old_node]
        #self.open_list.remove()


    def find_path(self,start, end, tiles = []):

        if len(tiles) == 0:
            self.tiles = R.tiles
        else:
            self.tiles = tiles

        if len(tiles) <= 0 or start[0] < 0 or start[1] < 0 or end[0] < 0 or end[1] < 0:
            print "FALSE"
            return None

        if self.check_blocked(start) and self.check_blocked(end):
            print str(start[0]), "/",str(start[1]),"to" + str(end[0]), "/",str(end[1]) + " tile was not traversable."
            return None

        if self.tiles[start[0]][start[1]].continent != self.tiles[end[0]][end[1]].continent:
            print "not on same continent"
            return None


        self.open_list = []
        self.node_costs.clear()
        self.node_status.clear()

        end_node = PathNode(end, 0)
        start_node = PathNode(start, 0, endNode=end_node)
        #print "weeee let's go."
        self.add_node(start_node)

        while len(self.open_list) > 0:
            current_node = self.open_list[len(self.open_list)-1] #putting this to 0 is cool.
            #check to see if the end has been reached.
            if current_node.is_equal_to_node(end_node) and current_node == self.open_list[0]:
                best_path = []
                while current_node != None:
                    best_path.insert(0, current_node.grid)
                    current_node = current_node.parent_node
                #return the path of grid points.
                print "open_list is " + str(len(self.open_list)) + " long"
                return best_path
            else:
                if current_node.is_equal_to_node(end_node) and current_node != self.open_list[0]:
                    current_node = self.open_list[len(self.open_list)-2]
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

                for neighbour in self.find_adjacent_nodes_2(current_node, end_node):
                    if self.node_status.has_key(neighbour.grid):
                        if self.node_status[neighbour.grid] == self.CLOSED:
                            continue
                        if self.node_status[neighbour.grid] == self.OPEN or neighbour.cost < self.node_costs[neighbour.grid]:
                            if neighbour.cost >= self.node_costs[neighbour.grid]:
                                continue
                            else:
                                self.replace_node(neighbour)
                    else:
                        self.add_node(neighbour)
                self.node_status[current_node.grid] = self.CLOSED
                current_node = None


        print "failed", len(self.open_list), start[0], start[1], " --- > ", end[0],end[1]
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
        #TODO: finish this.
        #NOT FINISHED
        length = len(self.open_list)
        index = -1

        if high == -1:
            high = length - 1

        mid = (high+low) /2

        if(length <= 0):
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
        mid = (high+low) /2
        if(length <= 0):
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
                if mid == length -1:
                    if self.open_list[mid].cost > cost:
                        index = mid+1
                    elif self.open_list[mid].cost <= cost:
                        index = mid
                elif mid == 0:
                    if self.open_list[0].cost > cost:
                        index = 1
                    elif self.open_list[0].cost <= cost:
                        index = 0
                else:
                    if self.open_list[mid].cost > cost and self.open_list[mid+1].cost < cost:
                        return mid +1
                    elif self.open_list[0].cost < cost and self.open_list[mid-1].cost > cost:
                        return mid
                    elif self.open_list[0].cost > cost:
                        index = self.add_to_open_list_(cost, node, high, mid+1)
                    elif self.open_list[0].cost < cost:
                        index = self.add_to_open_list_(cost, node, mid-1, low)
        return index



    def find_adjacent_nodes_2(self,current,end):
        nodes = []
        X = current.grid[0]
        Y = current.grid[1]
        distance = current.diag_heuristic(current.grid,end.grid)
        distance *= (1.0 + 1/1000)# agh
        #distance = distance + (distance * 0.1) #current distance + 10% so that it excludes directly away from the target.
        length_x = len(self.tiles) - 1
        length_y = len(self.tiles[0]) - 1

        #Orthogonal directions
        point = (X-1, Y)#left
        new_distance = current.diag_heuristic(point,end.grid)
        if X > 0 and not self.check_blocked(point) and new_distance < distance:
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.STRAIGHT, current, end))
        point = (X+1, Y)#right
        new_distance = current.diag_heuristic(point,end.grid)
        if X < length_x and  not self.check_blocked(point) and new_distance < distance:
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.STRAIGHT, current, end))
        point = (X, Y-1)#Up
        new_distance = current.diag_heuristic(point,end.grid)
        if Y > 0 and not self.check_blocked(point) and new_distance < distance:
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.STRAIGHT, current, end))
        point = (X, Y+1)#Down
        new_distance = current.diag_heuristic(point,end.grid)
        if Y < length_y and not self.check_blocked(point) and new_distance < distance:
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.STRAIGHT, current, end))

        #Diagonal directions.
        point = (X-1, Y-1)  #upleft
        new_distance = current.diag_heuristic(point,end.grid)
        if X > 0 and Y > 0 and not self.check_blocked(point) and new_distance < distance:
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.DIAG, current, end))
        point = (X-1, Y+1)#down left
        new_distance = current.diag_heuristic(point,end.grid)
        if X > 0 and Y < length_y and not self.check_blocked(point) and new_distance < distance:
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.DIAG, current, end))
        point = (X+1, Y-1)#up-right
        new_distance = current.diag_heuristic(point,end.grid)
        if X < length_x and Y > 0 and not self.check_blocked(point) and new_distance < distance:
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.DIAG, current, end))
        point = (X+1, Y+1)#down-right
        new_distance = current.diag_heuristic(point,end.grid)
        if X < length_x and Y < length_y and not self.check_blocked(point) and new_distance < distance:
            nodes.append(PathNode(point, self.get_cost(point) + current.cost + self.DIAG, current, end))


        return nodes

    def get_cost(self, point):
        #gets the cost of tile-movement.
        cost = self.tiles[point[0]][point[1]].cost
        return cost

class PathNode:
    OPEN = 0
    CLOSED = 1


    def __init__(self, grid, cost, parentNode=None, endNode=None):
        self.grid = grid
        self.direct_cost = cost
        self.cost = 0
        self.open = self.OPEN

        self.parent_node = parentNode
        self.end_node = endNode

        if self.end_node != None:
            self.cost = self.direct_cost + self.diag_heuristic(self.grid, self.end_node.grid)

    def diag_heuristic(self,start, end):
#         dx = abs(start[0] - end[0])
#         dy = abs(start[1] - end[1])
#         return 10 * max(dx, dy)

        dx = abs(start[0] - end[0])
        dy = abs(start[1] - end[1])
        beep = STRAIGHT * (dx + dy) + (DIAG - 2 * STRAIGHT) * min(dx, dy) #+ (dx + dy)* GRASS
        return beep

    def heuristic(self, node, end):
        return math.sqrt((end[0] - node[0])**2 + (end[1] - node[1])**2)

    def linear_cost(self):
        dx = self.end_node.grid[0] - self.grid[0]
        dy = self.end_node.grid[1] - self.grid[1]

        dx = abs(dx)
        dy = abs(dy)

        tempCost = 10 * min(dx, dy) + 10 * (max(dx, dy) - min(dx, dy))
        return tempCost

    def LinearCost(self, point):
        dx = point[0] - self.grid[0]
        dy = point[1] - self.grid[1]

        dx = abs(dx)
        dy = abs(dy)

        tempCost = 10 * min(dx, dy) + 10 * (max(dx, dy) - min(dx, dy))
        return tempCost

    def is_equal_to_node(self, node):
        if node.grid == self.grid:
            return True

        if node.grid[0] == self.grid[0] and node.grid[1] == self.grid[1]:
            return True

        return False