import pygame
import random
pygame.init()
# Variables:
run = True
w_hight = 857
w_width = 1170
temp = 0
score_name = ''
clock = pygame.time.Clock()
the_grid = pygame.display.set_mode((700, 800))
pygame.display.set_caption('Python on python, by Dah')
text_font = pygame.font.SysFont('Times New Roman', 20)
score_font = pygame.font.SysFont('Times New Roman', 33)
# main loop
speeding_up = 0
# count food to trigger bonuses
humgry = False
# Food trigger


# the Python
# loading images
bg = pygame.image.load('unnamed.RES')
logo = pygame.image.load('logo.RES')
head = pygame.image.load('snake_head.RES')
tail = pygame.image.load('snake_tail.RES')
turn = pygame.image.load('snake_turn.RES')
dont_hit_yourself = pygame.image.load('hit_tail.RES')
dont_hit_wall = pygame.image.load('hit_wall.RES')
# setting up the clock


class snake:
    def __init__(self, x, y):
        self.facing = 'up'
        self.x = x
        self.y = y
        self.color = (255, 202, 24)
        self.rad = 26
        self.speed = 3
        self.alive = 1
        self.tail = 4
        self.bonus = 10
        self.score = 0
        self.turn = []
        self.position = [(w_width/2, w_hight/2)]

    def draw_snake(self, the_grid):
        # Body
        if self.alive > 0:
            self.position.insert(0, (self.x, self.y))
            while len(self.position) > self.tail*5:
                del self.position[-1]
        pygame.draw.lines(the_grid, (0, 0, 0), False, self.position, width=22)
        pygame.draw.lines(the_grid, self.color, False, self.position, width=20)
        # tail
        if self.position[-2][1] == self.position[-1][1]:
            if self.position[-2][0] < self.position[-1][0]:
                tailposition = pygame.transform.rotate(tail, 90)
                the_grid.blit(tailposition, (self.position[-2][0], self.position[-2][1]-10))
            else:
                tailposition = pygame.transform.rotate(tail, 270)
                the_grid.blit(tailposition, (self.position[-2][0]-37, self.position[-2][1]-10))
        else:
            if self.position[-2][1] < self.position[-1][1]:
                tailposition = tail
                the_grid.blit(tailposition, (self.position[-2][0]-10, self.position[-2][1]))
            else:
                tailposition = pygame.transform.rotate(tail, 180)
                the_grid.blit(tailposition, (self.position[-2][0]-10, self.position[-2][1]-37))
        # turn animation
        for t in self.turn:
            if t[0] == 'rd' or t[0] == 'ul':
                the_grid.blit(turn, (t[1]-11, t[2]-11))
            elif t[0] == 'ru' or t[0] == 'dl':
                turnposition = pygame.transform.rotate(turn, 270)
                the_grid.blit(turnposition, (t[1]-11, t[2]-11))
            elif t[0] == 'ur' or t[0] == 'ld':
                turnposition = pygame.transform.rotate(turn, 90)
                the_grid.blit(turnposition, (t[1]-11, t[2]-11))
            else:
                turnposition = pygame.transform.rotate(turn, 180)
                the_grid.blit(turnposition, (t[1]-11, t[2]-11))
        if self.turn and self.turn[-1][1] == self.position[-2][0] and self.turn[-1][2] == self.position[-2][1]:
            del self.turn[-1]
        # it will give u head
        if self.facing == 'up':
            headposition = head
        elif self.facing == 'down':
            headposition = pygame.transform.flip(head, False, True)
        elif self.facing == 'left':
            headposition = pygame.transform.rotate(head, 90)
        else:
            headposition = pygame.transform.rotate(head, 270)
        the_grid.blit(headposition, (self.x-20, self.y-20))

    def control_snake(self):
        global temp
        key_dir = pygame.key.get_pressed()
        if key_dir[pygame.K_RIGHT] and self.facing != 'left' and self.facing != 'right':
            if temp < pygame.time.get_ticks():
                self.turn.insert(0, ('ur' if self.facing == 'up' else 'dr', self.x, self.y))
                self.facing = 'right'
                temp = pygame.time.get_ticks()+250
        if key_dir[pygame.K_LEFT] and self.facing != 'right' and self.facing != 'left':
            if temp < pygame.time.get_ticks():
                self.turn.insert(0, ('ul' if self.facing == 'up' else 'dl', self.x, self.y))
                self.facing = 'left'
                temp = pygame.time.get_ticks()+250
        if key_dir[pygame.K_UP] and self.facing != 'down' and self.facing != 'up':
            if temp < pygame.time.get_ticks():
                self.turn.insert(0, ('lu' if self.facing == 'left' else 'ru', self.x, self.y))
                self.facing = 'up'
                temp = pygame.time.get_ticks()+250
        if key_dir[pygame.K_DOWN] and self.facing != 'up' and self.facing != 'down':
            if temp < pygame.time.get_ticks():
                self.turn.insert(0, ('ld' if self.facing == 'left' else 'rd', self.x, self.y))
                self.facing = 'down'
                temp = pygame.time.get_ticks()+250

    def grow(self, the_grid):
        self.tail += 1
        global speeding_up
        global humgry
        humgry = False
        speeding_up += 1
        self.score += self.bonus
        if speeding_up == 10:
            speeding_up = 0
            python.bonus += 5
            if python.speed < 10:
                python.speed += 0.5

    def colision(self, the_grid):
        for t in self.position[25:-2]:
            if abs(t[0] - self.x) < 20 and abs(t[1] - self.y) < 20:
                self.alive -= 1
                self.speed = 0
                pygame.draw.rect(the_grid, (255, 255, 255), (250, 157, 600, 500), border_radius=20)
                pygame.draw.rect(the_grid, (0, 0, 0), (250, 157, 600, 500),
                                 width=5, border_radius=20)
                the_grid.blit(dont_hit_yourself, (445, 210))
                record = score_font.render(str(self.score)+' score points!', True, (0, 0, 0))
                game_over = score_font.render('GAME OVER!', True, (0, 0, 0))
                restart = text_font.render(
                    'Press SPACE to restart or ESC to Exit', False, (30, 30, 30))
                the_grid.blit(game_over, (450, 530))
                the_grid.blit(record, (450, 590))
                the_grid.blit(restart, (400, 630))
                key_dir = pygame.key.get_pressed()
                if key_dir[pygame.K_ESCAPE]:
                    scoring(score_name, self.score)
                    pygame.quit()
                if key_dir[pygame.K_SPACE]:
                    scoring(score_name, self.score)
                    highscore()

        if self.x <= 62 or self.x >= w_width-62 or self.y <= 62 or self.y >= w_hight-112:
            self.alive -= 1
            self.speed = 0
            pygame.draw.rect(the_grid, (255, 255, 255), (250, 157, 600, 500), border_radius=20)
            pygame.draw.rect(the_grid, (0, 0, 0), (250, 157, 600, 500), width=5, border_radius=20)
            the_grid.blit(dont_hit_wall, (440, 180))
            record = score_font.render(str(self.score)+' score points!', True, (0, 0, 0))
            game_over = score_font.render('GAME OVER!', True, (0, 0, 0))
            restart = text_font.render('Press SPACE to restart or ESC to Exit', False, (30, 30, 30))
            the_grid.blit(game_over, (450, 530))
            the_grid.blit(record, (450, 590))
            the_grid.blit(restart, (400, 630))
            key_dir = pygame.key.get_pressed()
            if key_dir[pygame.K_ESCAPE]:
                scoring(score_name, self.score)
                pygame.quit()
            if key_dir[pygame.K_SPACE]:
                scoring(score_name, self.score)
                highscore()

    def score_board(self, the_grid):
        score = score_font.render('Score: ' + str(self.score), True, (255, 0, 0))
        life = score_font.render('Bonus points: ' + str(self.bonus-10), False, (255, 0, 0))
        pygame.draw.rect(the_grid, (255, 255, 0), (100, 770, 300, 80), border_radius=7)
        pygame.draw.rect(the_grid, (10, 10, 0), (100, 770, 300, 80), width=3, border_radius=7)
        the_grid.blit(score, (120, 773))
        the_grid.blit(life, (120, 803))


class food:
    def __init__(self):
        self.rad = 15
        self.color = (255, 0, 0)
        self.x = ''
        self.y = ''

    def draw_food(self, the_grid):
        global humgry
        if humgry is False:
            food.new_food(the_grid)
        pygame.draw.circle(the_grid, self.color, (self.x, self.y), self.rad)
        pygame.draw.circle(the_grid, (0, 0, 0), (self.x, self.y), self.rad, width=2)
        if abs(python.x-self.x) <= 20 and abs(python.y - self.y) <= 20:
            python.grow(the_grid)

    def new_food(self, the_grid):
        global humgry
        humgry = True
        self.x = random.randrange(70, w_width-70)
        self.y = random.randrange(70, w_hight-120)


food = food()
# single instance, could be used to populate different type of foods


# FUNCTIONS

def highscore():
    global run
    run = False
    try:
        with open('data.wb', 'r') as score_safe:
            score_t = score_safe.read().split('_')
            del score_t[-1]
            score_t = score_t[0:9]
            names = []
            points = []
            position = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
            for t in score_t:
                temp = t.split(':')
                names.append(temp[0])
                points.append(temp[1])
            counter = 0
            for t in names:
                position[counter] = score_font.render(
                    position[counter] + '. ' + names[counter], False, (230, 14, 14))
                names[counter] = score_font.render(points[counter], False, (230, 14, 14))
                counter += 1
            highscore = True
            titel = score_font.render('HIGH SCORES:', True, (255, 0, 0))
            text = text_font.render(
                'Press SPACE to proceed or ESC to quit!', True, (200, 100, 9))
            while highscore:
                clock.tick(30)
                the_grid.fill((250, 250, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        highscore = 0
                key_dir = pygame.key.get_pressed()
                if key_dir[pygame.K_SPACE] or key_dir[pygame.K_RETURN]:
                    highscore = False
                    startgame()
                if key_dir[pygame.K_ESCAPE]:
                    highscore = False
                the_grid.blit(titel, (50, 50))
                the_grid.blit(text, (50, 700))
                counter = 0
                for t in names:
                    the_grid.blit(position[counter], (100, 100 + counter*40))
                    the_grid.blit(names[counter], (400, 100 + counter*40))
                    counter += 1
                pygame.display.update()

    except FileNotFoundError:
        score_safe = open('data.wb', 'x')
        score_safe.close()
    startgame()


def startgame():
    the_grid = pygame.display.set_mode((700, 650))
    starter = True
    enter_ntext = score_font.render('Enter name: ', True, (250, 0, 0))
    global python
    global score_name
    python = ''
    pygame.key.set_repeat()
    while starter:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                starter = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    starter = False
                elif event.key == pygame.K_RETURN:
                    score_name = python
                    python = snake(w_width/2, w_hight/2)
                    starter = False
                    main()
                elif event.key == pygame.K_BACKSPACE:
                    python = python[:-1]
                else:
                    python += event.unicode
        txt_surface = score_font.render(python, True, (0, 0, 0))
        the_grid.fill((250, 250, 0))
        the_grid.blit(logo, (-50, 50))
        the_grid.blit(enter_ntext, (80, 500))
        pygame.draw.rect(the_grid, (255, 0, 0), (75, 550, 400, 60), width=5, border_radius=20)
        the_grid.blit(txt_surface, (95, 560))
        pygame.display.update()


def scoring(name, scorepoints):
    score_list = []
    print(name)
    print(scorepoints)
    with open('data.wb', 'r') as score_safe:
        score_t = score_safe.read().split('_')
        del score_t[-1]
        # removing the final _ to evade problems while reading and splitting
        try:
            for t in score_t:
                temp = t.split(':')
                score_list.append((temp[0], temp[1]))
        except IndexError:
            pass
    score_safe = open('data.wb', 'w')
    num = 0
    for t in score_list:
        if int(t[1]) > scorepoints:
            num += 1
    print(num)
    score_list.insert(num, (name, scorepoints))
    for t in score_list:
        t = str(t[0])+':'+str(t[1])+'_'
        score_safe.write(t)


def redraw_the_grid():
    # continious motion
    if python.facing == 'right':
        python.x += python.speed
    elif python.facing == 'left':
        python.x -= python.speed
    elif python.facing == 'up':
        python.y -= python.speed
    elif python.facing == 'down':
        python.y += python.speed
    # pretty
    the_grid.blit(bg, (0, 0))
    python.draw_snake(the_grid)
    food.draw_food(the_grid)
    # colision of tail
    python.colision(the_grid)
    # score board
    python.score_board(the_grid)
    # update display
    pygame.display.update()


# mainloop
def main():
    global the_grid
    the_grid = pygame.display.set_mode((w_width, w_hight))
    global run
    run = True
    pygame.key.set_repeat(10)
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            python.control_snake()

        redraw_the_grid()


highscore()
pygame.quit()
