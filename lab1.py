# written by Litong Peng (lp5629)


import queue
import sys
import time
from math import inf
import numpy
from PIL import Image
from pixel import pixel


# the program that read the terrain image
def read_terrain_image(terrain_image):
    # initiate the terrain list
    terrain = []
    # open file
    file = Image.open(terrain_image)
    # convert rgb pixel
    rgb_terrain = file.convert('RGB')
    # for every pixel
    for i in range(395):
        for j in range(500):
            # get r,g,b value from each pixel
            r, g, b = rgb_terrain.getpixel((i, j))
            # the r,g,b value for open land
            if (r == 248) and (g == 148) and (b == 18):
                # append the terrain to the terrain list
                terrain.append('open_land')
                # the r,g,b value for rough meadow
            elif (r == 255) and (g == 192) and (b == 0):
                # append the terrain to the terrain list
                terrain.append('rough_meadow')
                # the r,g,b value for easy movement forest
            elif (r == 255) and (g == 255) and (b == 255):
                # append the terrain to the terrain list
                terrain.append('easy_movement_forest')
                # the r,g,b value for slow run forest
            elif (r == 2) and (g == 208) and (b == 60):
                # append the terrain to the terrain list
                terrain.append('slow_run_forest')
                # the r,g,b value for walk forest
            elif (r == 2) and (g == 136) and (b == 40):
                # append the terrain to the terrain list
                terrain.append('walk_forest')
                # the r,g,b value for impassible vegetation
            elif (r == 5) and (g == 73) and (b == 24):
                # append the terrain to the terrain list
                terrain.append('impassible_vegetation')
                # the r,g,b value for lake,swamp and marsh
            elif (r == 0) and (g == 0) and (b == 255):
                # append the terrain to the terrain list
                terrain.append('lake_swamp_marsh')
                # the r,g,b value for paved road
            elif (r == 71) and (g == 51) and (b == 3):
                # append the terrain to the terrain list
                terrain.append('paved_road')
                # the r,g,b value for footpath
            elif (r == 0) and (g == 0) and (b == 0):
                # append the terrain to the terrain list
                terrain.append('footpath')
                # otherwise, it is out of bound
            else:
                # append the terrain to the terrain list
                terrain.append('out_of_bounds')
    # return the terrain list
    return terrain


# the program that read the elevation file
def read_elevation_file(elevation_file):
    # initiate the elevation list
    elevation = []
    # open the file
    file = open(elevation_file)
    # for each line
    for line in file:
        # only need the first 395 elevation
        for word in line.strip(' ').split('   ')[:395]:
            # transfer it from scientific notation to normal number
            elevation.append((eval(word)))
    # return the elevation list
    return elevation


# the program that build the original map
def terrain_and_elevation(terrain, elevation):
    # initiate the original map dictionary
    original_map = {}
    # for every pixel
    i = 0
    for x in range(395):
        for y in range(500):
            # the key is coordinate x and y, value is its pixel form
            original_map[(x, y)] = pixel(x, y, elevation[i], terrain[i], None, 0)
            i += 1
    # return the original map dictionary
    return original_map


# the program check if the pixel's neighbors are all lake
def not_surround(pix, original):
    # for all neighbors
    for neighbor in pix.find_neighbors():
        # if there is one neighbor not lake
        if original.get(neighbor).color != 'lake_swamp_marsh':
            # that means not all neighbors are lake
            return True
    # else: all neighbors are lake
    return False


# the program draws the winter map
def winter(original):
    # 7 rounds
    for i in range(7):
        # for all pixels
        for o in original.values():
            # if it is lake and not all of its neighbors are lake,
            # which is lake edges
            if o.color == 'lake_swamp_marsh' and not_surround(o, original):
                # fro all neighbors
                for neighbor in o.find_neighbors():
                    # if it is lake
                    if original.get(neighbor).color == 'lake_swamp_marsh':
                        # change it to iced
                        original.get(neighbor).color = 'winter_lake'
    # return the winter map
    return original


# the program that draws the spring map
def spring(original):
    # for every pixel
    for o in original.values():
        # build a queue to store the 15 rounds for each pixel on lake edges
        Q = queue.Queue()
        # if it is lake and not all of its neighbors are lake,
        # which is lake edges
        if o.color == 'lake_swamp_marsh' and not_surround(o, original):
            # initiate the first tuple to the pixel,
            # the first[1] is used to calculate the height difference between this original pixel to the new pixel
            first = (o, o)
            # put the first pixel into the queue
            Q.put(first)
            # count the 15 rounds
            count = 0
            # while queue is not empty and no more than 15 rounds
            while not Q.empty() and count < 15:
                # for each neighbors of this pixel
                for neighbor in Q.get()[0].find_neighbors():
                    # if it is not in the lake
                    # and the height difference between the original one to it less than one meter
                    if original.get(neighbor).color != 'lake_swamp_marsh' and (
                            original.get(neighbor).z - first[1].z) < 1:
                        # put it into the queue, so we can find its neighbors continually
                        Q.put((original.get(neighbor), o))
                        # set its speed
                        original.get(neighbor).color = 'spring_lake'
                # count plus one
                count += 1
    # return the spring map
    return original


# the program deal with the seanson
def seasonal(original, season):
    # if it is summer
    if season == 'summer':
        # just return the original map
        return original
    # if it is fall
    elif season == 'fall':
        # for all pixels
        for o in original.values():
            # if it is easy movement forest
            if o.color == 'easy_movement_forest':
                # change its speed to "easy movement forest fall"
                o.color = 'easy_movement_forest_fall'
        # return the map
        return original
    elif season == 'winter':
        return winter(original)
    elif season == 'spring':
        return spring(original)


# the program rean the path file
def read_path_file(path_file):
    # initiate the points list
    points = []
    # open file
    file = open(path_file)
    # for each line
    for line in file:
        # coordinate x is the first element
        x = int(line.strip(' ').replace('\n', '').split(' ')[0])
        # coordinate y is the second element
        y = int(line.strip(' ').replace('\n', '').split(' ')[1])
        # add it to the list
        points.append((x, y))
    # return the points list
    return points


# the program calculate the speed
def calculate_speed(pix):
    if pix.color == 'open_land':
        return 10
    elif pix.color == 'rough_meadow':
        return 2
    elif pix.color == 'easy_movement_forest':
        return 8
    # when it is fall, it is easier to move on the easy_movement_forest
    elif pix.color == 'easy_movement_forest_fall':
        return 9
    elif pix.color == 'slow_run_forest':
        return 5
    elif pix.color == 'walk_forest':
        return 4
    elif pix.color == 'impassible_vegetation':
        return 0
    elif pix.color == 'lake_swamp_marsh':
        return 0
    # when it is winter, people can walk on the iced lake
    elif pix.color == 'winter_lake':
        return 10
    # when it is spring, people barely can walk on the lake
    elif pix.color == 'spring_lake':
        return 1
    elif pix.color == 'paved_road':
        return 10
    elif pix.color == 'footpath':
        return 10
    elif pix.color == 'out_of_bounds':
        return 0


# the program calculate the g value
def calculate_g(current, neighbor):
    # calculate the distance from two points
    distance = numpy.sqrt(
        pow(10.29 * (current.x - neighbor.x), 2) + pow(7.55 * (current.y - neighbor.y), 2) + pow(
            (current.z - neighbor.z), 2))
    # if you want to take the slope into count
    # slope = (current.z - neighbor.z) / (
    #     numpy.sqrt(pow(10.29 * (current.x - neighbor.x), 2) + pow(7.55 * (current.y - neighbor.y), 2)))
    # if current.z <= neighbor.z:
    #     if slope <= 1 / 2:
    #         s = 1
    #     elif 1 / 2 < slope <= 1:
    #         s = 0.9
    #     else:
    #         s = 0.8
    # else:
    #     if slope <= 1 / 2:
    #         s = 1
    #     elif 1 / 2 < slope <= 1:
    #         s = 1.1
    #     else:
    #         s = 1.2
    # speed = s * (calculate_speed(current) + calculate_speed(neighbor)) / 2
    # calculate the average speed
    speed = (calculate_speed(current) + calculate_speed(neighbor)) / 2
    # if speed is not 0
    if speed != 0:
        # return the speed
        return distance / speed
    # if it is impassible
    else:
        # return infinity
        return float(inf)


# the program calculate the heuristic value
def calculate_h(current, neighbor):
    return numpy.sqrt(
        pow(10.29 * (current.x - neighbor.x), 2) + pow(7.55 * (current.y - neighbor.y), 2) + pow(
            (current.z - neighbor.z), 2)) / 10


# the program find the best frontier in remaining with the lowest f value
def lowest(remaining):
    # print(remaining)
    # initiate the minimum f value to infinite
    minimum = float(inf)
    # for every frontier in remaining
    for r in remaining:
        # if it is smaller
        if r[1] < minimum:
            # change the minimum f value to this
            minimum = r[1]
            # change the best frontier to this
            frontier = r[0]
    # return the best frontier and its f value
    return frontier, minimum


# the program check whether it exists in remaining list
def not_show_before(neighbor, remaining):
    # for every element in remaining list
    for e in remaining:
        # if yes
        if (e[0].x == neighbor.x) and (e[0].y == neighbor.y):
            return False
    # if no
    return True


# the program check whether it exists in explored list
def already_explored(neighbor, explored):
    # for every element in explored list
    for e in explored:
        # if yes
        if (e.x == neighbor.x) and (e.y == neighbor.y):
            return False
    # if no
    return True


# the main program A* search algorithm
def a_star(current, goal, maps):
    # initiate the node to the begining node
    node = current
    # initiate the remaining list which store the explored nodes but not been choosen in that step
    remaining = []
    # initiate the explored list which store the explored noded and been used in that step
    explored = []
    # initiate the g value of first node to 0
    node.g = 0
    # while the node is not the goal
    while (node.x != goal.x) or (node.y != goal.y):
        # if the remaining list is not empty
        if remaining:
            # frontier and its f value in the best in remaining list
            frontier, frontier_f = lowest(remaining)
        # if the remaining list is empty
        else:
            # initiate the frontier and its f value to the begining node and ininity
            frontier, frontier_f = node, float(inf)
        # for every neighbor of this node
        for n in node.find_neighbors():
            # get its pixel form
            neighbor = maps.get(n)
            # if it has not been explored and not in the remaining list
            if (not_show_before(neighbor, remaining)) and (already_explored(neighbor, explored)):
                # the neighbor's g value is the sum of the g value of this node
                # and the g value betwen the node to the neighbor
                g = node.g + calculate_g(node, neighbor)
                # add its g value to its pixel form
                neighbor.g = g
                # its f value is its g value plus its heuristic value
                temp_f = g + calculate_h(neighbor, goal)
                # link the node to its neighbor
                neighbor.before = node
                # add the neighbor to the remaining list
                remaining.append((neighbor, temp_f))
                # if its f vlue is smaller
                if temp_f < frontier_f:
                    # then the frontier is this neighbor
                    frontier = neighbor
                    # and the best value till now is this neighbor's f value
                    frontier_f = temp_f
        # add this frontier node to the explored list
        explored.append(frontier)
        # for every element in remaining list
        for r in remaining:
            # if it is frontier
            if r[0].x == frontier.x and r[0].y == frontier.y:
                # then remove it
                remaining.remove(r)
        # change the node to this frontier
        node = frontier


# the program that recoed the best path backwards
def path(current, goal):
    # add the goal pixel to the list
    p = [goal]
    # while the node before the goal is not the begining node
    while goal.before != current:
        # add the node before the goal
        p.append(goal.before)
        # goal is the node before it
        goal = goal.before
    # add the begining node to the list
    p.append(current)
    # return the path list
    return p


# the program that output the image
def output_image(output_image_filename, result, terrain_image):
    # open the original image
    img = Image.open(terrain_image)
    # set the new color to draw the image
    route_color = (128, 0, 128)
    # for every path in result list
    for r in result:
        # for every pixel in path list
        for rr in r:
            # draw
            img.putpixel((rr.x, rr.y), route_color)
    # save the image
    img.save(output_image_filename)
    # show the image
    img.show()


# the main program
def main():
    # the first file given on command line
    terrain_image=sys.argv[1]
    # the second file given on command line
    elevation_file=sys.argv[2]
    # the third file given on command line
    path_file=sys.argv[3]
    # the forth file given on command line
    season=sys.argv[4]
    # the fifth file given on command line
    output_image_filename=sys.argv[5]

    # read the terrain image
    terrain = read_terrain_image(terrain_image)
    # read the elevation file
    elevation = read_elevation_file(elevation_file)
    # the original map
    original_map = terrain_and_elevation(terrain, elevation)
    # the seasonal map
    maps = seasonal(original_map, season)
    # read the path file
    points = read_path_file(path_file)
    # initiate the path list
    points_list = []
    # for every point in path
    for point in points:
        # add it to the path list
        points_list.append(maps.get(point))
    # initiate the result list
    result = []
    # for every point in the path list
    for i in range(len(points_list) - 1):
        # the beginning point
        current = points_list[i]
        # the goal point
        goal = points_list[i + 1]
        # using the A* algorithm to find the best path
        a_star(current, goal, maps)
        # trace backwards to record the best path
        pa = path(current, goal)
        # add it to the result list
        result.append(pa)
    # output the image
    output_image(output_image_filename, result, terrain_image)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(time.time() - start_time)
