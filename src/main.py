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
    
    def return_node_index(self,bridge,bridges):
        num_node = len(bridges)
        for i in range(num_node):
            if (bridge.pos.x == bridges[i].pos.x) and (bridge.pos.y == bridges[i].pos.y):
                return i
    
    
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
    
    def generate_node(self,max_node):
        """
        最初のノードを作る処理
        """
        bridges=[]
        for _ in range(max_node):
            while(True):
                bridge_tmp=(Bridge())
                bridge_len_tmp = len(bridges)
                #一個目であればそのままいれる
                if bridge_len_tmp==0:
                    bridges.append(bridge_tmp)
                    break

                #判定関数でヨシが出たらそこに生成
                if bridge_tmp.generate_node_judge(bridges,bridge_tmp):
                    bridges.append(bridge_tmp)
                    break
        return bridges
    
    def generate_node_judge(self,bridges,bridge_tmp):
        """
        既存のノードと位置を比べてそこにノード作って良いか判定
        """
        bridge_len_tmp=len(bridges)
        for i in range(bridge_len_tmp):
            #同じ場所には作らない
            if (bridge_tmp.pos.x == bridges[i].pos.x) and (bridge_tmp.pos.y == bridges[i].pos.y):
                return False

            #x軸について隣り合っては作らない
            if (((bridge_tmp.r_x + 1) == bridges[i].r_x) or ((bridge_tmp.r_x - 1) == bridges[i].r_x)) and (bridge_tmp.pos.y == bridges[i].pos.y):
                return False
            #y軸について隣り合っては作らない
            if (((bridge_tmp.r_y + 1) == bridges[i].r_y) or ((bridge_tmp.r_y - 1) == bridges[i].r_y)) and (bridge_tmp.r_x == bridges[i].r_x):
                return False
        return True

    
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
    
    def key_all_initialize(self,bridges):
        """
        全てのステータスを初期化する
        """
        num_node = len(bridges)
        for i in range(num_node):
            bridges[i].node_key=0
        return bridges
    
    def key_one_initialize(self,bridges):
        """
        ステータス1のものは、ノードでないてきとうなところをクリックしたらステータス0に戻す
        """
        num_node = len(bridges)
        for i in range(num_node):
            if bridges[i].node_key==1:
                bridges[i].node_key=0
        return bridges
    
    def key_one2two(self,bridge,bridges):
        """
        2つ選択したらステータス1のほうはステータス2にする
        """
        num_node = len(bridges)
        for i in range(num_node):
            #x軸かy軸が一緒だったらステータス2にする
            if bridges[i].node_key==1 and (bridges[i].pos.x==bridge.pos.x or bridges[i].pos.y==bridge.pos.y):
                bridges[i].node_key=2
                bridges[self.return_node_index(bridge,bridges)].node_key=2
                break
        #一緒じゃなかったらステータス0に戻す
        else:
            for i in range(num_node):
                if bridges[i].node_key==1:
                    bridges[i].node_key=0
        return bridges
            



class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT,title="BridgePuzzle")
        pyxel.mouse(True)
        pyxel.load("bridgepicture.pyxres")

        #NUM_INITIAL_NODEの数だけ同じところに生成しないように気をつけながらノードを生成する
        self.bridges = Bridge().generate_node(NUM_INITIAL_NODE)
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
                        self.bridges=bridge.key_one2two(bridge,self.bridges)

                    #ノードクリックしてる子がいたところでbreakしないとステータス2にならないバグがおきる(ノードの順番の前後でステータス2ならないバグ)
                    break
                    
            #てきとうなところクリックされたらステータス1のノードはステータス0にする（これはこのノードをクリックしてなくても行う）
            else:
                self.bridges = bridge.key_one_initialize(self.bridges)
        
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