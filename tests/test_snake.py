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

#Testy jednostkowe
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

def test_move_up(snake):
    """Sprawdza czy wąż przesuwa się w góre, czyli y rośnie"""
    snake.direction = curses.KEY_UP
    snake.move()

    assert snake.x[0] == 10
    assert snake.y[0] == 9

    assert len(snake.x) == 3

def test_wall_collision(snake):
    """Sprawdza czy nastąpi kolizja przy uderzeniu w scaine"""
    snake.x[0] = 0
    assert snake.check_wall_collision() is True


def test_self_collision(snake):
    """Sprawdza czy nastąpi kolizja przy uderzeniu samego siebie"""
    #głowa snake
    snake.x = [10, 10, 11]
    snake.y = [10, 10, 10]

    assert snake.check_self_collision()




