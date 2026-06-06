import sys
from random import randint

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
GRID_LIST = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

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

# Константы для значений по умолчанию
DEFAULT_BODY_COLOR = SNAKE_COLOR
DEFAULT_FPS = 5

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
            # Получаем направление, которое будет применено
            next_dir = game_object.next_direction or game_object.direction

            if event.key == pg.K_UP and next_dir != DOWN:
                game_object.update_direction(UP)
            elif event.key == pg.K_DOWN and next_dir != UP:
                game_object.update_direction(DOWN)
            elif event.key == pg.K_LEFT and next_dir != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and next_dir != LEFT:
                game_object.update_direction(RIGHT)
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                sys.exit()


class GameObject:
    """Основной класс от которого наследуются все остальные предметы в игре."""

    def __init__(self, position=GRID_LIST, body_color=DEFAULT_BODY_COLOR):
        self.position = position
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

    def _clear_grid_cell(self, position):
        """Затирает одну ячейку игрового поля цветом фона."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)


class Apple(GameObject):
    """Класс предмета яблоко."""

    def __init__(self, occupied=None, position=None, body_color=APPLE_COLOR):
        super().__init__(position, body_color)
        self.randomize_position(occupied)

    def randomize_position(self, full_positions=None):
        """Выдаёт случайные координаты для спавна яблока."""
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (x, y)
            if full_positions is None or (x, y) not in full_positions:
                break

    def draw(self):
        """Рисует яблоко в виде квадрата."""
        self._draw_grid_cell(self.position, self.body_color)


class Snake(GameObject):
    """Класс змейки"""

    def __init__(self):
        super().__init__()

        # длина змейки
        self.length = 1
        # список сегментов
        self.positions = [self.position]
        # текущее направление змейки
        self.direction = RIGHT
        # следующее направление, выбранное пользователем
        self.next_direction = None
        # последняя удалённая позиция
        self.last = None

    def move(self):
        """Определяем движение змейки."""
        # Применяем следующее направление, если оно задано
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

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
            self.last = self.positions.pop()
        else:
            self.last = None

    def reset(self):
        """Сброс настроек змейки к начальному состоянию."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    # Метод draw класса Snake
    def draw(self):
        """Рисует змейку."""
        # Затираем хвост, если он есть
        if self.last:
            self._clear_grid_cell(self.last)
        # Отрисовываем голову
        head_position = self.get_head_position()
        self._draw_grid_cell(head_position, self.body_color)

    def get_head_position(self):
        """Получаем позицию головы(первого элемента)."""
        return self.positions[0]

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self, new_direction):
        """Обновляет направление движения змейки."""
        self.next_direction = new_direction


def main():
    """Запускает игру «Змейка» и управляет игровым циклом.

    Инициализирует Pygame, создаёт объекты змейки и яблока,
    затем запускает бесконечный цикл игры с обработкой ввода,
    обновлением состояния и отрисовкой.
    """
    pg.init()

    # Начальное заполнение экрана
    screen.fill(BOARD_BACKGROUND_COLOR)

    snake = Snake()
    # Отрисовываем начальную змейку
    snake.draw()

    # Получаем начальные занятые позиции (только змейка)
    occupied = set(snake.positions)

    # Создаём яблоко
    apple = Apple(occupied)
    occupied.add(apple.position)

    # Создаём камень
    stone = Apple(occupied, body_color=STONE_COLOR)
    occupied.add(stone.position)

    # Создаём яд
    poison = Apple(occupied, body_color=POISON_COLOR)
    occupied.add(poison.position)

    # Отрисовываем начальные объекты
    apple.draw()
    stone.draw()
    poison.draw()

    # Скорость игры:
    fps = DEFAULT_FPS

    def get_full_positions():
        """Собирает все занятые клетки (змейка + все предметы)."""
        occupied = set(snake.positions)
        occupied.add(apple.position)
        occupied.add(stone.position)
        occupied.add(poison.position)
        return occupied

    def game_over():
        nonlocal fps
        fps = DEFAULT_FPS
        snake.reset()
        screen.fill(BOARD_BACKGROUND_COLOR)

        # Начинаем с позиций змейки
        occupied = set(snake.positions)

        # Пересоздаём яблоко
        apple.randomize_position(occupied)
        occupied.add(apple.position)

        # Пересоздаём камень
        stone.randomize_position(occupied)
        occupied.add(stone.position)

        # Пересоздаём яд
        poison.randomize_position(occupied)
        occupied.add(poison.position)

        apple.draw()
        stone.draw()
        poison.draw()

    while True:
        clock.tick(fps)
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            fps += 0.5
            # Затираем старое яблоко и рисуем новое
            apple._clear_grid_cell(apple.position)
            apple.randomize_position(get_full_positions())
            apple.draw()

        elif snake.get_head_position() == poison.position:
            fps -= 0.5
            if fps < 3:
                game_over()
            else:
                # Затираем старый яд и рисуем новый
                poison._clear_grid_cell(poison.position)
                poison.randomize_position(get_full_positions())
                poison.draw()

        elif snake.get_head_position() == stone.position:
            game_over()

        if snake.length < 1:
            game_over()

        if snake.get_head_position() in snake.positions[4:]:
            game_over()

        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
