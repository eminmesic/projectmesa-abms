from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from wood_carving.model import Artisan, ArtisanLearnerRelation

def artisan_learner_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Artisan:
        portrayal["Shape"] = "wood_carving/resources/artisan_expert.png"
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 1

    return portrayal

canvas_element = CanvasGrid(artisan_learner_portrayal, 15, 15, 600, 600)
chart_element = ChartModule([{"Label": "Artisan Expert", "Color": "#AA0000"},
                             {"Label": "Artisan Learner", "Color": "#0000AA"}])

<<<<<<< HEAD
model_params = {"initial_artisan_expert": UserSettableParameter('slider', 'Initial Artisan Expert Population', 20, 1, 100),
                "initial_artisan_learner": UserSettableParameter('slider', 'Initial Artisan Learner Population', 10, 1, 100)}
=======
model_params = {"sex": UserSettableParameter('checkbox', 'Gender', True),
                "knowledge": UserSettableParameter('slider', 'Knowledge', 20, 1, 100)}
>>>>>>> 688dde2468761190d1d94825b6c8e86eb3b351b9

server = ModularServer(ArtisanLearnerRelation, [canvas_element, chart_element], "Artisan Learner Relation", model_params)
server.port = 8521