from pos import Dir
import vision
import copy

def read_map(file_name):
  map_data = []
  obstacles = []

  with open(file_name, 'r') as file:
    # Read the size of the map
    n, m = map(int, file.readline().split())

      # Read the map matrix
    for _ in range(n):
      map_row = list(map(int, file.readline().split()))
      map_data.append(map_row)

    # Read the obstacle positions
    for line in file:
      obstacle = list(map(int, line.split()))
      obstacles.append(obstacle)

  return n, m, map_data, obstacles

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

def heuristic(matrix, obstacle = None):
  x, y = vision.find_seeker(matrix)
  n = len(matrix)
  m = len(matrix[0])
  matrix_cop = copy.deepcopy(matrix)
  
  if obstacle != None:
    u = obstacle[0]
    v = obstacle[1]
    a = obstacle[2]
    b = obstacle[3]

    for i in range(u, a + 1):
      for j in range(v, b + 1):
        matrix_cop[i][j] = 1

  def dfs(i, j, count):
    if i < 0 or i >= n or j < 0 or j >= m or matrix_cop[i][j] == 1:
      return
    
    count[0] += 1
    matrix_cop[i][j] = 1
    
    dfs(i + 1, j, count)
    dfs(i - 1, j, count)
    dfs(i, j + 1, count)
    dfs(i, j - 1, count)

  count = [0]
  dfs(x, y, count)

  return count[0]

def check_valid(matrix, obstacle):
  u = obstacle[0]
  v = obstacle[1]
  a = obstacle[2]
  b = obstacle[3]

  if 0 > u or u >= len(matrix):
    return False
  
  if 0 > a or a >= len(matrix):
    return False
  
  if 0 > v or v >= len(matrix[0]):
    return False
  
  if 0 > b or b >= len(matrix[0]):
    return False
  

  for i in range(u, a + 1):
    for j in range(v, b + 1):
      if matrix[i][j] == 1:
        return False
        
  return True

def get_neighbors(grid_size, obstacle, matrix):
  x, y = vision.find_seeker(matrix)
  row, col = grid_size
  neighbors = [(-1, 0), (1,0), (0,-1), (-1,-1), (0, 1), (-1, 1), (1, -1), (1, 1)]
  valid_neighbors = []

  for neighbor in neighbors:
    new_obstacle = (obstacle[0] + neighbor[0], obstacle[1] + neighbor[1], obstacle[2] + neighbor[0], obstacle[3] + neighbor[1])
    # print(obstacle)

    if check_valid(matrix, new_obstacle):
      valid_neighbors.append(new_obstacle)

  return valid_neighbors

def a_star(matrix, obstacle):
  obstacle_size = (abs(obstacle[0] - obstacle[2]) + 1)*(abs(obstacle[1]-obstacle[3]) + 1)
  grid_size = (len(matrix), len(matrix[0]))
  
  open_list = []
  closed_list = []

  start_node = Dir(obstacle)
  start_node.f = heuristic(matrix, obstacle)
  base = heuristic(matrix) - obstacle_size
  # print(base)

  open_list.append(start_node)

  while open_list:
    current_node = open_list.pop(0)
    closed_list.append(current_node)
    # print(current_node.f)

    if current_node.f < base:
      path = []
      while current_node.parent:
        path.append(current_node.obstacle)
        current_node = current_node.parent
      return path[::-1]

    for neighbor_pos in get_neighbors(grid_size, current_node.obstacle, matrix):
      neighbor_node = Dir(neighbor_pos, current_node)
      if neighbor_node in closed_list:
        continue
        
      neighbor_node.f = heuristic(matrix, neighbor_pos)
      # print(neighbor_node.h)

      # Update the node's parent if the new path is better
      for node in open_list:
        if node == neighbor_node:
          break
      else:
        open_list.append(neighbor_node)

      # print(open_list)
  return None   

def get_valid(matrix, obstacle):
  obstacle_size = (abs(obstacle[0] - obstacle[2]) + 1)*(abs(obstacle[1]-obstacle[3]) + 1)
  grid_size = (len(matrix), len(matrix[0]))
  
  open_list = []
  closed_list = []

  start_node = Dir(obstacle)
  start_node.f = heuristic(matrix, obstacle)
  if check_valid(matrix, obstacle):
    return obstacle
  base = heuristic(matrix) - obstacle_size
  # print(base)

  open_list.append(start_node)

  while open_list:
    current_node = open_list.pop(0)
    closed_list.append(current_node)
    # print(current_node.f)


    if current_node.f < base:
      path = []
      while current_node.parent:
        path.append(current_node.obstacle)
        current_node = current_node.parent
      return path[::-1]

    for neighbor_pos in get_neighbors(grid_size, current_node.obstacle, matrix):
      return neighbor_pos
    
      neighbor_node = Dir(neighbor_pos, current_node)
      if neighbor_node in closed_list:
        continue
        
      neighbor_node.f = heuristic(matrix, neighbor_pos)
      # print(neighbor_node.h)

      # Update the node's parent if the new path is better
      for node in open_list:
        if node == neighbor_node:
          break
      else:
        open_list.append(neighbor_node)

      # print(open_list)
  return None         

def main(filename):
  x, y, matrix, obstacles = read_map(filename)
  new_obstacle = []
  print(obstacles)
  unvisited_before = get_all_cells(matrix)
  for i, obstacle in enumerate(obstacles):

    if a_star(matrix, obstacle):
      new_obstacle.append((i, a_star(matrix, obstacle)))
      obstacle = new_obstacle[0][1][len(new_obstacle[0][1]) - 1]
      for i in range(obstacle[0], obstacle[2] + 1):
        for j in range(obstacle[1], obstacle[3] + 1):
          matrix[i][j] = 1
    else:
      new_obstacle.append((i, [get_valid(matrix, obstacle)]))
  # print(unvisited_before)

  # for o in new_obstacle:
  #   obstacle = o[1][len(o[1]) - 1]
  #   for i in range(obstacle[0], obstacle[2] + 1):
  #     for j in range(obstacle[1], obstacle[3] + 1):
  #       matrix[i][j] = 1

  unvisited_after = get_all_cells(matrix)
  # print(unvisited_after)

  new_position = []

  for u in unvisited_before:
    if u not in unvisited_after and matrix[u[0]][u[1]] != 1:
      new_position.append(u)

  # print(new_position)

  # print(get_neighbors((x,y), obstacles[0], matrix))
  # print(heuristic(matrix, (1, 3, 3, 7)))
      
  return new_obstacle, new_position
  # return new_obstacle

if __name__ == "__main__":
  print(main("map3.txt"))