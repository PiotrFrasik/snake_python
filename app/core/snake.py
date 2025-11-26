import curses, random
from core.game_over import GameOver

class Snake:
    def __init__(self, screen):
        self.screen = screen
        self.x, self.y, self.parts  = [], [], []
        self.direction = curses.KEY_RIGHT

    def random_start(self):
        list_key = [curses.KEY_RIGHT, curses.KEY_LEFT]
        self.direction = list_key[random.randint(0, len(list_key) - 1)]  #first move

        self.parts = list(" " * random.randint(3,5)) #snake length

        #Generate x,y snake: x increments by 1, y remains the same
        start_x = random.randint(30,50)
        start_y = random.randint(7,13)
        self.x, self.y = (list(range(start_x, start_x + len(self.parts)))
                              ,[start_y]*len(self.parts))

        if self.direction == curses.KEY_RIGHT:
            self.x.reverse()

    def check_wall_collision(self):
        if self.x[0] in [0,self.screen.getmaxyx()[1] - 1] or self.y[0] in [0,self.screen.getmaxyx()[0] - 1]:
            return True
        else:
            return False

    def check_self_collision(self):
        if self.x[0] in self.x[1:] and self.y[0] in self.y[1:]:
            return True
        else:
            return False

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

    def control_mechanism(self, neon_green, main_src, score_panel, draw_board):
        main_src.nodelay(True)
        blink_timer = 0
        self.random_start()
        while True:

            if self.check_wall_collision() or self.check_self_collision(): #init game_over
                GameOver(self.screen, main_src, neon_green, draw_board).draw()
                #raise Exception("End of game")
            else:
                key = main_src.getch()

                if key != -1:
                    self.direction = key

                self.move()

                self.draw(neon_green, score_panel, blink_timer)

                blink_timer += 1 #for blink line in board.score_panel

                if self.direction in [curses.KEY_LEFT, curses.KEY_RIGHT]:
                    curses.napms(150)
                else:
                    curses.napms(240)