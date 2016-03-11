from tkinter import *
import random


class Snake:
    def __init__(self, canvas, x, y, size):
        self.color = "red"
        self.old_direction = ""
        self.direction = "Up"  # Must be Up Down Left Right
        self.size = size
        self.segments = []
        self.head = canvas.create_rectangle(x, y, x + self.size, y + self.size, fill="pink")
        self.tail = canvas.create_rectangle(x + size, y, x + size, y + self.size, fill=self.color)
    
    def move(self, canvas, eat=False):
        # move head
        # fill empty space and add to segments
        # delete tail from both segments and canvas
        # assign new tail to variable
        old_coords = canvas.coords(self.head)
        dirs = {
            "Up": (0, -self.size),
            "Down": (0, self.size),
            "Left": (-self.size, 0),
            "Right": (self.size, 0)
        }
        canvas.move(self.head, dirs[self.direction][0], dirs[self.direction][1])
        self.segments.append(canvas.create_rectangle(old_coords[0], old_coords[1],
                                                     old_coords[2], old_coords[3], fill=self.color))
        if not eat:
            canvas.delete(self.tail)
            self.tail = self.segments[0]
            del self.segments[0]


class Game:
    def __init__(self):
        self.ROOT = Tk()
        self.WINDOW_HEIGHT = 600
        self.WINDOW_WIDTH = 800
        self.FIELD = Canvas(self.ROOT, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT, bg="black")
        self.FIELD.pack()
        self.snake = Snake(self.FIELD, 100, 100, 20)
        self.snake_speed = 100
        self.FIELD.bind("<KeyPress>", self.key_pressed)
        self.FIELD.focus_set()
        self.spawn_walls()
        self.food = 0
        self.spawn_food()
        self.ROOT.resizable(0, 0)
        self.food_freq = 50  # Used to adjust frequency of the food appearing.
        self.food_count = 0
        self.game_over_text = -1
        self.game_running = True
        self.game_loop()  # Must be one before last line!
        self.ROOT.mainloop()  # Must be last line!!!

    def game_loop(self):
        print("food count {}".format(self.food_count))
        self.food_count += 1
        if self.food_count == self.food_freq:
            self.spawn_food()
        self.snake.move(self.FIELD)
        check = self.check_game_over()
        if check == 2:
            self.snake.move(self.FIELD, eat=True)
            self.FIELD.after(self.snake_speed, self.game_loop)
            self.FIELD.delete(self.food)
            self.spawn_food(eat=True)
        elif check == 0:
            self.FIELD.after(self.snake_speed, self.game_loop)
        else:
            print("Game Over")
            self.game_running = False
            self.game_over_text = self.FIELD.create_text(self.WINDOW_WIDTH / 2, self.WINDOW_HEIGHT / 2,
                                                         text="Game Over", font="Arial 23", fill="White")


    def key_pressed(self, event):
        print(event.keysym)
        if event.keysym in ["Up", "Down", "Left", "Right"]:
            self.snake.direction = event.keysym
        elif event.keysym == "Return" and not self.game_running:
            self.new_game()

    def spawn_food(self, eat=False):
        self.food_count = 0
        if not eat:
            self.FIELD.delete(self.food)
        x = self.snake.size * int(random.randint(0, self.WINDOW_WIDTH - self.snake.size) / self.snake.size)
        y = self.snake.size * int(random.randint(0, self.WINDOW_HEIGHT - self.snake.size) / self.snake.size)
        self.food = self.FIELD.create_rectangle(x, y, x + self.snake.size, y + self.snake.size, fill="white")
        #  self.ROOT.after(5000, self.spawn_food)

    def blink_food(self):
        pass

    def check_game_over(self):
        # 0 nothing happens
        # 1 crashed
        # 2 eat food
        x1, y1, x2, y2 = self.FIELD.coords(self.snake.head)
        overlaps = self.FIELD.find_overlapping(x1, y1, x2, y2)
        print(overlaps)
        if len(overlaps) > 2:
            for i in range(1, len(overlaps)):
                if self.FIELD.coords(overlaps[i]) == self.FIELD.coords(self.snake.head):
                    return 2 if self.FIELD.coords(self.food) == self.FIELD.coords(overlaps[i]) else 1
        return 0

    def spawn_walls(self):
        """Spawns invisible walls around game area to keep player inside"""
        size = self.snake.size
        # north and south wall
        k = int(self.WINDOW_WIDTH / size)
        for i in range(k):
            self.FIELD.create_rectangle(i * size, -size, i * size + size, 0)
            self.FIELD.create_rectangle(i * size, self.WINDOW_HEIGHT, i * size + size, self.WINDOW_HEIGHT + size)

        k = int(self.WINDOW_HEIGHT / size)
        # east and west walls
        for i in range(k):
            self.FIELD.create_rectangle(self.WINDOW_WIDTH, i * size,
                                        self.WINDOW_WIDTH + size, i * size + size)
            self.FIELD.create_rectangle(-size, i * size,
                                        0, i * size + size)

    def new_game(self):
        #  BUG! DDO NOT USE!
        """game_running = True
        self.FIELD.delete(self.snake.head)
        self.FIELD.delete(self.snake.tail)
        for r in self.snake.segments:
            self.FIELD.delete(r)

        self.FIELD.delete(self.game_over_text)
        self.snake = Snake(self.FIELD, 100, 100, 20)
        self.snake_speed = 100
        self.game_loop()"""


Game()
