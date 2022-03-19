#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Yash Pratap Solanky, ysolanky
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import sys
from math import tanh, cos, asin, sqrt, pi


def get_roads(roads,start):

    list_roads = []
    for road in roads:
        road = road.rstrip("\n")
        if road.split(" ")[0] == start:
            list_roads.append((road.split(" ")))
    return list_roads

# from https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
def distance_bw(lat1, lon1, lat2, lon2):
    p = pi/180
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p) * cos(lat2*p) * (1-cos((lon2-lon1)*p))/2
    return 12742 * asin(sqrt(a)) * 0.621371
#End of code from stack overflow

def calc_distance(list1,string1,string2):

    if string2 and string1 in list1:
        return distance_bw(list1[string1][0], list1[string1][1], list1[string2][0], list1[string2][1])
    else:
        return 0 #I am returning 0 incase both the cities are not in our dictionary of longitutes and latitutes.


def get_route(start, end, cost):

    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    # The dictionary that we return at the end
    final_dict = {}

    #Loading the segments dataset
    roads_txt = open("road-segments.txt", "r")
    roads_list = roads_txt.readlines()
    roads = roads_list.copy()

    #Making a copy of every road and changing it from A-B to B-A, to make traversing easier as all roads are 2 way
    for sv in roads_list:
        # print(sv.split(" "))
        temp = sv.split(" ")[0]
        temp1 = sv.split(" ")[1]
        temp2 = sv.split(" ")[2]
        temp3 = sv.split(" ")[3]
        temp4 = sv.split(" ")[4]
        svs = temp1 + " " + temp + " " + temp2 + " " + temp3 + " " + temp4
        roads.append(svs)

    #Loading in the coordinates
    gps = open("city-gps.txt", "r")
    city_lat_long = {}
    for a in gps:
        city_lat_long[a.split(" ")[0]] = [float(a.split(" ")[1]), float(a.split(" ")[2])]

    #Fringe structure = Start, Entire row, End, Segments, Total miles, Total hours, Route taken, Delivery hours, heuristic
    fringe = []
    visited = []
    max_speed = 0
    #Adding successors of the start city to the fringe based on cost function given
    for i in roads:
        i = i.rstrip("\n")

        if int(i.split(" ")[3]) >= max_speed:
            max_speed = int(i.split(" ")[3])

        if i.split(" ")[0] == start:

            route_taken = [(i.split(" ")[1], i.split(" ")[4])]

            length = float(i.split(" ")[2])
            speed = float(i.split(" ")[3])
            time_taken = length / speed
            if speed >= 50:
                time_taken_delivery = time_taken + (tanh(length/1000)*2*(time_taken))
            else:
                time_taken_delivery = time_taken
            if cost == "distance":
                fringe.append([start, i.split(" "), i.split(" ")[1], 1, float(i.split(" ")[2]), time_taken, route_taken,
                           time_taken_delivery, float(i.split(" ")[2])+ (calc_distance(city_lat_long,i.split(" ")[1], end))])
            if cost == "segments":
                fringe.append([start, i.split(" "), i.split(" ")[1], 1, float(i.split(" ")[2]), time_taken, route_taken,
                           time_taken_delivery, 1])
            if cost == "time":
                fringe.append([start, i.split(" "), i.split(" ")[1], 1, float(i.split(" ")[2]), time_taken, route_taken,
                           time_taken_delivery, time_taken + (calc_distance(city_lat_long,i.split(" ")[1], end))/max_speed])
            if cost == "delivery":
                fringe.append([start, i.split(" "), i.split(" ")[1], 1, float(i.split(" ")[2]), time_taken, route_taken,
                           time_taken_delivery, time_taken_delivery + (calc_distance(city_lat_long,i.split(" ")[1], end))/max_speed])

    while len(fringe) > 0:

        fringe.sort(key=lambda x: x[8]) #Sorting the the last element of the fringe
        curr_route = fringe.pop(0) #popping the first element of the fringe
        #print(curr_route)
        visited.append(curr_route[1]) #Adding the current road to the visited list

        if cost == "distance":

            if curr_route[2] == end:
                final_dict["route-taken"] = curr_route[6]
                final_dict["total-segments"] = curr_route[3]
                final_dict["total-hours"] = curr_route[5]
                final_dict["total-miles"] = curr_route[4]
                final_dict["total-delivery-hours"] = curr_route[7]
                return final_dict

            successor_roads = get_roads(roads, curr_route[2])

            for i in successor_roads:

                if i not in visited:

                    visited.append(i)

                    route_taken = curr_route[6].copy()
                    route_taken.append((i[1], i[4]))
                    time_taken_n = float(curr_route[5])
                    time_taken_d = float(curr_route[7])
                    time_taken_c = float(i[2]) / float(i[3])

                    if int(i[3]) >= 50:
                        time_taken_delivery = time_taken_d + time_taken_c + (2 * tanh(float(i[2]) / 1000) * (time_taken_d + time_taken_c))
                    else:
                        time_taken_delivery = time_taken_d + time_taken_c

                    dist = calc_distance(city_lat_long, i[1], end)

                    # if dist == 0:
                    #     dist = curr_route[8] - float(i[2])

                    heu = int(curr_route[4]) + int(i[2]) + dist
                    #heu is the f(s). g(s) is the distance travelled so far. the h(s) is the long/lat distance.

                    fringe.append([i[0], i, i[1], int(curr_route[3]) + 1, float(curr_route[4]) + float(i[2]),
                                       time_taken_n + time_taken_c, route_taken, time_taken_delivery, heu])

        if cost == "segments":

            if curr_route[2] == end:
                final_dict["route-taken"] = curr_route[6]
                final_dict["total-segments"] = curr_route[3]
                final_dict["total-hours"] = curr_route[5]
                final_dict["total-miles"] = curr_route[4]
                final_dict["total-delivery-hours"] = curr_route[7]
                return final_dict

            successor_roads = get_roads(roads, curr_route[2])

            for i in successor_roads:

                if i not in visited:

                    visited.append(i)

                    route_taken = curr_route[6].copy()
                    route_taken.append((i[1], i[4]))
                    time_taken_n = float(curr_route[5])
                    time_taken_d = float(curr_route[7])
                    time_taken_c = float(i[2]) / float(i[3])

                    if int(i[3]) >= 50:
                        time_taken_delivery = time_taken_d + time_taken_c + (2 * tanh(float(i[2]) / 1000) * (time_taken_d + time_taken_c))
                    else:
                        time_taken_delivery = time_taken_d + time_taken_c

                    heu = int(curr_route[3]) + 1
                    #heu is the f(s). g(s) is the number of segments. I am not using a heuristic with segments. As I
                    # do not think with longitutes and latitudes, we can find a heuristic that is meaningful to the number of
                    # segments

                    fringe.append([i[0], i, i[1], int(curr_route[3]) + 1,  float(curr_route[4]) + float(i[2]),
                                       time_taken_n + time_taken_c, route_taken, time_taken_delivery, heu])

        if cost == "time":

            if curr_route[2] == end:
                final_dict["route-taken"] = curr_route[6]
                final_dict["total-segments"] = curr_route[3]
                final_dict["total-hours"] = curr_route[5]
                final_dict["total-miles"] = curr_route[4]
                final_dict["total-delivery-hours"] = curr_route[7]
                return final_dict

            successor_roads = get_roads(roads, curr_route[2])

            for i in successor_roads:

                if i not in visited:

                    visited.append(i)

                    route_taken = curr_route[6].copy()
                    route_taken.append((i[1], i[4]))
                    time_taken_n = float(curr_route[5])
                    time_taken_d = float(curr_route[7])
                    time_taken_c = float(i[2]) / float(i[3])

                    if int(i[3]) >= 50:
                        time_taken_delivery = time_taken_d + time_taken_c + (2 * tanh(float(i[2]) / 1000) * (time_taken_d + time_taken_c))
                    else:
                        time_taken_delivery = time_taken_d + time_taken_c

                    heu = time_taken_n + time_taken_c + (calc_distance(city_lat_long, i[1], end))/max_speed

                    # heu is the f(s). g(s) is the time taken so far. the h(s) is the distance from the current city to
                    # to goal divided by the speed of the current road

                    fringe.append([i[0], i, i[1], int(curr_route[3]) + 1,  float(curr_route[4]) + float(i[2]),
                                       time_taken_n + time_taken_c, route_taken, time_taken_delivery, heu])

        if cost == "delivery":

            if curr_route[2] == end:
                final_dict["route-taken"] = curr_route[6]
                final_dict["total-segments"] = curr_route[3]
                final_dict["total-hours"] = curr_route[5]
                final_dict["total-miles"] = curr_route[4]
                final_dict["total-delivery-hours"] = curr_route[7]
                return final_dict

            successor_roads = get_roads(roads, curr_route[2])

            for i in successor_roads:

                if i not in visited:

                    visited.append(i)

                    route_taken = curr_route[6].copy()
                    route_taken.append((i[1], i[4]))
                    time_taken_n = float(curr_route[5])
                    time_taken_d = float(curr_route[7])
                    time_taken_c = float(i[2]) / float(i[3])

                    if int(i[3]) >= 50:
                        time_taken_delivery = time_taken_d + time_taken_c + (2 * tanh(float(i[2]) / 1000) * (time_taken_d + time_taken_c))
                    else:
                        time_taken_delivery = time_taken_d + time_taken_c

                    heu = time_taken_delivery + calc_distance(city_lat_long, i[1], end)/max_speed

                    # heu is the f(s). g(s) is the time taken so far. the h(s) is the distance from the current city to
                    # to goal in the speed of the current road

                    fringe.append([i[0], i, i[1], int(curr_route[3]) + 1, float(curr_route[4]) + float(i[2]),
                                       time_taken_n + time_taken_c, route_taken, time_taken_delivery, heu])

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.3f" % result["total-hours"])
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])