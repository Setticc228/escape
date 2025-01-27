import os
import sys

import pygame

# Константы
FPS = 60
TILE_SIZE = 50
SCREEN_WIDTH = 1440  # 16 * TILE_SIZE
SCREEN_HEIGHT = 810  # 9 * TILE_SIZE
PLAYER_SIZE = SCREEN_WIDTH // 144

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()


# Загрузка изображений
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image.set_colorkey(colorkey)
    return image


# Классы
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(pos_x * TILE_SIZE, pos_y * TILE_SIZE)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = load_image('player.png', (255, 255, 255))  # Прозрачный фон
        self.rect = self.image.get_rect().move(pos_x * TILE_SIZE, pos_y * TILE_SIZE)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.direction = 'RIGHT'
        self.can_shoot = True

    def move(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)

    def update(self):
        if self.direction == 'LEFT':
            self.image = pygame.transform.flip(load_image('player.png', (255, 255, 255)), True, False)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction):
        super().__init__(bullets_group)
        self.image = load_image('bullet.png')
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.direction = direction
        self.speed = 10

    def update(self):
        if self.direction == 'RIGHT':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH:
            self.kill()


# Загрузка уровня
def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: list(x.ljust(max_width, '.')), level_map))


def generate_level(level):
    new_player = None
    for y, row in enumerate(level):
        for x, tile in enumerate(row):
            if tile == '.':
                Tile('empty', x, y)
            elif tile == '$':
                Tile('wall', x, y)
            elif tile == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                print(level[y][:x], level[y][x + 1:])
                level[y] = ''.join(level[y][:x]) + '.' + ''.join(level[y][x + 1:])
    return new_player


# Главное меню
def start_screen():
    fon = pygame.transform.scale(load_image('bg.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    start_button = font.render("Начать игру", True, (255, 255, 255))
    exit_button = font.render("Выход", True, (255, 255, 255))
    screen.blit(start_button, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
    screen.blit(exit_button, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 10))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if SCREEN_WIDTH // 2 - 100 < mouse_x < SCREEN_WIDTH // 2 + 100:
                    if SCREEN_HEIGHT // 2 - 50 < mouse_y < SCREEN_HEIGHT // 2:
                        return  # Начать игру
                    elif SCREEN_HEIGHT // 2 + 10 < mouse_y < SCREEN_HEIGHT // 2 + 60:
                        terminate()  # Выход
        clock.tick(FPS)


# Завершение игры
def terminate():
    pygame.quit()
    sys.exit()


# Основной игровой цикл
def main():
    global all_sprites, tiles_group, player_group, bullets_group, tile_images
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()

    tile_images = {
        'empty': load_image('grass.png'),
        'wall': load_image('box1.png')  # Замените на Ваши изображения
    }

    start_screen()
    level = load_level('data/level.txt')  # Убедитесь, что файл level.txt существует
    player = generate_level(level)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player.move(player.pos_x, player.pos_y - 1)
            if keys[pygame.K_s]:
                player.move(player.pos_x, player.pos_y + 1)
            if keys[pygame.K_a]:
                player.direction = 'LEFT'
                player.move(player.pos_x - 1, player.pos_y)
            if keys[pygame.K_d]:
                player.direction = 'RIGHT'
                player.move(player.pos_x + 1, player.pos_y)

            if player.can_shoot and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                bullet = Bullet(player.rect.centerx, player.rect.centery, player.direction)
                player.can_shoot = False

            if not keys[pygame.K_w] and not keys[pygame.K_a] and not keys[pygame.K_s] and not keys[pygame.K_d]:
                player.can_shoot = True

        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
