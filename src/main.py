import pyxel

class App:
    def __init__(self):
        pyxel.init(200, 200,title="BridgePuzzle")
        pyxel.load("bridgepicture.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            pyxel.blt(0, 0, 0, 0, 16, 16, 16)
        else:
            pyxel.blt(0, 0, 0, 0, 0, 16, 16)

App()