def read_map_from_file(file_name):
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

# Example usage:
file_name = 'map1_1.txt'  # Replace 'map_data.txt' with your file name
n, m, map_data= read_map_from_file(file_name)
print("Size of map:", n, "x", m)
print("Map data:")
for row in map_data:
    print(row)
