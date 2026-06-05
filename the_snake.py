import sys
from random import randint

import pygame as pg

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
                game_object.update_direction(UP)
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()


class GameObject:
    """Основной класс от которого наследуются все остальные предметы в игре."""

    def __init__(self, position=None, body_color=None):
        if position is None:
            self.position = GRID_LIST
        else:
            self.position = position

        if body_color is None:
            self.body_color = SNAKE_COLOR
        else:
            self.body_color = body_color

    def draw(self):
        """Базовый метод отрисовки."""
        fail_text = ('Метод draw не определён в классе')
        fail_class = self.__class__.__name__
        raise NotImplementedError(f'{fail_text} {fail_class}')

    def _draw_grid_cell(self, position, fill_color, border_color=BORDER_COLOR):
        """Отрисовывает одну ячейку игрового поля."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, fill_color, rect)
        pg.draw.rect(screen, border_color, rect, 1)

    def _random_position(self, full_positions=None):
        """Проверка на занятые."""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            position = (x, y)
            if full_positions is None or position not in full_positions:
                self.position = position
                break


class Apple(GameObject):
    """Класс предмета яблоко."""

    def __init__(self, position=None, body_color=APPLE_COLOR):
        self.position = position
        self.body_color = body_color
        self.randomize_position()

    def randomize_position(self, full_positions=None):
        """Выдаёт случайные координаты для спавна яблока."""
        self._random_position(full_positions)

    def draw(self):
        """Рисует яблоко в виде квадрата."""
        self._draw_grid_cell(self.position, self.body_color)


class Poison(Apple):
    """Класс предмета уменьшающего скорость змейки."""

    def __init__(self, position=None, body_color=POISON_COLOR):
        self.position = position
        self.body_color = body_color
        self.randomize_position()

    def randomize_position(self, full_positions=None):
        """Выдаёт случайные координаты для спавна яда."""
        self._random_position(full_positions)

    def draw(self):
        """Рисует яд в виде квадрата."""
        self._draw_grid_cell(self.position, self.body_color)


class Stone(Apple):
    """Класс предмета камень."""

    def __init__(self, position=None, body_color=STONE_COLOR):
        self.position = position
        self.body_color = body_color
        self.randomize_position()

    def randomize_position(self, full_positions=None):
        """Выдаёт случайные координаты для спавна камня."""
        self._random_position(full_positions)

    def draw(self):
        """Рисует камень в виде квадрата."""
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

    def move(self):
        """Определяем движение змейки."""
        head_position = self.get_head_position()
        dx, dy = self.direction
        head_x, head_y = head_position

        new_head = (
            head_x + dx * GRID_SIZE,
            head_y + dy * GRID_SIZE
        )

        # Код для выхода за пределы экрана.
        new_head = (
            new_head[0] % SCREEN_WIDTH,
            new_head[1] % SCREEN_HEIGHT
        )

        # Новая голова добавляется в начало списка
        self.positions.insert(0, new_head)

        # Последний элемент списка удаляется
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop(-1)
        else:
            self.last = None

    def reset(self):
        """Сброс настроек змейки к начальному состоянию."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        fps = 5
        screen.fill(BOARD_BACKGROUND_COLOR)
        return fps

    # Метод draw класса Snake
    def draw(self):
        """Рисует змейку."""
        for position in self.positions:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Получаем позицию головы(первого элемента)."""
        return self.positions[0]

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        self.direction = new_direction


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
    # Скорость игры:
    fps = 5

    def get_full_positions():
        """Собирает все занятые клетки (змейка + все предметы)."""
        occupied = set(snake.positions)
        occupied.add(apple.position)
        occupied.add(stone.position)
        occupied.add(poison.position)
        return occupied

    def game_over():
        nonlocal fps
        fps = snake.reset()
        occupied = get_full_positions()
        apple.randomize_position(occupied)
        stone.randomize_position(occupied)
        poison.randomize_position(occupied)

    while True:
        clock.tick(fps)
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            fps += 0.5
            apple.randomize_position(get_full_positions())

        elif snake.get_head_position() == poison.position:
            fps -= 0.5
            if fps < 3:
                game_over()
            else:
                poison.randomize_position(get_full_positions())

        elif snake.get_head_position() == stone.position:
            game_over()

        if snake.length < 1:
            game_over()

        if snake.get_head_position() in snake.positions[4:]:
            game_over()

        screen.fill(BOARD_BACKGROUND_COLOR)
        stone.draw()
        apple.draw()
        snake.draw()
        poison.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
