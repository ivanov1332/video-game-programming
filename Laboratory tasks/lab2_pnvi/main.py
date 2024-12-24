import pygame
import random
import os

# Initializing pygame
pygame.init()

# Parameters for window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Scavenger")

# Color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Read resources
RESOURCES_DIR = "resources"
SPACESHIP_IMG = pygame.image.load(os.path.join(RESOURCES_DIR, "spaceship.png"))
ASTEROID_IMG = pygame.image.load(os.path.join(RESOURCES_DIR, "asteroid.png"))
ENERGY_CRYSTAL_IMG = pygame.image.load(os.path.join(RESOURCES_DIR, "energy_crystal.png"))

# Sound effects
pygame.mixer.music.load(os.path.join(RESOURCES_DIR, "background_music.wav"))
CLASH_SOUND = pygame.mixer.Sound(os.path.join(RESOURCES_DIR, "clash_sound.wav"))

# Start background music
pygame.mixer.music.play(-1)  # -1 means reproduction without end(infinity)

# FPS
clock = pygame.time.Clock()
FPS = 60


# Class for player(spaceship)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(SPACESHIP_IMG, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def update(self):
        pass


# Class for energy crystals
class EnergyCrystal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(ENERGY_CRYSTAL_IMG, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(2, 4)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


# Class for asteroid
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(ASTEROID_IMG, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

def display_text(text, font_size, color, y_offset=0):
    font = pygame.font.SysFont("Arial", font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text_surface, text_rect)

# Main part of the game
def main():
    # Flag for the game (True=Running,False=Closed)
    run = True

    # Creating player
    player = Player()

    # Creating groups
    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    energy_crystals = pygame.sprite.Group()

    # Adding player into group where are all objects
    all_sprites.add(player)

    # Timer for generating asteroids and crystals
    pygame.time.set_timer(pygame.USEREVENT, 1500)
    pygame.time.set_timer(pygame.USEREVENT + 1, 2000)

    count_score=0

    while run:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.USEREVENT:
                # Creating asteroids
                asteroid = Asteroid()
                all_sprites.add(asteroid)
                asteroids.add(asteroid)

            if event.type == pygame.USEREVENT + 1:
                # Creating crystals
                crystal = EnergyCrystal()
                all_sprites.add(crystal)
                energy_crystals.add(crystal)

        # Player control
        keys = pygame.key.get_pressed()
        player.move(keys)

        # Updating on all objects
        all_sprites.update()

        # Checking for crashing with asteroids
        if pygame.sprite.spritecollide(player, asteroids, True):
            CLASH_SOUND.play()
            display_text("You lose,Game Over!",40, WHITE)
            display_text("Click to exit the game",30,WHITE,50)
            pygame.display.flip()
            pygame.time.wait(2000)
            run = False

        # Checking for collecting crystals
        if pygame.sprite.spritecollide(player, energy_crystals, True):
            count_score += 1
            print(f"Energy crystal collected! SCORE: {count_score}")

        if count_score == 5:
            display_text("YOU WIN, CONGRATULATIONS!", 40, WHITE)
            display_text("Click to exit", 30, WHITE, 50)
            pygame.display.flip()
            pygame.time.wait(2000)
            run = False

        # Drawing on window
        screen.fill(BLACK)
        all_sprites.draw(screen)
        pygame.display.flip()

        # FPS
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
