import curses

class Snake:
    def __init__(self, screen):
        self.screen = screen
        self.x, self.y = [10,11,12,13],[10,10,10,10]
        self.key = None
        self.direction = curses.KEY_RIGHT
        self.parts = [" "," "," "," "]

    def move(self):
        #Downolad x,y head of snake
        head_x = self.x[0]
        head_y = self.y[0]
        #Change direction
        if self.direction == curses.KEY_LEFT:
                head_x -= 1
        elif self.direction == curses.KEY_RIGHT:
                head_x += 1
        elif self.direction == curses.KEY_UP:
                head_y -= 1
        elif self.direction == curses.KEY_DOWN:
                head_y += 1
        #Add to list new_head
        self.x.insert(0, head_x)
        self.y.insert(0, head_y)
        #Delete tail of snake
        self.x.pop()
        self.y.pop()

    def draw(self, neon_green, score_panel, blink_timer):
        self.screen.erase()

        score_panel(neon_green, blink_timer)
        self.screen.attron(neon_green)
        self.screen.bkgd(neon_green)
        self.screen.border()
        #Draw the snake
        try:
            for index, element in enumerate(self.parts):
                self.screen.addstr(self.y[index], self.x[index], element, curses.A_REVERSE)
                curses.napms(10)
        except curses.error:
            pass

        self.screen.attroff(neon_green)
        self.screen.refresh()

    def control_mechanism(self, neon_green, main_src, score_panel):
        main_src.nodelay(True)
        blink_timer = 0

        while True:
            key = main_src.getch()

            if key != -1:
                self.direction = key

            self.move()

            self.draw(neon_green, score_panel, blink_timer)

            blink_timer += 1 #for blink line in board.score_panel

            if self.direction in [curses.KEY_LEFT, curses.KEY_RIGHT]:
                curses.napms(150)
            else:
                curses.napms(250)