import numpy as np
import pygame
import time


pygame.init()

width, height = 800, 800
screen = pygame.display.set_mode((height, width))

bg = 25, 25, 25
screen.fill(bg)
#Numero de celdas
nxC, nyC = 100, 100
#Dimensiones de la celda
dimCW = width/nxC
dimCH = height/nyC

#Estado de las celdas
gameState = np.zeros((nxC, nyC))

#Automata movil
gameState[21, 21] = 2
gameState[22, 22] = 2
gameState[22, 23] = 2
gameState[21, 23] = 2
gameState[20, 23] = 2

#Automata fijo
#Control de la ejecucion del juego
pauseExect = False
#Bucle de juego
while True:
    newGameState = np.copy(gameState)

    screen.fill(bg)
    time.sleep(0.1)

    #Registrar eventos de teclado y raton
    ev = pygame.event.get()

    for event in ev:
        # Detectamos si se presiona una tecla
        if event.type == pygame.KEYDOWN:
            pauseExect = not pauseExect
        #Detectamos si se preiona el mouse
        mouseClick = pygame.mouse.get_pressed()

        if sum(mouseClick) > 0:
            posX, posY = pygame.mouse.get_pos()
            celX, celY = int(np.floor(posX/dimCW)),  int(np.floor(posY/ dimCH))
            newGameState[celX, celY] = not mouseClick[2]

        if event.type == pygame.QUIT:
            pygame.quit()

    for y in range(0, nyC):
        for x in range(0, nxC):

            if not pauseExect:
                #Calcular el numero de vecinos cercanos
                n_neight = gameState[(x - 1) % nxC ,(y - 1) % nyC] + \
                           gameState[x % nxC, (y - 1) % nyC] + \
                           gameState[(x + 1) % nxC, (y - 1) % nyC] + \
                           gameState[(x - 1) % nxC, y % nyC] + \
                           gameState[(x + 1) % nxC, y % nyC] + \
                           gameState[(x - 1) % nxC, (y + 1) % nyC] + \
                           gameState[x % nxC, (y + 1) % nyC] + \
                           gameState[(x + 1) % nxC, (y + 1) % nyC]
                #Reglas
                #Regla 1: Una celula muerta con exactamente 3 vecinas vivas, "Revive"
                if gameState[x, y] == 0 and n_neight == 3:
                    newGameState[x, y] = 1
                #Regla 2: Una celula viva con menos de 2 o mas de 3 vecinas vivas "Muere"
                elif gameState[x, y] == 1 and (n_neight < 2 or n_neight > 3):
                    newGameState[x, y] = 0

            # Creamos el poligono de cada celda a dibujar
            poly = [((x) * dimCW, y * dimCH),
                    ((x+1)* dimCW,y*dimCH),
                    ((x+1)*dimCW,(y+1)*dimCH),
                    ((x)*dimCW,(y+1)*dimCH)]
            center = (x*dimCW, y * dimCH)
            #if newGameState[x, y] == 0:

                #pygame.draw.polygon(screen, (128, 128, 128), poly, 0)
            #else:
            if newGameState[x, y] == 1:
                pygame.draw.circle(screen, (255, 255, 255), center, 5)
            elif newGameState[x, y] == 2:
                pygame.draw.circle(screen, (255, 0, 0), center, 5)

    #Actualizar estado del juego
    gameState = np.copy(newGameState)

    pygame.display.flip()

