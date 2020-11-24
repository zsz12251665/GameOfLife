import numpy as np
from GameOfLife import ConwayGame

clg = ConwayGame(ConwayGame.commonModels.Oscillators.Pentadecathlon, loopingBound=False)
clg.startAnimation(interval=100)

clg.playground = np.pad(ConwayGame.commonModels.Guns.GGG, ((0, 20), (0, 20))) # Gosper Glider Gun
clg.startAnimation(interval=100)

clg.loopingBound = True
clg.playground = np.tile(ConwayGame.buildPlayground("bo$2bo$3o!", charset="ob$"), (10, 10)) # RLE from conwaylife.com
clg.startAnimation(interval=100)
