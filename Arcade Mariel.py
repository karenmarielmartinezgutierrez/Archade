
# Traer las funciones y clases de una librería
import pygame

# Trae específicamente una función del módulo random
from random import randint

# Iniciar Pygame
pygame.init()

# Fuente o tipo de letra para la pantalla de derrota o victoria
font = pygame.font.Font(None, 72)

# Ajustes generales
win_width = 800
win_height = 600
left_bound = win_width / 40
right_bound = win_width - 8 * left_bound
shift = 0
gravedad = 0.25
salto = 9
x_start, y_start = 20, 10
h_width = 65
h_height = 90
FPS = 60

# Archivos
img_file_back = 'Enemigo 1.png'
img_file_hero = 'Heroe.png'
img_file_enemy = 'Enemigo 2.png'
img_file_bomb = 'bomba.png'
img_file_princess = 'princesa.png'

# Colores
C_BLACK = (0, 0, 0)
C_RED = (255, 0, 0)
C_GREEN = (32, 128, 32)

# Poner el nombre de la ventana
pygame.display.set_caption("ARCADE")

# Crear nuestra ventana
window = pygame.display.set_mode((win_width, win_height))

# Cargar y modificar la imagen de fondo
back = pygame.transform.scale(
    pygame.image.load(img_file_back).convert(),
    (win_width, win_height)
)


# Herencia de clases
class FinalSprite(pygame.sprite.Sprite):
    def __init__(self, player_image, player_x, player_y):
        super().__init__()

        self.image = pygame.transform.scale(
            pygame.image.load(player_image).convert_alpha(),
            (60, 120)
        )

        # Conseguir el rectángulo de nuestra imagen
        self.rect = self.image.get_rect(
            topleft=(player_x, player_y)
        )


class Hero(pygame.sprite.Sprite):
    def __init__(self, filename, x, y, width, height):
        super().__init__()

        self.image = pygame.transform.scale(
            pygame.image.load(filename).convert_alpha(),
            (width, height)
        )

        self.rect = self.image.get_rect(topleft=(x, y))

        self.x_speed = 0
        self.y_speed = 0

        # Variable para saber si está sobre una plataforma
        self.stands_on = False

        # Posición vertical exacta
        self.y = float(y)

    # Método para aplicar gravedad
    def gravitate(self):
        self.y_speed += gravedad

    # Método para saltar
    def jump(self, y):
        if self.stands_on:
            self.y_speed = -y
            self.stands_on = False

    # Actualizar la imagen y su ubicación
    def update(self):

        # Movimiento horizontal
        self.rect.x += self.x_speed

        # Comprobar colisiones horizontales
        platforms_touched = pygame.sprite.spritecollide(
            self, barriers, False
        )

        for p in platforms_touched:
            if self.x_speed > 0:
                self.rect.right = min(
                    self.rect.right, p.rect.left
                )

            elif self.x_speed < 0:
                self.rect.left = max(
                    self.rect.left, p.rect.right
                )

        # Aplicar gravedad
        self.gravitate()

        # Movimiento vertical
        self.y += self.y_speed
        self.rect.y = round(self.y)

        # Comprobar colisiones verticales
        platforms_touched = pygame.sprite.spritecollide(
            self, barriers, False
        )

        self.stands_on = False

        if self.y_speed > 0:
            for p in platforms_touched:
                if self.rect.bottom >= p.rect.top:
                    self.rect.bottom = p.rect.top
                    self.y_speed = 0
                    self.stands_on = True
                    self.y = float(self.rect.y)

        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = p.rect.bottom
                self.y_speed = 0
                self.y = float(self.rect.y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=C_GREEN):
        super().__init__()

        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        self.rect = self.image.get_rect(topleft=(x, y))


class Enemy(pygame.sprite.Sprite):
    def __init__(
        self, x, y, min_x, max_x,
        filename=img_file_enemy,
        width=100, height=100
    ):
        super().__init__()

        self.image = pygame.transform.scale(
            pygame.image.load(filename).convert_alpha(),
            (width, height)
        )

        self.rect = self.image.get_rect(topleft=(x, y))

        self.min_x = min_x
        self.max_x = max_x
        self.speed = 3

    def update(self):
        if self.min_x == self.max_x:
            return

        if self.rect.x <= self.min_x:
            self.speed = abs(self.speed)

        elif self.rect.x >= self.max_x:
            self.speed = -abs(self.speed)

        self.rect.x += self.speed


# Función para crear o reiniciar el escenario
def crear_escenario():
    global all_sprites, barriers, enemies, bombs
    global robin, pr, shift

    shift = 0

    # Iniciar grupos
    all_sprites = pygame.sprite.Group()
    barriers = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bombs = pygame.sprite.Group()

    # Crear personaje
    robin = Hero(
        img_file_hero, x_start, y_start,
        h_width, h_height
    )
    all_sprites.add(robin)

    # Crear plataformas
    for wall in [
        (50, 150, 480, 20),
        (700, 50, 50, 360),
        (350, 380, 640, 20),
        (-200, 590, 1600, 20)
    ]:
        w = Wall(*wall)
        barriers.add(w)
        all_sprites.add(w)

    # Crear enemigos
    for enemy_pos in [
        (50, 480, 20, 200),
        (400, 480, 300, 500)
    ]:
        en = Enemy(*enemy_pos)
        all_sprites.add(en)
        enemies.add(en)

    # Crear bomba
    bomb = Enemy(
        550, 220, 0, 0,
        img_file_bomb, 60, 60
    )
    bombs.add(bomb)

    # Crear princesa
    pr = FinalSprite(
        img_file_princess,
        win_width + 500,
        win_height - 150
    )
    all_sprites.add(pr)


# Crear el escenario inicial
crear_escenario()

# Juego principal
run = True
finished = False
victoria = False

clock = pygame.time.Clock()

while run:
    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                robin.x_speed = -5

            elif event.key == pygame.K_RIGHT:
                robin.x_speed = 5

            elif event.key == pygame.K_UP:
                robin.jump(salto)

            elif event.key == pygame.K_r and finished:
                crear_escenario()
                finished = False
                victoria = False

        elif event.type == pygame.KEYUP:

            if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                robin.x_speed = 0

    if not finished:

        # Actualizar sprites
        all_sprites.update()

        # Movimiento de cámara
        if (
            (robin.rect.x > right_bound and robin.x_speed > 0)
            or
            (robin.rect.x < left_bound and robin.x_speed < 0)
        ):
            desplazamiento = robin.x_speed
            shift -= desplazamiento

            # Mover el escenario, pero no al jugador
            for s in all_sprites:
                if s != robin:
                    s.rect.x -= desplazamiento

            for s in bombs:
                s.rect.x -= desplazamiento

            # Actualizar límites de patrulla de enemigos
            for en in enemies:
                en.min_x -= desplazamiento
                en.max_x -= desplazamiento

        # Comprobar colisiones con enemigos y bombas
        if (
            pygame.sprite.spritecollide(robin, enemies, False)
            or pygame.sprite.spritecollide(robin, bombs, False)
        ):
            robin.kill()

        # Comprobar victoria
        if robin.alive() and pygame.sprite.collide_rect(robin, pr):
            finished = True
            victoria = True

        # Comprobar derrota
        if not robin.alive() or robin.rect.top > win_height:
            finished = True
            victoria = False

    # Dibujar el fondo antes de los personajes
    local_shift = shift % win_width

    window.blit(back, (local_shift - win_width, 0))
    window.blit(back, (local_shift, 0))

    # Dibujar plataformas, enemigos y personaje
    all_sprites.draw(window)
    bombs.draw(window)

    # Pantallas finales
    if finished:
        window.fill(C_BLACK)

        if victoria:
            text = font.render(
                "¡GANASTE!", True, C_RED
            )
        else:
            text = font.render(
                "JUEGO TERMINADO", True, C_RED
            )

        text_rect = text.get_rect(
            center=(win_width // 2, win_height // 2)
        )
        window.blit(text, text_rect)

        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render(
            "Presiona R para reiniciar",
            True,
            (255, 255, 255)
        )

        window.blit(
            restart_text,
            restart_text.get_rect(
                center=(win_width // 2, win_height // 2 + 65)
            )
        )

    pygame.display.update()

pygame.quit()
