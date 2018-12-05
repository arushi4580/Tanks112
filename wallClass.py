
#### Environment ####

class Wall(object):
    def __init__(self, x, y):
        self.cx = x
        self.cy = y
        self.length = 70
        self.x1 = self.cx - (self.length // 2)
        self.y1 = self.cy - (self.length // 2)
        self.x2 = self.cx + (self.length // 2)
        self.y2 = self.cy + (self.length // 2)
        print(self.x1, self.y1, self.x2, self.y2)
    
    def __repr__(self):
        return "Wall " + str(self.cx) + " " +  str(self.cy)
    
    def draw(self, canvas, color = "sienna4"):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill = color)

class DestructibleWall(Wall):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = "sienna3"
        self.hits = 0
        
    def __repr__(self):
        return "Destructible Wall " + str(self.cx) + " " +  str(self.cy)
    
    def draw(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill = self.color)
        
        