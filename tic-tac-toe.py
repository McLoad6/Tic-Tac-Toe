import pygame
import time
from copy import deepcopy


def position_searcher(position: list, table_list: list) -> bool:
    (x, y) = position
    return table_list[x][y] == 0


def winner(xoro: int, position: list, table_list: list):
    [x, y] = position
    if xoro == table_list[x][0] and xoro == table_list[x][1] and xoro == table_list[x][2]:
        return [(x * 200 + 100, 10), (x * 200 + 100, 590)]
    if xoro == table_list[0][y] and xoro == table_list[1][y] and xoro == table_list[2][y]:
        return [(10, y * 200 + 100), (590, y * 200 + 100)]
    if x == y:
        if xoro == table_list[0][0] and xoro == table_list[1][1] and xoro == table_list[2][2]:
            return [(10, 10), (590, 590)]
    if x+y == 2:
        if xoro == table_list[0][2] and xoro == table_list[1][1] and xoro == table_list[2][0]:
            return [(10, 590), (590, 10)]
    return False

def winner_step_test(table_list: list):
    for i in range(3):
        for j in range(3):
            if table_list[i][j] == 0:
                test_list = deepcopy(table_list)
                test_list[i][j] = 2
                if winner(2, [i, j], test_list) is not False:
                    return [i, j]
    for i in range(3):
        for j in range(3):
            if table_list[i][j] == 0:
                test_list = deepcopy(table_list)
                test_list[i][j] = 1
                if winner(1, [i, j], test_list) is not False:
                    return [i, j]
    return False
                
def step_is_edge(coordinate) -> bool:
    return (coordinate[0] == 0 or coordinate[0] == 2) and (coordinate[1] == 0 or coordinate[1] == 2)

def empty_space(table_list: list):
    for i in range(3):
        for j in range(3):
            if table_list[i][j] == 0:
                return [i, j]
    return False

def next_step(table_list: list) -> list:
    player_steps = 0
    for i in range(3):
        for j in range(3):
            if table_list[i][j] == 1:
                player_steps += 1
                (x, y) = (i, j)
    if player_steps == 1:
        if (x, y) == (1, 1):
            target_step = [0, 0]
        else:
            target_step = [1, 1]
    elif player_steps == 2:
        if (next_step := winner_step_test(table_list)) is not False:
            target_step = next_step
        else:
            if table_list[1][1] == 1:
                target_step = [0, 2]
            else:
                if (table_list[0][0] == 1 and table_list[2][2]) == 1 or (table_list[0][2] == 1 and table_list[2][0] == 1):
                    target_step = [0, 1]
                else:
                    for i in range(3):
                        for j in range(3):
                            if table_list[i][j] == 1 and (i + j) % 2 == 0:
                                step1 = [i, j]
                            elif table_list[i][j] == 1 and (i + j) % 2 == 1:
                                step2 = [i, j]
                    if step2[0] == 1:
                        target_step = [step1[0], step2[1]]
                    else:
                        target_step = [step2[0], step1[1]]
    elif player_steps == 3:
        if (next_step := winner_step_test(table_list)) is not False:
            target_step = next_step
        else:
            filled_x = []
            filled_o = []
            for i in range(3):
                for j in range(3):
                    if table_list[i][j] == 1:
                        filled_x.append([i, j])
                    elif table_list[i][j] == 2:
                        filled_o.append([i, j])
            edge = 0
            for coordinate in filled_x:
                if step_is_edge(coordinate):
                    edge +=1
                    if edge == 1:
                        corner_x1 = coordinate
                    else:
                        corner_x2 = coordinate
            for [x, y] in filled_o:
                if (x + y) % 2 == 1:
                    side_o = [x, y]
            if table_list[1][1] == 2:
                if edge == 1:
                    if corner_x1[0] == side_o[0]:
                        if corner_x1[0] == 0:
                            target_step = [2, corner_x1[1]]
                        else:
                            target_step = [0, corner_x1[1]]
                    else:
                        if corner_x1[1] == 0:
                            target_step = [corner_x1[0], 2]
                        else:
                            target_step = [corner_x1[0], 0]
                else:
                    if corner_x1[0] == corner_x2[0]:
                        target_step = [1, 0]
                    else:
                        target_step = [0, 1]
            else:
                if corner_x1[0] == side_o[0]:
                    if corner_x1[0] == 0:
                        target_step = [2, corner_x1[1]]
                    else:
                        target_step = [0, corner_x1[1]]
                else:
                    if corner_x1[1] == 0:
                        target_step = [corner_x1[0], 2]
                    else:
                        target_step = [corner_x1[0], 0]
    else:
        if (next_step := winner_step_test(table_list)) is not False:
            target_step = next_step
        else:
            target_step = empty_space(table_list)
    return target_step            

def visualisation():
    pygame.init()

    table_color = ['burlywood1', 'saddle brown']

    table_size = 600
    field_size = table_size // 3

    table = pygame.display.set_mode((table_size, table_size))

    table_list = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    xoro = 1  # x or o
    win = 0
    pvp = 0

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_location = event.dict["pos"]
                [x, y] = click_location
                pos_x = x // 200
                pos_y = y // 200
                position = [pos_x, pos_y]
                if position_searcher(position, table_list):
                    table_list[pos_x][pos_y] = xoro
                    if pvp == 0:
                        if (win_line := winner(xoro, position, table_list)) is not False:
                            win = 1
                        if win == 0 and empty_space(table_list) is not False:
                            [pos_x, pos_y] = next_step(table_list)
                            position = [pos_x, pos_y]
                            table_list[pos_x][pos_y] = 2
                            xoro = (xoro % 2) +1
                    if (win_line := winner(xoro, position, table_list)) is not False:
                        win = 1
                    xoro = (xoro % 2) +1

        for row in range(3):  # creating table
            color_index = row % 2
            for column in range(3):
                field = (column * field_size, row * field_size, field_size, field_size)
                table.fill(table_color[color_index], field)
                color_index = (color_index + 1) % 2  # color changing

        for i in range(3):
            a = table_list[i]
            for j in range(3):
                b = a[j]
                if b == 1:
                    [x, y] = [i*200, j*200]
                    pygame.draw.line(table, "blue", (x+10, y+10), (x+190, y+190), 5)
                    pygame.draw.line(table, "blue", (x+10, y+190), (x+190, y+10), 5)
                elif b == 2:
                    [x, y] = [i*200, j*200]
                    pygame.draw.circle(table, "red", (x+100, y+100), 80, 5)

        if win == 1:
            [[x1, y1], [x2, y2]] = win_line
            pygame.draw.line(table, "red", (x1, y1), (x2, y2), 20)
            pygame.display.flip()
            time.sleep(2)
            pygame.quit()

        pygame.display.flip()

    pygame.quit()


visualisation()
