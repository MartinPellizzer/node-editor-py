import pygame
import random

pygame.init()

window_w = 1920
window_h = 1080

cell_size = 16
col_num = window_w // cell_size
row_num = window_h // cell_size

screen = pygame.display.set_mode([window_w, window_h])

node_color_bg = '#303030'
junction_size = 8
junction_y = 48

node = {
    'id': 0,
    'name': 'speed',
    'val': '0',
    'x': 700,
    'y': 500,
    'w': 200,
    'h': 200,
    'junctions_in': [
        {
            'id': 0,
            'name': 'distance',
            'x': 0,
            'y': junction_y*1,
            'node_id': 1,
            'junction_id': 0,
        },
        {
            'id': 1,
            'name': 'time',
            'x': 0,
            'y': junction_y*2,
            'node_id': 2,
            'junction_id': 0,
        },
    ],
    'junctions_out': [
        {
            'id': 2,
            'name': 'val',
        },
    ]
}

node_distance = {
    'id': 1,
    'name': 'distance',
    'val': '10',
    'x': 300,
    'y': 400,
    'w': 200,
    'h': 100,
    'junctions_out': [
        {
            'id': 0,
            'name': 'val',
            'x': 200,
            'y': junction_y*1,
        },
    ]
}

node_time = {
    'id': 2,
    'name': 'time',
    'val': '2',
    'x': 300,
    'y': 600,
    'w': 200,
    'h': 100,
    'junctions_out': [
        {
            'id': 0,
            'name': 'val',
            'x': 200,
            'y': junction_y*1,
        },
    ],
}

nodes = []
nodes.append(node)
nodes.append(node_distance)
nodes.append(node_time)

node_drag_off_x = 0
node_drag_off_y = 0

node_snap = False

line_creating = False
line_starting_x = -1 
line_starting_y = -1


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        '''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (mouse_x > node['x'] and 
                    mouse_y > node['y'] and 
                    mouse_x < node['x'] + node['w'] and 
                    mouse_y < node['y'] + node['h']):
                    
                    node['x'] += 100
        '''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LALT:
                node_snap = True
            if event.key == pygame.K_UP:
                for node in nodes:
                    if node['name'] == 'distance':
                        node['val'] = str(float(node['val'])+1)

    screen.fill('#1d1d1d')

    # mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    # left click
    if pygame.mouse.get_pressed()[0] == True: 
        for node_i, node in enumerate(nodes):
            if not mouse_left_pressed:
                # junctions_in
                if 'junctions_in' in node:
                    junction_found = False
                    for junction in node['junctions_in']:
                        junction_x1 = node['x'] + junction['x'] - junction_size
                        junction_y1 = node['y'] + junction['y'] - junction_size
                        junction_x2 = node['x'] + junction['x'] + junction_size
                        junction_y2 = node['y'] + junction['y'] + junction_size
                        if (mouse_x > junction_x1 and
                            mouse_x < junction_x2 and
                            mouse_y > junction_y1 and
                            mouse_y < junction_y2):
                            line_creating = True
                            line_starting_x = mouse_x
                            line_starting_y = mouse_y
                            junction_found = True
                            break
                    if junction_found:
                        break
                node_x = node['x']
                node_y = node['y']
                node_w = node['w']
                node_h = node['h']
                if (mouse_x > node_x + node_w - junction_size and
                    mouse_x < node_x + node_w + junction_size and
                    mouse_y > node_y + 30 - junction_size and
                    mouse_y < node_y + 30 + junction_size):
                    print('junction')
                    line_creating = True
                    line_starting_x = mouse_x
                    line_starting_y = mouse_y
                elif mouse_x > node_x and mouse_x < node_x + node_w and mouse_y > node_y and mouse_y < node_y + node_h:
                    node_drag_id = node_i
                    node_drag_off_x = mouse_x - node['x']
                    node_drag_off_y = mouse_y - node['y']
        mouse_left_pressed = True
    else:
        if line_creating:
            line_creating = False

        mouse_left_pressed = False
        node_drag_id = -1

    # dragging
    if node_drag_id != -1:
        if node_snap:
            col_i = (mouse_x - node_drag_off_x + cell_size//2)//cell_size
            row_i = (mouse_y - node_drag_off_y + cell_size//2)//cell_size
            node_x_snap = col_i * cell_size
            node_y_snap = row_i * cell_size
            nodes[node_drag_id]['x'] = node_x_snap
            nodes[node_drag_id]['y'] = node_y_snap
        else:
            nodes[node_drag_id]['x'] = mouse_x - node_drag_off_x
            nodes[node_drag_id]['y'] = mouse_y - node_drag_off_y

    # grid
    cell_num = window_w // cell_size
    for i in range(cell_num):
        pygame.draw.line(screen, '#181818', (cell_size*i, 0), (cell_size*i, window_h))
        pygame.draw.line(screen, '#181818', (0, cell_size*i), (window_w, cell_size*i))
    _cell_size = cell_size*4
    _cell_num = window_w // _cell_size
    for i in range(_cell_num):
        pygame.draw.line(screen, '#101010', (_cell_size*i, 0), (_cell_size*i, window_h))
        pygame.draw.line(screen, '#101010', (0, _cell_size*i), (window_w, _cell_size*i))

    # creating line
    if line_creating:
        pygame.draw.line(screen, '#ffffff', 
            (line_starting_x, line_starting_y),
            (mouse_x, mouse_y),
        )

    for node in nodes:
        if 'junctions_in' in node:
            for junction in node['junctions_in']:
                if 'node_id' in junction and 'junction_id' in junction:
                    if junction['node_id'] != -1 and junction['junction_id'] != -1:
                        node_2 = {}
                        for _node in nodes:
                            if _node['id'] == junction['node_id']:
                                node_2 = _node
                                break
                        junction_2 = {}
                        for _junction in node_2['junctions_out']:
                            if _junction['id'] == junction['junction_id']:
                                junction_2 = _junction
                        line_x1 = node['x'] + junction['x']
                        line_y1 = node['y'] + junction['y']
                        line_x2 = node_2['x'] + junction_2['x']
                        line_y2 = node_2['y'] + junction_2['y']
                        pygame.draw.line(screen, '#ffffff', 
                            (line_x1, line_y1),
                            (line_x2, line_y2),
                        )
                

    # node
    for node in nodes:
        pygame.draw.rect(
            screen, node_color_bg, 
            (node['x'], node['y'], node['w'], node['h']), 
            0,
        )
        
        if 'junctions_in' in node:
            for junction in node['junctions_in']:
                pygame.draw.circle(
                    screen, "#ffffff", (node['x'], node['y'] + junction['y']), junction_size, width=0
                )
                
        # text
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 16)
        text_surface = font.render(node['name'], False, (255, 255, 255))
        screen.blit(text_surface, (node['x'], node['y']))

        text_surface = font.render(node['val'], False, '#ffffff')
        screen.blit(text_surface, (node['x'] + 80, node['y']))

        # calc
        for node in nodes:
            if node['name'] == 'speed':
                speed = 0
                distance = 0
                time = 0
            
                for junction_in in node['junctions_in']: 
                    if junction_in['name'] == 'distance':
                        node_2_id = junction_in['node_id']
                        node_2 = [n for n in nodes if n['id'] == junction_in['node_id']][0]
                        # junction_2 = [j for j in node_2['junctions_out'] if j['id'] == junction_in['junction_id']][0]
                        distance = node_2['val']
                    if junction_in['name'] == 'time':
                        node_2_id = junction_in['node_id']
                        node_2 = [n for n in nodes if n['id'] == junction_in['node_id']][0]
                        # junction_2 = [j for j in node_2['junctions_out'] if j['id'] == junction_in['junction_id']][0]
                        time = node_2['val']
                speed = float(distance)/float(time)
                node['val'] = str(speed)


    pygame.display.flip()

pygame.quit()
