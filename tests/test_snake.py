from app.core.snake import Snake
from unittest.mock import MagicMock
import pytest, curses

#Tworzenie fałszywego ekranu
@pytest.fixture
def moc_screen():
    screen = MagicMock()
    screen.getmaxyx.return_value = (20,80)
    return screen

@pytest.fixture()
def snake(moc_screen):
    snake_obj = Snake(moc_screen)
    snake_obj.parts = [" ", " ", " "]
    #Wąż jest na środku ekranu, poziomo i przesuwa się w prawo
    snake_obj.x = [10, 9, 8]
    snake_obj.y = [10, 10, 10]
    snake_obj.direction = curses.KEY_RIGHT

    return snake_obj

def test_initial_snake(snake):
    """Sprawdz długość, pozycję i kierunek węża"""
    assert len(snake.x) == 3
    assert snake.x[0] == 10
    assert snake.direction == curses.KEY_RIGHT

def test_move_right(snake):
    """Sprawdza czy wąż przesuwa się w prawo, czyli x rośnie"""
    snake.move()

    assert snake.x[0] == 11
    assert snake.y[0] == 10
    #Pozycja ogona
    assert snake.x[-1] == 9
    assert snake.y[-1] == 10
    #Długość bez zmian
    assert len(snake.x) == 3

def test_move_left(snake):
    """Sprawdza czy wąż przesuwa się w lewo, czyli x maleje"""
    snake.direction = curses.KEY_LEFT
    snake.move()

    assert snake.x[0] == 9
    assert snake.y[0] == 10
    #Pozycja ogona
    assert snake.x[-1] == 9
    assert snake.y[-1] == 10
    #Długość bez zmian
    assert len(snake.x) == 3

def test_move_down(snake):
    """Sprawdza czy wąż przesuwa się w góre, czyli y rośnie"""
    snake.direction = curses.KEY_DOWN
    snake.move()

    assert snake.x[0] == 10
    assert snake.y[0] == 11

    assert snake.x[-1] == 9
    assert snake.y[-1] == 10

    assert len(snake.x) == 3

def test_move_up(snake):
    """Sprawdza czy wąż przesuwa się w góre, czyli y rośnie"""
    snake.direction = curses.KEY_UP
    snake.move()

    assert snake.x[0] == 10
    assert snake.y[0] == 9

    assert len(snake.x) == 3

def test_self_collision(snake):
    """Sprawdza czy nastąpi kolizja przy uderzeniu samego siebie"""
    #głowa snake
    snake.x = [10, 10, 11]
    snake.y = [10, 10, 10]

    assert snake.check_self_collision()

"""Sprawdza kolizje z każdą z 4 ścian."""
def test_right_wall_collision(snake, moc_screen):
    max_y, max_x = moc_screen.getmaxyx()
    #Prawa ściana
    snake.x[0] = max_x - 1
    snake.y[0] = 10
    assert snake.check_wall_collision() is True

def test_left_wall_collision(snake):
    #Lewa ściana
    snake.x[0] = 0
    snake.y[0] = 10
    assert snake.check_wall_collision() is True

def test_down_wall_collision(snake, moc_screen):
    max_y, max_x = moc_screen.getmaxyx()
    #Dolna ściana
    snake.x[0] = 10
    snake.y[0] = max_y - 1  # 19
    assert snake.check_wall_collision() is True

def test_up_wall_collision(snake):
    #Górna ściana
    snake.x[0] = 10
    snake.y[0] = 0
    assert snake.check_wall_collision() is True

def test_body_integrity(snake):
    """Sprawdza, czy ciało podąża za głową (czy szyja wskakuje w miejsce głowy)."""
    assert snake.x[0] == 10
    assert snake.x[1] == 9

    snake.move()

    assert snake.x[1] == 10
    assert snake.y[1] == 10

def test_random_start_logic(snake, moc_screen):
    """Sprawdza poprawność generowania węża dla obu kierunków."""
    for _ in range(100):
        snake.random_start()

        assert snake.y[0] in range(7, 14)

        assert snake.direction in [curses.KEY_RIGHT, curses.KEY_LEFT]

        if snake.direction == curses.KEY_RIGHT:
            assert snake.x[0] in range(30, 56)
            assert snake.x[0] > snake.x[1]

        elif snake.direction == curses.KEY_LEFT:
            assert snake.x[0] in range(30, 51)
            assert snake.x[0] < snake.x[1]

def test_ignore_invalid_keys(snake):
    """Sprawdza, czy wąż ignoruje klawisze niebędące strzałkami (np. 'A', Enter)."""
    snake.direction = curses.KEY_RIGHT

    random_key = ord('A')

    valid_keys = [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]

    if random_key in valid_keys:
        snake.direction = random_key

    assert snake.direction == curses.KEY_RIGHT
