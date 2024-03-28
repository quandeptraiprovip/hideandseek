import vision
import copy

class Pos:
  def __init__(self, matrix, g, heuristic, parent=None):
    self.position = vision.find_seeker(matrix)
    self.parent = parent
    self.matrix = matrix
    self.g = g
    self.h = heuristic
    self.f = (self.g*(self.g + 1))/2 + self.h

  def __eq__(self, other):
    return self.h == other.h

  def __lt__(self, other):
    return self.h > other.h
  
  def __repr__(self):
    return str(self.h)
  
  def __hash__(self):
    return hash(str(self.position))
  
  def next_move(self):
    direction = [(-1,-1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    neighbor = []
    n = len(self.matrix)
    m = len(self.matrix[0])

    for dx, dy in direction:
      a, b = self.position
      newx = a + dx
      newy = b + dy
      if newx > 0 and newy > 0 and newx < n and newy < m and self.matrix[newx][newy] != 1:
        val, matrix_cop= calc_heuristic(newx, newy, self.matrix)
        neighbor.append(Pos(matrix_cop, self.g + 1, val, self))

    return neighbor
  

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