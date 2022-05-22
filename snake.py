import PySimpleGUI as sg
from time import time
from random import choice, randint

# Constants
FIELD_SIZE = 400
CELL_NUM = 10
CELL_SIZE = FIELD_SIZE // CELL_NUM
DIRECTIONS = {"left": (-1, 0), "right": (1, 0), "up": (0, 1), "down": (0, -1)}

def convert_cell_to_pixel(cell):
    top_left = cell[0] * CELL_SIZE, cell[1] * CELL_SIZE
    bottom_right = top_left[0] + CELL_SIZE, top_left[1] + CELL_SIZE
    return top_left, bottom_right

def draw_field(field, apple_pos, snake_body):
    field.erase()

    field.draw_rectangle(*convert_cell_to_pixel(apple_pos), fill_color="red")

    for i, pos in enumerate(snake_body):
        field.draw_rectangle(*convert_cell_to_pixel(pos), fill_color="green" if i else "yellow")

def get_rand_pos():
    return randint(0, CELL_NUM - 1), randint(0, CELL_NUM - 1)

def place_apple(snake_body):
    apple_pos = get_rand_pos()
    while apple_pos in snake_body:
        apple_pos = get_rand_pos()
    return apple_pos

def init_game():
    snake_head = (CELL_NUM // 2, CELL_NUM // 2)
    direction = DIRECTIONS[choice(list(DIRECTIONS.keys()))]
    snake_body = [(snake_head[0] - direction[0] * i, snake_head[1] - direction[1] * i) for i in range(3)]
    return snake_body, direction , place_apple(snake_body)

# Variables
snake_body, direction, apple_pos = init_game()

sg.theme("Green")
field = sg.Graph(canvas_size=(FIELD_SIZE, FIELD_SIZE), graph_bottom_left=(0, 0), graph_top_right=(FIELD_SIZE, FIELD_SIZE), background_color="black")
layout = [
    [field]
]
window = sg.Window("Snake", layout, return_keyboard_events=True)

start_time = time()
while True:
    event, values = window.read(timeout=10)

    if event == sg.WINDOW_CLOSED: break
    if event == "Left:37": direction = DIRECTIONS["left"]
    if event == "Up:38": direction = DIRECTIONS["up"]
    if event == "Right:39": direction = DIRECTIONS["right"]
    if event == "Down:40": direction = DIRECTIONS["down"]

    if time() - start_time >= 0.5:
        start_time = time()

        # Snake update
        new_head = snake_body[0][0] + direction[0], snake_body[0][1] + direction[1]
        snake_body.insert(0, new_head)
        if apple_pos == new_head:
            apple_pos = place_apple(snake_body)
        else:
            snake_body.pop()
        if new_head in snake_body[1:] or not 0 <= new_head[0] < CELL_NUM or not 0 <= new_head[1] < CELL_NUM:
            if sg.popup_yes_no(f"Game over!\nYou win {len(snake_body)} points!\nBegin new game?") == "Yes":
                snake_body, direction, apple_pos = init_game()
            else:
                break

        draw_field(field, apple_pos, snake_body)


window.close()