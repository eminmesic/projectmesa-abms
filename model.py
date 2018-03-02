import random

from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class ArtisanAgent(Agent):
    def __init__(self, unique_id, model, lifetime):
        super().__init__(unique_id, model)
        self.lifetime = lifetime
        self.age = random.randrange(15, self.lifetime)

    def step(self):
        self.move()
        self.age += 1

        if self.age > self.lifetime:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

class ArtisanModel(Model):
    description = 'A model for simulating Artisan and Learner relation.'

    def __init__(self, width, height, average_lifetime):
        self.height = height
        self.width = width
        self.lifetime = average_lifetime

        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)

        # Set up agents
        for i in range(10):
            x = random.randrange(self.width)
            y = random.randrange(self.height)

            artisan = ArtisanAgent(i, self, self.lifetime)
            self.grid.place_agent(artisan, (x, y))
            self.schedule.add(artisan)
        
        self.running = True

    def step(self):
        self.schedule.step()

        if self.schedule.get_agent_count() == 0:
            self.running = False