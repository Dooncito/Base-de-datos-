import pygame
import sys

from flechas_votacion import tkinter_controls
import threading

screen_width = 400
screen_height = 400
screen =None
page = None

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Intro:
    def __init__(self, user_id):
        self.screen = pygame.display.get_surface()
        self.alpha = -5
        self.imgLogo = pygame.image.load("Proyecto/assets/images/portada.jpg")
        self.user_id=user_id

        # Definir los colores
        self.white = (255, 255, 255)
        self.gray = (100, 100, 100)
        self.black = (0, 0, 0)

        # Definir fuente
        self.font = pygame.font.SysFont(None, 48)

        # Definir rectángulos para los botones
        self.start_button = pygame.Rect((self.screen.get_width() // 2) - 100, 300, 200, 50)
        self.quit_button = pygame.Rect((self.screen.get_width() // 2) - 100, 400, 200, 50)

    def draw_text(self, text, font, color, rect):
        """Función para dibujar texto en los botones."""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def bucle(self, events:list):
        global page
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.start_button.collidepoint(mouse_pos):
                    page = 1  # Cambia a la siguiente página/juego
                    tkinter_thread = threading.Thread(target=tkinter_controls, args=(self.user_id,))
                    tkinter_thread.start()
                if self.quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        self.screen.fill(self.black)
        width, height = self.screen.get_size()
        img_logo_copy = self.imgLogo.copy()
        img_logo_copy = pygame.transform.scale(img_logo_copy, (height,height))
        img_size = img_logo_copy.get_size()
        img_logo_copy.set_alpha(self.alpha)
        self.screen.blit(img_logo_copy, ((width-img_size[0])/2,0))

        # Dibujar los botones
        pygame.draw.rect(self.screen,
                         self.gray if self.start_button.collidepoint(pygame.mouse.get_pos()) else self.white,
                         self.start_button)
        pygame.draw.rect(self.screen,
                         self.gray if self.quit_button.collidepoint(pygame.mouse.get_pos()) else self.white,
                         self.quit_button)

        # Dibujar texto en los botones
        self.draw_text("Iniciar", self.font, self.black, self.start_button)
        self.draw_text("Salir", self.font, self.black, self.quit_button)

        pygame.display.flip()

class MazeGame:
    def __init__(self):
        self.screen=pygame.display.get_surface()
        self.current_level=1
        self.maze=self.cargar_maze(self.current_level)
        #Definir el tamaño del bloque y velocidad
        self.block_size = 20
        self.player_speed = self.block_size
        self.player_pos=[self.block_size, self.block_size]

    def cargar_maze(self,level):
        # Definir el laberinto (1 = pared, 0 = camino, 2 = meta)
        if level==1:
            return [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
            [1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
            [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 2, 1],  # '2' es la meta
            [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        ]
        return []

    def next_level(self):
        self.current_level += 1
        self.maze = self.cargar_maze(self.current_level)
        self.player_pos=[self.block_size, self.block_size] # Definir el jugador (un punto)

    # Función para dibujar el laberinto
    def draw_maze(self):
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                if self.maze[row][col] == 1:
                    pygame.draw.rect(self.screen, BLUE, (col * self.block_size, row * self.block_size, self.block_size, self.block_size))
                elif self.maze[row][col] == 2:
                    pygame.draw.rect(self.screen, GREEN, (col * self.block_size, row * self.block_size, self.block_size, self.block_size))

    # Función para dibujar al jugador
    def draw_player(self):
        pygame.draw.rect(self.screen, RED, (self.player_pos[0], self.player_pos[1], self.block_size, self.block_size))

    # Función para verificar si el movimiento es válido
    def is_valid_move(self,x, y):
        row = y // self.block_size
        col = x // self.block_size
        if self.maze[row][col] == 0 or self.maze[row][col] == 2:  # Permite moverse al camino y a la meta
            return True
        return False

    # Función para verificar si el jugador ha ganado
    def check_win(self):
        row = self.player_pos[1] // self.block_size
        col = self.player_pos[0] // self.block_size
        if self.maze[row][col] == 2:  # Si llega a la meta
            return True
        return False

    def bucle(self, events):
        # Lógica para la pantalla del juego
        screen.fill(WHITE)
        self.draw_maze()
        self.draw_player()

        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                global page
                page = 0  # Regresar a login

def main_game(user_id):
    global screen
    global page
    pygame.init()

    screen=pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Juego de Laberinto")

    intro, game = Intro(user_id), MazeGame()
    pages = [intro, game]

    # Bucle del juego
    clock = pygame.time.Clock()
    win = False
    page = 0
    running = True

    while running:
        events = pygame.event.get()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not win:
            # Obtener las teclas presionadas
            keys = pygame.key.get_pressed()

            # Movimiento del jugador
            if keys[pygame.K_LEFT]:
                new_x = game.player_pos[0] - game.player_speed
                if game.is_valid_move(new_x, game.player_pos[1]):
                    game.player_pos[0] = new_x
                    print("cuando se mueva a izquierda",new_x)
            if keys[pygame.K_RIGHT]:
                new_x = game.player_pos[0] + game.player_speed
                if game.is_valid_move(new_x, game.player_pos[1]):
                    game.player_pos[0] = new_x
                    print("cuando se mueva a derecha",new_x)
            if keys[pygame.K_UP]:
                new_y = game.player_pos[1] - game.player_speed
                if game.is_valid_move(game.player_pos[0], new_y):
                    game.player_pos[1] = new_y
                    print("cuando se mueva a arriba",new_y)
            if keys[pygame.K_DOWN]:
                new_y = game.player_pos[1] + game.player_speed
                if game.is_valid_move(game.player_pos[0], new_y):
                    game.player_pos[1] = new_y
                    print("cuando se mueva a abajo",new_y)

            # Verificar si el jugador ganó
            if game.check_win():
                win = True
        else:
            # Mostrar mensaje de ganaste
            font = pygame.font.Font(None, 74)
            text = font.render("¡Ganaste!", True, BLACK)
            screen.blit(text, (100, 150))
            # Salir de pygame
            pygame.quit()
            sys.exit()

        # Actualizar la pantalla
        pages[page].bucle(events)
        pygame.display.flip()
        clock.tick(10)