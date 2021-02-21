import pygame as pg
from NAVE import DIMENSIONES, FPS
import random
import sys

pg.init()
pg.font.init()

def fuente(t, s=72, c=(255, 255, 0), b=False, i=False):
    font = pg.font.SysFont("Arial", s, bold=b, italic=i)
    text = font.render(t, True, c)
    return text
fuenteGAMEOVER = fuente("GAME OVER")
SURF = pg.display.set_mode(DIMENSIONES)

class Planet:
    def __init__(self):
        self.image = pg.image.load("RECURSOS/IMAGENES/PLANETA.png")
        self.x = DIMENSIONES[0]
        self.y = (DIMENSIONES[1] - pg.Surface.get_height(self.image)) / 2

    def move(self, x, y):
        self.x += x
        self.y += y

    def getWidth(self):
        return pg.Surface.get_width(self.image)

class Nivel:
    def __init__(self, n, m):
        self.stop_level = False
        self.ending_level = False
        self.finish_level = False
        self.bigAsters = []
        self.aster = []
        self.nivel = n
        self.puntos = 0
        self.update_nivel()
        self.meta_nivel = m
        self.finalizando = False

    def update_nivel(self):
        for i in range(random.randint(2, 7)):
            ax3 = Asteroidex3()
            ax3.vx = random.randint(2, 15)
            self.aster.append(ax3)

        for i in range(1):
            ax3 = asteroide()
            self.bigAsters.append(ax3)

    def actualizarBigAsters(self):
        for bigAster in self.bigAsters:
            bigAster.actualizar(self.finalizando)

    def actualizarAsters(self):
        for aster in self.aster:
            aster.actualizar(self.finalizando)

    def tieneAsteroides(self):
        totalAsteroides = []
        for bigAster in self.bigAsters:
            totalAsteroides.append(bigAster.rect.x < - pg.Surface.get_width(bigAster.image))
        for aster in self.aster:
            totalAsteroides.append(aster.x < - pg.Surface.get_width(aster.image))
        return not all(totalAsteroides)

    def restart(self):
        self.bigAsters = []
        self.aster = []
        self.update_nivel()

    def get_numeroNivel(self):
        return self.nivel

class explosion(pg.sprite.Sprite):
    imagenes_files = ['EXPLOSION1.png', 'EXPLOSION2.png', 'EXPLOSION3.png', 'EXPLOSION4.png',  'EXPLOSION5.png', 'EXPLOSION6.png', 'EXPLOSION7.png', 'EXPLOSION8.png', 'EXPLOSION9.png',  'EXPLOSION10.png', 'EXPLOSION11.png', 'EXPLOSION12.png',  'EXPLOSION13.png']

    def __init__(self):
        super(explosion, self).__init__()
        self.image_act = 0
        self.imagenes = self.cargaImagenes()
        self.image = self.imagenes[self.image_act]
        self.rect = pg.Rect(5, 5, 150, 198)
        self.ciclos_tras_refresco = 0
        self.retardo_anim = 5

    def update(self):
        self.ciclos_tras_refresco += 1
        if self.ciclos_tras_refresco % self.retardo_anim == 0:
            self.image_act += 1
            if self.image_act >= len(self.imagenes):
                self.image_act = 0
        self.image = self.imagenes[self.image_act]

    def cargaImagenes(self):
        lista_imagenes = []
        for img in self.imagenes_files:
            lista_imagenes.append(pg.image.load(f"RECURSOS/IMAGENES/{img}"))
        return lista_imagenes

    def setPosition(self, x, y):
        self.rect.top = y
        self.rect.left = x

    def explote_sound(self):
        pg.mixer.init()
        pg.mixer.music.load("RECURSOS/AUDIOS/sonido-1.mp3")
        pg.mixer.music.play()
        pg.mixer.music.set_volume(0.01)

class nave:

    def __init__(self, x, y, vy):
        self.angle = 0
        self.vc = 5   # velocidad crucero
        self.x = x
        self.y = y
        self.vy = vy
        self.image = pg.image.load("RECURSOS/IMAGENES/NAVE.png")
        self.rect = pg.Surface.get_rect(self.image)
        self.rect.top = y
        self.rect.left = x
        self.setDimension()
        self.printPos = (0, 0)
        self.printImage = self.image

    def getRect(self):
        return self.rect

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def setDimension(self):
        self.height = pg.Surface.get_height(self.image)
        self.width = pg.Surface.get_width(self.image)

    def actualizar(self):
        self.y += self.vy
        self.rect.top += self.vy
        if self.y + 50 >= GAME_DIMENSIONS[1]:
            self.y = GAME_DIMENSIONS[1] - 50
            self.rect.top = GAME_DIMENSIONS[1] - 50
        if self.y <= 0:
            self.y = 0
            self.rect.top = 0
        self.printPos = (self.x, self.y)
        self.printImage = self.image
        if self.angle != 0:
            centro_naveX = self.rect.centerx
            centro_naveY = self.rect.centery
            nave_rotadaS = pg.transform.rotozoom(self.image, self.angle, 1)
            rectanguloRot = nave_rotadaS.get_rect(centerx=centro_naveX, centery=centro_naveY)
            self.printPos = rectanguloRot
            self.printImage = nave_rotadaS

    def naveAterrizando(self):
        if self.y < GAME_DIMENSIONS[1] / 2:
            self.y += self.vc
            self.rect.top += self.vc
        if self.y > GAME_DIMENSIONS[1] / 2:
            self.y -= self.vc
            self.rect.top -= self.vc
        if self.y == GAME_DIMENSIONS[1] / 2 and not self.x == GAME_DIMENSIONS[0] - self.width:
            self.x += self.vc
            self.rect.left += self.vc
        if self.x == GAME_DIMENSIONS[0] - self.width and self.angle < 180: # hasta que siga girando vaya aumentando de a 1
            self.angle += 1

    def manejar_eventos(self):
        teclas_pulsadas = pg.key.get_pressed()
        if teclas_pulsadas[pg.K_UP]:
            self.vy = -10
        elif teclas_pulsadas[pg.K_DOWN]:
            self.vy = 10
        else:
            self.vy = 0

class Asteroidex3():
    w = 50
    h = 50
    def __init__(self):
        self.x = -self.w
        self.y = random.randint(0, 550)
        self.vx = 4
        self.image = pg.image.load("RECURSOS/IMAGENES/ROCA1.png")
        self.rect = pg.Surface.get_rect(self.image)

    def actualizar(self, finalizando):
        self.x -= self.vx
        self.rect.x -= self.vx
        if self.x <= -50 and not finalizando:
            self.x = 850
            self.rect.x = 850
            self.y = random.randint(0, 550)
            self.rect.y = self.y
            self.vx = random.randint(2, 10)

class asteroide():
    imagenes_files = ['ROCA1.png', 'ROCA2.png', 'ROCA3.png', 'ROCA4.png',  'ROCA5.png',
                        'ROCA6.png',  'ROCA7.png']
    retardo_anim = 5

    def __init__(self):
        self.x = 928
        self.y = random.randint(2, 15)
        self.vx = 5
        self.vy = 0
        self.image_act = 0  
        self.ciclos_tras_refresco = 0 
        self.imagenes = self.cargaImagenes()
        self.image = self.imagenes[self.image_act]
        self.rect = self.image.get_rect(x=self.x, y=self.y)

    def cargaImagenes(self):
        lista_imagenes = []
        for img in self.imagenes_files:
            lista_imagenes.append(pg.image.load(f"RECURSOS/IMAGENES/{img}"))
        return lista_imagenes

    def actualizarPosicion(self, finalizando):

        if self.rect.x <= -128 and not finalizando:
            self.rect.x = 928
            self.rect.y = random.randint(0, 472)
        self.rect.x -= self.vx

    def actualizar_imagen(self):

        self.ciclos_tras_refresco += 1
        if self.ciclos_tras_refresco % self.retardo_anim == 0:
            self.image_act += 1
            if self.image_act >= len(self.imagenes):
                self.image_act = 0
        self.image = self.imagenes[self.image_act]

    def actualizar(self, finalizando):
        self.actualizarPosicion(finalizando)
        self.actualizar_imagen()

class Game:
    def __init__(self):
        self.timeLeft = 0
        self.numeroDeNiveles = 1
        self.puntosAcumulados = 0
        self.planet1 = Planet()
        self.clock = pg.time.Clock()
        self.pantalla = pg.display.set_mode(GAME_DIMENSIONS)
        self.bg = pg.image.load("RECURSOS/IMAGENES/BG.jpg")
        self.bg2 = pg.image.load("RECURSOS/IMAGENES/Portada-2.jpg")
        pg.display.set_caption("Futuro space ship")
        self.crash_nave = False
        self.nivel = Nivel(1, 10)
        self.vidas = 1
        self.puntos = 0
        self.goalRect = pg.Rect(0, 0, 1, 600)
        self.nave = nave(10, 275, 0)
        self.explote = Explote()

    #BUCLE PRINCIPAL
    def bucle_principal(self):
        game_over = False
        contador = 0

        while not game_over:

            events = pg.event.get()
            self.clock.tick(FPS)
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            if not self.nivel.stop_level:
                self.nave.manejar_eventos()
                self.nave.actualizar()
                self.nivel.actualizarAsters()
                self.nivel.actualizarBigAsters()          
                self.pantalla.blit(self.bg, (0, 0))

                allAsters = []

                for aster in self.nivel.aster:
                    allAsters.append(aster.rect)
                    self.pantalla.blit(aster.image, (aster.x, aster.y))
                for bigAster in self.nivel.bigAsters:
                    allAsters.append(bigAster.rect)
                    self.pantalla.blit(bigAster.image, (bigAster.rect.x, bigAster.rect.y))

                if self.nave.rect.collidelistall(allAsters):
                    self.explote.explote_sound()
                    self.nivel.stop_level = True
                    self.crash_nave = True
                    allAsters = []
                self.pantalla.blit(self.nave.image, (self.nave.x, self.nave.y))
                if self.goalRect.collidelistall(allAsters):
                    self.puntos += 1

                if self.puntos > self.nivel.meta_nivel:
                    self.nivel.finalizando = True
                if self.puntos > self.nivel.meta_nivel and not self.nivel.tieneAsteroides():
                    self.nivel.stop_level = True
                    self.nivel.ending_level = True
                    self.nave.vy = 0

            if self.nivel.stop_level:
                if self.crash_nave:
                    contador += 1
                    if contador < len(self.explote.imagenes) * self.explote.retardo_anim:
                        self.pantalla.blit(self.bg, (0, 0))
                        self.pantalla.blit(self.explote.image, (self.nave.x, self.nave.y - self.nave.getHeight() / 2))
                        self.explote.update()
                    if contador > 200:
                        self.vidas -= 1
                        contador = 0
                        timeLeft = pg.time.get_ticks()
                        if self.vidas > 0:
                            while ((pg.time.get_ticks() - timeLeft) / 1000) > 5:
                                self.pantalla.blit(self.bg, (0, 0))
                                textoVidas = create_font("No Te Rindas!, Inténtalo De Nuevo", 32, (255, 255, 255))
                                SURF.blit(textoVidas,((DIMENSIONES[0] - textoVidas.get_width()) / 2, DIMENSIONES[1] / 2))
                                pg.display.flip()
                        else:
                            while ((pg.time.get_ticks() - timeLeft) / 1000) > 5:
                                self.pantalla.blit(self.bg, (0, 0))
                                textoVidas = create_font("Game Over", 32, (255, 255, 255))
                                SURF.blit(textoVidas,((DIMENSIONES[0] - textoVidas.get_width()) / 2, DIMENSIONES[1] / 2))
                                pg.display.flip()
                            self.irAlaPortada()

                        self.nivel.restart()
                        self.nivel.stop_level = False
                        self.crash_nave = False
                        self.nivel.finalizando = False
                elif self.nivel.ending_level:
                    self.pantalla.blit(self.bg, (0, 0))

                    while self.planet1.x != (DIMENSIONES[0] - self.planet1.getWidth() / 2):
                        self.planet1.move(-0.25, 0)
                        self.pantalla.blit(self.bg, (0, 0))
                        self.pantalla.blit(self.planet1.image, (self.planet1.x, self.planet1.y))
                        self.pantalla.blit(self.nave.image, (self.nave.x, self.nave.y))
                        pg.display.flip()
                    self.nave.naveAterrizando()
                    self.nave.actualizar()
                    self.pantalla.blit(self.planet1.image, (self.planet1.x, self.planet1.y))
                    self.pantalla.blit(self.nave.printImage, self.nave.printPos)
                    if self.nave.angle == 180:
                        self.nivel.finish_level = True
                        self.nivel.ending_level = False
                        self.timeLeft = pg.time.get_ticks() # siempre va a ir en aumento el tiempo actual
                elif self.nivel.finish_level:

                    if self.nivel.get_numeroNivel() >= self.numeroDeNiveles:
                        textLevelComplete = create_font(" Juego Completado!, Pulse Enter ", 32, (255, 255, 255))
                        SURF.blit(textLevelComplete,((DIMENSIONES[0] - textLevelComplete.get_width()) / 2, DIMENSIONES[1] / 2))

                        tecla_pulsada = pg.key.get_pressed()
                        if tecla_pulsada[pg.K_RETURN]:
                            self.puntosAcumulados = 0
                            self.puntos = 0
                            self.vidas = 3
                            self.nivel = Nivel(1, 30)
                            self.nave = nave(10, 275, 0)

                        if ((pg.time.get_ticks() - self.timeLeft) / 1000) > 5:
                            self.paginaPrincipal()

                    else:
                        textLevelComplete = create_font(" Nivel " + str(self.nivel.nivel) + " Completado! Pulse Enter para continuar ",32, (255, 255, 255))
                        SURF.blit(textLevelComplete, ((DIMENSIONES[0] - textLevelComplete.get_width()) / 2, DIMENSIONES[1] / 2))

                        tecla_pulsada = pg.key.get_pressed()
                        if tecla_pulsada[pg.K_RETURN]:
                            self.puntosAcumulados = self.nivel.puntos
                            self.nivel = Nivel(self.nivel.get_numeroNivel() + 1, 30)
                            self.nave = nave(10, 275, 0)

            SURF.blit(create_font("Nivel:" + str(self.nivel.nivel), 32, (255, 255, 255)),((DIMENSIONES[0] / 6) * 0, 0))
            SURF.blit(create_font("Vidas:" + str(self.vidas), 32, (255, 255, 255)), ((DIMENSIONES[0] / 6) * 2, 0))
            SURF.blit(create_font("Puntos:" + str(self.puntos), 32, (255, 255, 255)), ((DIMENSIONES[0] / 6) * 4, 0))

            # Zona de refrescar pantalla
            pg.display.flip()

    def paginaPrincipal(self):
        portada = True
        pg.mixer.init()
        pg.mixer.music.load("RECURSOS/AUDIO/intro_.mp3")
        pg.mixer.music.play()
        pg.mixer.music.set_volume(0.05)
        SPACEHEIGHT = 80
        textPortada_s = 2
        textInstrucciones_s = 1
        while portada:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.pantalla.blit(self.bg2, (0, 0))

            textTitulo = create_font(" SPACE SHIP ", 100, (255, 255, 255))
            SURF.blit(textTitulo, ((GAME_DIMENSIONS[0] - textTitulo.get_width()) / 2, GAME_DIMENSIONS[1] / 4))
            textPortada = create_font(" Jugar ", textPortada_s * 16, (255, 255, 255))
            SURF.blit(textPortada, ((GAME_DIMENSIONS[0] - textPortada.get_width()) / 2, textTitulo.get_rect().centery + SPACEHEIGHT * 3))
            textInstrucciones = create_font(" Instrucciones ", textInstrucciones_s * 16, (255, 255, 255))
            SURF.blit(textInstrucciones, ((GAME_DIMENSIONS[0] - textInstrucciones.get_width()) / 2, textTitulo.get_rect().centery + SPACEHEIGHT * 3.5))

            tecla_pulsada = pg.key.get_pressed()
            if tecla_pulsada[pg.K_RETURN]:
                if textPortada_s > textInstrucciones_s:
                    self.puntosAcumulados = 0
                    self.puntos = 0
                    self.vidas = 2
                    self.nivel = Nivel(1, 30)
                    self.nave = nave(10, 275, 0)
                    portada = False
                    pg.mixer.music.stop()
                else:
                    self.irAlasInstrucciones()
            elif tecla_pulsada[pg.K_DOWN]:
                textPortada_s = 1
                textInstrucciones_s = 2
            elif tecla_pulsada[pg.K_UP]:
                textPortada_s = 2
                textInstrucciones_s = 1

            pg.display.flip()

    def Instrucciones(self):
        instrucciones= True
        SPACEHEIGHT = 80
        while instrucciones:
            events = pg.event.get()
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.pantalla.fill((11, 44, 94))

            textTitulo = create_font(" Instrucciones ", 50, (255, 255, 255))
            SURF.blit(textTitulo, ((DIMENSIONES[0] - textTitulo.get_width()) / 2, DIMENSIONES[1] / 4))

            tecla_pulsada = pg.key.get_pressed()
            if tecla_pulsada[pg.K_ESCAPE]:
                instrucciones = False

            pg.display.flip()