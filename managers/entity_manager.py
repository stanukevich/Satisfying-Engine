class EntityManager:
    def __init__(self):
        self.entities = []

    def add(self, entity):
        self.entities.append(entity)

    def update(self, dt):
        for entity in self.entities:
            entity.update(dt)  

    def draw(self, surface):
        for entity in self.entities:
            entity.draw(surface)