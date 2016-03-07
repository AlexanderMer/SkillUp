from tkinter import *
import random


flag_height = 200
flag_width = 400
main = Tk()
canvas = Canvas(main,width=flag_width, height=flag_height)
canvas.grid(row=0, column=0, rowspan=10)
canvas.config(bg="blue")
entry = Entry(text="test")
entry.grid(row=0, column=1)
def random_color():
    ct = [random.randrange(256) for x in range(3)]
    brightness = int(round(0.299 * ct[0] + 0.587 * ct[1] + 0.114 * ct[2]))
    ct_hex = "%02x%02x%02x" % tuple(ct)
    bg_color = '#' + "".join(ct_hex)
    fg_color = "white" if brightness < 120 else "black"
    return bg_color, fg_color

def line(event):
    global  old_coords
    if old_coords == 0:
        old_coords = event.x, event.y
    else:
        event.widget.create_line(old_coords[0], old_coords[1], event.x, event.y)
        old_coords = 0

def flag(event):
    global entry
    country = entry.get()
    if country == "UA":
       canvas.create_rectangle(0, 0, 400, 100, fill="blue", outline="blue")
       canvas.create_rectangle(0, 200, 400, 100, fill="yellow", outline="yellow")
    elif country == "JP":
        canvas.create_rectangle(0, 0, flag_width, flag_height, fill="white", outline="white")
        radius = flag_height / 3
        canvas.create_oval(flag_width / 2 - radius, flag_height / 2 - radius,
                           flag_width / 2 + radius, flag_height / 2 + radius, fill="red", outline="red")
    elif country == "GE":
        canvas.create_rectangle(0, 0, flag_width, flag_height, fill="white")
        thickness = flag_height / 6
        #  horizontal line
        canvas.create_rectangle(0, flag_height /2 - thickness / 2,
                                flag_width, flag_height / 2 + thickness / 2, fill="red", outline="red")
        #  vertical line
        canvas.create_rectangle(flag_width / 2 - thickness / 2, 0,
                                flag_width / 2 + thickness / 2, flag_height, fill="red", outline="red")
        #  crosses

    elif country == "IT":
        canvas.create_rectangle(0, 0, int(flag_width / 3), flag_height, fill="green", outline="green")
        canvas.create_rectangle(int(flag_width / 3), 0,
                                int(flag_width / 3) * 2, flag_height,
                                fill="white", outline="white")
        canvas.create_rectangle( int(flag_width / 3) * 2, 0, flag_width, flag_height, fill="red", outline="red")

snow_flakes = []
def create_snow_flake():
    size = int(flag_height / 30)
    global snow_flakes
    origin = random.randint(0, flag_width)
    snow_flakes.append(canvas.create_oval(origin, 0, origin + size, size, fill="white", outline="white"))

    main.after(900, create_snow_flake)

def move_snow_flakes():
    for s in snow_flakes:
        canvas.move(s, 0, 2)
    main.after(100, move_snow_flakes)

def small_cross(x, y):
    """Takes X and Y arguments and returns list of coordinates to create a small cross centered at X Y
    It is assumed that 0, 0 is in the upper left corner"""
    size = flag_height / 15 #  side of a square that makes up the center of the cross
    far_v = size * 1.5
    strange = size + size / 10

    return [(int(x - size), int(y - size)),                #  1
            (int(x - size - size / 10), int(y - size * 3)),  #  2
            (int(x + size + size / 10), int(y - size * 3)),  #  3
            (int(x + size), int(y - size)),                #  4
            (int(x + size * 3), int(y - size - size / 10)),  #  5
            (int(x + size + size / 10), int())]                          #  6
create_snow_flake()
move_snow_flakes()
entry.bind("<Return>", flag)
main.mainloop()