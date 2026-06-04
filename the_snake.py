import pygame as pg

import sys

from random import randint
# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
GRID_LIST = ((GRID_WIDTH // 2), (GRID_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона
BOARD_BACKGROUND_COLOR = (181, 184, 177)

# Цвет границы ячейки
BORDER_COLOR = (41, 49, 51)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Цвет камня
STONE_COLOR = (0, 0, 0)

# Цвет яда
POISON_COLOR = (0, 0, 255)

# Цвет по умолчанию
DEFAULT_COLOR = (168, 228, 160)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


def handle_keys(game_object):
    """Обрабатывает события клавиатуры.

    Корректно завершает работу приложения, а так же устанавливает
    направление движения объекта на основе нажатых клавиш,
    запрещая разворот на 180 градусов.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()


class GameObject:
    """Основной класс от которого наследуются все остальные предметы в игре"""

    def __init__(self, position=None, body_color=None):
        if position is None:
            self.position = GRID_LIST
        else:
            self.position = position

        if body_color is None:
            self.body_color = DEFAULT_COLOR
        else:
            self.body_color = body_color

    def draw(self):
        """Базовый метод отрисовки"""
        fail_class = self.__class__.__name__
        fail_text = ('Метод draw не определён в классе')
        raise NotImplementedError(f'{fail_text} {fail_class}')

    def _draw_grid_cell(self, position, fill_color, border_color=BORDER_COLOR):
        """Отрисовывает одну ячейку игрового поля."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, fill_color, rect)
        pg.draw.rect(screen, border_color, rect, 1)

    def _random_position(self):
        """ЗДЕСЬ ДОЛЖНА БЫТЬ ПРОВЕРКА НА ОТСУТСТВИЕ ЗАНЯТЫХ КЛЕТОК"""
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)


class Apple(GameObject):
    """Класс предемета яблоко"""

    def __init__(self, body_color=APPLE_COLOR):
        self.body_color = body_color
        self.randomize_position()

    def randomize_position(self):
        """Выдаёт случайные координаты для спавна яблока"""
        self._random_position()

    def draw(self):
        """Рисует яблоко в виде квадрата"""
        self._draw_grid_cell(self.position, self.body_color)


class Poison(Apple):
    """Класс предмета уменьшающего скорость и размер змейки при поедании"""

    def __init__(self, body_color=POISON_COLOR):
        self.body_color = body_color
        self.randomize_position()

    def randomize_position(self):
        """Выдаёт случайные координаты для спавна яда"""
        self._random_position()

    def draw(self):
        """Рисует яд в виде квадрата"""
        self._draw_grid_cell(self.position, self.body_color)


class Stone(Apple):
    """Класс предмета камень"""

    def __init__(self, body_color=STONE_COLOR):
        self.body_color = body_color
        self.randomize_position()

    def randomize_position(self):
        """Выдаёт случайные координаты для спавна камня"""
        self._random_position()

    def draw(self):
        """Рисует камень в виде квадрата"""
        self._draw_grid_cell(self.position, self.body_color)


class Snake(GameObject):
    """Класс змейки"""

    def __init__(self):
        GameObject.__init__(self)

        # длина змейки
        self.length = 1
        # список сегментов
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        # текущее направление змейки
        self.direction = RIGHT
        # следующее направление, выбранное пользователем;
        self.next_direction = None
        # цвет змейки
        self.body_color = SNAKE_COLOR
        # координаты последнего сегмента перед его удалением.
        self.last = None
        # скорость змейки
        self.speed = SPEED

    def move(self):
        """Определяем движение змейки"""
        head_position = self.get_head_position()
        dx, dy = self.direction
        head_x, head_y = head_position

        new_head = (
            head_x + dx * GRID_SIZE,
            head_y + dy * GRID_SIZE
        )

        # Код для выхода за пределы экрана.ПЕРЕРАБОТАТЬЬ!!!!
        if new_head[0] < 0:
            new_head = (SCREEN_WIDTH - GRID_SIZE, new_head[1])
        elif new_head[0] >= SCREEN_WIDTH:
            new_head = (0, new_head[1])
        if new_head[1] < 0:
            new_head = (new_head[0], SCREEN_HEIGHT - GRID_SIZE)
        elif new_head[1] >= SCREEN_HEIGHT:
            new_head = (new_head[0], 0)

        # Новая голова добавляется в начало списка
        self.positions.insert(0, new_head)

        # Последний элемент списка удаляется
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            del self.positions[-1]

    def reset(self):
        """Сброс настроек змейки к начальному состоянию"""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)

    # Метод draw класса Snake
    def draw(self):
        """Рисует змейку"""
        for position in self.positions:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Получаем позицию головы(первого элемента)"""
        return self.positions[0]

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def main():
    """Запускает игру «Змейка» и управляет игровым циклом.

    Инициализирует Pygame, создаёт объекты змейки и яблока,
    затем запускает бесконечный цикл игры с обработкой ввода,
    обновлением состояния и отрисовкой.
    """
    pg.init()
    snake = Snake()
    apple = Apple()
    stone = Stone()
    poison = Poison()

    def game_over():
        snake.reset()
        apple.randomize_position()
        stone.randomize_position()
        poison.randomize_position()
        snake.speed = SPEED

    while True:
        clock.tick(snake.speed)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.speed += 0.5
            apple.randomize_position()

        elif snake.get_head_position() == poison.position:
            snake.speed -= 0.5
            if snake.speed < 3:
                game_over()
            poison.randomize_position()

        elif snake.get_head_position() == stone.position:
            game_over()

        if snake.length < 1:
            game_over()

        if snake.get_head_position() in snake.positions[4:]:
            game_over()

        # Нужно экран поменять на занятые клетки
        screen.fill(BOARD_BACKGROUND_COLOR)
        stone.draw()
        apple.draw()
        snake.draw()
        poison.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
