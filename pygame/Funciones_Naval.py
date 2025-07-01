import random
from pygame import *
import pygame
import os

def printear_lista_continua(lista:list):
    """Recibe una lista y muestra sus elementos por pantalla.

    Args:
        lista (list): Lista cualquiera.
    """
    for i in range(len(lista)):
        if type(lista[i]) == list:
            printear_lista_continua(lista[i])
        elif i == len(lista):
            print(lista[i])
        else:
            print(lista[i],end=" ")


def printear_matriz(matriz:list):
    for f in range(len(matriz)):
        for c in range(len(matriz[f])):
            print(matriz[f][c], end= " ")
        print("")

def bool_aleatorio()->bool:
    numero = random.randint(0,1)
    if numero == 0:
        retorno = False
    else:
        retorno = True
    return retorno

def inicializar_matriz(filas:int,columnas:int,valor_inicial=0)->list:
    """Inicializa una matriz con la cantidad de filas y columas ingresadas. Por defecto los elmentos seran ceros pero se le puede pasar por parametro el valor de los elementos iniciales. 

    Args:
        filas (int): Cantidad de filas que tendra la matriz.
        columnas (int): Cantida de columnas que tendra la matriz.
        valor_inicial : Valor inicial que tendran los elementos de la matriz, por defecto en cero.

    Returns:
        list: Retorna la matriz inicializada.
    """
    matriz = []
    for i in range(filas):
        fila = [valor_inicial] * columnas
        matriz += [fila]
    return matriz

def colocar_barco(matriz:list,barco:list)->list:
    pos = bool_aleatorio()
    posicion_valida = False
    while posicion_valida == False:
        fila = random.randint(0,len(matriz)-1)
        columna = random.randint(0,len(matriz[0])-1)
        for i in range(len(barco)):
            if pos:
                if columna + i >= len(matriz[0]) or matriz[fila][columna + i] == 1:
                    break
                elif matriz[fila][columna + i] == 0 and i == len(barco)-1:
                    posicion_valida = True
            else:
                if fila + i >= len(matriz) or matriz[fila + i][columna] == 1:
                    break
                elif matriz[fila + i][columna] == 0 and i == len(barco)-1:
                    posicion_valida = True
    if posicion_valida:
        for i in range(len(barco)):
            if pos:
                matriz[fila][columna + i] = 1
            else:
                matriz[fila + i][columna] = 1
    coordenada = (fila,columna)
    poscicion = pos
    largo = len(barco)
    #cuadrado = pygame.Rect((27*columna)+27,(27*fila)+100,25,25)            
    datos_barco = [largo,coordenada,poscicion]
    return datos_barco

def colocacion_barcos(matriz:list,barco:list):
    lista_datos = []
    if len(barco) == 1:
        for c in range(4):
            datos = colocar_barco(matriz,barco)
            lista_datos.append(datos)
    elif len(barco) == 2:
        for c in range(3):
            datos = colocar_barco(matriz,barco)
            lista_datos.append(datos)
    elif len(barco) == 3:
        for c in range(2):
            datos = colocar_barco(matriz,barco)
            lista_datos.append(datos)
    elif len(barco) == 4:
        datos = colocar_barco(matriz,barco)
        lista_datos.append(datos)
    return lista_datos

def limpiar_datos(lista_barcos:list)->list:
    lista_limpia = []
    for i in range(len(lista_barcos)):
        tipos_barcos = lista_barcos[i]
        for f in range(len(tipos_barcos)):
            lista_limpia.append(tipos_barcos[f])
            
    return lista_limpia

def tablero_juego(dificultad:str="F")->list:
    filas = 10
    columnas = 10
    repeticiones = 1
    if dificultad == "M":
        filas *= 2
        columnas *= 2
        repeticiones *= 2
    elif dificultad == "D":
        filas *= 4
        columnas *= 4
        repeticiones *= 3

    submarino = [1]
    destructore = [1,1]
    crucero = [1,1,1]
    acorazado =[1,1,1,1]
    barcos = [submarino,destructore,crucero,acorazado]

    tablero = inicializar_matriz(filas,columnas)
    informacion_tablero = False
    for r in range(repeticiones):
        for barco in barcos:
            if informacion_tablero == False:
                info_barcos = [colocacion_barcos(tablero,barco)]
                informacion_tablero = True
            else:
                datos = colocacion_barcos(tablero,barco)
                info_barcos.append(datos)

    lista_limpia = limpiar_datos(info_barcos)

    tablero_info = [tablero,lista_limpia]
    return tablero_info
        
def generar_casilleros(matriz:list)->list:
    lista_casilleros = []
    for f in range(len(matriz)):
        for c in range(len(matriz[0])):
            cuadrado = pygame.Rect((27 * (1+c))+27,(27 * (1+f))+100,25,25) 
            casillero = [cuadrado, True, None]  # Ahora es una lista con color
            lista_casilleros.append(casillero)
    return lista_casilleros

def colocar_casilla(key,screen):
    pygame.draw.rect(screen,"white",key)

#Funciones Pygame
def centrar_eje_x(superfice, objeto_a_centrar)->int:
    """Se encarga de centrar un objeto en su eje X.

    Args:
        superfice : Superficie donde se va a centrar.
        objeto_a_centrar : Objeto que se va a centrar.
    Returns:
        int: centro del eje X.
    """
    centro = superfice.x +(superfice.width - objeto_a_centrar.get_width())/2
    return centro

def centrar_eje_y(superfice, objeto_a_centrar)->int:
    """Se encarga de centrar un objeto en su eje Y.

    Args:
        superfice : Superficie donde se va a centrar.
        objeto_a_centrar : Objeto que se va a centrar.
    Returns:
        int: centro del eje Y.
    """
    centro = superfice.y +(superfice.height - objeto_a_centrar.get_height())/2
    return centro

def poner_boton(screen, boton, palabra:str, color_apretado, color_no_apretado, fuente):
    """Se encarga de poner un boton en la pantalla.

    Args:
        screen : pantalla donde se colocara el boton.
        boton : boton a colocar.(El boton ya debe estar creado con su posicion y tamaño.)
        palabra (str): texto del boton.
        color_apretado : color del boton.
        color_no_apretado : color del boton al posicionarse encima.
        fuente : fuente del texto.
    """
    if boton.collidepoint(mouse.get_pos()):
        draw.rect(screen,(color_apretado), boton, 0)
    else:
        draw.rect(screen,(color_no_apretado), boton, 0)
    texto = fuente.render(palabra, True, ("white"))
    screen.blit(texto,(centrar_eje_x(boton,texto),centrar_eje_y(boton,texto)))

def cargar_imagen(ruta:str,medidas:tuple):
    # Obtener la ruta absoluta basada en la ubicación de este archivo
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_absoluta = os.path.join(base_path, ruta)
    imagen = pygame.image.load(ruta_absoluta)
    imagen_transformada = pygame.transform.scale(imagen,medidas)
    return imagen_transformada


def escribir_palabara(screen,text, pos=(0,0), size=16, color=(0,0,0)):
    font = pygame.font.SysFont("Consolas", size)
    screen.blit(font.render(text, True, color), pos)

def guardar_puntaje(nick, puntaje, archivo='puntajes.txt'):
    with open(archivo, 'a') as f:
        f.write(f'{nick},{puntaje}\n')

def obtener_mejores_puntajes(archivo='puntajes.txt', cantidad=3):
    puntajes = []
    try:
        with open(archivo, 'r') as f:
            for linea in f:
                partes = linea.strip().split(',')
                if len(partes) == 2:
                    nombre, puntos = partes
                    try:
                        puntos = int(puntos)
                        puntajes.append((nombre, puntos))
                    except ValueError:
                        continue  # Ignora líneas con puntaje no numérico
    except FileNotFoundError:
        pass
    
    # Ordenar por puntaje (de mayor a menor)
    for i in range(len(puntajes)):
        for j in range(i + 1, len(puntajes)):
            if puntajes[i][1] < puntajes[j][1]:
                puntajes[i], puntajes[j] = puntajes[j], puntajes[i]

    return puntajes[:cantidad]