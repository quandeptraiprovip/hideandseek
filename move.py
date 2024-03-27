import vision
import heapq
import copy
import draw

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


def next_move(x, y, n, m, matrix):
  direction = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
  neighbor = []

  for dx, dy in direction:
    newx= x + dx
    newy = y + dy
    if newx > 0 and newy > 0 and newx < n and newy < m and matrix[newx][newy] != 1:
      val, _= calc_heuristic(newx, newy, matrix)
      neighbor.append(((newx, newy),val))

  # heap = [(h, pos) for pos, h in neighbor]
  # heapq.heapify(heap)

  neighbor.sort(key=lambda x: x[1], reverse=True) 

  return neighbor

def catch(x, y, matrix, path):
  a, b = vision.find_seeker(matrix)
  while a > x:
    matrix[a][b] = 7
    a = a - 1
    matrix[a][b] = 3
    matrix = vision.vision(a, b, matrix)
    path.append((a,b))
    for row in matrix:
      print(row)
    print("\n")

  while a < x:
    matrix[a][b] = 7
    a = a + 1
    matrix[a][b] = 3
    matrix = vision.vision(a, b, matrix)
    path.append((a,b))
    for row in matrix:
      print(row)
    print("\n")

  while b < y:
    matrix[a][b] = 7
    b = b + 1
    matrix[a][b] = 3
    matrix = vision.vision(a, b, matrix)
    path.append((a,b))
    for row in matrix:
      print(row)
    print("\n")

  while b > y:
    matrix[a][b] = 7
    b = b - 1
    matrix[a][b] = 3
    matrix = vision.vision(a, b, matrix)
    path.append((a,b))
    for row in matrix:
      print(row)
    print("\n")

  return matrix, a, b, path

def move(matrix):
  x, y = vision.find_seeker(matrix)
  hiders = vision.find_hider(matrix)
  n = len(matrix)
  m = len(matrix[0])
  visited = dict()
  visited[(x, y)] = 1
  _,matrix = calc_heuristic(x, y, matrix)
  path = []
  catched = []


  while True:
  # for k in range(25):
    next = next_move(x, y, n, m, matrix)
    i = 0

    print(next)

    for moves in next:
      if moves[0] not in visited.keys():
        visited[moves[0]] = 1
        break
      else:
        if visited[moves[0]] == 1 or visited[moves[0]] == 2:
          visited[moves[0]] += 1
          break
      
      i = i + 1

      
    matrix[x][y] = 7
    x = next[i][0][0]
    y = next[i][0][1]
    matrix[x][y] = 3

    path.append((x, y))



    _, matrix = calc_heuristic(x, y, matrix)

    for i in range(len(hiders)):
      for pos in hiders:
        if matrix[pos[0]][pos[1]] == 7 and pos not in catched:
          matrix[pos[0]][pos[1]] = 2
          matrix, x, y, path = catch(pos[0], pos[1], matrix, path)
          catched.append(pos)


    for row in matrix:
      print(row)

    if [x, y] in hiders:
      break


    print("\n")

  draw.show("map1_1.txt", path)


def main():
  file_name = "map1_1.txt"
  n, m, matrix = vision.read_map(file_name)
  move(matrix)
  # i = calc_heuristic(7, 3, matrix)

  

if __name__ == "__main__":
  main()