import turtle, random


class BackGround(turtle.Turtle):  # draw other graph except numbers
    def __init__(self):
        super().__init__()
        self.penup()
        self.ht()

    def draw_block(self):
        self.shape('background.gif')  # draw background
        for i in allpos:
            self.goto(i)
            self.stamp()
        self.color('yellow', 'yellow')  # draw separate line
        self.goto(-215, 120)
        self.begin_fill()
        self.goto(215, 120)
        self.goto(215, 110)
        self.goto(-215, 110)
        self.end_fill()
        self.shape('title.gif')
        self.goto(-125, 210)
        self.stamp()
        self.shape('score.gif')
        self.goto(125, 245)
        self.stamp()
        self.shape('top-score.gif')
        self.goto(125, 170)
        self.stamp()

    def judge(self):  # sign of game_over or 2048 achieved
        global flag_win, flag_win_lose_text
        self.color('blue')
        judge = 0  # judge if there is space to move
        for i in block_dic.values():
            for j in block_dic.values():
                if i.num == 0 or i.num == j.num and i.distance(j) == 100:
                    judge += 1
        if judge == 0:  # impossible to move, gameover
            self.write('     GAME OVER\npress space to restart', align='center', font=('Arial', 30, 'bold'))
            flag_win_lose_text = False
        if flag_win is True:  # only judge the 2048 goal once
            for k in block_dic.values():
                if k.num == 2048:  # win
                    flag_win = False
                    self.write('     2048 achieved\npress enter to continue', align='center', font=('Arial', 30, 'bold'))
                    flag_win_lose_text = False

    def win_lose_clear(self):  # cleaner for marked word of win or lose
        global flag_win_lose_text
        self.clear()
        flag_win_lose_text = True

    def show_score(self):  # current score and maximum score
        global score, top_score
        if score > top_score:
            top_score = score
            with open('.\\score.txt', 'w') as f:
                f.write(f'{top_score}')
        self.color('white')
        self.goto(125, 210)
        self.clear()
        self.write(f'{score}', align='center', font=('Arial', 20, 'bold'))
        self.goto(125, 135)
        self.write(f'{top_score}', align='center', font=('Arial', 20, 'bold'))


class Block(turtle.Turtle):  # number boxes
    def __init__(self):
        super().__init__()
        self.ht()
        self.penup()
        self.num = 0

    def draw(self):
        self.clear()
        dic_draw = {2: '#eee6db', 4: '#efe0cd', 8: '#f5af7b',
                    16: '#fb9660', 32: '#f57d5a', 64: '#f95c3d',
                    128: '#eccc75', 256: '#eece61', 512: '#efc853',
                    1024: '#ebc53c', 2048: '#eec430', 4096: '#aeb879',
                    8192: '#aab767', 16384: '#a6b74f'}
        if self.num > 0:  # value more than 0, draw the box
            self.color(f'{dic_draw[self.num]}')  # choose color from the list
            self.begin_fill()
            self.goto(self.xcor()+48, self.ycor()+48)
            self.goto(self.xcor()-96, self.ycor())
            self.goto(self.xcor(), self.ycor()-96)
            self.goto(self.xcor()+96, self.ycor())
            self.goto(self.xcor(), self.ycor()+96)
            self.end_fill()
            self.goto(self.xcor()-48, self.ycor()-68)
            if self.num > 4:  # choose color depends on the number color in the list
                self.color('white')
            else:
                self.color('#6d6058')
            self.write(f'{self.num}', align='center', font=('Arial', 27, 'bold'))
            self.goto(self.xcor(), self.ycor()+20)


class Game():
    def init(self):
        back = BackGround()   # draw the background
        back.draw_block()
        for i in allpos:  # 16 turtle for a 4x4 game 
            block = Block()
            block.goto(i)
            block_dic[i] = block
        game.grow()

    def restart(self):  # how to restart
        global score, flag_win_lose_text
        score = 0
        for i in block_dic.values():
            i.num = 0
            i.clear()
        win_lose_text.clear()
        game.grow()
        flag_win_lose_text = True  # move on when marked words been removed

    def grow(self):  # random appear a number of 2 or 4
        block_list = []
        for i in allpos:
            if block_dic[i].num == 0:
                block_list.append(block_dic[i])  # select all turtles with empty box
        turtle_choice = random.choice(block_list)  # random pick one of them
        turtle_choice.num = random.choice([2, 2, 2, 2, 4])  # give it number 2 or 4 with diff possibility
        turtle_choice.draw()
        win_lose_text.judge()
        show_score_text.show_score()
        ms.update()

    def move_move(self, allpos1, allpos2, allpos3, allpos4):
        if flag_win_lose_text is True:
            count1 = self.move(allpos1)  # Four columns or rows are moved in sequence
            count2 = self.move(allpos2)
            count3 = self.move(allpos3)
            count4 = self.move(allpos4)
            if count1 or count2 or count3 or count4:  #  appearance of new number box depend on the detection of moved blocks
                self.grow()

    def move(self, pos_list):
        num_list = []  # coordinate of one "numbered" turtle
        for i in pos_list:
            num_list.append(block_dic[i].num)  #  list those turtles
        new_num_list, count = self.list_oper(num_list)  #  establish a new list
        for j in range(len(new_num_list)):  # given the new value to turtles/blocks
            block_dic[pos_list[j]].num = new_num_list[j]
            block_dic[pos_list[j]].draw()
        return count


    def move_up(self):
        allpos1 = allpos[::4]  # 4 rows
        allpos2 = allpos[1::4]
        allpos3 = allpos[2::4]
        allpos4 = allpos[3::4]
        self.move_move(allpos1, allpos2, allpos3, allpos4)

    def move_down(self):
        allpos1 = allpos[-4::-4]
        allpos2 = allpos[-3::-4]
        allpos3 = allpos[-2::-4]
        allpos4 = allpos[-1::-4]
        self.move_move(allpos1, allpos2, allpos3, allpos4)

    def move_left(self):
        allpos1 = allpos[:4]
        allpos2 = allpos[4:8]
        allpos3 = allpos[8:12]
        allpos4 = allpos[12:16]
        self.move_move(allpos1, allpos2, allpos3, allpos4)

    def move_right(self):
        allpos1 = allpos[-1:-5:-1]
        allpos2 = allpos[-5:-9:-1]
        allpos3 = allpos[-9:-13:-1]
        allpos4 = allpos[-13:-17:-1]
        self.move_move(allpos1, allpos2, allpos3, allpos4)



    def list_oper(self, num_list):  # num_list【2,0,2,2】
        global score
        count = True
        temp = []
        new_temp = []
        for j in num_list:
            if j != 0:
                temp.append(j)  # temp=[2,2,2]
        flag = True
        for k in range(len(temp)):
            if flag:
                if k < len(temp)-1 and temp[k] == temp[k+1]:
                    new_temp.append(temp[k]*2)
                    flag = False
                    score += temp[k]
                else:
                    new_temp.append(temp[k])  # new_temp=[4,2]
            else:
                flag = True
        for m in range(len(num_list)-len(new_temp)):
            new_temp.append(0)  # new_temp=[4,2,0,0]
        if new_temp == num_list:
            count = False  # detect changes in numlist, number blocks didn't move when there is no change in the list
        return(new_temp, count)


if __name__ == '__main__':
    ms = turtle.Screen()  # setting of the game window
    ms.setup(430, 630, 400, 50)
    ms.bgcolor('purple')
    ms.title('2048')
    ms.tracer(0)
    ms.register_shape('background.gif')
    ms.register_shape('title.gif')
    ms.register_shape('score.gif')
    ms.register_shape('top-score.gif')
    block_dic = {}  # coordinate, value for the corresponding turtle
    allpos = [(-150, 50), (-50, 50), (50, 50), (150, 50),
              (-150, -50), (-50, -50), (50, -50), (150, -50),
              (-150, -150), (-50, -150), (50, -150), (150, -150),
              (-150, -250), (-50, -250), (50, -250), (150, -250)]
    flag_win = True  # marked word of 2048 achieved only appeared once
    flag_win_lose_text = True  # define the marked words were cleaned or not, if not, cannot move the block/restart
    score = 0
    with open('.\\score.txt', 'r') as f:
        top_score = int(f.read())  #  read top scores stored in a file named score
    show_score_text = BackGround()
    win_lose_text = BackGround()
    game = Game()
    game.init()

    ms.listen()
    ms.onkey(game.move_up, 'Up')
    ms.onkey(game.move_down, 'Down')
    ms.onkey(game.move_left, 'Left')
    ms.onkey(game.move_right, 'Right')
    ms.onkey(win_lose_text.win_lose_clear, 'Return')
    ms.onkey(game.restart, 'space')

    ms.mainloop()

