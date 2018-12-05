
#### Graphics Functions ####

import tankClass
import wallClass
import bulletClass
from tkinter import *
import math

def init(data):
    data.margin = 50
    data.timerCalls = 0
    data.numLevels = 2
    data.mode = "start"
    data.level = "level1"

# makes a player tank
def makeTank(x, y, angle):
    tank = tankClass.Tank(x, y, angle)
    return tank
    
# makes a dumb tank
def makeDumbTank(x, y, angle):
    tank = tankClass.DumbTank(x, y, angle)
    return tank

# make a moving tank
def makeMovingTank(x, y, angle):
    tank = tankClass.MovingTank(x, y, angle)
    return tank

# make a wall
def makeWall(x, y):
    wall = wallClass.Wall(x, y)
    return wall
    
# make a destructible wall
def makeDestructibleWall(x, y):
    wall = wallClass.DestructibleWall(x, y)
    return wall

# make a bullet
def makeBullet(data, tank):
    x, y = tank.arm.size
    len = y / math.sin(math.radians(tank.angle))
    print(tank.angle)
    if math.cos(math.radians(tank.angle)) >= 0:
        bx = tank.x + (x/2)
    elif math.cos(math.radians(tank.angle)) < 0:
        bx = tank.x - (x/2)
    if math.sin(math.radians(tank.angle)) >= 0:
        by = tank.y + (y/2)
    elif math.sin(math.radians(tank.angle)) < 0:
        by = tank.y - (y/2)
    if math.isclose(tank.angle, 0, rel_tol = .04) or math.isclose(tank.angle, 180, rel_tol = 0.04):
        by = tank.y
    elif math.isclose(tank.angle, 90, rel_tol = .04) or math.isclose(tank.angle, 270, rel_tol = 0.04):
        bx = tank.x
    bx = tank.x + (tank.armLen * math.cos(math.radians(tank.angle)))
    by = tank.y + (tank.armLen * math.sin(math.radians(tank.angle)))
    return bulletClass.Bullet(bx, by, tank.angle)
    
# Determines what to do based on the mode after the mouse is pressed
def mousePressed(event, data):
    if data.mode == "start":
        startMousePressed(event, data)
    elif data.mode == "game":
        gameMousePressed(event, data)
    elif data.mode == "end":
        endMousePressed(event, data)
    elif data.mode == "win":
        winMousePressed(event, data)

# Determines what to do based on the mode after a key is pressed
def keyPressed(event, data):
    if data.mode == "start":
        startKeyPressed(event, data)
    elif data.mode == "game":
        gameKeyPressed(event, data)
    elif data.mode == "end":
        endKeyPressed(event, data)
    elif data.mode == "win":
        winKeyPressed(event, data)

def motion(event, data):
    if data.mode == "start":
        startMotion(event, data)
    elif data.mode == "game":
        gameMotion(event, data)
    elif data.mode == "end":
        endMotion(event, data)
    elif data.mode == "win":
        winMotion(event, data)

# Determines what the timer should do based on the mode
def timerFired(data):
    if data.mode == "start":
        startTimerFired(data)
    elif data.mode == "game":
        gameTimerFired(data)
    elif data.mode == "end":
        endTimerFired(data)
    elif data.mode == "win":
        winTimerFired(data)

# Determines what should be drawn based on the mode
def redrawAll(canvas, data):
    if data.mode == "start":
        startRedrawAll(canvas, data)
    elif data.mode == "game":
        gameRedrawAll(canvas, data)
    elif data.mode == "end":
        endRedrawAll(canvas, data)
    elif data.mode == "win":
        winRedrawAll(canvas, data)

#### Opening Screen ####

def startKeyPressed(event, data):
    pass

def startMousePressed(event, data):
    if (data.width / 2 - 100) <= event.x <= (data.width / 2 + 100):
        if (data.height * 3 / 5 - 25) <= event.y <= (data.height * 3 / 5 + 25):
            gameInit(data, data.level)
            data.mode = "game"

def startTimerFired(data):
    pass

def startMotion(event, data):
    pass

def startRedrawAll(canvas, data):
    fontSize = 28
    canvas.create_text(data.width / 2, data.height / 3, text = "T A N K S", fill = "white", font = "Arial 42 bold")
    canvas.create_rectangle(data.width / 2 - 100, data.height * 3 / 5 - 25, data.width / 2 + 100, data.height * 3 / 5 + 25, fill = "red4")
    canvas.create_text(data.width / 2, data.height * 3 / 5, text = "PLAY", fill = "white", font = "Arial 18 bold")

#### Game Functions ####

def gameMousePressed(event, data):
    pass

def gameMotion(event, data):
    x = event.x
    y = event.y
    data.tank.moveShooter(x, y)

def gameKeyPressed(event, data):
    # shoots a bullet
    if event.keysym == "space":
        data.bullets.append(makeBullet(data, data.tank))
    # sets the direction of the tank 
    if event.keysym == "Up":
        for wall in data.walls:
            if data.tank.wallHit(wall) == True:
                data.hitWall = True
                break
            elif data.tank.wallHit(wall) == False:
                data.hitWall = False
        data.tank.move(data.width, data.height, data.margin, data.hitWall, data.dir, "u")
        data.dir = "u"
    if event.keysym == "Down":
        for wall in data.walls:
            if data.tank.wallHit(wall) == True:
                data.hitWall = True
                break
            elif data.tank.wallHit(wall) == False:
                data.hitWall = False
        data.tank.move(data.width, data.height, data.margin, data.hitWall, data.dir, "d")
        data.dir = "d"
    if event.keysym == "Left":
        for wall in data.walls:
            if data.tank.wallHit(wall) == True:
                data.hitWall = True
                break
            elif data.tank.wallHit(wall) == False:
                data.hitWall = False
        if not data.hitWall:
            data.tank.rotate += 2
            data.tank.rotateTank()
        print(data.tank.rotate)
    if event.keysym == "Right":
        for wall in data.walls:
            if data.tank.wallHit(wall) == True:
                data.hitWall = True
                break
            elif data.tank.wallHit(wall) == False:
                data.hitWall = False
        if not data.hitWall:
            data.tank.rotate -= 2
            data.tank.rotateTank()
        print(data.tank.rotate)

    # move the tank
    # data.tank.move(data.width, data.height, data.margin, data.hitWall)

def gameTimerFired(data):
    data.timerCalls += 1
    for b in data.bullets:
        b.moveBullet()
        b.reactToWallHit(data.width, data.height, data.margin)
        if b.numWallsHit > 2:
            data.bullets.remove(b)
        for tank in data.gameTanks:
            if b.hitsTank(tank):
                data.gameTanks.remove(tank)
                data.bullets.remove(b)
                if data.gameTanks == []:
                    winInit(data)
                    data.mode = "win"
        if b.hitsTank(data.tank):
            endInit(data, "level1")
            data.mode = "end"
            data.gameTankBullets.remove(b)
        for wall in data.walls:
            if b.hitsWall(wall):
                data.bullets.remove(b)
            if isinstance(wall, wallClass.DestructibleWall) and wall.hits >= 2:
                data.walls.remove(wall)
    
    
    for tank in data.gameTanks:
        data.gameTank.moveShooter(data.tank)
        print(data.walls)
        w = None
        for wall in data.walls:
            if tank.wallHit(wall) != True or tank.wallHit(wall) != False:
                w = wall
                print(w)
                break
        if data.timerCalls % 2 == 0:
            tank.move(data.tank, w)
        if isinstance(tank, tankClass.MovingTank) and data.timerCalls % 20 == 0:
            #data.bullets.append(makeBullet(data, tank))
            break
    for tank in data.gameTanks:
        if isinstance(tank, tankClass.DumbTank) and tank.seesPlayer(data.tank):
            data.bullets.append(makeBullet(data, tank))
            break
    
    
# draws the window
def gameRedrawAll(canvas, data):
    l = data.level[-1]
    canvas.create_rectangle(data.margin, data.margin, data.width - data.margin, data.height - data.margin, fill = "grey", width = 0)
    canvas.create_text(data.width / 2, data.margin / 2, text = "LEVEL " + l, fill = "white", font = "Arial 18 bold")
    for wall in data.walls:
        wall.draw(canvas)
    data.tank.draw(canvas)
    for tank in data.gameTanks:
        tank.draw(canvas)
    for b in data.bullets:
        b.draw(canvas)
    # for b in data.gameTankBullets:
    #     b.draw(canvas)

def gameInit(data, level):
    if level == "level1":
        data.tank = makeTank(600, 370, 180)
        data.gameTank = tankClass.DumbTank(200, 200, 0)
        data.gameTanks = [data.gameTank]
        data.bullets = []
        data.playerBullets = []
        data.gameTankBullets = []
        data.walls = [wallClass.Wall(400, 370), wallClass.Wall(400, 230), wallClass.DestructibleWall(400, 300)]
        data.hitWall = False
        data.dir = "u"
    elif level == "level2":
        data.tank = makeTank(600, 300, 180)
        data.gameTank = tankClass.DumbTank(200, 200, 0)
        data.gameTanks = [data.gameTank, tankClass.MovingTank(200, 400, 0)]
        data.bullets = []
        data.playerBullets = []
        data.gameTankBullets = []
        data.walls = [wallClass.Wall(400, 370), wallClass.Wall(400, 230), wallClass.DestructibleWall(400, 300), wallClass.Wall(400, 160), wallClass.Wall(400, 440), wallClass.DestructibleWall(470, 160), wallClass.DestructibleWall(330, 440)]
        data.hitWall = False
        data.dir = "u"


#### Win Screen ####

def winInit(data):
    if int(data.level[-1]) >= data.numLevels:
        data.gameOver = True
    else:
        data.gameOver = False
        data.nextLevel = "level" + str(int(data.level[-1]) + 1)

def winKeyPressed(event, data):
    pass

def winMousePressed(event, data):
    if not data.gameOver:
        if data.width / 2 - 100 <= event.x <= data.width / 2 + 100:
            if data.height * 3 / 5 - 25 <= event.y <= data.height * 3 / 5 + 25:
                data.level = data.nextLevel
                print(data.level)
                gameInit(data, data.nextLevel)
                data.mode = "game"
    else:
        if data.width / 2 - 100 <= event.x <= data.width / 2 + 100:
            if data.height * 3 / 5 - 25 <= event.y <= data.height * 3 / 5 + 25:
                data.mode = "start"

def winMotion(event, data):
    pass

def winTimerFired(data):
    pass

def winRedrawAll(canvas, data):
    canvas.create_text(data.width / 2, data.height / 3, text = "YOU WIN", fill = "white", font = "Arial 42 bold")
    canvas.create_rectangle(data.width / 2 - 100, data.height * 3 / 5 - 25, data.width / 2 + 100, data.height * 3 / 5 + 25, fill = "red4")
    if data.gameOver:
        canvas.create_text(data.width / 2, data.height * 3 / 5, text = "Main Menu", fill = "white", font = "Arial 18 bold")
    else: 
        canvas.create_text(data.width / 2, data.height * 3 / 5, text = "Next", fill = "white", font = "Arial 18 bold")

#### End Screen ####

def endInit(data, level):
    data.level = level

def endKeyPressed(event, data):
    pass

def endMousePressed(event, data):
    if data.width / 2 - 100 <= event.x <= data.width / 2 + 100:
        if data.height * 3 / 5 - 25 <= event.y <= data.height * 3 / 5 + 25:
            gameInit(data, data.level)
            data.mode = "game"

def endMotion(event, data):
    pass

def endTimerFired(data):
    pass

def endRedrawAll(canvas, data):
    canvas.create_text(data.width / 2, data.height / 3, text = "YOU LOSE", fill = "white", font = "Arial 42 bold")
    canvas.create_rectangle(data.width / 2 - 100, data.height * 3 / 5 - 25, data.width / 2 + 100, data.height * 3 / 5 + 25, fill = "red4")
    canvas.create_text(data.width / 2, data.height * 3 / 5, text = "Try Again", fill = "white", font = "Arial 18 bold")

#################################################################
# run function from class notes
#################################################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='black', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
    
    def motionWrapper(event, canvas, data):
        motion(event, data)
        redrawAllWrapper(canvas, data)
    
    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind('<Motion>', lambda event:
                                motionWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(800, 600)
