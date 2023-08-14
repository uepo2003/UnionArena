from ginfo import *
from deck_list import decks
from random import *

#ゲームボードの作成
def make_field(player1_deck,player2_deck):
    player1_info = {"deck":player1_deck,
                    "front_line":[JJK036,None,None,None],
                    "energy_line":[None,None,None,None],
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
    if input("0か1で入力してください") == "0":
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
    
    print(info["action_point"])

    #ドロー処理
    ##GUI作成時にはここで一度引いたカードを表示する機能を追加するのもいいかも
    if first == "先行" and turn == 1:
        pass
    else:
        info["hand"].append(info["deck"].pop())

    #エクストラドロー
    ##一枚目のカードを見せてからex_drawをするかどうか選択させる
    if input("1か0で入力してください") == "1":
        info["action_point"] -= 1
        info["hand"].append(info["deck"].pop())
    
    return info

#移動フェイズ
def move_phaze(info):
    move_chars = []
    for index,flont_char in enumerate(info["front_line"]):
        if flont_char.step:
            move_chars.





#完成までは関数のテストに使用
if __name__ == "__main__":
    p1_info, p2_info = make_field(decks[0],decks[1])
    pq_info = standby(p1_info)
    print(p2_info)
    start_phaze(p1_info,"先行",1)

#テスト用コピペ
#    print([i.No for i in info["hand"]])
#    print([i.No for i in info["deck"]])