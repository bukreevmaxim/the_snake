from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (181,184,177)

# Цвет границы ячейки
BORDER_COLOR = (41,49,51)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет камня
STONE_COLOR = (0, 0, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()




def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT

# Тут опишите все классы игры.
class GameObject():
    def __init__(self, body_color = None): 
        self.position = ((GRID_WIDTH //2),(GRID_HEIGHT//2))
        self.body_color = body_color

    def draw(self):
        pass


class Apple(GameObject):
    def __init__(self):
        super().__init__(APPLE_COLOR)
        self.randomize_position()
    
    def randomize_position(self):
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    # Метод draw класса Apple
    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Stone(GameObject):
    def __init__(self):
        super().__init__(STONE_COLOR)
        self.randomize_position()
        
    def randomize_position(self):
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)
            
    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)



class Snake(GameObject):
    def __init__(self):
        super().__init__(SNAKE_COLOR)
        # длина змейки
        self.length = 1
        # список сегментов
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        #текущее направление змейки
        self.direction = RIGHT
        # следующее направление, выбранное пользователем;
        self.next_direction = None
        #цвет змейки
        self.body_color = SNAKE_COLOR
        #координаты последнего сегмента перед его удалением.
        self.last = None
        #скорость змейки
        self.speed = SPEED

    def move(self):
        head_position = self.get_head_position()
        dx, dy = self.direction
        head_x, head_y = head_position

        new_head = (
            head_x + dx * GRID_SIZE,
            head_y + dy * GRID_SIZE
        )

        # Код для выхода за пределы экрана.
        if new_head[0] < 0:
            new_head = (SCREEN_WIDTH - GRID_SIZE, new_head[1])
        elif new_head[0] >= SCREEN_WIDTH:
            new_head = (0, new_head[1])
        if new_head[1] < 0:
            new_head = (new_head[0], SCREEN_HEIGHT - GRID_SIZE)
        elif new_head[1] >= SCREEN_HEIGHT:
            new_head = (new_head[0], 0)

        #Новая голова добавляется в начало списка
        self.positions.insert(0, new_head)
        
        
        # Последний элемент списка удаляется
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            del self.positions[-1]


    def reset(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


    #Метод draw класса Snake
    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


    def get_head_position(self):
        return self.positions[0]

    #Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

def main():

    pygame.init()
    apple = Apple()
    snake = Snake()
    stone = Stone()
    def game_over():
        snake.reset()
        apple.randomize_position()
        stone.randomize_position()
        snake.speed = SPEED


    while True:
        clock.tick(snake.speed)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.speed += 0.3
            apple.randomize_position()
        
        if snake.get_head_position() == stone.position:
            game_over()
       

        if snake.get_head_position() in snake.positions[1:]:
            game_over()


        screen.fill(BOARD_BACKGROUND_COLOR)
        stone.draw()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()


