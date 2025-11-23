import curses, time

from core.board import BoardGame

#80x20
class StartGame:
    def __init__(self):
        self.screen = curses.initscr()

        #curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        #self.neon_green = curses.color_pair(1)

        self.board = BoardGame(self.screen)

    def main(self, stdscr):
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        neon_green = curses.color_pair(1)

        self.board.draw(neon_green)
        time.sleep(5)

        stdscr.refresh()
        stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(StartGame().main)