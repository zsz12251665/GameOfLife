import numpy as np
from GameOfLife import ConwayGame, PrototypeGame
from PIL import Image
import matplotlib.pyplot as plt

conway = ConwayGame(ConwayGame.commonModels.Oscillators.Pentadecathlon, loopingBound=False)
conway.startAnimation(interval=100)

conway.playground = np.pad(ConwayGame.commonModels.Guns.GGG, ((0, 20), (0, 20))) # Gosper Glider Gun
conway.startAnimation(interval=100)

conway.loopingBound = True # Change parameters
conway.playground = np.tile(ConwayGame.buildPlayground("bo$2bo$3o!", charset="ob$"), (10, 10)) # RLE from conwaylife.com
conway.startAnimation(interval=100)

img = Image.open(input()).convert("L") # Choose your image as the playground
proto = PrototypeGame(img, neighborhoodRange=2, aliveSwitches=[-1] * 5 + [0, 0, 1, 1, 1] + [-1] * 14 + [0])  # Design your own game
proto.startAnimation(showAnim=False, frames=50, saveAs={"filename": "test.gif", "writer": "imagemagick"})
