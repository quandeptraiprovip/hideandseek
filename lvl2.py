import vision
import heapq
import copy
import drawlv2
from node import Node
import random

def update_matrix(x, y, matrix):
  a, b = vision.find_seeker(matrix)
  matrix[a][b] = 7
  matrix[x][y] = 3
  matrix = vision.vision(x, y, matrix)

  n = len(matrix)
  m = len(matrix[0])

  return matrix

def get_all_cells(matrix):
  x, y = vision.find_seeker(matrix)
  n = len(matrix)
  m = len(matrix[0])
  matrix_cop = copy.deepcopy(matrix)


  def dfs(i, j, visited):
    if i < 0 or i >= n or j < 0 or j >= m or matrix_cop[i][j] == 1:
      return
    
    visited.append((i, j))
    matrix_cop[i][j] = 1
    
    dfs(i + 1, j, visited)
    dfs(i - 1, j, visited)
    dfs(i, j + 1, visited)
    dfs(i, j - 1, visited)

  visited = []
  dfs(x, y, visited)

  return visited

def a_star(start_position, goal_position, matrix):
  grid_size = (len(matrix), len(matrix[0]))
  def heuristic(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])
  
  def get_neighbors(position, grid_size):
    x, y = position
    row, col = grid_size
    neighbors = [(x-1, y), (x+1, y), (x, y-1),  (x-1, y-1), (x, y+1), (x-1, y+1), (x+1, y-1), (x+1, y+1)]
    valid_neighbors = [(i, j) for i, j in neighbors if 0 <= i < row and 0 <= j < col and matrix[i][j] != 1]
    return valid_neighbors
  
  open_list = []
  closed_list = []

  start_node = Node(start_position)
  goal_node = Node(goal_position)

  heapq.heappush(open_list, (start_node.f, start_node))

  while open_list:
    current_node = heapq.heappop(open_list)[1]
    closed_list.append(current_node)

    if current_node.position == goal_node.position:
      path = []
      while current_node:
        path.append(current_node.position)
        current_node = current_node.parent
      return path[::-1]

    for neighbor_pos in get_neighbors(current_node.position, grid_size):
      neighbor_node = Node(neighbor_pos, current_node)
      if neighbor_node in closed_list:
        continue
        
      neighbor_node.g = current_node.g + 1
      neighbor_node.h = heuristic(neighbor_node.position, goal_position)
      neighbor_node.f = neighbor_node.g + neighbor_node.h

      # Update the node's parent if the new path is better
      for node in open_list:
        if node[1] == neighbor_node and neighbor_node.g > node[1].g:
          break
      else:
        heapq.heappush(open_list, (neighbor_node.f, neighbor_node))

  return None

def cells_around_announce(center_x, center_y, matrix):
  cells_around = []
  for i in range(center_x - 3, center_x + 3 + 1):
    for j in range(center_y - 3, center_y + 3 + 1):
      if 0 <= i < len(matrix) and 0 <= j < len(matrix[0]) and matrix[i][j] != 1:
        cells_around.append((i, j))
  return cells_around

def move(matrix):
  unvisited = get_all_cells(matrix)
  n = len(unvisited)
  path = []
  announce = []
  a, b = (len(matrix), len(matrix[0]))

  x, y = vision.find_seeker(matrix)
  hiders = vision.find_hider(matrix)
  # print(hiders)
  n_announce = 1

  unvisited.pop(0)
  current = (x, y)

  def get_announce(announce, n, hiders):
    for i in range(n):

      random_number1 = random.randint(-3, 3)
      random_number2 = random.randint(-3, 3)

      while (not (0 <= random_number1 + hiders[i][0] < a and 0 <= random_number2 + hiders[i][1] < b)) or matrix[random_number1 + hiders[i][0]][random_number2 + hiders[i][1]] == 1 or ((random_number1 + hiders[i][0],random_number2 + hiders[i][1]) in hiders):
        random_number1 = random.randint(-3, 3)
        random_number2 = random.randint(-3, 3)

      announce.append((random_number1 + hiders[i][0], random_number2 + hiders[i][1]))

    print(n)

  while unvisited:
    n_path = len(path)
    goal = unvisited[0]
    unvisited.pop(0)
    catch = []

    matrix = update_matrix(current[0], current[1], matrix)

    moves = a_star(current, goal, matrix)
    moves.pop(0)
    
    matrix_cop = copy.deepcopy(matrix)

    # doan nay xu ly khi dang di ma gap announce
    if n_announce > 1:
      for i, move in enumerate(moves):
        if i == 5:
          break

        matrix_cop = update_matrix(move[0], move[1], matrix_cop)
        flag = False

        for location in announce[len(announce) - len(hiders):]:

          if matrix_cop[location[0]][location[1]] == 7:

            matrix = matrix_cop
            temp = cells_around_announce(location[0], location[1], matrix)

            for t in temp:
              if t in unvisited:
                unvisited.pop(unvisited.index(t))
            
            unvisited = temp + unvisited

        if flag:
          for j in range(len(moves) - 1, i, -1):
            moves.pop(j)


    if len(moves) + n_path > 5*n_announce:
      
      n_step = (len(moves) + n_path) - 5*n_announce

      
      for i in range(n_step):
        if moves:
          moves.pop(len(moves) - 1)

      n_announce += 1
      n_hiders = len(hiders)   
      
      get_announce(announce, n_hiders, hiders)


    for i, move in enumerate(moves):
      matrix = update_matrix(move[0], move[1], matrix)

      for hider in hiders:
        if matrix[hider[0]][hider[1]] == 7:
          uncatched = [(hider)]

          # print(moves)
          for j in range(len(moves) - 1, i, -1):
            moves.pop(j)


          # print(moves)
          current = move
          while uncatched:
            temp = a_star(current, uncatched[0], matrix)
            # print(temp)
            for t in temp:
              matrix = update_matrix(current[0], current[1], matrix)
              for hide in hiders:
                if hide not in uncatched and hide not in catch and matrix[hide[0]][hide[1]] == 7:
                  uncatched.append(hide)
              moves.append(t)
              current = t
            
              if n_path + len(moves) > 5*n_announce:
                get_announce(announce, len(hiders), hiders)
                n_announce += 1

            hiders.pop(hiders.index(uncatched[0]))
            catch.append(uncatched.pop(0))

          break

    

    temp = []

    for u in range(a):
      for v in range(b):
        if matrix[u][v] == 7:
          if (u, v) in unvisited:
            unvisited.pop(unvisited.index((u, v)))

    for move in moves:
      path.append(move)

    current = path[len(path) - 1]
    

    if len(hiders) == 0:
      break

  print("\n")
  print(path)
  # print(announce)
  # print(len(path), len(announce))
  drawlv2.show("map1_1.txt", path, announce)

    

def main():
  file_name = "map1_1.txt"
  n, m, matrix = vision.read_map(file_name)
  move(matrix)

if __name__ == "__main__":
  main()