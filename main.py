import pygame as pg
import random as rmd
#.\.venv\Scripts\Activate.ps1

#CONFIGURACIÓN DE LA PANTALLA
ancho, alto = 500, 500
colorFondo = (30, 30, 30)

#Configuracion del agente
tamanioAgente = 20
colorAgente = (0, 255, 0)
velocidadAgente = 2

#Cofiguracion de de los objetos
colorObstaculo = (255, 0, 0)
numeroObstaculos = 5
tamanioObstaculo = 40

#Iniciaciòn de pygame
pg.init()
pantalla = pg.display.set_mode((ancho, alto))
pg.display.set_caption("Agente reactivo")

# posicion inicial del agente
agenteX = rmd.randrange(0, ancho- tamanioAgente)
agenteY = rmd.randrange(0, alto- tamanioAgente)
direccion = rmd.choice (["ARRIBA", "ABAJO", "derecha", "IZQUIERDA"])

#Generar obstaculos en posiciones aleatorias
obstaculos= []
for _ in range (numeroObstaculos):
    obsX = rmd.randrange (0, ancho - tamanioObstaculo)
    obsY = rmd.randrange (0, alto - tamanioObstaculo)
    #append añade un elemento al final de la lista Obstaculos
    #pygame.Rect() Crea un objeto de tipo rectangulo (Posicion y tamaño)
    obstaculos.append(pg.Rect(obsX, obsY, tamanioObstaculo, tamanioObstaculo))

#Funciona para mover el agente
def moverAgente (x, y, direccion):
    if direccion == "ARRIBA":
        y -= velocidadAgente # La pantalla de pygame tiene el origen de coordenadas en la esquina superior izquierda, por lo que al movernos hacia abajo, la coordenada y aumenta
    elif direccion == "ABAJO": # Cuando y -=  Y sube verticalmemente y cuando Y += Y baja vertivalmente
        y += velocidadAgente
    elif direccion == "IZQUIERDA":
        x -= velocidadAgente
    elif direccion == "DERECHA":
        x += velocidadAgente
    return x, y

#Funcion para verrificar colision
def verificarColision (y, x, ):
    rectanguloAgente = pg.Rect(x, y, tamanioAgente, tamanioAgente)

    if x < 0 or x > ancho - tamanioAgente or y < 0 or y > alto - tamanioAgente:
        return True # colision con los bordes 
    for obs in obstaculos:
        if rectanguloAgente.colliderect(obs):
            return True #La funcion .collidirect()
    return False

# BUCLE PRINCIAPAL
ejecutando = True
while ejecutando:
    pg.time.delay (20)
    
    #verificar eventos (cierre de ventana)
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            ejecutando = False  
    
    #MOVER EL AGENTE
    nuevoY, nuevoX = moverAgente (agenteY, agenteX, direccion)

    # Si hay una coslision cambiar a una nueva direccion aleatoria
    if verificarColision (nuevoX, nuevoY):
        direccion = rmd.choice(["ARRIBA", "ABAJO", "IZQUIERDA", "DERECHA"])
    else:
        agenteY, agenteX = nuevoY, nuevoX

    #Dibuajar el entorno 
    pantalla.fill(colorFondo)
    pg.draw.rect(pantalla, colorAgente, (agenteX, agenteY, tamanioAgente, tamanioAgente))

    for obs in obstaculos:
        pg.draw.rect(pantalla, colorObstaculo, obs)
    pg.display.update()

#Cerrar pygame
pg.quit() 

     
    




0