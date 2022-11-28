import pygame
import time
import numpy as np
import pygame_gui

COLOR_BG = (10, 10 , 10)
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (255, 255, 255)
FIRE_COLOR = (255, 0, 0)

screen_size = (800, 600)

def hood_8(row, col):
    coords = []
    coords.append((row-1, col-1))
    coords.append((row-1, col))
    coords.append((row-1, col+1))
    coords.append((row, col-1))
    coords.append((row, col+1))
    coords.append((row+1, col-1))
    coords.append((row+1, col))
    coords.append((row+1, col+1))
    return coords

def hood_24(row, col):
    coords = []
    coords.append((row-2, col-2))
    coords.append((row-2, col-1))
    coords.append((row-2, col))
    coords.append((row-2, col+1))
    coords.append((row-2, col+2))
    coords.append((row-1, col-2))
    coords.append((row-1, col-1))
    coords.append((row-1, col))
    coords.append((row-1, col+1))
    coords.append((row-1, col+2))
    coords.append((row, col-2))
    coords.append((row, col-1))
    coords.append((row, col+1))
    coords.append((row, col+2))
    coords.append((row+1, col-2))
    coords.append((row+1, col-1))
    coords.append((row+1, col))
    coords.append((row+1, col+1))
    coords.append((row+1, col+2))
    coords.append((row+2, col-2))
    coords.append((row+2, col-1))
    coords.append((row+2, col))
    coords.append((row+2, col+1))
    coords.append((row+2, col+2))
    return coords

def sumAndClean(cells, coords, search, ignore=[]):
    sum = cont = 0
    for coord in coords:
        if cont not in ignore:
            if coord[0] < 0 or coord[1] < 0 or coord[0] >= cells.shape[0] or coord[1] >= cells.shape[1]:
                pass
            else:
                sum += 1 if cells[coord[0], coord[1]] == search else 0
        cont += 1
    return sum

def default(cells, row, col, search=2):
    sum = sumAndClean(cells, hood_8(row, col), search)
    return True if sum >= 1 else False

def north_1(cells, row, col, search=2):
    sum = sumAndClean(cells, hood_8(row, col), search, [5, 6, 7])
    return True if sum >= 1 else False

def north_2(cells, row, col, search=2):
    sum = sumAndClean(cells, hood_24(row, col), search, [0, 4, 5, 9, 10, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
    return True if sum >= 1 else False

def west_1(cells, row, col, search=2):
    sum = sumAndClean(cells, hood_8(row, col), search, [2, 4, 7])
    return True if sum >= 1 else False

def west_2(cells, row, col, search=2):
    sum = sumAndClean(cells, hood_24(row, col), search, [0, 1, 2, 3, 4, 8, 9, 12, 13, 17, 18, 19, 20, 21, 22, 23])
    return True if sum >= 1 else False

def south_1(cells, row, col, search=2):
    sum = sumAndClean(cells, hood_8(row, col), search, [0, 1, 2])
    return True if sum >= 1 else False

def south_2(cells, row, col, search=2):
    sum = sumAndClean(cells, hood_24(row, col), search, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14, 18, 19, 23])
    return True if sum >= 1 else False

def east_1(cells, row, col, search=2):
    sum = sumAndClean(cells, hood_8(row, col), search, [0, 3, 5])
    return True if sum >= 1 else False

def east_2(cells, row, col, search=2):
    sum = sumAndClean(cells, hood_24(row, col), search, [0, 1, 2, 3, 4, 5, 6, 10, 11, 14, 15, 19, 20, 21, 22, 23])
    return True if sum >= 1 else False

def northwest_1(cells, row, col, search=2):
    sum = sumAndClean(cells, hood_8(row, col), search, [4, 6, 7])
    return True if sum >= 1 else False

def northwest_2(cells, row, col, search=2):
    sum = sumAndClean(cells, hood_24(row, col), search, [3, 4, 8, 9, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
    return True if sum >= 1 else False

def southwest_1(cells, row, col, search=2):
    sum = sumAndClean(cells, hood_8(row, col), search, [1, 2, 4])
    return True if sum >= 1 else False

def southwest_2(cells, row, col, search=2):
    sum = sumAndClean(cells, hood_24(row, col), search, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13, 17, 18, 22, 23])
    return True if sum >= 1 else False

def southeast_1(cells, row, col, search=2):
    sum = sumAndClean(cells, hood_8(row, col), search, [0, 1, 3])
    return True if sum >= 1 else False

def southeast_2(cells, row, col, search=2):
    sum = sumAndClean(cells, hood_24(row, col), search, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 14, 15, 19, 20])
    return True if sum >= 1 else False

def northeast_1(cells, row, col, search=2):
    sum = sumAndClean(cells, hood_8(row, col), search, [3, 5, 6])
    return True if sum >= 1 else False

def northeast_2(cells, row, col, search=2):
    sum = sumAndClean(cells, hood_24(row, col), search, [0, 1, 5, 6, 10, 11, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23])
    return True if sum >= 1 else False

def hood_function(velocity, direction):
    if velocity == 1:
        if direction == "norte":
            return north_1
        elif direction == "sur":
            return south_1
        elif direction == "este":
            return east_1
        elif direction == "oeste":
            return west_1
        elif direction == "noroeste":
            return northwest_1
        elif direction == "noreste":
            return northeast_1
        elif direction == "sureste":
            return southeast_1
        elif direction == "suroeste":
            return southwest_1
    elif velocity == 2:
        if direction == "norte":
            return north_2
        elif direction == "sur":
            return south_2
        elif direction == "este":
            return east_2
        elif direction == "oeste":
            return west_2
        elif direction == "noroeste":
            return northwest_2
        elif direction == "noreste":
            return northeast_2
        elif direction == "sureste":
            return southeast_2
        elif direction == "suroeste":
            return southwest_2

    return default

def update(screen, cells, size, hood_fun, with_progress=False):
    update_cells = np.zeros((cells.shape[0], cells.shape[1]))
    
    for row, col in np.ndindex(cells.shape):
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT if cells[row, col] == 1 else FIRE_COLOR
        # print(row, col)
        # Si la celda tiene al menos un vecino 2
        if hood_fun(cells, row, col):
            # Si la celda es 1 se convierte en 2
            if cells[row, col] == 1:
                update_cells[row, col] = 2
                if with_progress:
                    color = COLOR_DIE_NEXT
        # Si la celda no tiene vecinos 2
        else:
            # Si la celda es 1 se queda en 1
            if cells[row, col] == 1:
                update_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT
                    
        pygame.draw.rect(screen, color, (col*size, row*size, size - 1, size - 1))
        
    return update_cells

def play(hood_fun, random=False):
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Fire Simulation")
    cells = np.zeros((60,80))
    if random:
        cells = np.random.randint(0, 2, size=(60,80))
    screen.fill(COLOR_GRID)
    update(screen, cells, 10, hood_fun)
    
    pygame.display.flip()
    pygame.display.update()
    
    running = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10, hood_fun)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if cells[pos[1]//10, pos[0]//10] != 1:
                    cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen, cells, 10, hood_fun)
                pygame.display.update()

            elif pygame.mouse.get_pressed()[1]:
                pos = pygame.mouse.get_pos()
                if cells[pos[1]//10, pos[0]//10] != 0:
                    cells[pos[1] // 10, pos[0] // 10] = 0
                update(screen, cells, 10, hood_fun)
                pygame.display.update()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                if cells[pos[1]//10, pos[0]//10] != 2:
                    cells[pos[1] // 10, pos[0] // 10] = 2
                update(screen, cells, 10, hood_fun)
                pygame.display.update()

        screen.fill(COLOR_GRID)
        
        if running:
            cells = update(screen, cells, 10, hood_fun, with_progress=True)
            pygame.display.update()

        if not running:
            time.sleep(0.001)
        else:
            time.sleep(0.9)


if __name__ == "__main__":
    direction = velocity = None
    velocity = int(input("Ingrese la velocidad del viento [0 - 2]:\n"))
    if velocity > 0:
        direction = input("Ingrese la dirección del viento [norte, sur, este, oeste, noroeste, noreste, sureste, suroeste]:\n").lower()
    hood_fun = hood_function(velocity, direction)
    random = input("Iniciar con un bosque aleatorio? [y/n]:\n").lower() == "y"
    play(hood_fun, random=random)
    # cells = np.zeros((7, 7))
    # cells[3, 3] = 2
    # cells[3, 4] = 2
    # cells[3, 2] = 1
    # print("OG\n",cells)
    # funcion = hood_function(1, "norte")
    # while True:
    #     new = np.zeros((7, 7))
    #     for row, col in np.ndindex(cells.shape):
    #         # Si la celda tiene al menos un vecino 1
    #         if funcion(cells, row, col):
    #             # Si la celda es 2 se convierte en 1
    #             if cells[row, col] == 2:
    #                 new[row, col] = 1
    #         # Si la celda no tiene vecinos 1
    #         else:
    #             # Si la celda es 2 se queda en 2
    #             if cells[row, col] == 2:
    #                 new[row, col] = 2
    #     cells = new
    #     print("NEW\n",cells)
    #     if cells.sum() == 0:
    #         break
    #     elif not 1 in cells:
    #         break
