import heapq

class Node:
  def __init__(self, position, parent=None):
    self.position = position
    self.parent = parent
    self.g = 0
    self.h = 0
    self.f = 0

  def __eq__(self, other):
    return self.position == other.position

  def __lt__(self, other):
    return self.f < other.f
  
  def heuristic(current, goal):
    return abs(current[0] - goal[0]) + abs(current[1] - goal[1])