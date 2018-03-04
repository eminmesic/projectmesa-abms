from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from model import ArtisanAgent, ArtisanModel
from util import ArtisanType

def artisan_portrayal(agent):
    # grid people configuration
    portrayal = {"scale": 0.9, "Layer": 1}

    if agent.get_title() == ArtisanType.APPRENTICE:
        portrayal["Shape"] = "images/apprentice.png"
    elif agent.get_title() == ArtisanType.MASTER:
        portrayal["Shape"] = "images/master.png"
    elif agent.get_title() == ArtisanType.MENTOR:
        portrayal["Shape"] = "images/mentor.png"

    return portrayal

# grid configuration
grid_width = 10
grid_height = 10
grid = CanvasGrid(artisan_portrayal, grid_width, grid_height, 600, 600)

# configure model params and form input values
model_params = {"width": grid_width,
                "height": grid_height,
                "initial_artisan_mentor": UserSettableParameter('slider', 'Intial artisan mentors', 2, 1, 15),
                "initial_artisan_student": UserSettableParameter('slider', 'Intial artisan student', 10, 1, 50),
                "step_time": UserSettableParameter('slider', 'Step time (month)', 6, 3, 12, 3),
                "average_lifetime": UserSettableParameter('slider', 'Average lifetime', 65, 50, 100)}

server = ModularServer(ArtisanModel, [grid], "Artisan Learner Relation", model_params)
server.port = 8521