from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from wood_carving.model import Artisan, ArtisanLearner

def artisan_learner_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    # if type(agent) is Artisan:
    #     portrayal["Shape"] = "wolf_sheep/resources/sheep.png"
    #     # https://icons8.com/web-app/433/sheep
    #     portrayal["scale"] = 0.9
    #     portrayal["Layer"] = 1

    # Definition of portrayal here

    return portrayal

canvas_element = CanvasGrid(artisan_learner_portrayal, 20, 20, 500, 500)
chart_element = ChartModule([{"Label": "Artisan", "Color": "#AA0000"}])

model_params = {"sex": UserSettableParameter('checkbox', 'Gender', True),
                "knowledge": UserSettableParameter('slider', 'Knowledge', 20, 1, 100)}

server = ModularServer(ArtisanLearner, [canvas_element, chart_element], "Artisan Learner Relationship", model_params)
server.port = 8521