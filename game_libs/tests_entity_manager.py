import unittest
from game_libs.entity_manager import EntityManager


class MockEntity():
    def __init__(self):
        self.name = "test"

    def draw(self):
        return "draw"


class MockEntityNoDrawMethod():
    def __init__(self):
        self.name = "test"


class TestsEntityManager(unittest.TestCase):

    def setUp(self):
        self.EM = EntityManager()

    def test_entity_add(self):
        self.EM.create_entity('TestEntity')
        self.assertIn('TestEntity', self.EM.entities)

    def test_entity_remove(self):
        ent = 'TestEntity'
        self.EM.create_entity(ent)
        self.EM.destroy_entity(ent)
        self.assertNotIn(ent, self.EM.entities)

    def test_entity_draw(self):
        e = MockEntity()
        self.EM.create_entity(e)
        self.EM.draw_entities()
        self.assertIn('draw', [res for res in self.EM.draw_entities()])

    def test_entity_draw_success(self):
        e = MockEntity()
        self.EM.create_entity(e)
        self.EM.draw_entities()
        self.assertTrue(self.EM.draw_entities())

    def test_has_no_draw_method(self):
        e = MockEntityNoDrawMethod()
        self.EM.create_entity(e)
        self.assertTrue(len([res for res in self.EM.draw_entities()]) < len(self.EM.entities))
