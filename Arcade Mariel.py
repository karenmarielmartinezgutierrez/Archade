
# Importar la librería Pygame
import pygame

# Importar función para generar números aleatorios
from random import randint

# Iniciar todos los módulos de Pygame
pygame.init()

# Fuente para los mensajes de victoria y derrota
font = pygame.font.Font(None, 72)


#Ajustes generales del juego

# Tamaño de la ventana
win_width = 800
win_height = 600

# Límites para el movimiento de la cámara
left_bound = win_width / 40
right_bound = win_width - 8 * left_bound

# Desplazamiento del escenario
shift = 0

# Gravedad aumentada para caer más rápido
gravedad = 0.5

# Fuerza del salto
salto = 13

# Posición inicial del personaje
x_start, y_start = 20, 10

# Tamaño del héroe (más pequeño)
h_width = 45
h_height = 60

# Fotogramas por segundo
FPS = 60


#Archivos de los personajes
img_file_hero = 'Heroe.png'
img_file_enemy = 'Enemigo 2.png'
img_file_bomb = 'bomba.png'
img_file_princess = 'princesa.png'

#Fondos de los 5 niveles
fondos = [
    'Galaxia.png',
    'Planeta.jpg',
    'Bosque.jpg',
    'volcan.jpg',
    'desierto.jpg'
]


#Configuracines de los 5 niveles# Cada nivel tiene:

niveles = [

    #Nivel Galaxia
    {
        # Posición y tamaño de cada plataforma
        'plataformas': [
            (50, 150, 480, 20),
            (350, 380, 400, 20),
            (850, 320, 250, 20)
        ],

        # Enemigos y límites de patrulla
        'enemigos': [
            (400, 490, 350, 550),
            (850, 490, 800, 1050)
        ],

        # Posiciones de las bombas
        'bombas': [
            (650, 250)
        ],

        # Velocidad de enemigos
        'velocidad': 3
    },

    #Nivel planeta
    {
        'plataformas': [
            (100, 200, 350, 20),
            (500, 350, 350, 20),
            (900, 250, 300, 20)
        ],

        'enemigos': [
            (250, 490, 200, 450),
            (650, 490, 600, 850),
            (1000, 490, 950, 1150)
        ],

        'bombas': [
            (550, 280),
            (900, 180)
        ],

        'velocidad': 3
    },

    #Nivel bosque
    {
        'plataformas': [
            (50, 180, 300, 20),
            (400, 300, 300, 20),
            (750, 400, 300, 20),
            (1100, 250, 250, 20)
        ],

        'enemigos': [
            (200, 490, 150, 350),
            (500, 490, 450, 650),
            (800, 490, 750, 950)
        ],

        'bombas': [
            (350, 230),
            (700, 300),
            (1050, 180)
        ],

        'velocidad': 4
    },

    #Nivel volcan
    {
        'plataformas': [
            (50, 250, 300, 20),
            (400, 350, 300, 20),
            (750, 200, 300, 20),
            (1100, 350, 250, 20)
        ],

        'enemigos': [
            (200, 490, 150, 350),
            (500, 490, 450, 650),
            (800, 490, 750, 950),
            (1100, 490, 1050, 1200)
        ],

        'bombas': [
            (350, 180),
            (650, 280),
            (900, 130)
        ],

        'velocidad': 5
    },

   #Nivel desierto
    {
        'plataformas': [
            (50, 150, 350, 20),
            (450, 300, 300, 20),
            (800, 200, 300, 20),
            (1100, 350, 250, 20)
        ],

        'enemigos': [
            (200, 490, 150, 350),
            (450, 490, 400, 600),
            (700, 490, 650, 850),
            (950, 490, 900, 1100)
        ],

        'bombas': [
            (300, 220),
            (550, 230),
            (800, 130),
            (1100, 280)
        ],

        'velocidad': 6
    }
]



# El nivel 0 representa el primer nivel
nivel = 0


#
C_BLACK = (0, 0, 0)
C_RED = (255, 0, 0)
C_GREEN = (32, 128, 32)


# ============================================
# CREAR LA VENTANA
# ============================================

# Nombre de la ventana
pygame.display.set_caption("ARCADE")

# Crear la ventana del juego
window = pygame.display.set_mode(
    (win_width, win_height)
)


# ============================================
# CLASE FINALSPRITE
# ============================================

# Se utiliza para crear a la princesa
class FinalSprite(pygame.sprite.Sprite):

    def __init__(self, player_image, player_x, player_y):

        # Iniciar la clase Sprite
        super().__init__()

        # Cargar la imagen de la princesa
        # Nuevo tamaño: 40 x 65 píxeles
        self.image = pygame.transform.scale(
            pygame.image.load(player_image).convert_alpha(),
            (40, 65)
        )

        # Crear el rectángulo de colisión
        self.rect = self.image.get_rect(
            topleft=(player_x, player_y)
        )


# ============================================
# CLASE HERO
# ============================================

# Clase que controla al personaje principal
class Hero(pygame.sprite.Sprite):

    def __init__(self, filename, x, y, width, height):

        super().__init__()

        # Cargar la imagen del héroe
        self.image = pygame.transform.scale(
            pygame.image.load(filename).convert_alpha(),
            (width, height)
        )

        # Rectángulo de posición y colisiones
        self.rect = self.image.get_rect(
            topleft=(x, y)
        )

        # Velocidad horizontal del personaje
        self.x_speed = 0

        # Velocidad vertical del personaje
        self.y_speed = 0

        # Indicar si está parado en una plataforma
        self.stands_on = False

        # Guardar posición vertical exacta
        self.y = float(y)


    # ========================================
    # APLICAR GRAVEDAD
    # ========================================

    def gravitate(self):

        # Aumentar la velocidad de caída
        self.y_speed += gravedad


    # ========================================
    # HACER SALTAR AL PERSONAJE
    # ========================================

    def jump(self, y):

        # Solamente puede saltar si está apoyado
        if self.stands_on:

            # Aplicar fuerza hacia arriba
            self.y_speed = -y

            # Ya no está sobre una plataforma
            self.stands_on = False


    # ========================================
    # ACTUALIZAR MOVIMIENTO DEL HÉROE
    # ========================================

    def update(self):

        # ------------------------------------
        # MOVIMIENTO HORIZONTAL
        # ------------------------------------

        # Mover al héroe a izquierda o derecha
        self.rect.x += self.x_speed

        # Comprobar colisiones con plataformas
        platforms_touched = pygame.sprite.spritecollide(
            self, barriers, False
        )

        # Evitar atravesar paredes
        for p in platforms_touched:

            # Si va hacia la derecha
            if self.x_speed > 0:
                self.rect.right = p.rect.left

            # Si va hacia la izquierda
            elif self.x_speed < 0:
                self.rect.left = p.rect.right


        # ------------------------------------
        # APLICAR GRAVEDAD
        # ------------------------------------

        self.gravitate()


        # ------------------------------------
        # MOVIMIENTO VERTICAL
        # ------------------------------------

        # Actualizar posición vertical
        self.y += self.y_speed

        # Convertir posición a píxeles
        self.rect.y = round(self.y)

        # Detectar plataformas
        platforms_touched = pygame.sprite.spritecollide(
            self, barriers, False
        )

        # Inicialmente no está apoyado
        self.stands_on = False


        # ------------------------------------
        # COLISIÓN AL CAER
        # ------------------------------------

        if self.y_speed > 0:

            for p in platforms_touched:

                # Colocar al personaje encima
                # de la plataforma
                if self.rect.bottom >= p.rect.top:

                    self.rect.bottom = p.rect.top

                    # Detener caída
                    self.y_speed = 0

                    # Permitir otro salto
                    self.stands_on = True

                    # Actualizar posición exacta
                    self.y = float(self.rect.y)


        # ------------------------------------
        # COLISIÓN AL SUBIR
        # ------------------------------------

        elif self.y_speed < 0:

            for p in platforms_touched:

                # Evitar atravesar plataformas
                # con la cabeza
                self.rect.top = p.rect.bottom

                # Detener movimiento vertical
                self.y_speed = 0

                # Actualizar posición
                self.y = float(self.rect.y)


# ============================================
# CLASE WALL
# ============================================

# Clase utilizada para crear plataformas
class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, color=C_GREEN):

        super().__init__()

        # Crear una superficie rectangular
        self.image = pygame.Surface(
            (width, height)
        )

        # Pintar la plataforma
        self.image.fill(color)

        # Crear rectángulo de posición
        self.rect = self.image.get_rect(
            topleft=(x, y)
        )


# ============================================
# CLASE ENEMY
# ============================================

# Clase que controla enemigos y bombas
class Enemy(pygame.sprite.Sprite):

    def __init__(
        self, x, y, min_x, max_x,
        filename=img_file_enemy,
        width=60, height=60
    ):

        super().__init__()

        # Cargar imagen del enemigo
        # Nuevo tamaño normal: 60 x 60 píxeles
        self.image = pygame.transform.scale(
            pygame.image.load(filename).convert_alpha(),
            (width, height)
        )

        # Posición inicial
        self.rect = self.image.get_rect(
            topleft=(x, y)
        )

        # Límite izquierdo de movimiento
        self.min_x = min_x

        # Límite derecho de movimiento
        self.max_x = max_x

        # Velocidad inicial
        self.speed = 3


    # ========================================
    # MOVIMIENTO DE LOS ENEMIGOS
    # ========================================

    def update(self):

        # Si los límites son iguales,
        # el sprite permanece quieto
        if self.min_x == self.max_x:
            return

        # Al llegar al límite izquierdo,
        # cambia hacia la derecha
        if self.rect.x <= self.min_x:
            self.speed = abs(self.speed)

        # Al llegar al límite derecho,
        # cambia hacia la izquierda
        elif self.rect.x >= self.max_x:
            self.speed = -abs(self.speed)

        # Mover al enemigo
        self.rect.x += self.speed


# ============================================
# FUNCIÓN PARA CREAR LOS ESCENARIOS
# ============================================

def crear_escenario():

    # Variables globales utilizadas
    global all_sprites, barriers, enemies, bombs
    global robin, pr, shift, back

    # Reiniciar el desplazamiento
    shift = 0


    # ----------------------------------------
    # CARGAR EL FONDO DEL NIVEL
    # ----------------------------------------

    # Obtener el nombre de la imagen
    img_file_back = fondos[nivel]

    # Cargar y ajustar el fondo
    back = pygame.transform.scale(
        pygame.image.load(img_file_back).convert(),
        (win_width, win_height)
    )


    # ----------------------------------------
    # CREAR GRUPOS DE SPRITES
    # ----------------------------------------

    # Grupo de todos los sprites visibles
    all_sprites = pygame.sprite.Group()

    # Grupo de plataformas
    barriers = pygame.sprite.Group()

    # Grupo de enemigos
    enemies = pygame.sprite.Group()

    # Grupo de bombas
    bombs = pygame.sprite.Group()


    # ----------------------------------------
    # CREAR AL HÉROE
    # ----------------------------------------

    robin = Hero(
        img_file_hero,
        x_start,
        y_start,
        h_width,
        h_height
    )

    # Añadir héroe a los sprites
    all_sprites.add(robin)


    # ----------------------------------------
    # OBTENER DATOS DEL NIVEL
    # ----------------------------------------

    datos = niveles[nivel]


    # ----------------------------------------
    # CREAR PLATAFORMAS
    # ----------------------------------------

    # Recorrer las plataformas del nivel
    for wall in datos['plataformas']:

        # Crear plataforma
        w = Wall(*wall)

        # Agregar al grupo de colisiones
        barriers.add(w)

        # Agregar al grupo visible
        all_sprites.add(w)


    # ----------------------------------------
    # CREAR EL SUELO
    # ----------------------------------------

    # Suelo principal del escenario
    suelo = Wall(
        -200, 590, 1800, 20
    )

    # Agregar suelo a colisiones
    barriers.add(suelo)

    # Dibujar el suelo
    all_sprites.add(suelo)


    # ----------------------------------------
    # CREAR ENEMIGOS
    # ----------------------------------------

    # Recorrer posiciones de los enemigos
    for enemy_pos in datos['enemigos']:

        # Crear enemigo
        en = Enemy(*enemy_pos)

        # Asignar velocidad según el nivel
        en.speed = datos['velocidad']

        # Agregar enemigo a los grupos
        all_sprites.add(en)
        enemies.add(en)


    # ----------------------------------------
    # CREAR BOMBAS
    # ----------------------------------------

    # Crear las bombas del nivel
    for bomb_x, bomb_y in datos['bombas']:

        bomb = Enemy(
            bomb_x,
            bomb_y,
            0,
            0,
            img_file_bomb,
            40,
            40
        )

        # Las bombas miden 40 x 40 píxeles
        bombs.add(bomb)


    # ----------------------------------------
    # CREAR PRINCESA
    # ----------------------------------------

    # La princesa aparece cerca del final
    pr = FinalSprite(
        img_file_princess,
        1300,
        460
    )

    # Agregar princesa al escenario
    all_sprites.add(pr)


# ============================================
# INICIAR EL PRIMER NIVEL
# ============================================

crear_escenario()


# ============================================
# VARIABLES DEL JUEGO PRINCIPAL
# ============================================

# Controla si la ventana permanece abierta
run = True

# Indica si el juego terminó
finished = False

# Indica si el jugador ganó
victoria = False

# Reloj del juego
clock = pygame.time.Clock()


# ============================================
# BUCLE PRINCIPAL DEL JUEGO
# ============================================

while run:

    # Mantener 60 FPS
    clock.tick(FPS)


    # ----------------------------------------
    # DETECTAR EVENTOS DEL TECLADO
    # ----------------------------------------

    for event in pygame.event.get():

        # Cerrar ventana
        if event.type == pygame.QUIT:
            run = False


        # ------------------------------------
        # TECLAS PRESIONADAS
        # ------------------------------------

        elif event.type == pygame.KEYDOWN:

            # Mover hacia la izquierda
            if event.key == pygame.K_LEFT:
                robin.x_speed = -7

            # Mover hacia la derecha
            elif event.key == pygame.K_RIGHT:
                robin.x_speed = 7

            # Saltar con flecha arriba
            elif event.key == pygame.K_UP:
                robin.jump(salto)

            # Reiniciar con la tecla R
            elif event.key == pygame.K_r and finished:

                # Volver al primer nivel
                nivel = 0

                # Crear nuevamente el escenario
                crear_escenario()

                # Reiniciar estados
                finished = False
                victoria = False


        # ------------------------------------
        # TECLAS LIBERADAS
        # ------------------------------------

        elif event.type == pygame.KEYUP:

            # Detener movimiento horizontal
            if event.key in [
                pygame.K_LEFT,
                pygame.K_RIGHT
            ]:
                robin.x_speed = 0


    # ========================================
    # ACTUALIZAR EL JUEGO
    # ========================================

    if not finished:

        # Actualizar todos los sprites
        all_sprites.update()


        # ------------------------------------
        # MOVIMIENTO DE CÁMARA
        # ------------------------------------

        # Si el héroe llega al límite
        # de la pantalla, mover el escenario
        if (
            (robin.rect.x > right_bound and robin.x_speed > 0)
            or
            (robin.rect.x < left_bound and robin.x_speed < 0)
        ):

            # Calcular desplazamiento
            desplazamiento = robin.x_speed

            # Actualizar desplazamiento del fondo
            shift -= desplazamiento


            # --------------------------------
            # MOVER EL ESCENARIO
            # --------------------------------

            for s in all_sprites:

                # Mover todos menos al héroe
                if s != robin:
                    s.rect.x -= desplazamiento


            # --------------------------------
            # MOVER LAS BOMBAS
            # --------------------------------

            for s in bombs:
                s.rect.x -= desplazamiento


            # --------------------------------
            # AJUSTAR POSICIÓN DEL HÉROE
            # --------------------------------

            robin.rect.x -= desplazamiento


            # --------------------------------
            # ACTUALIZAR ENEMIGOS
            # --------------------------------

            # Ajustar sus límites de patrulla
            for en in enemies:

                en.min_x -= desplazamiento
                en.max_x -= desplazamiento


        # ------------------------------------
        # COLISIONES CON ENEMIGOS Y BOMBAS
        # ------------------------------------

        # Si el héroe toca un enemigo
        # o una bomba, pierde
        if (
            pygame.sprite.spritecollide(
                robin, enemies, False
            )
            or pygame.sprite.spritecollide(
                robin, bombs, False
            )
        ):

            # Eliminar héroe del grupo
            robin.kill()


        # ------------------------------------
        # COMPROBAR VICTORIA DEL NIVEL
        # ------------------------------------

        # Si el héroe toca a la princesa
        if robin.alive() and pygame.sprite.collide_rect(
            robin, pr
        ):

            # Si todavía quedan niveles
            if nivel < len(niveles) - 1:

                # Avanzar al siguiente nivel
                nivel += 1

                # Crear el nuevo escenario
                crear_escenario()

            else:

                # Terminó todos los niveles
                finished = True

                # Marcar victoria
                victoria = True


        # ------------------------------------
        # COMPROBAR DERROTA
        # ------------------------------------

        # Pierde al morir o caer de pantalla
        if (
            not robin.alive()
            or robin.rect.top > win_height
        ):

            finished = True
            victoria = False


    # ========================================
    # DIBUJAR EL FONDO
    # ========================================

    # Calcular desplazamiento repetido
    local_shift = shift % win_width

    # Primera copia del fondo
    window.blit(
        back,
        (local_shift - win_width, 0)
    )

    # Segunda copia del fondo
    window.blit(
        back,
        (local_shift, 0)
    )


    # ========================================
    # DIBUJAR PERSONAJES Y PLATAFORMAS
    # ========================================

    # Dibujar héroe, enemigos y plataformas
    all_sprites.draw(window)

    # Dibujar bombas
    bombs.draw(window)


    # ========================================
    # MOSTRAR NÚMERO DEL NIVEL
    # ========================================

    if not finished:

        # Fuente para indicador de nivel
        font_nivel = pygame.font.Font(None, 36)

        # Crear texto
        texto_nivel = font_nivel.render(
            f"NIVEL {nivel + 1} / 5",
            True,
            (255, 255, 255)
        )

        # Dibujar texto en pantalla
        window.blit(
            texto_nivel,
            (20, 20)
        )


    # ========================================
    # PANTALLAS FINALES
    # ========================================

    if finished:

        # Fondo negro
        window.fill(C_BLACK)


        # ------------------------------------
        # MENSAJE DE VICTORIA
        # ------------------------------------

        if victoria:

            text = font.render(
                "¡GANASTE!",
                True,
                C_RED
            )


        # ------------------------------------
        # MENSAJE DE DERROTA
        # ------------------------------------

        else:

            text = font.render(
                "JUEGO TERMINADO",
                True,
                C_RED
            )


        # ------------------------------------
        # CENTRAR MENSAJE
        # ------------------------------------

        text_rect = text.get_rect(
            center=(
                win_width // 2,
                win_height // 2
            )
        )

        # Mostrar mensaje
        window.blit(text, text_rect)


        # ------------------------------------
        # TEXTO PARA REINICIAR
        # ------------------------------------

        font_small = pygame.font.Font(
            None, 36
        )

        restart_text = font_small.render(
            "Presiona R para reiniciar",
            True,
            (255, 255, 255)
        )

        # Dibujar mensaje de reinicio
        window.blit(
            restart_text,
            restart_text.get_rect(
                center=(
                    win_width // 2,
                    win_height // 2 + 65
                )
            )
        )


    # ========================================
    # ACTUALIZAR PANTALLA
    # ========================================

    # Mostrar todos los cambios del fotograma
    pygame.display.update()


# ============================================
# CERRAR PYGAME
# ============================================

pygame.quit()
