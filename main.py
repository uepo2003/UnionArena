from ginfo import *
from deck_list import decks
from random import *

#ゲームボードの作成
def make_field(player1_deck,player2_deck):
    player1_info = {"deck":player1_deck,
                    "front_line":[JJK001,JJK016,None,None],
                    "energy_line":[JJK006,JJK024,None,None],
                    "life":[],
                    "hand":[],
                    "tarsh":[],
                    "remove":[],
                    "action_point":0}

    player2_info = {"deck":player2_deck,
                    "front_line":[None,None,None,None],
                    "energy_line":[None,None,None,None],
                    "life":[],
                    "hand":[],
                    "tarsh":[],
                    "remove":[],
                    "action_point":0}
    
    return [player1_info,player2_info]

#手札とライフの用意
##どう考えてもこれとゲームボードの作成の処理くっつけたほうが軽くなるなぁ
def standby(info):
    
    #手札の設定
    shuffle(info["deck"])
    for _ in range(7):
        info["hand"].append(info["deck"].pop())
    
    #マリガン機能
    ##ここの処理軽くできる可能性あり
    if input("マリガンです。0か1で入力してください") == "1":
        for _ in range(7):
            info["deck"].insert(0,info["hand"].pop())
        for _ in range(7):
            info["hand"].append(info["deck"].pop())
        shuffle(info["deck"])
    
    #ライフの設定
    for _ in range(7):
        info["life"].append(info["deck"].pop())
    
    return info   
 

#スタートフェイズ
def start_phaze(info,first,turn):
    #リフレッシュステップ
    for front_char in info["front_line"]:
        if front_char != None and front_char.active == False:
            front_char.active = True
    for energy_char in info["energy_line"]:
        if energy_char != None and energy_char.active == False:
            energy_char.active = True
    
    #アクションポイントの設定
    if first == "先行":
        if turn == 1:
            info["action_point"] = 1
        elif turn == 2:
            info["action_point"] = 2
        else:
            info["action_point"] = 3
    
    elif first == "後攻":
        if turn <= 2:
            info["action_point"] = 2
        else:
            info["action_point"] = 3 

    #ドロー処理
    ##GUI作成時にはここで一度引いたカードを表示する機能を追加するのもいいかも
    if first == "先行" and turn == 1:
        pass
    else:
        info["hand"].append(info["deck"].pop())

    #エクストラドロー
    ##一枚目のカードを見せてからex_drawをするかどうか選択させる
    if input("エクストラドローです。1か0で入力してください") == "1":
        info["action_point"] -= 1
        info["hand"].append(info["deck"].pop())
    
    return info


#移動フェイズ
##先に移動可能なキャラクター全てを各lineから取り出す→その後改めて再配置させる
##計2つの関数を作成する。できればくっつけた方が軽いのでGUIとの合わせ次第では一つにする

#移動可能なキャラクターを取り出す
def pickup_char(info):    
    move_chars = []
    for index,front_char in enumerate(info["front_line"]):
        if front_char != None and front_char.step:
            move_chars.append(info["front_line"].pop(index))
            info["front_line"].insert(index,None)
    
    for index,energy_char in enumerate(info["energy_line"]):
        if energy_char != None and energy_char.type == "char":
            move_chars.append(info["energy_line"].pop(index))
            info["energy_line"].insert(index,None)
    
    return info,move_chars

#再配置
##move_charsから取り出したキャラクター"全て"に対して行う。←これは組み合わせの際に実装
##引数のフォーマット:(info, move_chars*更新用, 配置先のライン名*front_line or energy_line, ラインの番号*0~3, 対象のキャラクター)
def relocation(info,move_chars,line,index,char):
    if info[line][index] == None:
        info[line][index] = char
        move_chars.remove(char)
    #配置先にキャラクターがあるならリムーブして配置
    else:
        ##この部分をポップで出したい
        if input("配置先にカードが存在します。リムーブしますか？0か1で入力してください") == 1:
            info["remove"].append(info[line].pop(index))
            info[line].insert(index,char)
            move_chars.remove(char)
        ##リムーブしない場合は勝手に処理をスキップ。かつmove_charsに更新が入らない
        ##move_charsの更新方法は少し無駄が入るな、、。要検討

    return info,move_chars





#完成までは関数のテストに使用
if __name__ == "__main__":
    p1_info, p2_info = make_field(decks[0],decks[1])
    
    print(f'front_line:{p1_info["front_line"]} energy_line:{p1_info["energy_line"]}')
    p1_info, move_chars = relocation(p1_info,"front_line",3,JJK036)
    p1_info, move_chars = relocation(p1_info,"front_line",0,JJK024)
    print(f'front_line:{p1_info["front_line"]} energy_line:{p1_info["energy_line"]}')

#テスト用コピペ
#    print([i.No for i in info["hand"]])
#    print([i.No for i in info["deck"]])