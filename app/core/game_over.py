import curses

class GameOver:
    def __init__(self, screen_snake, main_src, neon_green, draw_board):
        self.screen_snake = screen_snake
        self.main_src = main_src
        self.neon_green = neon_green
        self.draw_board = draw_board

    def draw_title(self):
        game_over_title = [
            " ██████   █████   ███    ███ ███████    ██████  ██    ██ ███████ ██████ ",
            "██       ██   ██  ████  ████ ██        ██    ██ ██    ██ ██      ██   ██",
            "██   ███ ███████  ██ ████ ██ █████     ██    ██ ██    ██ █████   ██████ ",
            "██    ██ ██   ██  ██  ██  ██ ██        ██    ██  ██  ██  ██      ██   ██",
            " ██████  ██   ██  ██      ██ ███████    ██████    ████   ███████ ██   ██"
        ]

        self.main_src.nodelay(False)

        self.screen_snake.attron(self.neon_green)
        list(map(lambda line:
                 self.screen_snake.addstr(5 + game_over_title.index(line),
                                          4, line), game_over_title))
        self.screen_snake.addstr(13, 25, "PRESS ENTER TO START NEW GAME", curses.A_BOLD)
        self.screen_snake.attroff(self.neon_green)

        self.screen_snake.refresh()

    def new_game(self):
        self.main_src.nodelay(True)
        if self.screen_snake.getch() in [10, 13, curses.KEY_ENTER]:
            self.draw_board.draw(self.neon_green)

    def draw(self):
        self.draw_title()
        self.new_game()