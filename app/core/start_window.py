import curses

class WelcomeWindow:
    """Draw welcome window with huge title SNAKE"""
    def __init__(self, screen, neon_green):
        self.snake_title = [
                    " █████   ██   █    ██    ██  █  ██████",
                    "█        █ █  █   █  █   █ █    █     ",
                    " █████   █  █ █   ████   ██     █████ ",
                    "     █   █   ██  █    █  █ █    █     ",
                    "█████    █    █  █    █  █  ██  ██████"
                    ]

        self.screen = screen
        self.neon_green = neon_green
        self.line_title = 6
        self.screen.refresh()

    def start_window(self):
        blink_timer = 0
        self.screen.nodelay(True)
        while True:
            self.screen.erase()

            #Draw the title
            list(map(lambda line:
                     self.screen.addstr(self.line_title + self.snake_title.index(line),
                                        22, line), self.snake_title))

            self.screen.attron(self.neon_green)
            self.screen.bkgd(self.neon_green)
            self.screen.border()

            blink_timer += 1
            if blink_timer % 10 < 5:
                self.screen.addstr(14, 28,"PRESS ENTER TO START GAME",
                              curses.A_BOLD)
            else: pass

            self.screen.attroff(self.neon_green)
            self.screen.refresh()
            curses.napms(150)

            key = self.screen.getch()

            if key in [10, 13, curses.KEY_ENTER]:
                self.screen.clear()
                self.screen.refresh()
                self.screen.nodelay(False)
                break