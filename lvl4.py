import vision
import heapq
import copy
import drawlv4
from node import Node
import random
from pos import Dir
import block_path

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

def cells_around_announce(center_x, center_y, matrix, old_unvisited):
  cells_around = []
  for i in range(center_x - 3, center_x + 3 + 1):
    for j in range(center_y - 3, center_y + 3 + 1):
      if 0 <= i < len(matrix) and 0 <= j < len(matrix[0]) and matrix[i][j] != 1 and (i,j) in old_unvisited:
        cells_around.append((i, j))
  return cells_around

def cells_around_obstacle(obstacle, size):
  cells = []

  for i in range(obstacle[0] - 1, obstacle[2] + 2):
    for j in range(obstacle[1] - 1, obstacle[3] + 2):
      if i < 0 or i > size[0]:
        continue
      if j < 0 or j > size[1]:
        continue

      if  i == obstacle[0] - 1 or i == obstacle[2] + 1:
        cells.append((i,j))

      if j == obstacle[1] - 1 or j == obstacle[3] + 1:
        cells.append((i,j))

  return cells

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

    # gia su ta dat obstacle vao map
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

def a_star_obstacle(matrix, obstacle):
  obstacle_size = (abs(obstacle[0] - obstacle[2]) + 1)*(abs(obstacle[1]-obstacle[3]) + 1)
  grid_size = (len(matrix), len(matrix[0]))
  
  open_list = []
  closed_list = []

  start_node = Dir(obstacle)
  start_node.f = heuristic(matrix, obstacle)
  # base = heuristic(matrix) - obstacle_size
  base = heuristic(matrix) - obstacle_size
  # print(base)

  open_list.append(start_node)

  while open_list:
    current_node = open_list.pop(0)
    closed_list.append(current_node)
    # print(current_node.f)

    if current_node.f == base:
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


def move(matrix, obstacles):
  unvisited = get_all_cells(matrix)
  old_unvisited = unvisited.copy()
  a, b = (len(matrix), len(matrix[0]))
  obstacle_nearby = []
  obstacle_visited = []

  for i ,obstacle in enumerate(obstacles):
    # print(cells_around_obstacle(obstacle, (a,b)))
    for o in cells_around_obstacle(obstacle, (a,b)):
      if o in unvisited:
        if i not in obstacle_nearby:
          obstacle_nearby.append(i)
        break

  # print(obstacle_nearby)


  n = len(unvisited)
  path = []
  announce = []
  new_obstacle = []

  x, y = vision.find_seeker(matrix)
  hiders = vision.find_hider(matrix)
  new_hiders = hiders.copy()
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


  while unvisited:
    n_path = len(path)
    goal = unvisited[0]
    
    unvisited.pop(0)
    while goal == current or matrix[goal[0]][goal[1]] == 1:
      if unvisited:
        goal = unvisited.pop(0)
      else:
        break
    
    if goal[0] == 4 and goal[1] == 15:
      for row in matrix:
        print(row)
        
    catch = []
    print(current, goal)
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
            temp = cells_around_announce(location[0], location[1], matrix, old_unvisited)

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

    # di chuyen obsstacle
    if not unvisited:
      while obstacle_nearby:
        obstacle_visited.append(obstacle_nearby[0])
        obs = obstacle_nearby.pop(0)
        # loai obstacle duoc chon de di chuyen ra khoi map
        for i in range(obstacles[obs][0], obstacles[obs][2] + 1):
          for j in range(obstacles[obs][1], obstacles[obs][3] + 1):
            matrix[i][j] = 0

        #tim vi tri moi cho obstacle
        path_obs = a_star_obstacle(matrix, obstacles[obs])
        # print(path_obs)

        if path_obs:
          new_obs = path_obs[len(path_obs) - 1]
          # bo obstacle moi vao map
          for i in range(new_obs[0], new_obs[2] + 1):
            for j in range(new_obs[1], new_obs[3] + 1):
              matrix[i][j] = 1
          
          # for row in matrix:
          #   print(row)

          # tao list unvisited moi
          unvisited = get_all_cells(matrix)
          old_unvisited = unvisited.copy()

          for u in range(a):
            for v in range(b):
              if matrix[u][v] == 7:
                if (u, v) in unvisited:
                  unvisited.pop(unvisited.index((u, v)))

          for i,obstacle in enumerate(obstacles):
            # print(cells_around_obstacle(obstacle, (a,b)))
            for o in cells_around_obstacle(obstacle, (a,b)):
              if o in unvisited:
                if i not in obstacle_nearby and i not in obstacle_visited:
                  obstacle_nearby.append(i)
                break

          # print(obstacle_nearby)

          new_obstacle.append((obs ,len(path), path_obs[len(path_obs) - 1]))
          break
        else:
          for i in range(obstacles[obs][0], obstacles[obs][2] + 1):
            for j in range(obstacles[obs][1], obstacles[obs][3] + 1):
              matrix[i][j] = 1
        
      
  # print(new_obstacle)

  # print("\n")
  print(path)
  # print(announce)
  # print(len(path), len(announce))
  print(new_hiders)
  print(new_obstacle)
  drawlv4.show("map1_1.txt", path, announce, new_obstacle, new_hiders)

    

def main():
  file_name = "map1_1.txt"
  n, m, matrix, obstacles = vision.read_map(file_name)
  hiders = vision.find_hider(matrix)
  # loai het obstacle ra khoi map
  for obstacle in obstacles:
    for i in range(obstacle[0], obstacle[2] + 1):
      for j in range(obstacle[1], obstacle[3] + 1):
        matrix[i][j] = 0

  # tim vi tri obstacle moi
  new_obstacle, new_pos = block_path.main(file_name)
  # tao map moi
  if new_obstacle:
    obstacles = []
    for o in new_obstacle:
      obstacle = o[1][len(o[1]) - 1]
      obstacles.append(obstacle)
      for i in range(obstacle[0], obstacle[2] + 1):
        for j in range(obstacle[1], obstacle[3] + 1):
          matrix[i][j] = 1

  # vi tri hider moi
  n_position = len(new_pos)
  for hider in hiders:
    matrix[hider[0]][hider[1]] = 0
    hider = new_pos[random.randint(0, n_position - 1)]
    matrix[hider[0]][hider[1]] = 2

  move(matrix, obstacles)
  # print(cells_around_obstacle(obstacles[0], (n, m)))

if __name__ == "__main__":
  main()