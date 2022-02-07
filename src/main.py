import pyxel

SCREEN_WIDTH = 200
SCREEN_HEIGHT = 200
NUM_INITIAL_NODE=10

class Vec2:
    def __init__(self, x, y,node):
        self.x = x
        self.y = y
        self.node=node

class Bridge:
    def __init__(self):
        self.node_key= 0 #最初は通常ノードから。通常ノードはは0,0に格納されてるタイルなので0

        #横6,縦9マスにする
        self.r_x = pyxel.rndi(1, 6)
        self.r_y=pyxel.rndi(1,9)
        #ノード一個が16幅なので、通常ノードは0なので
        self.pos = Vec2(
            self.r_x*16,
            self.r_y*16,
            self.node_key
        )
    
    def node_state(self,state_key):
        if state_key==0:
            #デフォルト
            return 0
        elif state_key==1:
            #選択されたら選択ノードを出すので0,32に入っているタイルを返したい
            return 32
        elif state_key==2:
            #ブリッジすべて使っている
            return 16
        else:
            return 0
        


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT,title="BridgePuzzle")
        pyxel.mouse(True)
        pyxel.load("bridgepicture.pyxres")

        self.bridges = [Bridge() for _ in range(10)]

        pyxel.run(self.update, self.draw)

    def update(self):
        # 終わりボタン(q)
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        
        num_node = len(self.bridges)
        
        #クリックしたら選択ノードになって、もう一度クリックで戻す処理
        #クリックしたら
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for i in range(num_node):
                bridge = self.bridges[i]
                #マウスクリックの判定をしたいので、円の中心とマウスの距離だしたい
                node_x = bridge.pos.x+8- pyxel.mouse_x
                node_y = bridge.pos.y+8- pyxel.mouse_y

                #半径より近いか（そのノードをクリックしているか）
                if node_x*node_x+node_y*node_y<8*8:
                    #ノードステータスが通常なら、選択ノードに変える
                    if bridge.node_key==0:
                        bridge.node_key=1
                    #選択済みでもう一回クリックされたら通常に戻す
                    elif bridge.node_key==1:
                        bridge.node_key=0

    def draw(self):
        pyxel.cls(0)

        #ノードの描画
        for bridge in self.bridges:
            pyxel.blt(bridge.pos.x, bridge.pos.y, 0, 0, bridge.node_state(bridge.node_key), 16, 16)

App()