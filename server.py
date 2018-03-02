from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from model import ArtisanAgent, ArtisanModel

def artisan_portrayal(agent):
    portrayal = {"scale": 0.9, "Layer": 1}

    if agent.get_title() == "apprentice":
        portrayal["Shape"] = "images/apprentice.png"
    elif agent.get_title() == "master":
        portrayal["Shape"] = "images/master.png"
    elif agent.get_title() == "mentor":
        portrayal["Shape"] = "images/mentor.png"

    return portrayal

grid_width = 10
grid_height = 10

grid = CanvasGrid(artisan_portrayal, grid_width, grid_height, 600, 600)

model_params = {"width": grid_width,
                "height": grid_height,
                "initial_artisan_mentor": UserSettableParameter('slider', 'Intial artisan mentors', 2, 1, 15),
                "initial_artisan_student": UserSettableParameter('slider', 'Intial artisan student', 10, 1, 50),
                "average_lifetime": UserSettableParameter('slider', 'Average lifetime', 65, 50, 100)}

server = ModularServer(ArtisanModel, [grid], "Artisan Learner Relation", model_params)
server.port = 8521