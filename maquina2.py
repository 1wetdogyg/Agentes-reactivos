import pygame as pg
import random as rmd

# .\.venv\Scripts\Activate.ps1
# venv\Scripts\activate.bat


# ==========================================================
# CONFIGURACIÓN DE LA PANTALLA
# ==========================================================

ancho, alto = 500, 500
colorFondo = (30, 30, 30)


# ==========================================================
# CONFIGURACIÓN DE LOS AGENTES
# ==========================================================

tamanioAgente = 20
velocidadAgente = 2

colorAgente = (0, 255, 0)
colorAgenteManual = (0, 200, 255)
colorAgenteAuto = (0, 0, 150)


# ==========================================================
# CONFIGURACIÓN DE LOS OBSTÁCULOS
# ==========================================================

colorObstaculo = (255, 0, 0)
numeroObstaculos = 5
tamanioObstaculo = 40


# ==========================================================
# CONFIGURACIÓN DEL BOTÓN
# ==========================================================

colorBotonAuto = (100, 100, 100)
colorBotonManual = (0, 100, 200)  # Corregido: 2000 -> 200
colorTextoBoton = (255, 255, 255)

rectBoton = pg.Rect(10, 10, 180, 30)


# ==========================================================
# DIRECCIONES OPUESTAS
# ==========================================================

OPUESTOS = {
    "ARRIBA": "ABAJO",
    "ABAJO": "ARRIBA",
    "IZQUIERDA": "DERECHA",
    "DERECHA": "IZQUIERDA"
}


DIRECCIONES = [
    "ARRIBA",
    "ABAJO",
    "IZQUIERDA",
    "DERECHA"
]


# ==========================================================
# INICIALIZACIÓN DE PYGAME
# ==========================================================

pg.init()

pantalla = pg.display.set_mode((ancho, alto))
pg.display.set_caption("Agente reactivo")

clock = pg.time.Clock()


# ==========================================================
# CONFIGURACIÓN DEL TEXTO
# ==========================================================

try:
    pg.font.init()
    fuente = pg.font.Font(None, 24)
    usarTexto = True

except (RuntimeError, Exception):
    usarTexto = False


# ==========================================================
# AGENTE 1
# ==========================================================

agenteX = rmd.randrange(0, ancho - tamanioAgente)
agenteY = rmd.randrange(0, alto - tamanioAgente)

direccion = rmd.choice(DIRECCIONES)

rectanguloAgente = pg.Rect(
    agenteX,
    agenteY,
    tamanioAgente,
    tamanioAgente
)


# ==========================================================
# AGENTE 2
# ==========================================================

Agente2_x = rmd.randrange(0, ancho - tamanioAgente)
Agente2_y = rmd.randrange(0, alto - tamanioAgente)

direccion2_auto = rmd.choice(DIRECCIONES)

rectanguloAgente2 = pg.Rect(
    Agente2_x,
    Agente2_y,
    tamanioAgente,
    tamanioAgente
)

# False = automático
# True = manual
modoManualAgente2 = False


# ==========================================================
# GENERACIÓN DE OBSTÁCULOS
# ==========================================================

obstaculos = []

for _ in range(numeroObstaculos):

    while True:

        obsX = rmd.randint(
            0,
            ancho - tamanioObstaculo
        )

        obsY = rmd.randint(
            0,
            alto - tamanioObstaculo
        )

        nuevoObs = pg.Rect(
            obsX,
            obsY,
            tamanioObstaculo,
            tamanioObstaculo
        )

        # Comprobar colisión con agentes y botón
        colision = (
            nuevoObs.colliderect(rectanguloAgente)
            or nuevoObs.colliderect(rectanguloAgente2)
            or nuevoObs.colliderect(rectBoton)
        )

        # Comprobar colisión con otros obstáculos
        colisionObstaculos = any(
            nuevoObs.colliderect(obs)
            for obs in obstaculos
        )

        if not colision and not colisionObstaculos:
            obstaculos.append(nuevoObs)
            break


# ==========================================================
# FUNCIÓN PARA MOVER UN AGENTE AUTOMÁTICAMENTE
# ==========================================================

def moverAgenteAuto(x, y, direccion):

    if direccion == "ARRIBA":
        y -= velocidadAgente

    elif direccion == "ABAJO":
        y += velocidadAgente

    elif direccion == "IZQUIERDA":
        x -= velocidadAgente

    elif direccion == "DERECHA":
        x += velocidadAgente

    return x, y


# ==========================================================
# OBTENER NUEVA DIRECCIÓN
# ==========================================================

def obtenerNuevaDireccion(direccionActual):

    direccionProhibida = OPUESTOS[direccionActual]

    opcionesValidas = DIRECCIONES.copy()

    opcionesValidas.remove(direccionProhibida)

    return rmd.choice(opcionesValidas)


# ==========================================================
# VERIFICAR COLISIÓN
# ==========================================================

def verificarColision(x, y, rectOtroAgente):

    rect = pg.Rect(
        x,
        y,
        tamanioAgente,
        tamanioAgente
    )

    # Colisión con los bordes
    if (
        x < 0
        or x > ancho - tamanioAgente
        or y < 0
        or y > alto - tamanioAgente
    ):
        return True

    # Colisión con obstáculos
    for obs in obstaculos:

        if rect.colliderect(obs):
            return True

    # Colisión con el otro agente
    if rect.colliderect(rectOtroAgente):
        return True

    return False


# ==========================================================
# BUCLE PRINCIPAL
# ==========================================================

ejecutando = True

while ejecutando:

    # Control de FPS
    clock.tick(50)


    # ======================================================
    # ACTUALIZAR RECTÁNGULOS DE LOS AGENTES
    # ======================================================

    rectanguloAgente.topleft = (
        agenteX,
        agenteY
    )

    rectanguloAgente2.topleft = (
        Agente2_x,
        Agente2_y
    )


    # ======================================================
    # PROCESAR EVENTOS
    # ======================================================

    for evento in pg.event.get():

        # Cerrar ventana
        if evento.type == pg.QUIT:
            ejecutando = False

        # Botón de cambio de modo
        if (
            evento.type == pg.MOUSEBUTTONDOWN
            and evento.button == 1
        ):

            if rectBoton.collidepoint(evento.pos):

                modoManualAgente2 = not modoManualAgente2


    # ======================================================
    # MOVER AGENTE 1
    # ======================================================

    nuevoX, nuevoY = moverAgenteAuto(
        agenteX,
        agenteY,
        direccion
    )

    if verificarColision(
        nuevoX,
        nuevoY,
        rectanguloAgente2
    ):

        direccion = obtenerNuevaDireccion(direccion)

    else:

        agenteX = nuevoX
        agenteY = nuevoY


    # ======================================================
    # MOVER AGENTE 2
    # ======================================================

    if not modoManualAgente2:

        # ----------------------------------------------
        # MODO AUTOMÁTICO
        # ----------------------------------------------

        nuevoX2, nuevoY2 = moverAgenteAuto(
            Agente2_x,
            Agente2_y,
            direccion2_auto
        )

        if verificarColision(
            nuevoX2,
            nuevoY2,
            rectanguloAgente
        ):

            direccion2_auto = obtenerNuevaDireccion(
                direccion2_auto
            )

        else:

            Agente2_x = nuevoX2
            Agente2_y = nuevoY2

    else:

        # ----------------------------------------------
        # MODO MANUAL
        # ----------------------------------------------

        teclas = pg.key.get_pressed()

        nuevoX2 = Agente2_x
        nuevoY2 = Agente2_y


        # Movimiento horizontal
        if teclas[pg.K_a]:

            nuevoX2 -= velocidadAgente

        elif teclas[pg.K_d]:

            nuevoX2 += velocidadAgente


        # Movimiento vertical
        if teclas[pg.K_w]:

            nuevoY2 -= velocidadAgente

        elif teclas[pg.K_s]:

            nuevoY2 += velocidadAgente


        # Comprobar movimiento completo
        # Se comprueba primero X
        if not verificarColision(
            nuevoX2,
            Agente2_y,
            rectanguloAgente
        ):

            Agente2_x = nuevoX2


        # Se comprueba después Y
        if not verificarColision(
            Agente2_x,
            nuevoY2,
            rectanguloAgente
        ):

            Agente2_y = nuevoY2


    # ======================================================
    # DIBUJAR FONDO
    # ======================================================

    pantalla.fill(colorFondo)


    # ======================================================
    # DIBUJAR OBSTÁCULOS
    # ======================================================

    for obs in obstaculos:

        pg.draw.rect(
            pantalla,
            colorObstaculo,
            obs
        )


    # ======================================================
    # DIBUJAR BOTÓN
    # ======================================================

    colorBoton = (
        colorBotonManual
        if modoManualAgente2
        else colorBotonAuto
    )

    pg.draw.rect(
        pantalla,
        colorBoton,
        rectBoton
    )


    # ======================================================
    # DIBUJAR TEXTO DEL BOTÓN
    # ======================================================

    if usarTexto:

        textoBoton = (
            "Control: Manual"
            if modoManualAgente2
            else "Control: Automático"
        )

        textoRenderizado = fuente.render(
            textoBoton,
            True,
            colorTextoBoton
        )

        pantalla.blit(
            textoRenderizado,
            (
                rectBoton.x + 5,
                rectBoton.y + 5
            )
        )


    # ======================================================
    # DIBUJAR AGENTE 1
    # ======================================================

    pg.draw.rect(
        pantalla,
        colorAgente,
        (
            agenteX,
            agenteY,
            tamanioAgente,
            tamanioAgente
        )
    )


    # ======================================================
    # DIBUJAR AGENTE 2
    # ======================================================

    colorAgente2 = (
        colorAgenteManual
        if modoManualAgente2
        else colorAgenteAuto
    )

    pg.draw.rect(
        pantalla,
        colorAgente2,
        (
            Agente2_x,
            Agente2_y,
            tamanioAgente,
            tamanioAgente
        )
    )


    # ======================================================
    # ACTUALIZAR PANTALLA
    # ======================================================

    pg.display.update()


# ==========================================================
# CERRAR PYGAME
# ==========================================================

pg.quit()