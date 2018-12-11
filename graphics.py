
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
    bx = tank.x + (tank.armLen * math.cos(math.radians(tank.angle)))
    by = tank.y + (tank.armLen * math.sin(math.radians(tank.angle)))
    return bulletClass.Bullet(bx, by, tank.angle)
    
# Determines what to do based on the mode after the mouse is pressed
def mousePressed(event, data):
    if data.mode == "start":
        startMousePressed(event, data)
    elif data.mode == "levelEditor":
        levelEditorMousePressed(event, data)
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
    elif data.mode == "levelEditor":
        levelEditorKeyPressed(event, data)
    elif data.mode == "game":
        gameKeyPressed(event, data)
    elif data.mode == "end":
        endKeyPressed(event, data)
    elif data.mode == "win":
        winKeyPressed(event, data)

def motion(event, data):
    if data.mode == "start":
        startMotion(event, data)
    elif data.mode == "levelEditor":
        levelEditorMotion(event, data)
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
    elif data.mode == "levelEditor":
        levelEditorTimerFired(data)
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
    elif data.mode == "levelEditor":
        levelEditorRedrawAll(canvas, data)
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

#### Level Editor ####

def levelEditorInit(data):
    gameInit(data, data.level)
    data.selected = None

def levelEditorMousePressed(event, data):
    if (data.width - 140 <= event.x <= data.width - 40) and (10 <= event.y <= 40):
        data.mode = "game"
    elif data.selected != None:
        if isinstance(data.selected, tankClass.Tank):
            x, y = data.selected.body.size
            x /= 2
            y /= 2
        if isinstance(data.selected, wallClass.Wall):
            x = data.selected.length / 2
            y = data.selected.length / 2
        if data.margin <= event.x + x <= data.width - data.margin \
        and data.margin <= event.x - x <= data.width - data.margin \
        and data.margin <= event.y + y <= data.height - data.margin \
        and data.margin <= event.y - y <= data.height - data.margin:
            
            for w in data.walls:
                if (w.x1 <= event.x + x <= w.x2 or w.x1 <= event.x - x <= w.x2) \
                and (w.y1 <= event.y + y <= w.y2 or w.y1 <= event.y - y <= w.y2):
                    return 
            for t in data.gameTanks:
                x1, y1 = t.body.size
                x1 /= 2
                y1 /= 2
                if (t.x - x1 <= event.x + x <= t.x + x1 or t.x - x1 <= event.x - x <= t.x + x1)\
                and (t.y - y1 <= event.y + y <= t.y + y1 or t.y - y1 <= event.y - y <= t.y + y1):
                    return
            x2, y2 = data.tank.body.size
            x2 /= 2
            y2 /= 2
            if (data.tank.x - x2 <= event.x - x <= data.tank.x + x2 or data.tank.x - x2 <= event.x + x <= data.tank.x + x2) \
            and (data.tank.y - y2 <= event.y - y <= data.tank.y + y2 or data.tank.y - y2 <= event.y + y <= data.tank.y + y2):
                return
            if isinstance(data.selected, tankClass.DumbTank):
                data.gameTanks.append(tankClass.DumbTank(event.x, event.y, 0))
            elif isinstance(data.selected, tankClass.MovingTank):
                data.gameTanks.append(tankClass.MovingTank(event.x, event.y, 0))
            elif isinstance(data.selected, wallClass.DestructibleWall):
                data.walls.append(wallClass.DestructibleWall(event.x, event.y))
            elif isinstance(data.selected, wallClass.Wall):
                data.walls.append(wallClass.Wall(event.x, event.y))
            data.selected = None
    elif data.selected == None:
        for w in data.walls:
            if (w.x1 <= event.x <= w.x2) and (w.y1 <= event.y <= w.y2):
                data.selected = w
                data.walls.remove(w)
        for t in data.gameTanks:
            x1, y1 = t.body.size
            x1 /= 2
            y1 /= 2
            if (t.x - x1 <= event.x <= t.x + x1) and (t.y - y1 <= event.y <= t.y + y1):
                data.selected = t 
                data.gameTanks.remove(t)
    
    if data.height - 40 <= event.y <= data.height - 10:
        if 50 <= event.x <= 150:
            data.selected = tankClass.DumbTank(event.x, event.y, 0)
        elif 200 <= event.x <= 300:
            if data.tank == None:
                data.selected = tankClass.Tank(event.x, event.y, 0)
        elif 350 <= event.x <= 450:
            data.selected = tankClass.MovingTank(event.x, event.y, 0)
        elif 500 <= event.x <= 600:
            data.selected = wallClass.Wall(event.x, event.y)
        elif 650 <= event.x <= 750:
            data.selected = wallClass.DestructibleWall(event.x, event.y)
        

def levelEditorKeyPressed(event, data):
    if event.keysym == "Escape":
        data.selected = None
    if event.keysym == "BackSpace":
        data.selected = None

def levelEditorMotion(event, data):
    if data.selected != None:
        if isinstance(data.selected, tankClass.DumbTank):
            data.selected = tankClass.DumbTank(event.x, event.y, 0)
        elif isinstance(data.selected, tankClass.MovingTank):
            data.selected = tankClass.MovingTank(event.x, event.y, 0)
        elif isinstance(data.selected, wallClass.DestructibleWall):
            data.selected = wallClass.DestructibleWall(event.x, event.y)
        elif isinstance(data.selected, wallClass.Wall):
            data.selected = wallClass.Wall(event.x, event.y)
    

def levelEditorTimerFired(data):
    pass

def levelEditorRedrawAll(canvas, data):
    canvas.create_rectangle(data.margin, data.margin, data.width - data.margin, data.height - data.margin, fill = "grey", width = 0)
    canvas.create_text(data.width / 2, data.margin / 2, text = "LEVEL EDITOR", fill = "white", font = "Arial 18 bold")
    canvas.create_rectangle(data.width - 140, 10, data.width - 40, 40, fill = "red4", width = 0)
    canvas.create_text(data.width - 90, 25, text = "RETURN", fill = "white", font = "Arial 13 bold")
    canvas.create_rectangle(50, data.height - 40, 150, data.height - 10, fill = "red4", width = 0)
    canvas.create_text(100, data.height - 25, text = "DumbT", fill = "white", font = "Arial 13")
    canvas.create_rectangle(200, data.height - 40, 300, data.height - 10, fill = "red4", width = 0)
    canvas.create_text(250, data.height - 25, text = "T", fill = "white", font = "Arial 13")
    canvas.create_rectangle(350, data.height - 40, 450, data.height - 10, fill = "red4", width = 0)
    canvas.create_text(400, data.height - 25, text = "MovingT", fill = "white", font = "Arial 13")
    canvas.create_rectangle(500, data.height - 40, 600, data.height - 10, fill = "red4", width = 0)
    canvas.create_text(550, data.height - 25, text = "W", fill = "white", font = "Arial 13")
    canvas.create_rectangle(650, data.height - 40, 750, data.height - 10, fill = "red4", width = 0)
    canvas.create_text(700, data.height - 25, text = "BreakableW", fill = "white", font = "Arial 13")
    for wall in data.walls:
        wall.draw(canvas)
    data.tank.draw(canvas)
    for tank in data.gameTanks:
        tank.draw(canvas)
    for b in data.bullets:
        b.draw(canvas)
    if data.selected != None:
        data.selected.draw(canvas)
    

#### Game Functions ####

def gameMousePressed(event, data):
    if (data.width - 100 <= event.x <= data.width - 40) and (10 <= event.y <= 40):
        data.mode = "levelEditor"
        levelEditorInit(data)

def gameMotion(event, data):
    x = event.x
    y = event.y
    data.tank.moveShooter(x, y)

def gameKeyPressed(event, data):
    # shoots a bullet
    if event.keysym == "space":
        data.bullets.append(makeBullet(data, data.tank))
        print("added", data.bullets)
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
            data.tank.rotate += 3
            data.tank.rotateTank()
        #print(data.tank.rotate)
    if event.keysym == "Right":
        for wall in data.walls:
            if data.tank.wallHit(wall) == True:
                data.hitWall = True
                break
            elif data.tank.wallHit(wall) == False:
                data.hitWall = False
        if not data.hitWall:
            data.tank.rotate -= 3
            data.tank.rotateTank()
        #print(data.tank.rotate)

    # move the tank
    # data.tank.move(data.width, data.height, data.margin, data.hitWall)

def gameTimerFired(data):
    data.timerCalls += 1
    for b in data.bullets:
        b.moveBullet()
        b.reactToWallHit(data.width, data.height, data.margin)
        if b.numWallsHit > 2:
            data.bullets.remove(b)
            #print("hit 3 walls", data.bullets)
        for tank in data.gameTanks:
            if b.hitsTank(tank):
                data.gameTanks.remove(tank)
                data.bullets.remove(b)
                #print("hit tank", data.bullets)
                if data.gameTanks == []:
                    winInit(data)
                    data.mode = "win"
        if b.hitsTank(data.tank):
            endInit(data, "level1")
            data.mode = "end"
            data.bullets.remove(b)
            #print("hit player", data.bullets)
        for wall in data.walls:
            if b.hitsWall(wall):
                data.bullets.remove(b)
                print("hit a wall", wall)
                break
        for wall in data.walls:
            if isinstance(wall, wallClass.DestructibleWall) and wall.hits >= 2:
                data.walls.remove(wall)
    for tank in data.gameTanks:
        tank.moveShooter(data.tank)
        #print(data.walls)
        w = None
        for wall in data.walls:
            if tank.wallHit(wall) == True:
                w = wall
                #print(w)
                break
        if data.timerCalls % 2 == 0:
            tank.move(data.tank, w, data.width, data.height, data.margin)
            
        if isinstance(tank, tankClass.MovingTank) and data.timerCalls % 20 == 0:
            data.bullets.append(makeBullet(data, tank))
            break
    for tank in data.gameTanks:
        if isinstance(tank, tankClass.DumbTank) and tank.seesPlayer(data.tank):
            data.bullets.append(makeBullet(data, tank))
            print("game added", data.bullets)
            break
    
    
# draws the window
def gameRedrawAll(canvas, data):
    l = data.level[-1]
    canvas.create_rectangle(data.margin, data.margin, data.width - data.margin, data.height - data.margin, fill = "grey", width = 0)
    canvas.create_text(data.width / 2, data.margin / 2, text = "LEVEL " + l, fill = "white", font = "Arial 18 bold")
    canvas.create_rectangle(data.width - 100, 10, data.width - 40, 40, fill = "red4", width = 0)
    canvas.create_text(data.width - 70, 25, text = "EDIT", fill = "white", font = "Arial 13 bold")
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
