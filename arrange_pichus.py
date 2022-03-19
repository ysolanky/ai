#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : [Yash Pratap Solanky]
#
# Based on skeleton code in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
    return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
    return "\n".join(["".join(row) for row in house_map])

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
    return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

# Get list of successors of given house_map state
def successors(house_map):
    return [add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == '.']

# check if house_map is a goal state
def is_goal(house_map, k):
    return count_pichus(house_map) == k

def is_pichu(house_map):
    pichu_loc = [(row_i, col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i] == "p"] #Identifying location of 'p' on the map. Took this line of code from route_pichu.py
    count = 0 #I make use of a counter to not return True or False prematurely.

    for (i,j) in pichu_loc: #Looping through pichu_loc. It will contain coordinates of all "p" on the map.
        for (a,b) in pichu_loc:
            if i==a and j==b: #If they are the same, we can continue
                continue
            elif i < a and j == b: #If they are upwards of one another
                if is_wall(house_map,i,j,a,b) == True: #If there is a wall or @ in between them then we can continue
                    continue
                count =+ 1 #if there is no wall in between them then they can see one another. So we add to the count.
            elif i > a and j == b: #Downwards
                if is_wall(house_map,i,j,a,b) == True:
                    continue
                count =+ 1
            elif j > b and i == a: #Towards Right
                if is_wall(house_map,i,j,a,b) == True:
                    continue
                count =+ 1
            elif j < b and i == a: #Towards Left
                if is_wall(house_map,i,j,a,b) == True:
                    continue
                count =+ 1
            elif i<a and j>b and i-a==j-b: #left downwards diagonal
                if is_wall(house_map,i,j,a,b) == True:
                    continue
                count = + 1
            elif i<a and j<b and i-a== -(j-b): #right upwards diagonal
                if is_wall(house_map,i,j,a,b) == True:
                    continue
                count = + 1
            elif i>a and j<b and i-a== -(j-b):
                if is_wall(house_map,i,j,a,b) == True:
                    continue
                count = + 1
            elif i>a and j>b and i-a==j-b: #left upwards diagonal
                if is_wall(house_map,i,j,a,b) == True:
                    continue
                count = + 1

    if count > 0:
        return False #If count is increased for any condition that means that one pichu can see another pichu, so we return False
    else:
        return True #If count is still 0 like we initilaised then we return true, meaning that no pichu cans ee another pichu.

def is_wall(house_map,i,j,a,b): #Another function to check if there is a wall in between "p"
    obstacle = [(row_i, col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i] in ["X","@"]] #As we have to treat "@" like a wall as well, we look for it along with "X"
    for c,d in obstacle: #If any of these conditions indicating a X or @ between p's is fulfiled we figure out that they cannot see one another.
        if i<c<a and j == b == d: #wall is in between 2 pichus on the same column
            return True
        elif a<c<i and j == b == d: #wall is in between 2 pichus on the same column
            return True
        elif b < d < j and i == c == a: #wall is in between 2 pichus on the same row
            return True
        elif j < d < b and i == c == a: #wall is in between 2 pichus on the same row
            return True
        elif i<c<a and j>d>b and i-a==j-b: #There is a wall in the diagonal of 2 pichus. Similarly, for the other 3 possible diagonals.
            return True
        elif i<c<a and j<d<b and i-a== -(j-b):
            return True
        elif i>c>a and j<d<b and i-a== -(j-b):
            return True
        elif i>c>a and j>d>b and i-a==j-b:
            return True

# Arrange agents on the map
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_house_map,k):
    fringe = [initial_house_map]
    visited = [] #We make a visited set just to add each house map to it to avoid visiting same ones more times

    while len(fringe) > 0:
        for new_house_map in successors(fringe.pop(0)):#we again change pop() to pop(0) so as to perfrom BFS and not DFS.

            if is_pichu(new_house_map) == True and new_house_map not in visited: #Making sure this house map passes our is_pichu function and therfore passes is_wall function while we check if it in in visited list
                visited.append(new_house_map) #As its not already in the list, we add it to it.
                if is_goal(new_house_map,k):
                    return(new_house_map,True)
                fringe.append(new_house_map)
    return ['',False] #If the fringe is empty that means that we have searched all possible moves without returning the goal state. So we return False.


# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])
    # This is k, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
    solution = solve(house_map, k)
    print ("Here's what we found:")
    print (printable_house_map(solution[0]) if solution[1] else "False")


