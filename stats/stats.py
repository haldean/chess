import chess
import material
import openings

class Stats(object):
    def __init__(self, game, eco_data):
        self.opening, self.possible_openings = (
            openings.opening_stats(game, eco_data))
        self.white_material, self.black_material = (
            material.material_values(game))
        if self.white_material > self.black_material:
            self.material_advantage = chess.color_names[chess.white]
        elif self.black_material > self.white_material:
            self.material_advantage = chess.color_names[chess.black]
        else:
            self.material_advantage = None
        self.material_difference = abs(self.white_material - self.black_material)
