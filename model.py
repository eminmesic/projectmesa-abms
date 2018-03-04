import random

from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from util import ArtisanType

class ArtisanAgent(Agent):
    def __init__(self, unique_id, model, lifetime, knowledge):
        '''
            Configure agent with input data
        '''
        super().__init__(unique_id, model)
        self.lifetime = lifetime
        self.age = random.randrange(15, self.lifetime)
        self.knowledge = knowledge
        self.learn_ability = random.choice([True, False])
        self.teach_ability = random.choice([True, False])

    def get_title(self):
        '''
            Method helps us to check the person in the execution of other methods
        '''
        if self.knowledge < 0.4:
            return ArtisanType.APPRENTICE
        elif self.knowledge >= 0.4 and self.knowledge < 0.6:
            return ArtisanType.MASTER
        elif self.knowledge >= 0.6:
            return ArtisanType.MENTOR

    def step(self):
        '''
            Method called for every step of our agent
        '''
        self.move()
        self.knowledge_transfer()
        self.age += 1
    
        if self.age > self.model.average_lifetime:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)

    def move(self):
        '''
            Method set the configuration of moving our agent over the grid
        '''
        if self.get_title() == ArtisanType.MENTOR:
            return

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def knowledge_transfer(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        # Need definition of transfering knowledge
        pass

class ArtisanModel(Model):
    description = 'A model for simulating Artisan and Learner relation.'

    def __init__(self, width, height, initial_artisan_mentor, initial_artisan_student, step_time, average_lifetime):
        '''
            Constructor method of our model
            Create model and configure with model parameters
        '''
        self.height = height
        self.width = width
        self.initial_artisan_mentor = initial_artisan_mentor
        self.initial_artisan_student = initial_artisan_student
        self.step_time = step_time
        self.average_lifetime = average_lifetime

        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)

        # agent must have unique id
        unique_id = 0

        '''
            Set up mentors with specific configuration
            Configure unique id
            Generate random lifetime
            Create agent
            Set newly created agent to the random position on grid and allow schedule
        '''
        for i in range(self.initial_artisan_mentor):
            unique_id += 1
            lifetime = random.randrange(self.average_lifetime - 10, self.average_lifetime + 10)
            artisan = ArtisanAgent(unique_id, self, lifetime, 0.6)
            self.grid.place_agent(artisan, (random.randrange(self.width), random.randrange(self.height)))
            self.schedule.add(artisan)

        '''
            Set up other agents
            Configure unique id
            Generate random lifetime
            Create agent
            Set newly created agent to the random position on grid and allow schedule
        '''
        for i in range(initial_artisan_student):
            unique_id += 1
            lifetime = random.randrange(self.average_lifetime - 10, self.average_lifetime + 10)
            artisan = ArtisanAgent(unique_id, self, lifetime, random.uniform(0, 0.4))
            self.grid.place_agent(artisan, (random.randrange(self.width), random.randrange(self.height)))
            self.schedule.add(artisan)
        
        self.running = True

    def step(self):
        '''
            method executed for every step triggered automatically or manually
        '''
        self.running = True
        self.schedule.step() #this method called same method of agent

        # some specific logic on model level
        if self.schedule.get_agent_count() == 0:
            self.running = False