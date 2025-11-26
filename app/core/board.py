import curses, time
from core.start_window import WelcomeWindow
from core.snake import Snake


class BoardGame:
    """Draw the board game window for snake and apples"""
    def __init__(self, screen):
        self.rows = screen.getmaxyx()[0]
        self.cols = screen.getmaxyx()[1]

        self.screen = screen
        self.upper_window = curses.newwin(3, self.cols, 0, 0)
        self.snake_window = curses.newwin(self.rows-3, self.cols,
                                         3,0)

        self.snake = Snake(self.snake_window)

    def score_panel(self,neon_green, blink_timer):
        self.upper_window.erase()

        #Draw the score and apple count
        self.upper_window.attron(neon_green)
        self.upper_window.bkgd(neon_green)
        self.upper_window.addstr(1, 1, f"SCORE: 0000", curses.A_BOLD)

        if blink_timer % 10 < 5: #Blink line
            self.upper_window.addstr(1, 35, "S N A K E", curses.A_BOLD)
        else: pass

        #self.upper_window.addstr(1, self.cols - 4, f"ó00", curses.A_BOLD)
        self.upper_window.border()
        self.upper_window.attroff(neon_green)
        self.upper_window.refresh()

    def snake_panel(self,neon_green):
        #Draw the game board
        self.snake_window.attron(neon_green)
        self.snake_window.bkgd(neon_green)
        self.snake_window.border()
        self.snake_window.attroff(neon_green)
        self.snake_window.refresh()

    def draw(self, neon_green):
        self.snake.control_mechanism(neon_green, self.screen,self.score_panel, self)




