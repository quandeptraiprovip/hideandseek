import vision
import copy

class Dir:
  def __init__(self, obstacle = None ,parent = None):
    self.obstacle = obstacle
    self.parent = parent
    self.f = 0

  def __eq__(self, other):
    return self.obstacle == other.obstacle
  
  def __lt__(self, other):
    return self.f > other.f