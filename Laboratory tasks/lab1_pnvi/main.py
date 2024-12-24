import pygame
import random

pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Fill Puzzle")

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
WHITE = (255, 255, 255)

GRID_SIZE = 5
tile_size = WIDTH // GRID_SIZE


class Square(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x * tile_size
        self.rect.y = y * tile_size
        self.color = WHITE
        self.image.fill(self.color)

    def update(self, color=None):
        if color:
            self.color = color
        self.image.fill(self.color)

    def get_neighbors(self, all_squares):
        neighbors = []
        x, y = self.rect.x // tile_size, self.rect.y // tile_size
        for tile in all_squares:
            adj_x, adj_y = tile.rect.x // tile_size, tile.rect.y // tile_size
            if (abs(adj_x - x) == 1 and adj_y == y) or (abs(adj_y - y) == 1 and adj_x == x):
                neighbors.append(tile)
        return neighbors


def display_text(text, font_size, color, y_offset=0):
    font = pygame.font.SysFont("Arial", font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)


def all_squares_check(all_squares):
    for square in all_squares:
        for neighbor in square.get_neighbors(all_squares):
            if square.color == neighbor.color:
                return False
    return True


def game_loop():
    all_squares = pygame.sprite.Group()
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            square = Square(x, y)
            all_squares.add(square)

    run = True
    while run:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for tile in all_squares:
                    if tile.rect.collidepoint(mouse_x, mouse_y):
                        new_color = random.choice(colors)
                        while new_color == tile.color:
                            new_color = random.choice(colors)

                        neighbors = tile.get_neighbors(all_squares)
                        if all(neighbor.color != new_color for neighbor in neighbors):
                            tile.update(new_color)
                        break

        all_squares.update()
        all_squares.draw(screen)

        if all_squares_check(all_squares):
            display_text("Game is finished! Good Game!", 40, (0, 255, 0), -50)
            pygame.display.flip()
            pygame.time.wait(3000)
            run = False

        display_text("Click on a square to change its color.", 20, (0, 0, 0), -200)
        pygame.display.flip()

    pygame.quit()


game_loop()
