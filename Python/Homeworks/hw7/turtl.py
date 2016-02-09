import turtle


def polygon(n):
    degrees = 180 * (n - 2) / n
    print(degrees)

    for d in range(n):
        turtle.fd(100)
        turtle
        turtle.lt(180 - degrees)


def rotating():
    offset = 2
    turtle.speed(100)
    for n in range(int(160)):
        square()
        turtle.lt(offset)


def square():
    for a in range(4):
        turtle.fd(100)
        turtle.lt(90)


def one():
    turtle.rt(90)
    turtle.pd()
    turtle.fd(100)
    turtle.pu()
    turtle.lt(90)
    turtle.fd(20)
    turtle.lt(90)
    turtle.fd(100)
    turtle.rt(90)
    turtle.pd()


def two():
    turtle.fd(200)

    turtle.fd(50)
    turtle.rt(90)
    turtle.fd(50)
    turtle.rt(90)
    turtle.fd(50)
    turtle.lt(90)
    turtle.fd(50)
    turtle.lt(90)
    turtle.fd(50)
    turtle.pu()
    turtle.fd(20)
    turtle.lt(90)
    turtle.fd(100)
    turtle.rt(90)
    turtle.pd()


odin = one
dva = two
turtle.bgcolor('Yellow')
turtle.color('Red')
numbers = {1: odin, 2: dva}

inp = input('number ? ')
for n in inp:
    numbers[int(n)]()
