import vision
from pos import Pos
import copy
import heapq

def calc_heuristic(x, y, matrix):
  a, b = vision.find_seeker(matrix)
  matrix_cop = copy.deepcopy(matrix)
  matrix_cop[a][b] = 7
  matrix_cop[x][y] = 3
  matrix_cop = vision.vision(x, y, matrix_cop)
  # print(x, y)

  # for i in range(len(matrix)):
  #   print(matrix[i])
  #   print(matrix_cop[i])
  #   print("\n")

  n = len(matrix)
  m = len(matrix[0])
  count = 0

  for i in range(n):
    for j in range(m):
      if matrix_cop[i][j] != matrix[i][j]:
        count = count + 1

  return count, matrix_cop

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

      for i in range(len(obstacles)):
        x = obstacles[i][0]
        y = obstacles[i][1]
        a = obstacles[i][2]
        b = obstacles[i][3]

        for i in range(x, a + 1):
          for j in range(y, b + 1):
            map_data[i][j] = 1

    return n, m, map_data

_, _, matrix = read_map("map1_1.txt")
x, y = vision.find_seeker(matrix)
_ ,matrix = calc_heuristic(x, y, matrix)

cur = Pos(matrix, 0, 0, None)
next = cur.next_move()

cells = [cur]

for k in range(1):
  current = heapq.heappop(cells)

  next = current.next_move()
  # print(current.h)


  for moves in next:
    heapq.heappush(cells, moves)

    
while cells:
  print(heapq.heappop(cells))