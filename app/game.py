import curses, time

from core.board import BoardGame
from core.start_window import WelcomeWindow

class StartGame:
    def __init__(self):
        self.screen = curses.initscr()
        self.board = BoardGame(self.screen)

    def check_size_screen(self):
        rows, cols = self.screen.getmaxyx()
        # terminal size validation
        if not (rows == 20 and cols == 80):
            raise Exception("Terminal size must be exactly 20 and 80 (rows x cols).\n"
                            f"Current size: {rows} x {cols}.")

    def main(self, stdscr):
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        neon_green = curses.color_pair(1)

        self.check_size_screen()

        start_window = WelcomeWindow(self.screen, neon_green)

        curses.curs_set(0) #remove mouse cursor

        start_window.start_window()

        self.board.draw(neon_green)

        time.sleep(5)


if __name__ == "__main__":
    curses.wrapper(StartGame().main)