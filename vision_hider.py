class Pos:
  def __init__(self, x, y, parent, heuristic = -1):
    self.x = x
    self.y = y
    self.parent = parent
    self.heuristic = heuristic

  def __lt__(self, other):
    return self.heuristic < other.heuristic
  
  def __eq__(self, other):
    return self.heuristic == other.heuristic
  

def find_seeker(matrix):
  for i, row in enumerate(matrix):
    for j, element in enumerate(matrix[i]):
      if element == 3:
        return i, j

  return None   

def find_hider(matrix):
  hiders = []
  for i, row in enumerate(matrix):
    for j, element in enumerate(matrix[i]):
      if element == 2:
        hiders.append((i,j))
  
  return hiders
        
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

    return n, m, map_data, obstacles

def get_vision(matrix, x, y, a, b):
  arr = [[0,0,0,0],
         [0,0,0,0],
         [0,0,0,0],
         [0,0,0,0]]
  
  n = len(matrix)
  m = len(matrix[0])
  
  if 3 == matrix[0][0]:
    for i in range(n):
      for j in range(m):
        arr[i][j] = matrix[i][j]

  if 3 == matrix[n - 1][0]:
    for i in range(n):
      for j in range(m):
        arr[4 - n + i][j] = matrix[i][j]

  if 3 == matrix[n - 1][m - 1]:
    for i in range(n):
      for j in range(m):
        arr[4 - n + i][4 - m + j] = matrix[i][j]

  if 3 == matrix[0][m - 1]:
    for i in range(n):
      for j in range(m):
        arr[i][4 - m + j] = matrix[i][j]
  # a = 3 khi phan x khac voi top right = 0 khi giong
  # b = 1 khi phan y khac voi top right = 0 khi giong
  p = q = r = s = 0
  if b == 1: 
    p = 3 
    q = 1
    r = -1
    s = -3

  if arr[abs(a - 3)][1 + q] == 1:
    arr[abs(a - 3)][2 + r] = 6 if arr[abs(a - 3)][2 + r] != 1 else arr[abs(a - 3)][2 + r]
    arr[abs(a - 3)][3 + s] = 6 if arr[abs(a - 3)][3 + s] != 1 else arr[abs(a - 3)][3 + s]    
    arr[abs(a - 2)][3 + s] = 6 if arr[abs(a - 2)][3 + s] != 1 else arr[abs(a - 2)][3 + s]

    if arr[abs(a - 2)][1 + q] == 1:
      arr[abs(a - 2)][2 + r] = 6 if arr[abs(a - 2)][2 + r] != 1 else arr[abs(a - 2)][2 + r]
  

  if arr[abs(a - 2)][1 + q] == 1:
    arr[abs(a - 1)][2 + r] = 6 if arr[abs(a - 1)][2 + r] != 1 else arr[abs(a - 1)][2 + r]
    arr[a][3 + s] = 6 if arr[a][3 + s] != 1 else arr[a][3 + s]
    arr[a][2 + r] = 6 if arr[a][2 + r] != 1 else arr[a][2 + r]
    arr[abs(a - 1)][3 + s] = 6 if arr[abs(a - 1)][3 + s] != 1 else arr[abs(a - 1)][3 + s]

    if arr[abs(a - 2)][0 + p] == 1:
      arr[abs(a - 1)][1 + q] = 6 if arr[abs(a - 1)][1 + q] != 1 else arr[abs(a - 1)][1 + q]

  if arr[abs(a - 2)][0 + p] == 1:
    arr[a][0 + p] = 6 if arr[a][0 + p] != 1 else arr[a][0 + p]
    arr[abs(a - 1)][0 + p] = 6 if arr[abs(a - 1)][0 + p] != 1 else arr[abs(a - 1)][0 + p]
    arr[a][1 + q] = 6 if arr[a][1 + q] != 1 else arr[a][1 + q]

  if arr[abs(a - 1)][0 + p] == 1:
    arr[a][0 + p] = 6 if arr[a][0 + p] != 1 else arr[a][0 + p]
  
  if arr[abs(a - 1)][1 + q] == 1:
    arr[a][1 + q] = 6 if arr[a][1 + q] != 1 else arr[a][1 + q]
    arr[a][2 + r] = 6 if arr[a][2 + r] != 1 else arr[a][2 + r]

  if arr[abs(a - 1)][2 + r] == 1:
    arr[a][3 + s] = 6 if arr[a][3 + s] != 1 else arr[a][3 + s]

  if arr[abs(a - 3)][2 + r] == 1:
    arr[abs(a - 3)][3 + s] = 6 if arr[abs(a - 3)][3 + s] != 1 else arr[abs(a - 3)][3 + s]
  
  if arr[abs(a - 2)][2 + r] == 1:
    arr[abs(a - 2)][3 + s] = 6 if arr[abs(a - 2)][3 + s] != 1 else arr[abs(a - 2)][3 + s]
    arr[abs(a - 1)][3 + s] = 6 if arr[abs(a - 1)][3 + s] != 1 else arr[abs(a - 1)][3 + s]

  
  for i in range(4):
    for j in range(4):
      if(arr[i][j] == 0) or arr[i][j] == 2:
        arr[i][j] = 7
      else:
        if arr[i][j] == 6:
          arr[i][j] = 0


  return arr



def get_submatrix(matrix, start_row, end_row, start_col, end_col):
  submatrix = [row[start_col: end_col] for row in matrix[start_row: end_row]]

  return submatrix

def vision(x, y ,matrix):
  n = len(matrix)
  m = len(matrix[0])

  a = x - 3
  b = x + 4
  c = y - 3
  d = y + 4

  if a < 0:
    a = 0

  if b > n:
    b = n

  if c < 0:
    c = 0

  if d > m:
    d = m
  
  # top right
  sub = get_vision(get_submatrix(matrix, a, x + 1, y, d), x, y, 0, 0)
  for i in  range(a, x + 1):
    for j in range(y, d):
      if matrix[i][j] != 7:
        matrix[i][j] = sub[i - (x - 3)][j - y]

  # top left
  sub = get_vision(get_submatrix(matrix, a, x + 1, c, y + 1), x, y, 0, 1)
  for i in range(a, x + 1):
    for j in range(c, y + 1):
      if matrix[i][j] != 7:
        matrix[i][j] = sub[i - (x - 3)][j - (y - 3)]

  # bot left
  sub = get_vision(get_submatrix(matrix, x, b, c, y + 1), x, y, 3, 1)
  for i in range(x, b):
    for j in range(c, y + 1):
      if matrix[i][j] != 7:
        matrix[i][j] = sub[i - x][j - (y - 3)]

  # bot right
  sub = get_vision(get_submatrix(matrix, x, b, y, d), x, y, 3, 0)
  for i in range(x, b):
    for j in range(y, d):
      if matrix[i][j] != 7:
        matrix[i][j] = sub[i - x][j - y]

  return matrix



def main():
  file_name = "map.txt"
  n, m, matrix, obstacles = read_map(file_name)
  x, y = find_seeker(matrix)
  matrix = vision(x, y, matrix)
  for row in matrix:
    print(row)

if __name__ == "__main__":
  main()
