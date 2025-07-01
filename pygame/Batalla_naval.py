from Funciones_Naval import *
import pygame as pg
import os

#COLORES
naranja = (255,163,38,254)
naranja_apretado = (243,188,44,254)
color_verde = (22,244,8)
color_blanco = (255,255,255)
color_negro = (0,0,0)
color_azul = (138, 158, 255)
azul_2 = (110, 125, 255)
gris_apretado = (125,125,125)
gris = (200,200,200)

#DIMENSIONES
width = 900
height = 600
screen = pg.display.set_mode((width,height),pg.RESIZABLE)
ancho = screen.get_width()
alto = screen.get_height()

#IMAGENES
fondo_menu = cargar_imagen("Proyecto_Batalla_Naval/Elementos_Naval/fondo_gpt1.webp", (width, height))
fondo_juego = cargar_imagen("Proyecto_Batalla_Naval/Elementos_Naval/fondo_jugando.webp",(width,height))
titulo_2 = cargar_imagen("Proyecto_Batalla_Naval/Elementos_Naval/titulo_pixel.png",(width*0.50,height*0.60))
inicio_buque = cargar_imagen("Proyecto_Batalla_Naval/Elementos_Naval/buque_naval.webp",(width*0.80,height*0.80))

#BOTONES
boton_start = Rect(ancho/2-130/2,100,130,50)
boton_dificultad = Rect(ancho/2-130/2,200,130,50)
boton_puntajes = Rect(ancho/2-130/2,300,130,50)
boton_salir = Rect(ancho/2-130/2,400,130,50)
facil = Rect(ancho/2-130/2,100,130,50)
medio = Rect(ancho/2-130/2,200,130,50)
dificil = Rect(ancho/2-130/2,300,130,50)
boton_volver = Rect(ancho-130-50,20,130,50)
boton_reiniciar = Rect(50+150,20,130,50)
boton_musica = Rect(50,20,130,50)


#PRUEBAS
'''
tablero_real = tablero_juego("D")
tablero_covertura = inicializar_matriz(len(tablero_real),len(tablero_real[0]))
printear_matriz(tablero_real[0])
datos_barcos = tablero_real[1]
"""print(datos_barcos)
"""
for i in range(len(datos_barcos)):
    printear_lista_continua(datos_barcos[i])
    print(f"- Numero : {i+1}")
'''
#printear_matriz(tablero_covertura)

#JUEGO

pg.init()
pg.mixer.init()

# Ruta absoluta para la música
base_path = os.path.dirname(os.path.abspath(__file__))
musica_path = os.path.join(base_path, "Elementos_Naval", "musica_juego.mp3")

#BANDERAS
inicio = True
menu = False
jugando = False
menu_dificultad = False
puntajes = False
musica = True
dificultad = "F"
pidiendo_nick = False
viendo_puntajes = False
nick = ''

#tablero_real = tablero_juego()
pg.mixer.music.load(musica_path)
pg.mixer.music.play(-1)

def iniciar_nueva_partida(dificultad):
    juego = tablero_juego(dificultad)
    tablero_real = juego[0]
    lista_barcos = juego[1]
    tablero_covertura = inicializar_matriz(len(tablero_real),len(tablero_real[0]))
    lista_casilleros = generar_casilleros(tablero_real)
    barcos_estado = [barco[0] for barco in lista_barcos]
    puntaje = 0
    disparos_realizados = 0
    return tablero_real, lista_barcos, tablero_covertura, lista_casilleros, barcos_estado, puntaje, disparos_realizados

game = True
while game:
    
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            game = False

        if pidiendo_nick:
            if evento.type == pg.KEYDOWN:
                if evento.key == pg.K_RETURN:
                    if nick.strip() != '':
                        print(f'Guardando: {nick},{puntaje}')  # Depuración
                        guardar_puntaje(nick, puntaje)
                        pidiendo_nick = False
                        menu = True
                        nick = ''
                    else:
                        print('El nombre no puede estar vacío')
                elif evento.key == pg.K_BACKSPACE:
                    nick = nick[:-1]
                else:
                    if len(nick) < 12: # Limita la cantidad de caracteres
                        nick += evento.unicode
            continue  # ¡IMPORTANTE! Salta el resto del manejo de eventos

        if evento.type == pg.MOUSEBUTTONDOWN:
            if inicio:
                inicio = False
                menu = True

            if menu:
                if evento.button == 1:
                    if boton_start.collidepoint(mouse.get_pos()):
                        tablero_real, lista_barcos, tablero_covertura, lista_casilleros, barcos_estado, puntaje, disparos_realizados = iniciar_nueva_partida(dificultad)
                        menu = False
                        jugando = True
                                       
                    elif boton_dificultad.collidepoint(mouse.get_pos()):
                        menu = False
                        menu_dificultad = True
                    elif boton_puntajes.collidepoint(mouse.get_pos()):
                        menu = False
                        viendo_puntajes = True
                    elif boton_salir.collidepoint(mouse.get_pos()):
                        game = False
                    elif boton_musica.collidepoint(mouse.get_pos()):
                        if musica:
                            pg.mixer.music.stop()
                            musica = False
                        else:
                            pg.mixer.music.play(-1)
                            musica = True
                    

            if jugando:
                if evento.button == 1:
                        #detecta clicks de casilleros y procesa el disparo
                    for idx, (rect, activo, color) in enumerate(lista_casilleros):
                        if rect.collidepoint(mouse.get_pos()) and activo:
                            filas = len(tablero_real)
                            columnas = len(tablero_real[0])
                            fila = idx // columnas
                            columna = idx % columnas

                            if not tablero_covertura[fila][columna]:
                                tablero_covertura[fila][columna] = True
                                lista_casilleros[idx][1] = False  # Desactivar casillero
                                disparos_realizados += 1

                                if tablero_real[fila][columna] == 1:
                                    puntaje += 5
                                    lista_casilleros[idx][2] = (0, 255, 0)  # Verde para acierto
                                    # Buscar a qué barco pertenece este casillero
                                    for i, barco in enumerate(lista_barcos):
                                        largo, (f, c), horizontal = barco
                                        for j in range(largo):
                                            if horizontal:
                                                if (fila, columna) == (f, c + j):
                                                    barcos_estado[i] -= 1
                                                    if barcos_estado[i] == 0:
                                                        puntaje += 10 * largo  # Hundido
                                                    break
                                            else:
                                                if (fila, columna) == (f + j, c):
                                                    barcos_estado[i] -= 1
                                                    if barcos_estado[i] == 0:
                                                        puntaje += 10 * largo  # Hundido
                                                    break
                                else:
                                    puntaje -= 1
                                    lista_casilleros[idx][2] = (255, 0, 0)  # Rojo para fallo
                                
                                # Chequear final del juego
                                fin_partida = True
                                for estado in barcos_estado:
                                    if estado != 0:
                                        fin_partida = False
                                        break
                                if fin_partida:
                                    jugando = False
                                    pidiendo_nick = True

                    if boton_volver.collidepoint(mouse.get_pos()):
                        jugando = False
                        menu = True
                    elif boton_reiniciar.collidepoint(mouse.get_pos()):
                        tablero_real, lista_barcos, tablero_covertura, lista_casilleros, barcos_estado, puntaje, disparos_realizados = iniciar_nueva_partida(dificultad)
                    elif boton_musica.collidepoint(mouse.get_pos()):
                        if musica:
                            pg.mixer.music.stop()
                            musica = False
                        else:
                            pg.mixer.music.play(-1)
                            musica = True

            if menu_dificultad:
                if evento.button == 1:
                    if boton_volver.collidepoint(mouse.get_pos()):
                        menu_dificultad = False
                        menu = True
                    elif facil.collidepoint(mouse.get_pos()):
                        dificultad = "F"
                    elif medio.collidepoint(mouse.get_pos()):
                        dificultad = "M"
                    elif dificil.collidepoint(mouse.get_pos()):
                        dificultad = "D"

            if viendo_puntajes:
                if evento.type == pg.MOUSEBUTTONDOWN and evento.button == 1:
                    if boton_volver.collidepoint(mouse.get_pos()):
                        viendo_puntajes = False
                        menu = True

    #PANTALLA
    if jugando:
        screen.blit(fondo_juego,(0,0))
        menu_font = pg.font.SysFont("Consolas", 15)
        poner_boton(screen,boton_volver,"Volver",naranja_apretado,naranja,menu_font)
        poner_boton(screen,boton_reiniciar,"Reiniciar",naranja_apretado,naranja,menu_font)
        poner_boton(screen,boton_musica,"Musica",naranja_apretado,naranja,menu_font)

        # Mostrar puntaje en tiempo real
        escribir_palabara(screen, f'Puntaje: {puntaje}', pos=(width - 250, 70), size=24, color=color_blanco)

        # Dibuja los casilleros con su color
        for rect, activo, color in lista_casilleros:
            if color:
                pg.draw.rect(screen, color, rect)
            else:
                pg.draw.rect(screen, (200, 200, 200), rect)  # Gris si no fue disparado
            pg.draw.rect(screen, (0, 0, 0), rect, 1)  # Borde negro

    else:
        screen.blit(fondo_menu,(0,0))
        if inicio:
            screen.blit(inicio_buque,(width/2-inicio_buque.get_width()/2+30,height/2-(inicio_buque.get_height()/2-100)))
            screen.blit(titulo_2,(width/2-titulo_2.get_width()/2,height/2-(titulo_2.get_height()/2+200)))

    if menu:
        menu_font = pg.font.SysFont("Consolas", 15)
        poner_boton(screen,boton_start,"Jugar",naranja_apretado,naranja,menu_font)
        poner_boton(screen,boton_dificultad,"Dificultad",naranja_apretado,naranja,menu_font)
        poner_boton(screen,boton_puntajes,"Ver Puntajes",naranja_apretado,naranja,menu_font)
        poner_boton(screen,boton_salir,"Salir",naranja_apretado,naranja,menu_font)
        poner_boton(screen,boton_musica,"Musica",naranja_apretado,naranja,menu_font)

    if menu_dificultad:
        menu_font = pg.font.SysFont("Consolas", 15)
        poner_boton(screen,boton_volver,"Volver",naranja_apretado,naranja,menu_font)
        poner_boton(screen,facil,"Facil",naranja_apretado,naranja,menu_font)
        poner_boton(screen,medio,"Medio",naranja_apretado,naranja,menu_font)
        poner_boton(screen,dificil,"Dificil",naranja_apretado,naranja,menu_font)

    if pidiendo_nick:
        screen.fill(color_negro)
        font_grande = pg.font.SysFont('Consolas', 32)
        font_chica = pg.font.SysFont('Consolas', 24)
        texto_victoria = font_grande.render(f'¡Ganaste! Puntaje final: {puntaje}', True, color_blanco)
        texto_ingreso = font_chica.render('Ingresa tu nombre y presiona Enter:', True, color_blanco)
        texto_nick = font_grande.render(nick, True, naranja)
        screen.blit(texto_victoria,(width/2 - texto_victoria.get_width()/2, 200))
        screen.blit(texto_ingreso,(width/2 - texto_ingreso.get_width()/2, 260))
        screen.blit(texto_nick,(width/2 - texto_nick.get_width()/2, 310))

    if viendo_puntajes:
        screen.blit(fondo_menu, (0,0))
        font_grande = pg.font.SysFont('Consolas', 40)
        font_normal = pg.font.SysFont('Consolas', 32)
        menu_font = pg.font.SysFont("Consolas", 15)
        
        titulo = font_grande.render('Mejores Puntajes', True, naranja)
        screen.blit(titulo, (width/2 - titulo.get_width()/2, 100))
        
        mejores = obtener_mejores_puntajes()
        if not mejores:
            texto = font_normal.render('No hay puntajes guardados', True, color_blanco)
            screen.blit(texto, (width/2 - texto.get_width()/2, 250))
        else:
            for i, (nombre, puntos) in enumerate(mejores):
                nombre_mostrar = nombre if nombre.strip() != '' else '(Sin nombre)'
                texto = font_normal.render(f'{i+1}. {nombre_mostrar}: {puntos}', True, color_blanco)
                screen.blit(texto, (width/2 - texto.get_width()/2, 200 + i * 50))
        
        poner_boton(screen, boton_volver, "Volver", naranja_apretado, naranja, menu_font)

    pg.display.flip()    

pg.quit()

def obtener_mejores_puntajes(archivo='puntajes.txt', cantidad=3):
    puntajes = []
    try:
        with open(archivo, 'r') as f:
            for linea in f:
                partes = linea.strip().split(',')
                if len(partes) == 2:
                    nombre, puntos = partes
                    puntajes.append((nombre, int(puntos)))
    except FileNotFoundError:
        pass
    puntajes.sort(key=lambda x: x[1], reverse=True)
    return puntajes[:cantidad]

def guardar_puntaje(nick, puntaje, archivo='puntajes.txt'):
    with open(archivo, 'a') as f:
        f.write(f'{nick},{puntaje}\n')
