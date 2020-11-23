import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class GameOfLife:
    def __init__(self, playground, *, neighborhoodRange=1, aliveSwitches=[-1, -1, 0, 1, -1, -1, -1, -1, -1], loopingBound=False):
        self.playground = (np.array(playground) > 127) * 255
        self.neighborhoodRange = neighborhoodRange
        self.aliveSwitches = aliveSwitches
        self.loopingBound = loopingBound

    def __str__(self):
        return str(self.playground)

    def countNeighourCells(self, x, y):
        n, m = self.playground.shape
        p = self.playground / 255
        x_l, x_r = x - self.neighborhoodRange, x + self.neighborhoodRange + 1
        y_l, y_r = y - self.neighborhoodRange, y + self.neighborhoodRange + 1
        if self.loopingBound:
            return int(np.sum([p[i % n, j % m] for i in range(x_l, x_r) for j in range(y_l, y_r)]) - p[x, y])
        else:
            return int(np.sum(p[max(x_l, 0):min(x_r, n), max(y_l, 0):min(y_r, m)]) - p[x, y])

    def nextFrame(self):
        n, m = self.playground.shape
        status = np.array([[self.aliveSwitches[self.countNeighourCells(x, y)] for y in range(m)] for x in range(n)])
        self.playground = (status == 0) * self.playground + \
            (status == 1) * 255 + (status == -1) * 0

    def startAnimation(self, *, interval=200):
        def update(*args):
            im.set_array(self.playground)
            self.nextFrame()
            return im,

        fig = plt.figure()
        fig.canvas.set_window_title("Conway's Game of Life")
        im = plt.imshow(self.playground, animated=True)
        animation.FuncAnimation(fig, update, interval=interval)
        plt.show()

    @staticmethod
    def buildPlayground(string, *, charset="AD,"):
        def decode(string):
            res = []
            cnt = 0
            for ch in string:
                if "0" <= ch <= "9":
                    cnt = cnt * 10 + int(ch)
                elif ch in charset[0:2]:
                    res += ([255] if ch == charset[0] else [0]) * max(cnt, 1)
                    cnt = 0
            return res

        arr = list(map(decode, string.split(charset[2])))
        maxlen = max(map(len, arr))
        for row in arr:
            row += [0] * (maxlen - len(row))
        return np.pad(arr, ((1, 1), (1, 1)))


class ConwayGame(GameOfLife):
    def __init__(self, playground, *, loopingBound=False):
        GameOfLife.__init__(self, playground, loopingBound=loopingBound)

    class commonModels:
        """
        Source: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life#Examples_of_patterns
        See More: https://conwaylife.com/wiki/Category:Lists_of_patterns
        """
        class StillLifes:
            Block = GameOfLife.buildPlayground("AA,AA")
            Beehive = GameOfLife.buildPlayground("DAA,ADDA,ADDA,DAA")
            Loaf = GameOfLife.buildPlayground("DAA,ADDA,DADA,DDA")
            Boat = GameOfLife.buildPlayground("AA,ADA,DA")
            Ship = GameOfLife.buildPlayground("AA,ADA,DAA")
            Tub = GameOfLife.buildPlayground("DA,ADA,DA")
            Pond = GameOfLife.buildPlayground("DAA,ADDA,DAA")

        class Oscillators:
            Blinker = GameOfLife.buildPlayground(",3A,")
            Toad = GameOfLife.buildPlayground(",D3A,3A,")
            Beacon = GameOfLife.buildPlayground("AA,A,3DA,DDAA")
            Pulsar = GameOfLife.buildPlayground(",3D3A3D3A,,DA4DADA4DA,DA4DADA4DA,DA4DADA4DA,3D3A3D3A,,3D3A3D3A,DA4DADA4DA,DA4DADA4DA,DA4DADA4DA,,3D3A3D3A,")
            Pentadecathlon = GameOfLife.buildPlayground(",,,3D3A,DDA3DA,DA5DA,,A7DA,A7DA,,DA5DA,DDA3DA,3D3A,,,")
            Clock = GameOfLife.buildPlayground("DDA,ADA,DADA,DA")

        class Spaceships:
            """
            Glider: Glider
            LWSS: Light-weight Spaceship
            MWSS: Middle-weight Spaceship
            HWSS: Heavy-weight Spaceship
            """
            Glider = GameOfLife.buildPlayground("DA,DDA,3A")
            LWSS = GameOfLife.buildPlayground("ADDA,4DA,A3DA,D4A,")
            MWSS = GameOfLife.buildPlayground("DA,A3DA,5DA,A4DA,D5A,,")
            HWSS = GameOfLife.buildPlayground("DDAA,A4DA,6DA,A5DA,D6A,,")

        class Guns:
            """
            GGG: Gosper Glider Gun
            """
            GGG = GameOfLife.buildPlayground("24DA,22DADA,12DAA6DAA12DAA,11DA3DA4DAA12DAA,AA8DA5DA3DAA,AA8DA3DADAA4DADA,10DA5DA7DA,11DA3DA,12DAA")
