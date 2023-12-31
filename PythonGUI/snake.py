import PySimpleGUI as sg
from time import time
from random import randint

FIELD_SIZE = 400
CELL_NUM = 10
CELL_SIZE = FIELD_SIZE/CELL_NUM

def convert_pos_to_pixel(cell):
    tl = cell[0] * CELL_SIZE, cell[1] * CELL_SIZE
    br = tl[0] + CELL_SIZE, tl[1] + CELL_SIZE  
    return tl,br

def place_apple():
    apple_pos = randint(0, CELL_NUM - 1), randint(0, CELL_NUM - 1) 
    while apple_pos in snake_body:
        apple_pos = (randint(0, CELL_NUM - 1), randint(0, CELL_NUM - 1))
    return apple_pos

snake_body = [(4,4),(3,4),(2,4)]
DIRECTIONS = {'left':(-1,0),'right':(1,0),'up':(0,1),'down':(0,-1)}
direction = DIRECTIONS['up']

apple_pos = place_apple()
apple_eaten = False

sg.theme('Green')
field = sg.Graph(canvas_size = (FIELD_SIZE,FIELD_SIZE),
                 graph_bottom_left = (0,0),
                 graph_top_right = (FIELD_SIZE,FIELD_SIZE),
                 background_color = 'black') 
layout = [[field], [sg.Push(), sg.Text('Points:'), sg.Text('0', key = '-Points-')]]

window = sg.Window('Snake', layout, return_keyboard_events = True)

start_time = time()
while True:
    event, values = window.read(timeout = 10)
    
    if event == sg.WIN_CLOSED: break
    if event == 'Left:113': direction = DIRECTIONS['left']
    if event == 'Up:111': direction = DIRECTIONS['up']
    if event == 'Right:114': direction = DIRECTIONS['right']
    if event == 'Down:116': direction = DIRECTIONS['down']

    time_since_start = time() - start_time
    if time_since_start >= 0.5:
        start_time = time()

        if apple_pos == snake_body[0]:
            apple_pos = place_apple()
            apple_eaten = True

        new_head = (snake_body[0][0] + direction[0],snake_body[0][1] + direction[1])
        snake_body.insert(0, new_head)
        if not apple_eaten:
            snake_body.pop()
        apple_eaten = False

        points = len(snake_body)-3
        window['-Points-'].update(points)

        if not 0 <= snake_body[0][0] <= CELL_NUM - 1 or not 0 <= snake_body[0][1] <= CELL_NUM - 1 or snake_body[0] in snake_body[1:]:
            sg.popup(f'Points:{points}')
            break

        field.DrawRectangle((0,0), (FIELD_SIZE, FIELD_SIZE), 'black')

        tr, br = convert_pos_to_pixel(apple_pos)
        field.DrawRectangle(tr, br,'red')
  
        for index, part in enumerate(snake_body):
            tl, br = convert_pos_to_pixel(part)
            color = 'yellow' if index == 0 else 'green'
            field.DrawRectangle(tl, br, color)

window.close()