import random

from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class Artisan(Agent):
    grid = None
    x = None
    y = None
    more = True
    energy = None

    def __init__(self, pos, model, more=True, energy = None):
        super().__init__(pos, model)
        self.pos = pos
        self.more = more
        self.energy = energy

    def random_move(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.more, True)
        next_move = random.choice(next_moves)
        self.model.grid.move_agent(self, next_move)

    def step(self):
        self.random_move()
        living = True

class ArtisanLearner(Model):
    height = 20
    width = 20

    knowledge = 0
    sex = None

    verbose = False

    description = 'A model for simulating Artisan and Learner relationship'

    def __init__(self, height=20, width=20, 
                       knowledge=0, sex=None):
        
        self.height = height
        self.width = width
        self.knowledge = knowledge
        self.sex = sex

        self.grid = MultiGrid(self.height, self.width, torus=True)