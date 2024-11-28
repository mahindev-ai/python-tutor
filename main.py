import pygame
import random
import sys

# Inicializar PyGame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Reloj
clock = pygame.time.Clock()
FPS = 10

# Función: Mostrar texto
def draw_text(surface, text, font, size, color, x, y):
    font_obj = pygame.font.Font(font, size)
    text_surface = font_obj.render(text, True, color)
    surface.blit(text_surface, (x, y))

# Función: Generar nueva comida
def generate_food(snake_body):
    while True:
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        if (x, y) not in snake_body:
            return x, y

# Bucle principal del juego
def main():
    # Variables del juego
    snake = [(100, 100), (90, 100), (80, 100)]  # Coordenadas iniciales
    direction = "RIGHT"
    food = generate_food(snake)
    score = 0

    running = True
    while running:
        screen.fill(BLACK)

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        # Mover la serpiente
        head_x, head_y = snake[0]
        if direction == "UP":
            head_y -= CELL_SIZE
        elif direction == "DOWN":
            head_y += CELL_SIZE
        elif direction == "LEFT":
            head_x -= CELL_SIZE
        elif direction == "RIGHT":
            head_x += CELL_SIZE

        # Agregar nueva cabeza
        new_head = (head_x, head_y)
        snake.insert(0, new_head)

        # Verificar si la serpiente come la comida
        if new_head == food:
            score += 1
            food = generate_food(snake)
        else:
            snake.pop()  # Eliminar la cola si no comió

        # Verificar colisiones
        if (
            head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT or
            new_head in snake[1:]
        ):
            running = False

        # Dibujar la comida
        pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], CELL_SIZE, CELL_SIZE))

        # Dibujar la serpiente
        for segment in snake:
            pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))

        # Dibujar los bordes de la pantalla
        pygame.draw.rect(screen, WHITE, pygame.Rect(0, 0, WIDTH, HEIGHT), 3)

        # Mostrar puntaje
        draw_text(screen, f"Score: {score}", None, 24, WHITE, 10, 10)

        # Actualizar pantalla
        pygame.display.flip()
        clock.tick(FPS)

    # Pantalla de Game Over
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", None, 50, WHITE, WIDTH // 4, HEIGHT // 3)
    draw_text(screen, f"Score: {score}", None, 30, WHITE, WIDTH // 3, HEIGHT // 2)
    draw_text(screen, "Press ENTER to Restart", None, 20, WHITE, WIDTH // 4, HEIGHT // 1.5)
    pygame.display.flip()

    wait_for_key()

# Esperar tecla para reiniciar
def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                main()

# Ejecutar el juego
if __name__ == "__main__":
    main()
