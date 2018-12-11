
import math
import tankClass
import wallClass

#### Bullet Class ####

class Bullet(object):
    def __init__(self, x, y, angle):
        self.angle = angle
        self.speed = 10
        self.x = x
        self.y = y
        self.r = 5
        self.numWallsHit = 0
        
    def __repr__(self):
        return "Bullet " + str(self.angle)
    
    def moveBullet(self):
        self.x += self.speed * math.cos(math.radians(self.angle))
        self.y += self.speed * math.sin(math.radians(self.angle))
    
    def reactToWallHit(self, screenWidth, screenHeight, margin):
        # hits the left or right side of the window
        if self.x + self.r >= screenWidth - margin or self.x - self.r <= margin:
            self.angle = 180 - self.angle
            self.numWallsHit += 1
        # hits the top or bottom of the window
        elif self.y - self.r <= margin or self.y + self.r >= screenHeight - margin:
            self.angle = -self.angle
            self.numWallsHit += 1
    
    def hitsTank(self, tank):
        if not isinstance(tank, tankClass.Tank):
            return False
        else:
            x, y = tank.body.size
            if (tank.x - (x/2)) <= self.x <= (tank.x + (x/2)) and (tank.y - (y/2)) <= self.y <= (tank.y + (y/2)):
                return True 
            # dist = math.sqrt((tank.x - self.x) ** 2 + (tank.y - self.y) ** 2)
            return False
    
    def hitsWall(self, wall):
        x1 = wall.x1
        y1 = wall.y1
        x2 = wall.x2
        y2 = wall.y2
        if ((x1 <= self.x + self.r <= x2) or (x1 <= self.x - self.r <= x2)) and ((y1 <= self.y + self.r <= y2) or (y1 <= self.y - self.r <= y2)):
            if isinstance(wall, wallClass.DestructibleWall):
                print(wall, wall.hits)
                wall.hits += 1
                wall.color = "sienna2"
            return True
    
    # graphics of bullet (use online graphics for cool looking bullet)
    def draw(self, canvas):
        canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill = "white")
        
        