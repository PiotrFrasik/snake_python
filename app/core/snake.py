import curses, random
from .game_over import GameOver
from .apples import Apples

class Snake:
    def __init__(self, screen):
        self.screen = screen
        self.x, self.y, self.parts  = [], [], []
        self.score = 0
        self.direction = None
        self.old_direction = None
        self.apples = Apples(self.screen)

    def random_start(self):
        list_key = [curses.KEY_RIGHT, curses.KEY_LEFT]
        #first move
        self.direction = list_key[random.randint(0, len(list_key) - 1)]

        self.parts = list(" " * random.randint(3,5)) #snake length

        #Generate x,y snake: x increments by 1, y remains the same
        start_x = random.randint(10,30)
        start_y = random.randint(3,10)
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
        head = (self.x[0], self.y[0])
        part_body = list(zip(self.x[1:], self.y[1:]))

        if head in part_body:
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
        self.screen.attron(neon_green)
        self.screen.bkgd(neon_green)
        self.screen.border()
        #Draw the snake
        for index, element in enumerate(self.parts):
            self.screen.addstr(self.y[index], self.x[index], element, curses.A_REVERSE)
        self.screen.attroff(neon_green)

        #Draw apples in random place
        if [self.x[0], self.y[0]] == self.apples.return_xy():
            self.parts.append(" ")
            self.x.append(self.x[-1])
            self.y.append(self.y[-1])

            self.score += 3
            self.apples.random_generate()
            self.apples.draw(neon_green)
        else:
            self.apples.draw(neon_green)

        #Draw score panel
        score_panel(neon_green, blink_timer, self.score)

        self.screen.refresh()

    def check_new_direction(self, key):
        if (key == curses.KEY_LEFT and self.direction == curses.KEY_RIGHT) or \
                (key == curses.KEY_RIGHT and self.direction == curses.KEY_LEFT) or \
                (key == curses.KEY_UP and self.direction == curses.KEY_DOWN) or \
                (key == curses.KEY_DOWN and self.direction == curses.KEY_UP):
            pass
        else:
            self.direction = key

    def control_mechanism(self, neon_green, main_src, score_panel, draw_board):
        main_src.nodelay(True)
        blink_timer = 0
        self.score = 0

        self.random_start()
        self.apples.random_generate()

        while True:

            if self.check_wall_collision() or self.check_self_collision(): #init game_over
                GameOver(self.screen, main_src, neon_green, draw_board).draw()
            else:
                key = main_src.getch()

                if key != -1:

                    self.check_new_direction(key)

                self.move()

                self.draw(neon_green, score_panel, blink_timer)

                blink_timer += 1  #for blink line in board.score_panel
                #change speed
                if self.direction in [curses.KEY_LEFT, curses.KEY_RIGHT]:
                    curses.napms(100)
                else:
                    curses.napms(160)