import pyxel

SCREEN_WIDTH = 200
SCREEN_HEIGHT = 200
NUM_INITIAL_NODE=17

class Vec2:
    def __init__(self, x, y,node,number):
        self.x = x
        self.y = y
        self.node_number=number
        self.node=node
        

class Bridge:
    def __init__(self):
        self.node_key= 0 #最初は通常ノードから。通常ノードはは0,0に格納されてるタイルなので0

        #横6,縦9マスにする
        self.r_x = pyxel.rndi(0, 6)
        self.r_y=pyxel.rndi(0,9)

        #ノードの番号を決める
        self.r_number=pyxel.rndi(0,6)

        #ノード一個が16幅なので、通常ノードは0なので
        self.pos = Vec2(
            self.r_x*16,
            self.r_y*16,
            self.r_number,
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
    
    def is_node_select(self,bridges):
        """
        ブリッジを繋げるとき、２つクリックで選択して、そこにブリッジをかけたい。
        クリック１つ目がすでにあるかどうかの判定をしてTrue or Falseで返したい。
        """
        num_node = len(bridges)
        for i in range(num_node):
            bridge=bridges[i]
            if bridge.node_key==1:
                return True
        return False
    
    def print_all_bridge(self,bridges):
        """
        デバック用の全てのブリッジのステータスを確認できるところ
        """
        num_node = len(bridges)
        for i in range(num_node):
            bridge=bridges[i]
            print(f"X : {bridge.r_x}, Y : {bridge.r_y}, KEY : {bridge.node_key}")
        print("-----------------")
    
    def key_initialize(self,bridges):
        """
        ノードでないところをクリックしたらステータスをクリアする
        """
        num_node = len(bridges)
        for i in range(num_node):
            bridges[i].node_key=0
        return bridges
            



class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT,title="BridgePuzzle")
        pyxel.mouse(True)
        pyxel.load("bridgepicture.pyxres")

        self.bridges = []
        for _ in range(NUM_INITIAL_NODE):
            generate_frag=True
            while(generate_frag):
                bridge_tmp=(Bridge())
                bridge_len_tmp = len(self.bridges)
                if bridge_len_tmp!=0:
                    for i in range(bridge_len_tmp):
                        if (bridge_tmp.pos.x == self.bridges[i].pos.x) and (bridge_tmp.pos.y == self.bridges[i].pos.y):
                            break
                    else:
                        self.bridges.append(bridge_tmp)
                        generate_frag=False
                else:
                    self.bridges.append(bridge_tmp)
                    break

                if generate_frag==False:
                    break

                
                
                            

        pyxel.run(self.update, self.draw)

    def update_bridge(self):
        num_node = len(self.bridges)
        #クリックでブリッジを繋げる処理
        #クリックしたら
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for i in range(num_node):
                bridge = self.bridges[i]
            
                #マウスクリックの判定をしたいので、円の中心とマウスの距離だしたい
                node_x = bridge.pos.x+8- pyxel.mouse_x
                node_y = bridge.pos.y+8- pyxel.mouse_y
            
                #半径より近いか（そのノードをクリックしているか）
                if node_x*node_x+node_y*node_y<8*8:
                    #ノードステータスが通常かつ他に選択されたノードがなかったら、選択ステータスに変えるだけ
                    if bridge.node_key==0 and not bridge.is_node_select(self.bridges):
                        bridge.node_key=1
                        
                    #ノードステータスが通常かつ他に選択されたノードがあったら、そこの間にブリッジを繋げる
                    elif bridge.node_key==0 and bridge.is_node_select(self.bridges):
                        bridge.node_key=2
                    else:
                        bridge.node_key=1
                    break
                    
                #選択済みでてきとうなところクリックされたら通常に戻す（これはこのノードをクリックしてなくても行う）
            else:
                self.bridges = bridge.key_initialize(self.bridges)
        
        #ブリッジを繋げるために、xかyが同じであるか判定する
        
        #ブリッジを繋げるために、道中に他ノードがいないか判定する

    def update(self):
        # 終わりボタン(q)
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.update_bridge()


    def draw(self):
        pyxel.cls(0)

        #ノードの描画
        for bridge in self.bridges:
            
            pyxel.blt(bridge.pos.x, bridge.pos.y, 0, bridge.r_number*16, bridge.node_state(bridge.node_key), 16, 16)

App()