import curses, random

class Apples:
    def __init__(self, screen_snake):
        self.screen_snake = screen_snake
        self.xy_apple = []
        self.xy_max = self.screen_snake.getmaxyx()

    def random_generate(self):
        self.xy_apple = [random.randint(2, self.xy_max[1]-2),
                         random.randint(2, self.xy_max[0]-2)]

    def return_xy(self):
        return self.xy_apple

    def draw(self, neon_green):
        self.screen_snake.addstr(self.xy_apple[1], self.xy_apple[0],
                                 "ó", curses.A_BOLD | neon_green)