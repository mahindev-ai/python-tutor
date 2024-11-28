import pygame
import random
import sys

# Inicializar PyGame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Defender")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Configuración del jugador
player_width, player_height = 50, 40
player_x, player_y = WIDTH // 2, HEIGHT - 70
player_speed = 5

# Configuración de enemigos
enemy_width, enemy_height = 50, 40
enemy_speed = 3
enemies = []

# Puntaje y vidas
score = 0
lives = 3

# Fuentes
font = pygame.font.Font(None, 36)

# Función: Dibujar texto
def draw_text(surface, text, font, size, color, x, y):
    font_obj = pygame.font.Font(font, size)
    text_surface = font_obj.render(text, True, color)
    surface.blit(text_surface, (x, y))

# Función: Crear enemigos
def spawn_enemy():
    x = random.randint(0, WIDTH - enemy_width)
    y = random.randint(-100, -40)
    enemies.append(pygame.Rect(x, y, enemy_width, enemy_height))

# Función: Verificar colisiones
def check_collision(player, enemies):
    global lives
    for enemy in enemies:
        if player.colliderect(enemy):
            lives -= 1
            enemies.remove(enemy)
            if lives <= 0:
                return True
    return False

# Función: Actualizar enemigos
def update_enemies(enemies):
    global score
    for enemy in enemies:
        enemy.y += enemy_speed
        if enemy.y > HEIGHT:
            enemies.remove(enemy)
            score += 1  # Sumar puntos al esquivar enemigos

# Función: Pantalla de Game Over
def game_over_screen():
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", None, 72, RED, WIDTH // 2 - 150, HEIGHT // 2 - 50)
    draw_text(screen, f"Score: {score}", None, 36, WHITE, WIDTH // 2 - 80, HEIGHT // 2 + 20)
    draw_text(screen, "Press ENTER to Restart", None, 24, WHITE, WIDTH // 2 - 150, HEIGHT // 2 + 60)
    pygame.display.flip()
    wait_for_key()

# Función: Esperar tecla
def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

# Bucle principal
# Bucle principal
def main():
    global score, lives, enemies
    clock = pygame.time.Clock()
    running = True

    player = pygame.Rect(player_x, player_y, player_width, player_height)

    # Crear enemigos iniciales
    for _ in range(5):
        spawn_enemy()

    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Controles del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x < WIDTH - player_width:
            player.x += player_speed
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= player_speed
        if keys[pygame.K_DOWN] and player.y < HEIGHT - player_height:
            player.y += player_speed

        # Dibujar jugador
        pygame.draw.rect(screen, BLUE, player)

        # Crear nuevos enemigos
        if random.randint(1, 50) == 1:
            spawn_enemy()

        # **Llamar a la función update_enemies**
        update_enemies(enemies)

        # Dibujar enemigos
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)

        # Verificar colisiones
        if check_collision(player, enemies):
            game_over_screen()
            return

        # Dibujar puntaje y vidas
        draw_text(screen, f"Score: {score}", None, 36, WHITE, 10, 10)
        draw_text(screen, f"Lives: {lives}", None, 36, WHITE, WIDTH - 120, 10)

        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(60)

# Ejecutar juego
if __name__ == "__main__":
    main()
