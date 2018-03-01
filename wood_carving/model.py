import random

from mesa import Model, Agent
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class Artisan(Agent):
    grid = None
    x = None
    y = None
    more = True

    def __init__(self, pos, model, more=True):
        super().__init__(pos, model)
        self.pos = pos
        self.more = more

    def random_move(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.more, True)
        next_move = random.choice(next_moves)
        self.model.grid.move_agent(self, next_move)

    def step(self):
        self.random_move()
        living = True    

class ArtisanLearnerRelation(Model):
    height = 20
    width = 20

    initial_artisan_expert = 20
    initial_artisan_learner = 10

    verbose = False

    description = 'A model for simulating Artisan and Learner relation.'

    def __init__(self, height=20, width=20,
                 initial_artisan_expert=20, initial_artisan_learner=10):
        
        self.height = height
        self.width = width
        self.initial_artisan_expert = initial_artisan_expert
        self.initial_artisan_learner = initial_artisan_learner

        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.testattr = 0
        self.datacollector = DataCollector(
            {"testattr": "testattr"},  # Model-level count of happy agents
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]})

        # Create artisan expert
        for i in range(self.initial_artisan_expert):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            artisanExpert = Artisan((x, y), self, True)
            self.grid.place_agent(artisanExpert, (x, y))

        # Create artisan learner
        for i in range(self.initial_artisan_learner):
            x = random.randrange(self.width)
            y = random.randrange(self.height)
            artisanLearner = Artisan((x, y), self, True)
            self.grid.place_agent(artisanLearner, (x, y))

        self.running = True
        # self.datacollector.collect(self)

        def step(self):
            # self.schedule.step()
            # collect data
            self.datacollector.collect(self)