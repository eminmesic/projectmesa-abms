import random

from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from util import ArtisanType

class ArtisanAgent(Agent):
    def __init__(self, unique_id, model, type, lifetime, age, knowledge):
        '''
            Configure agent with input data
        '''
        super().__init__(unique_id, model)
        self.type = type
        self.lifetime = lifetime
        self.age = age
        self.knowledge = knowledge
        self.teach_ability = random.uniform(0.5, 1)
        self.affinity = random.uniform(0, 1)
        self.education = 0 # max education if 4 years (in months)
        self.teacher = None

    def step(self):
        '''
            Method called for every step of our agent
        '''
        self.age += self.model.step_time / 12.0
        self.education += self.model.step_time / 12.0

        self.move()
        self.knowledge_transfer()
        self.check_lifetime()

    def move(self):
        '''
            Method set the configuration of moving our agent over the grid
        '''
        if self.type == ArtisanType.MENTOR or self.type == ArtisanType.APPRENTICE:
            return

        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def knowledge_transfer(self):
        if self.education >= 4 and self.knowledge < 0.2:
            self.remove_agent()
            return
        elif self.education >= 4 and self.type == ArtisanType.APPRENTICE:
            self.teacher = None
            self.type = ArtisanType.MASTER
        elif self.knowledge >= 0.6 and (self.type == ArtisanType.MASTER or self.type == ArtisanType.APPRENTICE):
            self.teacher = None
            self.model.grid.move_to_empty()
            self.type = ArtisanType.MENTOR

        if self.type == ArtisanType.APPRENTICE and self.teacher:
            '''
                Calculate knowled with formula 
                (Zm - Zt) * M * L / t
                (Mentor knowledge - Apprentice knowledge) * Mentor teach ability * Apprentice affinity / (year * month / step time)
            '''
            self.knowledge += (self.teacher.knowledge - self.knowledge) * self.teacher.teach_ability * self.affinity / (4 * 12 / self.model.step_time)
        else:
            # self learning
            self.knowledge += 0.001

    def check_lifetime(self):
        '''
            Method check lifetime of agent and removes from model
        '''
        if self.age >= self.lifetime:
            self.remove_agent()

    def remove_agent(self):
        self.model.grid._remove_agent(self.pos, self)
        self.model.schedule.remove(self)

class ArtisanModel(Model):
    description = 'A model for simulating Artisan and Learner relation.'

    def __init__(self, width, height, initial_artisan_mentor, initial_artisan_apprentice, min_affinity, step_time, average_lifetime):
        '''
            Constructor method of our model
            Create model and configure with model parameters
        '''
        self.height = height
        self.width = width
        self.initial_artisan_mentor = initial_artisan_mentor
        self.initial_artisan_apprentice = initial_artisan_apprentice
        self.min_affinity = min_affinity
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
            age = float(random.randrange(15, lifetime))
            artisan = ArtisanAgent(unique_id, self, ArtisanType.MENTOR, lifetime, age, 0.6)
            self.grid.place_agent(artisan, self.grid.find_empty())
            self.schedule.add(artisan)

        '''
            Set up other agents
            Configure unique id
            Generate random lifetime
            Create agent
            Set newly created agent to the random position on grid and allow schedule
        '''
        for i in range(initial_artisan_apprentice):
            unique_id += 1
            lifetime = random.randrange(self.average_lifetime - 10, self.average_lifetime + 10)
            artisan = ArtisanAgent(unique_id, self, ArtisanType.APPRENTICE, lifetime, 15.0, 0)
            self.grid.place_agent(artisan, (random.randrange(self.width), random.randrange(self.height)))
            self.schedule.add(artisan)
        
        self.running = True
        self.is_started = False

    def step(self):
        '''
            method executed for every step triggered automatically or manually
        '''
        self.running = True
        if not self.is_started:
            self.sort_apprentice()
            self.is_started = True

        self.schedule.step() #this method called same method of agent

        # some specific logic on model level
        if self.schedule.get_agent_count() == 0:
            self.running = False
    
    def sort_apprentice(self):
        mentor_agents = [x for x in self.schedule.agents if x.type == ArtisanType.MENTOR]
        apprentice_agents = [x for x in self.schedule.agents if x.type == ArtisanType.APPRENTICE]

        mentor_agents = sorted([x for x in self.schedule.agents if x.type == ArtisanType.MENTOR], key=lambda m: m.affinity, reverse=True)
        apprentice_agents = sorted([x for x in self.schedule.agents if x.type == ArtisanType.APPRENTICE], key=lambda m: m.affinity, reverse=False)

        for mentor in mentor_agents:
            mentor_position = mentor.pos

            for i in range(5):
                if not apprentice_agents:
                    break

                apprentice = apprentice_agents.pop()
                if apprentice.affinity >= self.min_affinity:
                    possible_positions = self.grid.get_neighborhood(
                        mentor_position,
                        moore=False,
                        include_center=True)
                    new_position = random.choice(possible_positions)
                    apprentice.teacher = mentor
                    self.grid.move_agent(apprentice, new_position)
                else:
                    apprentice.remove_agent()

        if apprentice_agents:
           for apprentice in apprentice_agents:
                apprentice.remove_agent()