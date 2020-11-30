import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class PrototypeGame:
    """
    The prototype version of game of life, with neighborhood range and the behaviour of cells (changing to dead or alive or keeping status) adjustable

    Data Members:
        playground: a 2-Dimensional array-like (filling with 0 or 1), the original cell statuses in the "world"
        loopingBound: a boolean value, whether the rightmost column is adjust to the leftmost column and the top row is adjust to the bottom row (if not the outer space will be treated as full of dead cells all the time)
        neighborhoodRange: an integer, the range of neighbour cells which each cell will affects
        cellBehaviour: an array of {-1, 0, 1} with the length of $neighborhoodRange^2$, if the number of alive cells in the neighborhood range is $a$,
            when cellBehaviour[a] == -1, the cell will become a dead cell in the next generation;
            when cellBehaviour[a] == 0, the cell will not change its status in the next generation;
            when cellBehaviour[a] == 1, the cell will become an alive cell in the next generation.
    """
    def __init__(self, playground, *, loopingBound=False, neighborhoodRange=1, cellBehaviour=[-1, -1, 0, 1, -1, -1, -1, -1, -1]):
        self.playground = (np.array(playground) > np.max(playground) / 2) * 1
        self.neighborhoodRange = neighborhoodRange
        self.cellBehaviour = cellBehaviour
        self.loopingBound = loopingBound

    def __str__(self):
        return str(self.playground)

    def countNeighourCells(self, x, y):  # Count the number of alive cells in neighborhood range
        n, m = self.playground.shape
        x_l, x_r = x - self.neighborhoodRange, x + self.neighborhoodRange + 1
        y_l, y_r = y - self.neighborhoodRange, y + self.neighborhoodRange + 1
        if self.loopingBound:
            return np.sum([self.playground[i % n, j % m] for i in range(x_l, x_r) for j in range(y_l, y_r)]) - self.playground[x, y]
        else:
            return np.sum(self.playground[max(x_l, 0):min(x_r, n), max(y_l, 0):min(y_r, m)]) - self.playground[x, y]

    def nextGeneration(self):  # Calculate the next generation of all cells in the playground
        n, m = self.playground.shape
        status = np.array([[self.cellBehaviour[self.countNeighourCells(x, y)] for y in range(m)] for x in range(n)])
        return (status == 0) * self.playground + (status == 1) * 1 + (status == -1) * 0

    def startAnimation(self, *, showAnim=True, interval=200, saveAs=None, frames=None):  # Built-in method to show the animation of generaion iteration of the cells (Visualize the game)
        """
        showAnim: a boolean value, whether pop a window to show the animation
        interval: an integer, the minimal time interval between two frames (measured in milliseconds)
            P. S.
                When showAnim=True, the actual time interval might be larger due to the latency of rendering a frame in real time.
        saveAs: a dictionary with two key-value pairs "filename" and "writer", which is the filename and the writer of the output file
            e. g.
                saveAs={"filename": "animation.gif", "writer": "imagemagick"}  # Save the animation as a GIF image
                saveAs={"filename": "animation.mp4", "writer": "ffmpeg"}  # Save the animation as a video
            P. S.
                - Values in SaveAs will be passed to anim.save()
                - imagemagick and ffmpeg needs to be installed separately by "sudo apt install imagemagick ffmpeg"
        frames: an integer or an iterable object, the number of generations in the game
        """
        def init(*args):  # Initialize the figure
            im.set_array(self.playground)
            return im,

        def update(*args):  # Update the figure
            im.set_array(self.playground)
            self.playground = self.nextGeneration()
            return im,

        fig = plt.figure()
        plt.axis("off")
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        fig.canvas.set_window_title("Game of Life Animation")
        im = plt.imshow(self.playground, animated=True)
        anim = animation.FuncAnimation(fig, update, frames=frames, interval=interval, init_func=init, blit=True)
        if saveAs:  # Save to file
            anim.save(**saveAs)
        if showAnim:  # Show the animation
            plt.show()

    @staticmethod
    def buildPlayground(RLE, *, charset="AD,"):  # Generate the playground with RLE
        """
        RLE: a string in Run Length Encoding, recording the playground
        charset: a string or list of the type of characters.
            charset[0]: Alive Cells
            charset[1]: Dead Cells
            charset[2]: End Of Line (filling with dead cells at the end)
        """
        def decode(RLE):  # Decoding RLE
            res = []
            cnt = 0
            for ch in RLE:
                if "0" <= ch <= "9":
                    cnt = cnt * 10 + int(ch)
                elif ch in charset[0:2]:
                    res += [ch == charset[0]] * max(cnt, 1)
                    cnt = 0
            return res

        arr = list(map(decode, RLE.split(charset[2])))
        maxlen = max(map(len, arr))
        for row in arr:  # Filling with dead cells at the end
            row += [0] * (maxlen - len(row))
        return np.pad(arr, ((1, 1), (1, 1)))  # Buffer area to prevent structures affecting each other


class ConwayGame(PrototypeGame):
    """
    Conway's Game of Life, the original and the most common version of Game of Life

    Data Members:
        playground: a 2-Dimensional array-like (filling with 0 or 1), the original cell statuses in the "world"
        loopingBound: a boolean value, whether the rightmost column is adjust to the leftmost column and the top row is adjust to the bottom row (if not the outer space will be treated as full of dead cells all the time)
    """
    def __init__(self, playground, *, loopingBound=False):
        PrototypeGame.__init__(self, playground, loopingBound=loopingBound, neighborhoodRange=1, cellBehaviour=[-1, -1, 0, 1, -1, -1, -1, -1, -1])

    class commonModels:
        """
        A library of the most common structures in the Conway's Game of Life.
        Source: https://conwaylife.com/wiki/Category:Lists_of_patterns
        """
        class StillLifes:
            """
            A still life is a pattern that does not change from one generation to the next.
            """
            Block = PrototypeGame.buildPlayground("AA,AA")
            Beehive = PrototypeGame.buildPlayground("DAA,ADDA,ADDA,DAA")
            Loaf = PrototypeGame.buildPlayground("DAA,ADDA,DADA,DDA")
            Boat = PrototypeGame.buildPlayground("AA,ADA,DA")
            Ship = PrototypeGame.buildPlayground("AA,ADA,DAA")
            Tub = PrototypeGame.buildPlayground("DA,ADA,DA")
            Pond = PrototypeGame.buildPlayground("DAA,ADDA,DAA")

        class Oscillators:
            """
            An oscillator is a pattern that is a predecessor of itself.
            """
            Blinker = PrototypeGame.buildPlayground(",3A,")
            Toad = PrototypeGame.buildPlayground(",D3A,3A,")
            Beacon = PrototypeGame.buildPlayground("AA,A,3DA,DDAA")
            Pulsar = PrototypeGame.buildPlayground(",3D3A3D3A,,DA4DADA4DA,DA4DADA4DA,DA4DADA4DA,3D3A3D3A,,3D3A3D3A,DA4DADA4DA,DA4DADA4DA,DA4DADA4DA,,3D3A3D3A,")
            Pentadecathlon = PrototypeGame.buildPlayground(",,,3D3A,DDA3DA,DA5DA,,A7DA,A7DA,,DA5DA,DDA3DA,3D3A,,,")
            Clock = PrototypeGame.buildPlayground("DDA,ADA,DADA,DA")

        class Spaceships:
            """
            A spaceship is a finite pattern that returns to its initial state after a number of generations but in a different location.

            LWSS: Light-weight Spaceship
            MWSS: Middle-weight Spaceship
            HWSS: Heavy-weight Spaceship
            """
            Glider = PrototypeGame.buildPlayground("DA,DDA,3A")
            LWSS = PrototypeGame.buildPlayground("ADDA,4DA,A3DA,D4A,")
            MWSS = PrototypeGame.buildPlayground("DA,A3DA,5DA,A4DA,D5A,,")
            HWSS = PrototypeGame.buildPlayground("DDAA,A4DA,6DA,A5DA,D6A,,")

        class Guns:
            """
            A gun is a stationary pattern that repeatedly emits spaceships forever.

            GGG: Gosper Glider Gun
            """
            GGG = PrototypeGame.buildPlayground("24DA,22DADA,12DAA6DAA12DAA,11DA3DA4DAA12DAA,AA8DA5DA3DAA,AA8DA3DADAA4DADA,10DA5DA7DA,11DA3DA,12DAA")
