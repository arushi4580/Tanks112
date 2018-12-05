
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
        tBody = self.bodyO.copy()
        self.body = tBody.rotate(self.rotate, expand = True)
        self.bodyTk = ImageTk.PhotoImage(self.body)
        
    
    # moves the tank if it is not at the edge of the window and it is not hitting a wall
    def move(self, screenWidth, screenHeight, margin, hitWall, dir, currDir):
        x, y = self.body.size
        print(hitWall)
        # hitting the right side of the window
        if (self.x + (x // 2) <= screenWidth - margin)\
        and (self.x - (x // 2) >= margin) \
        and (self.y + (self.length // 2) <= screenHeight - margin or self.direction == [0, -1] or self.direction[1] == 0) \
        and (self.y - (self.length // 2) >= margin or self.direction == [0, 1] or self.direction[1] == 0) \
        and (hitWall == False or (hitWall == True and currDir != dir)):
            if currDir == "u":
                self.x += self.speed * math.cos(math.radians(90 + self.rotate))
                self.y += self.speed * math.sin(math.radians(270 + self.rotate))
            elif currDir == "d":
                self.x += self.speed * math.cos(math.radians(270 + self.rotate))
                self.y += self.speed * math.sin(math.radians(90 + self.rotate))
            # moves the shooter with the rest of the tank
            # self.endOfArmX = self.x + self.arm * math.cos(math.radians(self.angle))
            # self.endOfArmY = self.y + self.arm * math.sin(math.radians(self.angle))
    
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
        tArm = self.armO.copy()
        self.arm = tArm.rotate(-(self.angle + 90), expand = True)
        self.armTk = ImageTk.PhotoImage(self.arm)
        
    
    def wallHit(self, wall):
        x, y = self.body.size
        if not isinstance(wall, wallClass.Wall):
            return False
        # hits left side
        elif (wall.x2 >= self.x + (x / 2) >= wall.x1) and ((wall.y1 < self.y + (y / 2) < wall.y2) or (wall.y1 < self.y - (y / 2) < wall.y2)):
            print("hit left")
            return True
        # hits right side
        elif (wall.x2 >= self.x - (x / 2) >= wall.x1) and ((wall.y1 < self.y + (y / 2) < wall.y2) or (wall.y1 < self.y - (y / 2) < wall.y2)):
            print("hit right")
            #if self.direction[0] == -1:
            return True
        # hits bottom side
        elif (wall.y1 <= self.y - (y / 2) <= wall.y2) and ((wall.x2 > self.x + (x / 2) > wall.x1) or (wall.x2 > self.x - (x / 2) > wall.x1)):
            print("hit bottom")
            #if self.direction[1] == -1:
               # print("wrong way")
            return True
        # hits top side
        elif (wall.y1 <= self.y + (y / 2) <= wall.y2) and ((wall.x2 > self.x + (x / 2) > wall.x1) or (wall.x2 > self.x - (x / 2) > wall.x1)):
            print("hit top")
            #if self.direction[1] == 1:
            return True
        return False
    
    # tank graphics (use graphics from online for a cool looking tank)
    def draw(self, canvas):
        x, y = self.body.size
        x1, y1 = self.arm.size
        canvas.create_rectangle(self.x - (x/2), self.y - (y/2), self.x + (x/2), self.y + (y/2))
        canvas.create_image(self.x, self.y, image = self.bodyTk)
        canvas.create_rectangle(self.x - (x1/2), self.y - (y1/2), self.x + (x1/2), self.y + (y1/2))
        canvas.create_image(self.x, self.y, image = self.armTk)
        # canvas.create_rectangle(self.x - (self.width / 2), self.y - (self.length / 2), self.x + (self.width / 2), self.y + (self.length / 2), fill = self.color)
        # canvas.create_oval(self.x - 12, self.y - 12, self.x + 12, self.y + 12, fill = self.color)
        # canvas.create_line(self.x, self.y, self.x - 5 * math.cos(math.radians(self.angle)), self.y - 5 * math.sin(math.radians(self.angle)), fill = "black", width = 10)
        # canvas.create_line(self.x, self.y, self.endOfArmX, self.endOfArmY, fill = "black", width = 10)


#### Types of Tanks ####

class DumbTank(Tank):
    # graphics for dumb tank AI
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle)
        self.color = "brown"
        self.range = 120
        self.currRange = 0
        self.dir = 1
    
    def move(self, player, wall):
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
        self.color = "SteelBlue3"
    
    def wallHit(self, wall):
        if not isinstance(wall, wallClass.Wall):
            return False
        # hits left side
        elif (wall.x2 >= self.x + (self.width / 2) >= wall.x1) and ((wall.y1 < self.y + (self.length / 2) < wall.y2) or (wall.y1 < self.y - (self.length / 2) < wall.y2)):
            print("hit left")
            if self.direction[0] == 1:
                return "x"
        # hits right side
        elif (wall.x2 >= self.x - (self.width / 2) >= wall.x1) and ((wall.y1 < self.y + (self.length / 2) < wall.y2) or (wall.y1 < self.y - (self.length / 2) < wall.y2)):
            print("hit top")
            if self.direction[0] == -1:
                return "x"
        # hits bottom side
        elif (wall.y1 <= self.y - (self.length / 2) <= wall.y2) and ((wall.x2 > self.x + (self.width / 2) > wall.x1) or (wall.x2 > self.x - (self.width / 2) > wall.x1)):
            print("hit bottom")
            if self.direction[1] == -1:
                print("wrong way")
                return "y"
        # hits top side
        elif (wall.y1 <= self.y + (self.length / 2) <= wall.y2) and ((wall.x2 > self.x + (self.width / 2) > wall.x1) or (wall.x2 > self.x - (self.width / 2) > wall.x1)):
            print("hit top")
            if self.direction[1] == 1:
                return "y"
        return True
    
    def move(self, player, wall):
        pX = player.x
        pY = player.y
        hit = self.wallHit(wall)
        print(hit)
        if hit == "x":
            self.direction[0] = 0
        elif hit == "y":
            self.direction[1] = 0
        if pX > self.x:
            if hit != "x":
                self.direction[0] = 1
        elif pX < self.x:
            if hit != "x":
                self.direction[0] = -1
        elif pY > self.y:
            if hit != "y":
                self.direction[1] = 1
        elif pY < self.y:
            if hit != "y":
                self.direction[1] = -1
        print(self.direction)
        self.x += self.speed * self.direction[0]
        self.y += self.speed * self.direction[1]
        # moves the shooter with the rest of the tank
        self.endOfArmX = self.x + self.arm * math.cos(math.radians(self.angle))
        self.endOfArmY = self.y + self.arm * math.sin(math.radians(self.angle))
    
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
        self.endOfArmX = self.x + self.arm * math.cos(math.radians(self.angle))
        self.endOfArmY = self.y + self.arm * math.sin(math.radians(self.angle))

class SmartTank(Tank):
    def __init__(self, x, y, angle):
        super().__init__(x, y, angle)
        self.color = "green"
    
