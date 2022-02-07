import pyxel

MOUSE_KEY=0
SELECT_KEY=0 #0で通常、1で選択
NODE_STATE=0 #0で通常、1で満タン


class Bridge:
    def __init__(self):
        self.node= 0 #通常ノードは0,0に格納されてるタイルなので0
    
    def node_state(self,state_key):
        if state_key==1:
            #選択されたら選択ノードを出すので0,32に入っているタイルを返したい
            self.node=32
        else:
            self.node=0
        return self.node
        
        

class App:
    def __init__(self):
        pyxel.init(200, 200,title="BridgePuzzle")
        pyxel.mouse(True)
        pyxel.load("bridgepicture.pyxres")
        self.bridge=Bridge()
        self.select_key=0
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
            
        #クリックしたら選択ノードになって、もう一度クリックで戻す
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.select_key==0:
            self.select_key=1
        elif pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.select_key==1:
            self.select_key=0
        
        pyxel.blt(0, 0, 0, 0, self.bridge.node_state(self.select_key), 16, 16)

App()