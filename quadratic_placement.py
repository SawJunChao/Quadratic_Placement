import random
import math
import matplotlib.pyplot as plt


class Block:
    def __init__(self, height, width, x=None, y=None):
        self.height = height
        self.width = width
        self.x = x
        self.y = y


def create_horizontal_grid(boundary_height, boundary_width, grid_spacing):
    num_lines = boundary_height // (grid_spacing + 5)
    lines = []
    for i in range(num_lines):
        y = i * (grid_spacing + 5)
        lines.append((0, y, boundary_width, y))


    return lines


def random_placement(blocks, boundary_height, boundary_width, min_spacing):
    for block in blocks:
        block.x = random.randint(min_spacing, boundary_width - block.width - min_spacing)
        block.y = random.randint(min_spacing, boundary_height - block.height - min_spacing)
    return blocks


def quadratic_placement(blocks, boundary_height, boundary_width, min_spacing):
    total_blocks = len(blocks)
    num_blocks_side = math.ceil(math.sqrt(total_blocks))
    block_width = blocks[0].width
    block_height = blocks[0].height


    rect_width = num_blocks_side * block_width + (num_blocks_side - 1) * min_spacing
    rect_height = num_blocks_side * block_height + (num_blocks_side - 1) * min_spacing


    start_x = (boundary_width - rect_width) // 2
    start_y = (boundary_height - rect_height) // 2


    current_x = start_x
    current_y = start_y


    for i, block in enumerate(blocks):
        block.x = current_x
        block.y = current_y


        current_x += block_width + min_spacing


        if (i + 1) % num_blocks_side == 0:
            current_x = start_x
            current_y += block_height + min_spacing


    return blocks


def quadratic_placement_blocks(sram_blocks, blocks_a, blocks_b, boundary_height, boundary_width, min_spacing):
    # Perform quadratic placement for SRAM blocks
    sram_blocks = quadratic_placement(sram_blocks, boundary_height, boundary_width, min_spacing)


    # Calculate the total width of the SRAM blocks rectangle
    sram_rect_width = math.ceil(math.sqrt(len(sram_blocks))) * sram_blocks[0].width + \
                      (math.ceil(math.sqrt(len(sram_blocks))) - 1) * min_spacing


    # Calculate the total height of the SRAM blocks rectangle
    sram_rect_height = math.ceil(math.sqrt(len(sram_blocks))) * sram_blocks[0].height + \
                       (math.ceil(math.sqrt(len(sram_blocks))) - 1) * min_spacing


    # Calculate the center coordinates of the SRAM blocks rectangle
    sram_rect_center_x = sram_blocks[0].x + sram_rect_width // 2
    sram_rect_center_y = sram_blocks[0].y + sram_rect_height // 2


    # Calculate the position of block A on the top and bottom of the SRAM blocks rectangle
    block_a_x = sram_rect_center_x - blocks_a[0].width // 2
    block_a_y_top = sram_blocks[0].y - blocks_a[0].height - min_spacing
    block_a_y_bottom = sram_blocks[0].y + sram_rect_height + min_spacing


    # Calculate the position of block B on the left and right of the SRAM blocks rectangle
    block_b_y = sram_rect_center_y - blocks_b[0].height // 2
    block_b_x_left = sram_blocks[0].x - blocks_b[0].width - min_spacing
    block_b_x_right = sram_blocks[0].x + sram_rect_width + min_spacing


    # Assign the positions for block A
    blocks_a[0].x = block_a_x
    blocks_a[0].y = block_a_y_top
    blocks_a[1].x = block_a_x
    blocks_a[1].y = block_a_y_bottom


    # Assign the positions for block B
    blocks_b[0].x = block_b_x_left
    blocks_b[0].y = block_b_y
    blocks_b[1].x = block_b_x_right
    blocks_b[1].y = block_b_y


    return sram_blocks, blocks_a, blocks_b


def visualize_initial_placement(sram_blocks, blocks_a, blocks_b, boundary_height, boundary_width, grid_lines):
    fig, ax = plt.subplots()
    ax.set_xlim([0, boundary_width])
    ax.set_ylim([0, boundary_height])
   
    Alt =0
    for line in grid_lines:
        if(Alt==0):
            ax.plot([line[0], line[2]], [line[1], line[3]], color='blue')
            Alt =1
        else:
            ax.plot([line[0], line[2]], [line[1], line[3]], color='orange')
            Alt = 0


    for block in sram_blocks:
        ax.add_patch(plt.Rectangle((block.x, block.y), block.width, block.height, color='blue'))


    for block in blocks_a:
        ax.add_patch(plt.Rectangle((block.x, block.y), block.width, block.height, color='green'))


    for block in blocks_b:
        ax.add_patch(plt.Rectangle((block.x, block.y), block.width, block.height, color='red'))


    plt.show()




if __name__ == "__main__":
    # Create 20 SRAM blocks
    sram_blocks = []
    for _ in range(20):
        sram_blocks.append(Block(10, 10))


    # Create 2 blocks (A)
    blocks_a = []
    for _ in range(2):
        blocks_a.append(Block(10, 800))


    # Create 2 blocks (B)
    blocks_b = []
    for _ in range(2):
        blocks_b.append(Block(80, 10))


    # Set the boundary size
    boundary_height = 500
    boundary_width = 500


    # Set the minimum spacing
    min_spacing = 30
   
    # Set grip spacing
    grip_spacing = 15


    # Create the horizontal grid lines
    grid_lines = create_horizontal_grid(boundary_height, boundary_width, grip_spacing)


    # Perform random placement for SRAM blocks
    sram_blocks = random_placement(sram_blocks, boundary_height, boundary_width, min_spacing)


    # Perform random placement for blocks A
    blocks_a = random_placement(blocks_a, boundary_height, boundary_width, min_spacing)


    # Perform random placement for blocks B
    blocks_b = random_placement(blocks_b, boundary_height, boundary_width, min_spacing)


    # Visualize the initial placement
    visualize_initial_placement(sram_blocks, blocks_a, blocks_b, boundary_height, boundary_width, grid_lines)


    # Perform quadratic placement for SRAM blocks
    sram_blocks = quadratic_placement(sram_blocks, boundary_height, boundary_width, min_spacing)


    # Perform quadratic placement for blocks A and B
    sram_blocks, blocks_a, blocks_b = quadratic_placement_blocks(sram_blocks, blocks_a, blocks_b, boundary_height, boundary_width, min_spacing)


    # Visualize the final placement
    visualize_initial_placement(sram_blocks, blocks_a, blocks_b, boundary_height, boundary_width, grid_lines)