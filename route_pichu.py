#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : [Yash Pratap Solanky, ysolanky]
#
# Based on skeleton code provided in CSCI B551, Fall 2021.

import sys

# Parse the map from a given filename
def parse_map(filename):
        with open(filename, "r") as f:
                return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
                
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
        return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
        moves = ((row+1,col), (row-1,col), (row,col-1), (row,col+1))

        # Return only moves that are within the house_map and legal (i.e. go through open space ".")
        return [move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]

# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

def search(house_map):
        # Find pichu start position
        pichu_loc = [(row_i, col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i] == "p"][0]
        visited = set() # Created a visited set so that we do not visit any position more than once
        direction = "" #defined direction as empty as it will store the direction we will take
        fringe = [(pichu_loc, 0, direction)] #I modified the fringe to also store the direction that we are taking

        while fringe:

                (curr_move, curr_dist, dist) = fringe.pop(0) #instead of pop(), I used pop(0) so that we use fringe like a queue and not a stack. Thereby performing BFS and not DFS
                for move in moves(house_map, *curr_move):

                        if house_map[move[0]][move[1]]=="@":
                                return (curr_dist+1, dist + dir_path(move,curr_move))
                        elif move not in visited: #Not in visited implements the use of the set that we created earlier
                                visited.add(move)# We add the current move to the set
                                fringe.append((move, curr_dist + 1, dist + dir_path(move,curr_move))) #Adding the move, current distance +1 and the dir_path function which calculates the direction.

        return ["-1", ""] #If the fringe is empty that means that we have searched all possible moves without returning the goal state. So we return -1.

def dir_path(move1,move2): #I created this function to be able to figure out which direction the move is taking place in compared to our previous move.
        direction = ""
        if move1[0] < move2[0] and move1[1] == move2[1]: #If row1<row2 and columns are same we can conclude that its an upwards move. Similarly we calculare D,R and L.
                direction = direction + "U"
        elif move1[0] > move2[0] and move1[1] == move2[1]:
                direction = direction + "D"
        elif move1[1] > move2[1] and move1[0] == move2[0]:
                direction = direction + "R"
        elif move1[1] < move2[1] and move1[0] == move2[0]:
                direction = direction + "L"

        return direction #This function just returns 1 direction. Which is added to previous direction in the search function when dir_path is called .

# Main Function
if __name__ == "__main__":
        house_map=parse_map(sys.argv[1])
        print("Shhhh... quiet while I navigate!")
        solution = search(house_map)
        print("Here's the solution I found:")
        print(str(solution[0]) + " " + solution[1])