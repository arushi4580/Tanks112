
import math
import wallClass
from tkinter import *
import numpy as np
from PIL import Image, ImageTk


class Tank(object):
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.rotate = 0
        self.direction = [0, 0]
        self.speed = 5
        self.width = 60
        self.length = 50
        self.angle = angle
        self.color = "orange"
        
        body = Image.open("body.gif")
        self.bodyO = body.copy().resize((75, 100)).convert('RGBA')
        self.body = self.bodyO.copy()
        arm = Image.open("arm1.gif")
        self.armO = arm.copy().resize((38, 150)).convert('RGBA')
        self.arm = self.armO.copy()
        
        x, y = self.arm.size
        self.armLen = 85
        
        # data = np.array(self.arm)
        # red, green, blue, alpha = data.T
        # blue_areas = (red <= 100) & (blue >= 200) & (green <= 100)
        # data[..., :-1][blue_areas.T] = (255, 0, 0)
        # 
        # self.arm = Image.fromarray(data)
        # self.arm.show()
        # 
        self.bodyTk = ImageTk.PhotoImage(self.body)
        self.armTk = ImageTk.PhotoImage(self.arm)
        
    def rotateTank(self):
        self.rotate %= 360
        tBody = self.bodyO.copy()
        self.body = tBody.rotate(self.rotate, expand = True)
        self.bodyTk = ImageTk.PhotoImage(self.body)
        
    
    # moves the tank if it is not at the edge of the window and it is not hitting a wall
    def move(self, screenWidth, screenHeight, margin, hitWall, dir, currDir):
        x, y = self.body.size
        #print(hitWall)
        # hitting the right side of the window
        if (self.x + (x // 2) <= screenWidth - margin)\
        and (self.x - (x // 2) >= margin) \
        and (self.y + (y // 2) <= screenHeight - margin) \
        and (self.y - (y // 2) >= margin) \
        and (hitWall == False or (hitWall == True and currDir != dir)):
            if currDir == "u":
                self.x += self.speed * math.cos(math.radians(90 + self.rotate))
                self.y += self.speed * math.sin(math.radians(270 + self.rotate))
            elif currDir == "d":
                self.x += self.speed * math.cos(math.radians(270 + self.rotate))
                self.y += self.speed * math.sin(math.radians(90 + self.rotate))
    
    # rotates the shooter
    def moveShooter(self, x, y):
        # find the two legs of the right triangle made by the shooter arm and 
        # the center of the tank
        dx = x - self.x
        dy = y - self.y
        # avoids division by 0 errors for the 90 and 270 degrees
        if dx == 0 and dy < 0:
            self.angle = 270
        elif dx == 0 and dy > 0:
            self.angle = 90
        else:
            self.angle = math.degrees(math.atan(dy / dx))
            # accounts for the lower half of the unit circle
            if dx < 0:
                self.angle += 180
        #print(self.angle)
        tArm = self.armO.copy()
        self.arm = tArm.rotate(-(self.angle + 90), expand = True)
        self.armTk = ImageTk.PhotoImage(self.arm)
        
    
    def wallHit(self, wall):
        x, y = self.body.size
        if not isinstance(wall, wallClass.Wall):
            return False
        # hits left side
        elif (wall.x2 >= self.x + (x / 2) >= wall.x1) and ((wall.y1 < self.y + (y / 2) < wall.y2) or (wall.y1 < self.y - (y / 2) < wall.y2)):
            #print("hit left")
            return True
        # hits right side
        elif (wall.x2 >= self.x - (x / 2) >= wall.x1) and ((wall.y1 < self.y + (y / 2) < wall.y2) or (wall.y1 < self.y - (y / 2) < wall.y2)):
            #print("hit right")
            return True
        # hits bottom side
        elif (wall.y1 <= self.y - (y / 2) <= wall.y2) and ((wall.x2 > self.x + (x / 2) > wall.x1) or (wall.x2 > self.x - (x / 2) > wall.x1)):
            #print("hit bottom")
            return True
        # hits top side
        elif (wall.y1 <= self.y + (y / 2) <= wall.y2) and ((wall.x2 > self.x + (x / 2) > wall.x1) or (wall.x2 > self.x - (x / 2) > wall.x1)):
            #print("hit top")
            return True
        return False
    
    # tank graphics (use graphics from online for a cool looking tank)
    def draw(self, canvas):
        x, y = self.body.size
        x1, y1 = self.arm.size
        #canvas.create_rectangle(self.x - (x/2), self.y - (y/2), self.x + (x/2), self.y + (y/2))
        canvas.create_image(self.x, self.y, image = self.bodyTk)
        #canvas.create_rectangle(self.x - (x1/2), self.y - (y1/2), self.x + (x1/2), self.y + (y1/2))
        canvas.create_image(self.x, self.y, image = self.armTk)


#### Types of Tanks ####

class DumbTank(Tank):
    # graphics for dumb tank AI
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle)
        
        body = Image.open("DumbTank.gif")
        self.bodyO = body.copy().resize((75, 100)).convert('RGBA')
        self.body = self.bodyO.copy()
        #self.body.show()
        arm = Image.open("DumbArm.gif")
        self.armO = arm.copy().resize((38, 150)).convert('RGBA')
        self.arm = self.armO.copy()
        self.bodyTk = ImageTk.PhotoImage(self.body)
        self.armTk = ImageTk.PhotoImage(self.arm)
        
        self.color = "brown"
        self.range = 120
        self.currRange = 0
        self.dir = 1
    
    def move(self, player, wall, screenWidth, screenHeight, margin):
        pass
    
    def moveShooter(self, player):
        if self.currRange >= self.range:
            self.dir = -1
        elif self.currRange <= 0:
            self.dir = 1
        if self.dir == 1:
            self.currRange += 3
            self.angle += 3
        elif self.dir == -1:
            self.currRange -= 3
            self.angle -= 3
        tArm = self.armO.copy()
        self.arm = tArm.rotate(-(self.angle + 90), expand = True)
        self.armTk = ImageTk.PhotoImage(self.arm)
    
    def seesPlayer(self, player):
        x = player.x
        y = player.y
        # find the two legs of the right triangle made by the shooter arm and 
        # the center of the tank
        dx = x - self.x
        dy = y - self.y
        # avoids division by 0 errors for the 90 and 270 degrees
        if dx == 0 and dy < 0:
            angle = 270
        elif dx == 0 and dy > 0:
            angle = 90
        else:
            angle = math.degrees(math.atan(dy / dx))
            # accounts for the lower half of the unit circle
            if dx < 0:
                angle += 180
        #print(self.angle, angle)
        if math.isclose(self.angle, angle, rel_tol = 0.08):
            return True
        return False
        

class MovingTank(Tank):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle)
        self.speed = 2
        
        body = Image.open("MovingTank.gif")
        self.bodyO = body.copy().resize((75, 100)).convert('RGBA')
        self.body = self.bodyO.copy()
        #self.body.show()
        arm = Image.open("MovingArm.gif")
        self.armO = arm.copy().resize((38, 150)).convert('RGBA')
        self.arm = self.armO.copy()
        self.bodyTk = ImageTk.PhotoImage(self.body)
        self.armTk = ImageTk.PhotoImage(self.arm)
    
    def move(self, player, wall, screenWidth, screenHeight, margin):
        
        x, y = self.body.size
        #print(hitWall)
        # hitting the right side of the window
        if (self.x + (x // 2) > screenWidth - margin)\
        or (self.x - (x // 2) < margin) \
        or (self.y + (y // 2) > screenHeight - margin) \
        or (self.y - (y // 2) < margin):
            return
        
        pX = player.x
        pY = player.y
        hit = self.wallHit(wall)
        
        dx = pX - self.x
        dy = pY - self.y
        #print(dx, dy)
        # avoids division by 0 errors for the 90 and 270 degrees
        if dx == 0 and dy < 0:
            #print("dx = 0")
            self.rotate = 0
        elif dx == 0 and dy > 0:
            #print("dx = 0 and dy > 0")
            self.rotate = 180
        elif dy == 0 and dx < 0:
            self.rotate = 90
        elif dy == 0 and dx > 0:
            self.rotate = 270
        else:
            if dx <= 0 and dy < 0:
               # print("2nd")
                self.rotate = math.degrees(math.atan(dx / dy))
            elif dx < 0 and dy >= 0:
               # print("3rd")
                self.rotate = abs(math.degrees(math.atan(dy / dx))) + 90
            elif dx >= 0 and dy > 0:
               # print("4th")
                self.rotate = math.degrees(math.atan(dx / dy)) + 180
            elif dx > 0 and dy <= 0:
               # print("1st")
                self.rotate = abs(math.degrees(math.atan(dy / dx))) + 270
        #print("Moving Tank", self.rotate)
        self.rotateTank()
        if hit:
           # print("moving hit wall")
            self.x += self.speed * math.cos(math.radians(270 + self.rotate))
            self.y += self.speed * math.sin(math.radians(90 + self.rotate))
            self.rotate += 90
            self.rotateTank()
            dist = 0
            while dist < 10:
                self.x += self.speed * math.cos(math.radians(90 + self.rotate))
                self.y += self.speed * math.sin(math.radians(270 + self.rotate))
                dist += 1
        else:
            #print("moving tank not hit wall")
            self.x += self.speed * math.cos(math.radians(90 + self.rotate))
            self.y += self.speed * math.sin(math.radians(270 + self.rotate))
       
    
    
    def moveShooter(self, player):
        x = player.x
        y = player.y
        # find the two legs of the right triangle made by the shooter arm and 
        # the center of the tank
        dx = x - self.x
        dy = y - self.y
        # avoids division by 0 errors for the 90 and 270 degrees
        if dx == 0 and dy < 0:
            self.angle = 270
        elif dx == 0 and dy > 0:
            self.angle = 90
        else:
            self.angle = math.degrees(math.atan(dy / dx))
            # accounts for the lower half of the unit circle
            if dx < 0:
                self.angle += 180
        tArm = self.armO.copy()
        self.arm = tArm.rotate(-(self.angle + 90), expand = True)
        self.armTk = ImageTk.PhotoImage(self.arm)

class SmartTank(Tank):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle)
        self.color = "green"
    
