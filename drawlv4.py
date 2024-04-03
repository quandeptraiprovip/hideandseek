import cv2
import numpy as np
import vision
import block_path

# Define colors
COLORS = {
    0: (255, 255, 255),  # Empty path (white)
    1: (0, 0, 0),        # Wall (black)
    2: (0, 255, 0),      # Hider (green)
    3: (0, 0, 255),       # Seeker (red)
    7: (255, 255, 255),  
    5: (128, 0, 128),    # Obstacles
    9: (128, 256, 128)     # Announce 
}

# Function to create matrix graphic
def create_matrix_graphic(matrix):
    # Get the size of the matrix
    n = len(matrix)
    m = len(matrix[0])
    
    # Define image size
    image_size = (n * 50, m * 50, 3)
    # Create a white image
    img = np.ones(image_size, dtype=np.uint8) * 255

    # Draw rectangles based on matrix
    for i in range(n):
        for j in range(m):
            color = COLORS[matrix[i][j]]
            cv2.rectangle(img, (j*50, i*50), ((j+1)*50, (i+1)*50), color, -1)

    return img

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
            map_data[i][j] = 5

    return map_data, obstacles

# Example input array

def show(filename, moves, announces, obs, new_hiders):

# Create matrix graphic
  matrix, obstacles = read_map(filename)
  pause = 10000
  if obs:
    obstacle = obs.pop(0)
    pause = obstacle[1]
    obstacle_index = obstacle[0]
    new_obstacle = obstacle[2]

  x, y = vision.find_seeker(matrix)
  hiders = vision.find_hider(matrix)
  n_hider = len(new_hiders)
  matrix_img = create_matrix_graphic(matrix)
  flag = False
  announce_locations = []
  n_moves = 0
  start = False

  new_obstacles, _ = block_path.main(filename)



  if matrix_img.shape[0] > 0 and matrix_img.shape[1] > 0:
    cv2.imshow('Matrix Graphic', matrix_img)
    cv2.waitKey(1000) 
    step = 5

    if new_obstacles:
      for i ,hider in enumerate(hiders):
        matrix[hider[0]][hider[1]] = 0
      for i in range(len(new_hiders)):
        matrix[new_hiders[i][0]][new_hiders[i][1]] = 2

      hiders = new_hiders.copy()

      for obstacle in obstacles:
        for i in range(obstacle[0], obstacle[2] + 1):
          for j in range(obstacle[1], obstacle[3] + 1):
            matrix[i][j] = 0
      
      obstacles = []
      for o in new_obstacles:
        obstacle = o[1][len(o[1]) - 1]
        obstacles.append(obstacle)
        for i in range(obstacle[0], obstacle[2] + 1):
          for j in range(obstacle[1], obstacle[3] + 1):
            matrix[i][j] = 5

      cv2.imshow('Matrix Graphic', matrix_img)
      cv2.waitKey(250) 
      

    for move in moves:
      if matrix_img.shape[0] > 0 and matrix_img.shape[1] > 0:

        if pause == 0:
          print(new_obstacle)
          for i in range(obstacles[obstacle_index][0], obstacles[obstacle_index][2] + 1):
            for j in range(obstacles[obstacle_index][1], obstacles[obstacle_index][3] + 1):
              matrix[i][j] = 0

          for i in range(new_obstacle[0], new_obstacle[2] + 1):
            for j in range(new_obstacle[1], new_obstacle[3] + 1):
              matrix[i][j] = 5
          if obs:
            obstacle = obs.pop(0)
            pause = obstacle[1] - n_moves
            obstacle_index = obstacle[0]
            new_obstacle = obstacle[2]
          else:
            pause = 1000000

          print(pause)

        else:

        # phan xu ly announce
          if move in new_hiders:
            n_hider -= 1

          if step == 0:
            if flag:
              for i in range(len(announce_locations)):
                matrix[announce_locations[i][0]][announce_locations[i][1]] = 0


            announce_locations = []
            for i in range(n_hider):
              announce = announces.pop(0)
              announce_locations.append(announce)
              matrix[announce[0]][announce[1]] = 9

            # for row in matrix:
            #   print(row)

            flag = True
            if announces:
              step = 5

              

          matrix[x][y] = 0
          matrix[move[0]][move[1]] = 3
          x = move[0]
          y = move[1]
          step -= 1
          pause -= 1
          n_moves += 1

        matrix_img = create_matrix_graphic(matrix)
        cv2.imshow('Matrix Graphic', matrix_img)
        cv2.waitKey(250)
      else:
        print("Error: Empty image")

  cv2.waitKey(0)
  cv2.destroyAllWindows()

if __name__ == "__main__":
    matrix, obstacles = read_map("map1_1.txt")
    show("map1_1.txt", [(1,2), (3,2), (3,4), (2,3), (4,5), (2,3)], [(2,13), (4,15), (6,7)])
