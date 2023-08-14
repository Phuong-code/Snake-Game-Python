from tkinter import *
import random
import time
GAME_WIDTH = 800
GAME_HEIGHT = 600
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "dark green"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"
class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR, tags="snake")
            self.squares.append(square)

class Food:

    def __init__(self):
        x = random.randint(0, (GAME_WIDTH/SPACE_SIZE)-1)*SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT/SPACE_SIZE)-1)*SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=FOOD_COLOR, tags="food")

def move(snake, food):
    x, y = snake.coordinates[0]
    if direction == "down":
        y += SPACE_SIZE
    elif direction == "up":
        y -= SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if check_collision(snake):
        game_over()
        window.bind("<Return>", play_again)
    else:
        if x == food.coordinates[0] and y == food.coordinates[1]:
            global score
            score += 1
            score_label.config(text=f"SCORE = {score}")
            canvas.delete("food")
            food = Food()
        else:
            del snake.coordinates[-1]
            canvas.delete(snake.squares[-1])
            del snake.squares[-1]
        window.after(SPEED, move, snake, food)
        bind_keys()

def bind_keys():
    window.bind("<w>", lambda event: change_direction("up"))
    window.bind("<s>", lambda event: change_direction("down"))
    window.bind("<a>", lambda event: change_direction("left"))
    window.bind("<d>", lambda event: change_direction("right"))


def change_direction(new_direction):
    window.unbind("<Up>")
    window.unbind("<Down>")
    window.unbind("<Left>")
    window.unbind("<Right>")
    global direction
    if (new_direction == "up" and direction != "down") or\
            (new_direction == "down" and direction != "up") or\
            (new_direction == "left" and direction != "right") or\
            (new_direction == "right" and direction != "left"):
        direction = new_direction


def check_collision(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    for body in snake.coordinates[1:]:
        if x == body[0] and y == body[1]:
            return True
    return False

def game_over():
    score_label.config(text=f"SCORE = {score}        Press Enter to play again...")

def play_again(event):
    window.unbind("<Return>")
    canvas.delete(ALL)
    global score, direction
    score = 0
    direction = "down"
    snake = Snake()
    food = Food()
    score_label.config(text=f"SCORE = {score}")
    move(snake, food)

window = Tk()
window.title("Snake Game")
window.resizable(False, False)
score = 0
direction = "down"

score_label = Label(window, text=f"SCORE = {score}", font=20)
score_label.pack()

canvas = Canvas(window, width=GAME_WIDTH, height=GAME_HEIGHT, background=BACKGROUND_COLOR)
canvas.pack()

window.update()

x = int(- window.winfo_width()/2 + window.winfo_screenwidth()/2)
y = int(- window.winfo_height()/2 + window.winfo_screenheight()/2)
window.geometry(f"{window.winfo_width()}x{window.winfo_height()}+{x}+{y}")



snake = Snake()
food = Food()
move(snake, food)

window.mainloop()