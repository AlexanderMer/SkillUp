from tkinter import  *

root = Tk()
canvas = Canvas(root, height=200, width=400)
canvas.pack()


def small_cross(x, y):
    """Takes X and Y arguments and returns list of coordinates to create a small cross centered at X Y
    It is assumed that 0, 0 is in the upper left corner"""
    size = 200 / 15 #  side of a square that makes up the center of the cross
    far_v = size * 1.5
    strange = size + size / 10

    return [int(x - size), int(y - size),                  #  1
            int(x - size - size / 10), int(y - size * 3),  #  2
            int(x + size + size / 10), int(y - size * 3),  #  3
            int(x + size), int(y - size),                  #  4
            int(x + size * 3), int(y - size - size / 10),  #  5
            int(x + size + size / 10), int(y + size + size / 10),#  6
            int(x + size), int(y + size),                    #  7
            int(x - size - size / 10), int(y + size * 3), #  8
            int(x - size), int(y + size)]     #  12





canvas.create_polygon(small_cross(100, 100), fill="green")
root.mainloop()