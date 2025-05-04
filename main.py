from PIL import Image, ImageDraw
from random import randint, choice

# Maze size (cells)
width, height = 30, 30
cell_size = 20
radius = cell_size // 3
grid_width = 1
moves = []

img_width = width * cell_size
img_height = height * cell_size

# Create a white image
img = Image.new("RGB", (img_width, img_height), "white")
draw = ImageDraw.Draw(img)

# Draw vertical lines
for x in range(width + 1):
    x_pos = x * cell_size
    draw.line([(x_pos, 0), (x_pos, img_height)], fill="black", width=grid_width)

# Draw horizontal lines
for y in range(height + 1):
    y_pos = y * cell_size
    draw.line([(0, y_pos), (img_width, y_pos)], fill="black", width=grid_width)


starting_pos = (randint(1, width) * cell_size - (cell_size // 2), randint(1, height-1) * cell_size - (cell_size // 2))
draw.ellipse((starting_pos[0]-radius, starting_pos[1]-radius, starting_pos[0]+radius, starting_pos[1]+radius), fill=(0, 0, 0))

end_pos = (randint(1, width) * cell_size - (cell_size // 2), randint(1, height) * cell_size - (cell_size // 2))
while end_pos == starting_pos:
    end_pos = (randint(1, width) * cell_size - (cell_size // 2), randint(1, height) * cell_size - (cell_size // 2))
draw.ellipse((end_pos[0]-radius, end_pos[1]-radius, end_pos[0]+radius, end_pos[1]+radius), fill=(0, 0, 0))

path = [starting_pos]
moves.append(starting_pos)
last_move = starting_pos
visited = {starting_pos}

count = 0

while moves:
    available = []
    for i in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        dummy = last_move
        move = (dummy[0] + (i[0] * cell_size), dummy[1] + (i[1] * cell_size))
        if (0 <= move[0] < img_width and 0 <= move[1] < img_height) and ((move[0], move[1]) not in visited):
            available.append((move[0], move[1]))

    if len(available) >= 1:
        if len(available) >= 2 and last_move not in moves:
            moves.append(last_move)
        chosen = choice(available)

        midpoint = ((last_move[0] + chosen[0]) // 2, (last_move[1] + chosen[1]) // 2)
        if chosen[0] == last_move[0]:
            draw.line([(midpoint[0]-(cell_size//2)+grid_width, midpoint[1]), (midpoint[0]+(cell_size//2)-grid_width, midpoint[1])], fill="white", width=grid_width)
        else:
            draw.line([(midpoint[0], midpoint[1]-(cell_size//2)+grid_width), (midpoint[0], midpoint[1]+(cell_size//2)-grid_width)], fill="white", width=grid_width)


        last_move = chosen
        visited.add(chosen)
        if end_pos not in path:
            path.append(last_move)


    if len(available) == 0:
        last_move = moves.pop()
        if end_pos not in path:
            path = path[:path.index(last_move)+1]



    count += 1


# Shortest Path Finder
path = path[:path.index(end_pos)+1]
for i in range(1, len(path)):
    draw.line([path[i-1], path[i]], fill="red", width=grid_width*2)


# Save the maze
img.save("maze.png")

