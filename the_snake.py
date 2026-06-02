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
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 8

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Основной класс:
class GameObject():
    def __init__(self, body_colour):
        self.body_colour = body_colour
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
    def draw(self):
        pass
       
class Apple(GameObject):
    def __init__(self, position):
        super().__init__(APPLE_COLOR)
        self.position = position
    
    def randomize_position(self):
        # Вычитаем единицу чтобы яблоко не выходило за пределы экрана
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)
        
    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_colour, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

class Snake(GameObject):
    def __init__(self, position):
        super().__init__(SNAKE_COLOR)
        self.position = position

        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.body_colour = SNAKE_COLOR
        self.last = None
    
    def get_head_position(self):
        return self.positions[0]
        
    def move(self, apple_position):
        head_position = self.get_head_position()
        head_x, head_y = head_position
        dx, dy = self.direction

        new_head = (
            head_x + dx * GRID_SIZE,
            head_y + dy * GRID_SIZE
        )
      
        #Код для выхода за пределы экрана.
        if new_head[0] < 0:
            new_head = (SCREEN_WIDTH - GRID_SIZE, new_head[1])
        elif new_head[0] >= SCREEN_WIDTH:
            new_head = (0, new_head[1])
        if new_head[1] < 0:
            new_head = (new_head[0], SCREEN_HEIGHT - GRID_SIZE)
        elif new_head[1] >= SCREEN_HEIGHT:
            new_head = (new_head[0], 0)

        #Код для столкновения с самим собой.
        if new_head in self.positions[1:]:
            return False

        #Обновление списка позиций(добавляет голову в начало)
        self.positions.insert(0, new_head)
        #Если змейка ест яблоко.
        if new_head == apple_position:
            self.length +=1

            if len(self.positions) > 1:
                self.last = self.positions[-1]
        else:
            self.last = self.positions[-1] 
            self.positions.pop(-1)
        return True
    
    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_colour, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_colour, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

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
          

def main():
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake(position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    apple = Apple(position=(0, 0))
    apple.randomize_position() 

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        
        if snake.next_direction:
            snake.direction = snake.next_direction
            snake.next_direction = None

        if not snake.move(apple.position):
            break
        
        screen.fill(BOARD_BACKGROUND_COLOR) 
        apple.draw()  
        snake.draw()  
        pygame.display.flip()  
        

if __name__ == '__main__':
    main()
