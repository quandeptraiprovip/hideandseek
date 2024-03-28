import vision
import heapq
import copy
import draw
from node import Node

def calc_heuristic(x, y, matrix):
  a, b = vision.find_seeker(matrix)
  matrix[a][b] = 7
  matrix[x][y] = 3
  matrix = vision.vision(x, y, matrix)
  # print(x, y)

  # for i in range(len(matrix)):
  #   print(matrix[i])

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



def move(matrix):
  unvisited = get_all_cells(matrix)
  n = len(unvisited)
  path = []
  a, b = (len(matrix), len(matrix[0]))

  x, y = vision.find_seeker(matrix)
  hiders = vision.find_hider(matrix)
  n_hiders = len(hiders)
  is_catched = False


  unvisited.pop(0)
  current = (x, y)

  while unvisited:
    goal = unvisited[0]
    unvisited.pop(0)

    matrix = calc_heuristic(current[0], current[1], matrix)

    moves = a_star(current, goal, matrix)

    for i, move in enumerate(moves):
      matrix = calc_heuristic(move[0], move[1], matrix)

      

      for hider in hiders:
        if matrix[hider[0]][hider[1]] == 7:
          print(moves)
          for j in range(len(moves) - 1, i, -1):
            moves.pop(j)

          print(moves)

        

          temp = a_star(move, hider, matrix)
          print(temp)
          for t in temp:
            moves.append(t)

          is_catched = True
          break
      
      if is_catched:
        break

          

          



    for u in range(a):
      for v in range(b):
        if matrix[u][v] == 7:
          if (u, v) in unvisited:
            unvisited.pop(unvisited.index((u, v)))
            # print((u, v))

    # for row in matrix:
    #   print(row)

    # print("\n")
    # print(len(unvisited))

    for move in moves:
      path.append(move)

    current = goal

    if is_catched:
      break


  print(path)
  draw.show("map1_1.txt", path)

    

def main():
  file_name = "map1_1.txt"
  n, m, matrix = vision.read_map(file_name)
  move(matrix)
  # i = calc_heuristic(7, 3, matrix)

  

if __name__ == "__main__":
  main()