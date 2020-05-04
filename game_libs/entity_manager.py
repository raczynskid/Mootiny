class EntityManager:
    """class to handle creating and destroying entities in game
    created entites should be added to EntityManager, and all events should be handled through it"""

    def __init__(self):
        """initialize empty list to store existing entities"""
        self.entities = []

    def create_entity(self, entity):
        """add a new entity to the manager"""
        self.entities.append(entity)

    def destroy_entity(self, entity):
        """remove an entity from the manager"""
        self.entities.remove(entity)

    def draw_entities(self):
        """
        call draw method for all entites in manager
        if entity does not have callable "draw" method, raise AttributeError but proceed
        """
        for e in self.entities:
            try:
                yield e.draw()
            except AttributeError:
                print("Object cannot be drawn")
                pass
