import pygame
import sys
from Batalla_naval import *

pygame.init()

ANCHO, ALTO = 600, 700
TAMAÑO_CASILLA = 60

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Batalla Naval")

fuente = pygame.font.SysFont("Arial", 30)


datos_tablero = tablero_juego()
casillas = datos_tablero[0] 
info_barcos = datos_tablero[1]  

FILAS = len(casillas)
COLUMNAS = len(casillas[0])

# Inicializamos matriz de disparos
impactos = [[False for _ in range(COLUMNAS)] for _ in range(FILAS)]

# Generamos todas las posiciones ocupadas por naves
nave = []
for barco in info_barcos:
    (fila, col), horizontal, largo = barco
    for i in range(largo):
        if horizontal:
            nave.append((fila, col + i))
        else:
            nave.append((fila + i, col))

# Estado de cada parte de la nave (True si fue impactada)
nave_destruida = [False] * len(nave)

puntaje = 0

def mostrar_puntaje():
    texto = fuente.render(f"Puntaje: {puntaje:04}", True)
    pantalla.blit(texto, (20, ALTO - 60))

corriendo = True
while corriendo:
    mostrar_puntaje()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

        elif evento.type == pygame.MOUSEBUTTONDOWN:
            x, y = evento.pos
            if y < FILAS * TAMAÑO_CASILLA:
                fila = y // TAMAÑO_CASILLA
                col = x // TAMAÑO_CASILLA
                if not impactos[fila][col]:  
                    impactos[fila][col] = True

                    if casillas[fila][col] == 1:
                        puntaje += 5
                        if (fila, col) in nave:
                            index = nave.index((fila, col))
                            nave_destruida[index] = True
                            if all(nave_destruida):
                                puntaje += 10 * len(nave)
                    else:
                        puntaje -= 1
                else:
                    print("Casilla ya fue disparada")

    pygame.display.flip()

pygame.quit()
sys.exit()
