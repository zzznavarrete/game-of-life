import pygame
import numpy as np
import time


pygame.init()

# Ancho y alto de la pantalla
width, height = 500, 500
# Creacion de la pantalla
screen = pygame.display.set_mode((500,500), pygame.RESIZABLE)


# Color del fondo = Casi negro.
bg = 25, 25, 25

# Pintamos el fondo con el color elegido.
screen.fill(bg)


nxC, nyC = 50, 50

dimCW = width / nxC
dimCH = height / nyC

# Estado de las celdas, viva = 1, muertas = 0
gameState = np.zeros((nxC, nyC))


# Autómata palo
gameState[5, 3] = 1
gameState[5, 4] = 1
gameState[5, 5] = 1

# Autómata móvil
gameState[21, 21] = 1
gameState[22, 22] = 1
gameState[22, 23] = 1
gameState[21, 23] = 1
gameState[20, 23] = 1

# Control de la ejecución
pause_exec = False

# Bucle de ejecucion
while True:

    newGameState = np.copy(gameState)
    screen.fill(bg)
    time.sleep(0.1)

    # Registramos eventos de teclado y ratón.
    ev = pygame.event.get()

    for event in ev:
        if event.type == pygame.KEYDOWN:
            pause_exec = not pause_exec

        mouse_click = pygame.mouse.get_pressed()
        # print(mouse_click)

        if sum(mouse_click) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX / dimCW)), int(np.floor(posY / dimCH))
            newGameState[celX, celY] = not mouse_click[2]

    for y in range(0, nxC):
        for x in range(0, nyC):

            if pause_exec:

                # Calculamos el número de vecinos cercanos.
                n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC ] + \
                          gameState[(x)     % nxC, (y - 1) % nyC ] + \
                          gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                          gameState[(x - 1) % nxC, (y) % nyC] + \
                          gameState[(x + 1) % nxC, (y) % nyC] + \
                          gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                          gameState[(x)     % nxC, (y + 1) % nyC] + \
                          gameState[(x + 1) % nxC, (y + 1) % nyC]

                # Rule #1: Una célula muerta con exactamente 3 vecinas vivas, "revive".
                if gameState[x, y] == 0 and n_neigh == 3:
                    newGameState[x, y] = 1

                # Rule #2: Una célular viva con menos de 2 o más de 3 vecinas vive, "muere".
                elif gameState[x,y] == 1 and (n_neigh < 2 or n_neigh > 3):
                    newGameState[x, y] = 0

                # Creamos el polígocno de cada celda a dibujar
            poly = [((x) * dimCW, y * dimCH),
                    ((x+1) * dimCW, y * dimCH),
                    ((x+1) * dimCW, (y+1) * dimCH),
                    ((x) * dimCW, (y+1) * dimCH)]

            # Y dibujamos la celda para cada par de x e y.
            if newGameState[x, y] == 0:
                pygame.draw.polygon(screen, (128, 128, 128),  poly, 1)
            else:
                pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

    # Actualizamos el estado
    gameState = np.copy(newGameState)

    # Actualizamos la pantalla.
    pygame.display.flip()
