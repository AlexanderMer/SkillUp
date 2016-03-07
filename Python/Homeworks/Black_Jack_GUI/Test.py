from tkinter import *

main = Tk()
canvas = Canvas(main, height=500, width=500, bg="pink")
canvas.grid()
rec = canvas.create_rectangle(50, 50, 150, 150)
print(canvas.coords(rec))
canvas.move(rec, 50, 50)
main.mainloop()