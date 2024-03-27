def hide_cells(map_matrix, seeker_position, vision_range):
    n = len(map_matrix)
    m = len(map_matrix[0])

    def is_valid(x, y):
        return 0 <= x < n and 0 <= y < m

    seeker_x, seeker_y = seeker_position
    hidden_cells = set()

    for dx in range(-vision_range, vision_range + 1):
        for dy in range(-vision_range, vision_range + 1):
            x, y = seeker_x + dx, seeker_y + dy
            if is_valid(x, y):
                # Check if the cell is within the vision range
                if dx ** 2 + dy ** 2 <= vision_range ** 2:
                    # Check if there's a wall or obstacle blocking the vision
                    if map_matrix[x][y] == 1:
                        # Determine the direction of the cell relative to the seeker
                        direction_x = 1 if x > seeker_x else -1 if x < seeker_x else 0
                        direction_y = 1 if y > seeker_y else -1 if y < seeker_y else 0
                        # Check if the blocking wall hides cells in certain directions
                        if dx * direction_x > 0 or dy * direction_y > 0:
                            hidden_cells.add((x, y))

    return hidden_cells

# Example usage:
map_matrix = [
    [0, 0, 0, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 1, 1, 0, 0],
    [0, 0, 0, 0, 0],
]

seeker_position = (1, 2)  # Example seeker position
vision_range = 2  # Example vision range

hidden_cells = hide_cells(map_matrix, seeker_position, vision_range)
print("Hidden cells:", hidden_cells)
