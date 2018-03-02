from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from model import ArtisanAgent, ArtisanModel

def artisan_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}

    # portrayal = {}

    # if type(agent) is Artisan:
    #     portrayal["Shape"] = "resources/artisan_expert.png"
    #     portrayal["scale"] = 0.9
    #     portrayal["Layer"] = 1

    return portrayal

grid_width = 15
grid_height = 15

grid = CanvasGrid(artisan_portrayal, grid_width, grid_height, 600, 600)
# chart_element = ChartModule([{"Label": "Artisan Expert", "Color": "#AA0000"},
#                              {"Label": "Artisan Learner", "Color": "#0000AA"}])

model_params = {"width": grid_width,
                "height": grid_height,
                "average_lifetime": UserSettableParameter('slider', 'Average lifetime', 50, 50, 100)}

server = ModularServer(ArtisanModel, [grid], "Artisan Learner Relation", model_params)
server.port = 8521