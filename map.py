from wall import Wall

class Map:
    def __init__(self):
        self.walls = []

    def add(self, wall: Wall):
        self.walls.append(wall)

    def draw(self, surface):
        for wall in self.walls:
            wall.draw(surface)