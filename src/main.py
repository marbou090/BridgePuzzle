import pyxel

SCREEN_WIDTH = 200
SCREEN_HEIGHT = 200
NUM_INITIAL_NODE=17

class Vec2:
    def __init__(self, x, y,node,number,bridge_index):
        self.x = x
        self.y = y
        self.node_number=number
        self.node=node
        self.bridge_index_list=[]

class Vec1:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        

class Node:
    def __init__(self):
        #self.node_key= 0 #最初は通常ノードから。通常ノードはは0,0に格納されてるタイルなので0

        #横6,縦9マスにする
        self.r_x = pyxel.rndi(0, 6)
        self.r_y=pyxel.rndi(0,9)

        #ノードの番号を決める
        self.r_number=pyxel.rndi(0,6)

        #ノード一個が16幅なので、通常ノードは0なので
        self.pos = Vec2(
            self.r_x*16,
            self.r_y*16,
            0,
            self.r_number,
            []
        )
        
    
    def return_node_index(self,node,nodes):
        num_node = len(nodes)
        for i in range(num_node):
            if (node.pos.x == nodes[i].pos.x) and (node.pos.y == nodes[i].pos.y):
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
        nodes=[]
        for _ in range(max_node):
            while(True):
                node_tmp=(Node())
                node_len_tmp = len(nodes)
                #一個目であればそのままいれる
                if node_len_tmp==0:
                    nodes.append(node_tmp)
                    break

                #判定関数でヨシが出たらそこに生成
                if node_tmp.generate_node_judge(nodes,node_tmp):
                    nodes.append(node_tmp)
                    break
        return nodes
    
    def generate_node_judge(self,nodes,node_tmp):
        """
        既存のノードと位置を比べてそこにノード作って良いか判定
        """
        node_len_tmp=len(nodes)
        for i in range(node_len_tmp):
            #同じ場所には作らない
            if (node_tmp.pos.x == nodes[i].pos.x) and (node_tmp.pos.y == nodes[i].pos.y):
                return False

            #x軸について隣り合っては作らない
            if (((node_tmp.r_x + 1) == nodes[i].r_x) or ((node_tmp.r_x - 1) == nodes[i].r_x)) and (node_tmp.pos.y == nodes[i].pos.y):
                return False
            #y軸について隣り合っては作らない
            if (((node_tmp.r_y + 1) == nodes[i].r_y) or ((node_tmp.r_y - 1) == nodes[i].r_y)) and (node_tmp.r_x == nodes[i].r_x):
                return False
        return True

    
    def is_node_select(self,nodes):
        """
        クリック１つ目がすでにあるかどうかの判定をしてTrue or Falseで返したい。
        """
        num_node = len(nodes)
        for i in range(num_node):
            node=nodes[i]
            if node.pos.node==1:
                return True
        return False
    
    def print_all_node(self,nodes):
        """
        デバック用の全てのブリッジのステータスを確認できるところ
        """
        num_node = len(nodes)
        for i in range(num_node):
            node=nodes[i]
            print(f"X : {node.r_x}, Y : {node.r_y}, KEY : {node.pos.node}")
        print("-----------------")
    
    def key_all_initialize(self,nodes):
        """
        全てのステータスを初期化する
        """
        num_node = len(nodes)
        for i in range(num_node):
            nodes[i].pos.node=0
        return nodes
    
    def key_one_initialize(self,nodes):
        """
        ステータス1のものは、ノードでないてきとうなところをクリックしたらステータス0に戻す
        """
        num_node = len(nodes)
        for i in range(num_node):
            if nodes[i].pos.node==1:
                nodes[i].pos.node=0
        return nodes
    
    def key_one2two(self,node,nodes,bridges):
        """
        2つ選択したらステータス1のほうはステータス2にする
        """
        num_node = len(nodes)
        for i in range(num_node):
            #x軸かy軸が一緒で、間にノードがいなかったらステータスを2にする
            if self.judge_key_one2two(node,nodes[i],nodes):
                nodes[i].pos.node=2 
                nodes[self.return_node_index(node,nodes)].pos.node=2

                #ブリッジをかけるので、ブリッジリストにいれるインデックスをノード側で持っておく
                nodes[i].pos.bridge_index_list.append(len(bridges))
                nodes[self.return_node_index(node,nodes)].pos.bridge_index_list.append(len(bridges)-1)
                
                #ブリッジをかける処理
                break
        #一緒じゃなかったらステータス0に戻す
        else:
            for i in range(num_node):
                if nodes[i].pos.node==1:
                    nodes[i].pos.node=0
        return nodes

    def judge_key_one2two(self,node1,node2,nodes):
        """
        ノード2つについてブリッジを繋げて良いのかを判定する
        """
        if node2.pos.node==1:
            
            #x軸かy軸が一緒かどうか、間にノードはいないか
            
            if node2.pos.x==node1.pos.x and self.is_node_between(node1,node2,"x",nodes):
                #間に他のノードがいないか
                return True
                
            if node2.pos.y==node1.pos.y and self.is_node_between(node1,node2,"y",nodes):
                return True
        return False
                    
    
    def is_node_between(self,node1,node2,axis,nodes):
        """
        ノード１とノード２の間に他ノードがいないかを判別する。axisがxなら「x軸が一緒」、yなら「yが一緒」
        """
        if axis=="x":
            node1_position = node1.pos.y
            node2_position = node2.pos.y


            node_max = max(node1_position,node2_position)
            node_min = min(node1_position,node2_position)

            num_node = len(nodes)
            for i in range(num_node):
                if nodes[i].pos.y >node_min and nodes[i].pos.y <node_max and nodes[i].pos.x == node1.pos.x:
                    return False
            
            return True
        
        if axis=="y":
            node1_position = node1.pos.x
            node2_position = node2.pos.x


            node_max = max(node1_position,node2_position)
            node_min = min(node1_position,node2_position)

            num_node = len(nodes)
            for i in range(num_node):
                if nodes[i].pos.x >node_min and nodes[i].pos.x <node_max and nodes[i].pos.y == node1.pos.y:
                    return False
            
            return True
    def find_index_pair(self,nodes,index):
        """
        投げられたブリッジインデックスをもつノード返す。つまり返すのはノード２つ。
        """
        return_list=[]
        for i in range(len(nodes)):
            for t in range(len(nodes[i].pos.bridge_index_list)):
                if nodes[i].pos.bridge_index_list[t] == index:
                    return_list.append(nodes[i])
        return return_list

class Bridge:
    def __init__(self, x1, y1, x2, y2):
        self.pos1=Vec1(
            x1,
            y1
        )
        self.pos2=Vec1(
            x2,
            y2
        )
    
    
    



class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT,title="nodePuzzle")
        pyxel.mouse(True)
        pyxel.load("bridgepicture.pyxres")

        #NUM_INITIAL_NODEの数だけ同じところに生成しないように気をつけながらノードを生成する
        self.nodes = Node().generate_node(NUM_INITIAL_NODE)
        self.bridges=[]
        pyxel.run(self.update, self.draw)

    def update_node(self):
        num_node = len(self.nodes)
        #クリックでブリッジを繋げる処理
        #クリックしたら
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for i in range(num_node):
                
                node = self.nodes[i]
            
                #マウスクリックの判定をしたいので、円の中心とマウスの距離だしたい
                node_x = node.pos.x+8- pyxel.mouse_x
                node_y = node.pos.y+8- pyxel.mouse_y
            
                #半径より近いか（そのノードをクリックしているか）
                if node_x*node_x+node_y*node_y<8*8:
                    #ノードステータスが通常かつ他に選択されたノードがなかったら、選択ステータスに変えるだけ
                    if node.pos.node==0 and not node.is_node_select(self.nodes):
                        node.pos.node=1
                        
                    #ノードステータスが通常かつ他に選択されたノードがあったら、そこの間にブリッジを繋げる
                    elif node.pos.node==0 and node.is_node_select(self.nodes):
                        self.nodes=node.key_one2two(node,self.nodes,self.bridges)

                    #ノードクリックしてる子がいたところでbreakしないとステータス2にならないバグがおきる(ノードの順番の前後でステータス2ならないバグ)
                    break
                    
            #てきとうなところクリックされたらステータス1のノードはステータス0にする（これはこのノードをクリックしてなくても行う）
            else:
                self.nodes = node.key_one_initialize(self.nodes)
        
    def update_bridge(self,nodes):
        #ブリッジを繋げる処理
        node_index=0
        self.bridges=[]
        #ブリッジのインデックス０から順にノードのブリッジインデックスリストを見ていき、
        #インデックスがあればそこのをブリッジにいれる
        while(True):
            index_node_list=nodes[0].find_index_pair(nodes,node_index)
            #まだ橋を一個もかけてないとかのときは抜ける
            if len(index_node_list)<=node_index or len(index_node_list)==0:
                break
            #ここのx座標とかy座標の調節はまったくしてない
            self.bridges.append(Bridge(index_node_list[node_index].pos.x+16,index_node_list[node_index].pos.y,index_node_list[node_index].pos.x,index_node_list[node_index].pos.y))
            node_index=node_index+1
            

    def update(self):
        # 終わりボタン(q)
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.update_node()
        self.update_bridge(self.nodes)


    def draw(self):
        pyxel.cls(0)

        #ノードの描画
        for node in self.nodes:
            pyxel.blt(node.pos.x, node.pos.y, 0, node.pos.node_number*16, node.node_state(node.pos.node), 16, 16)
        for bridge in self.bridges:
            pyxel.blt(bridge.pos1.x,bridge.pos2.x,0,48,0,16,16)

App()