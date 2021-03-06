from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from model import ArtisanAgent, ArtisanModel
from util import ArtisanType

def canvas_calculation(grid):
    if grid > 15 and grid < 25:
        return grid * 35
    if grid >= 25:
        return 1000  
    return 600

def artisan_portrayal(agent):
    # grid people configuration
    portrayal = {"scale": 1, "text": round(agent.knowledge, 2)}

    if agent.type == ArtisanType.APPRENTICE and agent.teacher != None:
        portrayal["Shape"] = "images/apprentice.png"
        portrayal["Layer"] = 2
    elif agent.type == ArtisanType.APPRENTICE:
        portrayal["Shape"] = "images/apprentice_other.png"
        portrayal["Layer"] = 1
    elif agent.type == ArtisanType.MASTER:
        portrayal["Shape"] = "images/master.png"
        portrayal["Layer"] = 3
    elif agent.type == ArtisanType.MENTOR:
        portrayal["Shape"] = "images/mentor.png"
        portrayal["Layer"] = 4

    return portrayal

# grid configuration
grid_width = 20#int(input("Grid width: "))
grid_height = 20#int(input("Grid height: "))

canvas_width = canvas_calculation(grid_width)
canvas_height = canvas_calculation(grid_height)
grid = CanvasGrid(artisan_portrayal, grid_width, grid_height, canvas_width, canvas_height)
chart = ChartModule([{"Label": "Apprentice", "Color": "#000000"},
                     {"Label": "Master", "Color": "#6D0000"},
                     {"Label": "Mentor", "Color": "#996459"}], data_collector_name="total_collector")

# configure model params and form input values
model_params = {"width": grid_width,
                "height": grid_height,
                "disaster": UserSettableParameter('slider', 'Disaster in years (0 - no disaster)', 0, 0, 100, 20),
                "initial_artisan_mentor": UserSettableParameter('slider', 'Intial artisan mentors', 2, 1, 15),
                "initial_artisan_master": UserSettableParameter('slider', 'Intial artisan masters', 5, 0, 50, 5),
                "initial_artisan_apprentice": UserSettableParameter('slider', 'Intial artisan apprentice', 10, 5, 1000, 5),
                "max_apprentice_per_mentor": UserSettableParameter('slider', 'Max apprentice per mentor', 5, 1, 20),
                "step_time": UserSettableParameter('slider', 'Step time (month)', 6, 3, 12, 3),
                "average_lifetime": UserSettableParameter('slider', 'Average lifetime', 65, 50, 100)}

server = ModularServer(ArtisanModel, [grid, chart], "Artisan Learner Relation", model_params)
server.port = 8521