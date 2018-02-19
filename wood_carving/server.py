from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement

from wood_carving.model import WoodCarvingModel


class HappyElement(TextElement):
    '''
    Display a text count of how many happy agents there are.
    '''

    def render(self, model):
        return "Mentor carvers: " + str(model.happy)


def carving_draw(agent):
    '''
    Portrayal Method for canvas
    '''
    if agent is None:
        return
    portrayal = {"Shape": "circle", "r": 0.5, "Filled": "true", "Layer": 0}

    if agent.type == 0:
        portrayal["Color"] = "Green"
    else:
        portrayal["Color"] = "Blue"
    return portrayal

happy_element = HappyElement()
canvas_element = CanvasGrid(carving_draw, 20, 20, 600, 600)
happy_chart = ChartModule([{"Label": "happy", "Color": "Black"}])

server = ModularServer(WoodCarvingModel,
                       [canvas_element, happy_element, happy_chart],
                       "Wood-carving Model",
                       20, 20, 0.8, 0.2, 4)
