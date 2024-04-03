import cv2
import numpy as np
import vision

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

    return map_data

# Example input array

def show(filename, moves, announces):

# Create matrix graphic
  matrix = read_map(filename)
  x, y = vision.find_seeker(matrix)
  hiders = vision.find_hider(matrix)
  n_hider = len(hiders)
  matrix_img = create_matrix_graphic(matrix)
  flag = False
  announce_locations = []

  if matrix_img.shape[0] > 0 and matrix_img.shape[1] > 0:
    cv2.imshow('Matrix Graphic', matrix_img)
    cv2.waitKey(250) 
    step = 5

  

    for move in moves:
      if matrix_img.shape[0] > 0 and matrix_img.shape[1] > 0:
          
        # phan xu ly announce
        if move in hiders:
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

        matrix_img = create_matrix_graphic(matrix)
        cv2.imshow('Matrix Graphic', matrix_img)
        cv2.waitKey(250)
      else:
        print("Error: Empty image")

  cv2.waitKey(0)
  cv2.destroyAllWindows()

if __name__ == "__main__":
    matrix = read_map("map1_1.txt")
    show("map1_1.txt", [(1,2), (3,2), (3,4), (2,3), (4,5), (2,3)], [(2,13), (4,15), (6,7)])
