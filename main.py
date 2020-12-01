import numpy as np
from GameOfLife import ConwayGame, PrototypeGame
from PIL import Image
from tkinter.filedialog import askopenfilename

if __name__ == "__main__":
	conway = ConwayGame(ConwayGame.commonModels.Oscillators.Pentadecathlon, loopingBound=False)  # Construct a game object
	conway.startAnimation()

	conway.playground = np.pad(ConwayGame.commonModels.Guns.GGG, ((0, 20), (0, 20)))  # Change the playground with built-in model, Gosper Glider Gun
	conway.startAnimation(interval=100)

	conway.loopingBound = True  # Change parameters
	conway.playground = ConwayGame.buildPlayground("bo$2bo$3o!", charset="ob$")  # Change the playground with glider RLE from conwaylife.com
	conway.startAnimation(interval=100)

	img = Image.open(askopenfilename(title="Choose a file...")).convert("L")  # Choose your image as the playground
	proto = PrototypeGame(img, neighborhoodRange=2, cellBehaviour=[-1] * 5 + [0, 0, 1, 1, 1] + [-1] * 14 + [0])  # Design your own game
	proto.startAnimation(showAnim=False, frames=50, saveAs={"filename": "test4.gif", "writer": "imagemagick"})  # Save the animation
