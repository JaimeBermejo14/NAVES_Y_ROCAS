import pygame as pg
from CARPETA1 import GAME_DIMENSIONS, FPS
import random
import sys

pg.init()

class Explosion(pg.sprite.Sprite): 
    imagenes_files = ['EXPLOSION1.png', 'EXPLOSION2.png', 'EXPLOSION3.png', 'EXPLOSION4.png',  'EXPLOSION5.png']

    def __init__(self):
        super(Explosion, self).__init__()
        self.imagenes = self.cargaImagenes()
        self.index = 0
        self.image = self.imagenes[self.index]
        self.rect = pg.Rect(5, 5, 150, 198)

    def update(self):
        self.index += 1

        if self.index >= len(self.imagenes):
            self.index = 0
        self.image = self.imagenes[self.index]

    def cargaImagenes(self):
        lista_imagenes = []
        for img in self.imagenes_files:
            lista_imagenes.append(pg.image.load(f"imagenes/{img}"))
        return lista_imagenes

    def setPosition(self, x, y):
        self.rect.top = y
        self.rect.left = x

class nave:
    def __init__(self, x, y, vy):
        self.x = x
        self.y = y
        self.vy = vy
        self.image = pg.image.load("/imagenes/NAVE.png")
        self.rect = pg.Surface.get_rect(self.image)
        self.rect.top = y
        self.rect.left = x
        self.setDimension()

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

    def eventos(self):

        teclas_pulsadas = pg.key.get_pressed()
        if teclas_pulsadas[pg.K_UP]:
            self.vy = -10
        elif teclas_pulsadas[pg.K_DOWN]:
            self.vy = 10
        else:
            self.vy = 0

class Asteroidex3():
    w=50
    h=50
    def __init__(self):
        self.x = -self.w
        self.y = random.randint(0, 550)
        self.vx = 4
        self.image = pg.image.load("imagenes/ROCA10.png")
        self.rect = pg.Surface.get_rect(self.image)

    def actualizar(self):
        self.x -= self.vx
        self.rect.x -= self.vx
        if self.x <= -50:
            self.x = 850
            self.rect.x = 850
            self.y = random.randint(0, 550)
            self.rect.y = self.y
            self.vx = random.randint(2, 15)

class asteroide():
    imagenes_files = ['ROCA1.png', 'ROCA2.png', 'ROCA3.png', 'ROCA4.png',  'ROCA5.png',
                        'ROCA6.png',  'ROCA7.png', 'ROCA08.png', 'ROCA9.png']
    retardo_anim = 5  # mientras mas aumenta en valor mas lenta es la animacion

    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.image_act = 0   
        self.ciclos_tras_refresco = 0 
        self.imagenes = self.cargaImagenes()
        self.image = self.imagenes[self.image_act] 

        self.rect = self.image.get_rect(x=x,y=y)

    def cargaImagenes(self):
        lista_imagenes = []
        for img in self.imagenes_files:
            lista_imagenes.append(pg.image.load(f"imagenes/{img}"))
        return lista_imagenes

    def NuevaPosicion(self):
        # Gestionar posicion del asteroide

        if self.rect.x <= -128:
            self.rect.x = 928
            self.rect.y = random.randint(0, 472)
        self.rect.x -= self.vx

    def actualizarImagen(self):
        # Gestionar imagen activa (disfraz de asteroide)

        self.ciclos_tras_refresco += 1

        if self.ciclos_tras_refresco % self.retardo_anim == 0:
            self.image_act += 1
            if self.image_act >= len(self.imagenes):
                self.image_act = 0
        
        self.image = self.imagenes[self.image_act]

    def actualizar(self):
        self.NuevaPosicion()
        self.actualizarImagen()

class Game:
    def __init__(self):
        self.clock = pg.time.Clock()      
        self.pantalla = pg.display.set_mode( GAME_DIMENSIONS )
        self.bg = pg.image.load("imagenes/BG.pg")
        pg.display.set_caption("NAVE")

        self.asteroide = asteroide( 928, 236, 5, 0)

        self.aster = []
        for i in range(random.randint(2, 7)):
            ax3 = Asteroidex3()
            ax3.vx = random.randint(2, 15)
            self.aster.append(ax3)
        
        self.nave = nave( 10, 275, 0)

        self.explosion = Explosion()
        self.mygroup = pg.sprite.Group(self.explosion)

    # bucle principal   
    def bucle_principal(self):        
        game_over = False

        while not game_over:
            # Gestión de eventos
            events = pg.event.get()
            self.clock.tick(FPS)
            for event in events:
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.nave.eventos()
            # Zona de Actualización de elementos del juego
            self.nave.actualizar()
            self.asteroide.actualizar()

            for aster in self.aster :
                aster.actualizar()

            # Zona de pintado de elementos 
   
            self.pantalla.blit(self.bg, (0, 0))
            self.pantalla.blit(self.asteroide.image, (self.asteroide.rect.x, self.asteroide.rect.y))
            pg.draw.rect(self.pantalla,(0, 255, 0, 0.5), self.asteroide.rect)
 
            if self.nave.rect.colliderect(self.asteroide.rect):
                self.explosion.setPosition(self.nave.x , self.nave.y - self.nave.getHeight()/2)
                self.mygroup.update()
                self.mygroup.draw(self.pantalla)

            for aster in self.aster :
                self.pantalla.blit(aster.image, (aster.x, aster.y))
                pg.draw.rect(self.pantalla,(0, 255, 0), aster.rect)

            self.pantalla.blit(self.nave.image, (self.nave.x, self.nave.y))
            pg.draw.rect(self.pantalla,(255, 0, 0), self.nave.rect)

            # Zona de refrescar pantalla
            pg.display.flip()