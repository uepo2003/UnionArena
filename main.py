from ginfo import *
from deck_list import decks
from random import *
from log_class import GameLog
#ゲームボードの作成
def make_bord(player1_deck,player2_deck):
    player1_info = {"deck":player1_deck,
                    "front_line":[JJK006,JJK037,JJK036,None],
                    "energy_line":[None,None,None,None],
                    "life":[],
                    "hand":[],
                    "trash":[],
                    "remove":[],
                    "observe":[],
                    "action_point":0}

    player2_info = {"deck":player2_deck,
                    "front_line":[JJK001,JJK016,None,None],
                    "energy_line":[None,None,None,None],
                    "life":[],
                    "hand":[],
                    "trash":[],
                    "remove":[],
                    "observe":[],
                    "action_point":0}
    
    global log_maneger
    log_maneger = GameLog()

    return [player1_info,player2_info]

#常時監視関数をlogの結果から実行非実行させる
def monitoring(log,log_observer):
    for func in log_observer:
        func(log)

#手札とライフの用意
##どう考えてもこれとゲームボードの作成の処理くっつけたほうが軽くなるなぁ
def standby(info):
    print("バトルの準備をします。")
    #手札の設定
    shuffle(info["deck"])
    for _ in range(7):
        info["hand"].append(info["deck"].pop())
    
    print(f"\n手札です\n{[i.No for i in info['hand']]}")
    
    #マリガン機能
    ##ここの処理軽くできる可能性あり
    if input("\nマリガンしますか？。0か1で入力してください") == "1":
        
        for _ in range(7):
            info["deck"].insert(0,info["hand"].pop())
        for _ in range(7):
            info["hand"].append(info["deck"].pop())
        shuffle(info["deck"])
        print("マリガンしました")
        print(f"手札です\n{[i.No for i in info['hand']]}")
    input("\nキーを入力してください")
    #ライフの設定
    for _ in range(7):
        info["life"].append(info["deck"].pop())
    
    return info   
 

#スタートフェイズ
def start_phaze(info,first,turn):
    print("スタートフェイズ！")
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
        print(f'ドローしたカード:{info["hand"][-1].No}')

    #エクストラドロー
    ##一枚目のカードを見せてからex_drawをするかどうか選択させる
    print(f"手札:{[i.No for i in info['hand']]}")
    if input("エクストラドローしますか？。1か0で入力してください") == "1":
        info["action_point"] -= 1
        info["hand"].append(info["deck"].pop())
        print(f"ドローしたカード:{info['hand'][-1].No}")
    
    return info

def move_faze(info):
    print("移動フェイズ！")
    while True:
        print(split_gui)
        print(f"""
front_line
{[i if i == None else i.No for i in info["front_line"]]}

energy_line
{[i if i == None else i.No for i in info["energy_line"]]}
              """)

        print("0.移動フェイズを終わる 1.移動させるキャラクターを選択する")
        num = int(input("0か1で選択してください"))
        if num == 0:
            input("移動フェイズを終了します。キーを入力してください")
            break
        if num == 1:
            print("移動させたいカードの座標を確認します。")
            target_line = input("ラインを入力してください")
            target_index = int(input("インデックス番号を入力してください"))
            if info[target_line][target_index] == None:
                print("移動対象を確認できなかったため移動をキャンセルします。")
                continue
            print("移動先の座標を確認します。")
            move_line = input("ラインを入力してください")
            move_index = int(input("インデックス番号を入力してください"))
            move_char(info,target_line,target_index,move_line,move_index)
    return info
        


#新生移動フェイズ
def move_char(info,target_line,target_index,move_line,move_index):
    target_char = info[target_line][target_index]
    move_char = info[move_line][move_index]

    if target_char.type == "field" and move_line == "front_line":
        print("フィールドカードはフロントラインに移動できません。")
        return info
    elif not (target_line == "front_line" and target_char.step) and move_line == "energy_line":
        print("ステップを持っていないフロントラインのキャラクターはエナジーラインに移動できません。")
        return info
    
    elif not move_char == None:
        choice = input("移動先に他のカードがあります。リムーブしますか？0か1で入力してください")
        if choice == "0":
            if  not (move_line == "front_line" and move_char.step) and target_line == "energy_line":
                print("ステップを持っていないフロントラインのキャラクターはエナジーラインに移動できません。")
                return info
            else:
                print("移動先のカードと場所を入れ替えます。")
                info[target_line][target_index] = move_char
                info[move_line][move_index] = target_char
                return info
        
        elif choice == "1":
            print("リムーブしました。")
            info["remove"].appned(move_char)
    
    print("移動が完了しました。")
    info[move_line][move_index] = target_char
    info[target_line][target_index] = None
    return info


#メインステップ
def main_faze(ally_info,enemy_info):
    print("メインステップ！")
    while True:
        print(split_gui)
        print("0.メインステップを終了する 1.手札からカードを使用する 2.起動メインを使う 3.盤面を確認する 4.墓地を確認する 5.リムーブエリアを確認する" )
        num = int(input("0~2で入力してください。"))

        if num == 0:
            print("メインステップを終了します。")
            break
        if num == 1:
            print(f"手札:{[[index,i.No] for index,i in enumerate(ally_info['hand'])]}")
            num_1 = int(input("使用したいカードのインデックス番号を入力してください。"))
            card = ally_info["hand"][num_1]
            ally_info, enemy_info = use_card(ally_info,enemy_info,card,num_1)
        if num == 2:
            print("起動メインを使用したいカードの座標を確認します。")
            line = input("対象のラインを入力してください")
            index = int(input("対象のインデックス番号を入力してください"))
            target_card = ally_info[line][index]
            if target_card.main_effect == []:
                print("対象は起動メインを持っていません")
                continue
            elif len(target_card.main_effect) == 1:
                ally_info, enemy_info = boot_main(ally_info,enemy_info,line,index,0)
            else:
                print(f"起動メイン:{[[m_index,i] for m_index,i in enumerate(target_card.main_effect)]}")
                main_index = int(input("どの起動メインを使用するかインデックス番号で入力してください"))
                ally_info, enemy_info = boot_main(ally_info,enemy_info,line,index,main_index)
        if num == 3:
            display_info(ally_info,enemy_info)
        if num == 4:
            display_trash(ally_info)
        if num == 5:
            display_remove(ally_info)

    return ally_info, enemy_info
        
#手札からカードを使用する
def use_card(ally_info,enemy_info,card,card_num):
    all_energy = sum([0 if char == None else char.out_E for char in ally_info["energy_line"]])
    AP = ally_info["action_point"]

    if not (card.summon_AP <= AP and card.summon_E <= all_energy):
        print("必要コストを満たしていません")
        return ally_info,enemy_info
    
    if card.type == "char":
        line = input("召喚するラインを入力してください")
        index = int(input("召喚するインデックス番号を入力してください"))
        if not ally_info[line][index] == None:
            choice = input("召喚先にカードがあります。リムーブしますか？0か1で入力してください")
            if choice == "0":
                return ally_info,enemy_info
            elif choice == "1":
                ally_info["remove"].append(ally_info[line][index])
                ally_info[line][index] = None  
        ally_info, enemy_info = card.use(ally_info,enemy_info,card_num,line,index)

    elif card.type == "field":
        index = int(input("召喚するインデックス番号を入力してください"))
        if not ally_info["energy_line"][index] == None:
            choice = input("召喚先にカードがあります。リムーブしますか？0か1で入力してください")
            if choice == "0":
                return ally_info,enemy_info
            elif choice == "1":
                ally_info["remove"].append(ally_info[line][index])
                ally_info[line][index] = None 
        ally_info, enemy_info = card.use(ally_info,enemy_info,card,card_num,index)

    elif card.type == "event":
        ally_info, enemy_info = card.use(ally_info,enemy_info,card,card_num)
    
    return ally_info, enemy_info


#起動メインを使う
def boot_main(ally_info,enemy_info,target_line,target_index,main_index):
    ally_info, enemy_info = ally_info[target_line][target_index].main_effect[main_index][1](ally_info,enemy_info)
    ally_info[target_line][target_index].main_effect[main_index][0] += 1
    return ally_info,enemy_info


#アタックフェイズ
def attack_faze(ally_info,enemy_info):
    print("アタックフェイズ！")
    
    while len([C for C in ally_info["front_line"] if not (C == None) and C.active == True]) > 0:
        print(split_gui)
        print("フロントライン")
        for element in ([index,char] if char == None else [index, char.No, char.active] for index, char in enumerate(ally_info["front_line"])):
            print(element,end=" ")
        print("\n0.アタックフェイズを終了する 1.アタックを行う")
        num = int(input("\n0か1で入力してください。"))
        
        if num == 0:
            break
        elif num == 1:
            num1 = int(input("アタックしたいキャラクターのインデックス番号を入力してください"))
            if ally_info["front_line"][num1] == None:
                print("座標にキャラクターが存在しません。")
                continue
            elif not(ally_info["front_line"][num1].active):
                print("レストではアタックできません。")
                continue
            else:
                ally_info, enemy_info = ally_info["front_line"][num1].attack(ally_info,enemy_info,num1)


    input("アタックフェイズを終了します。キーを入力してください")
    return ally_info,enemy_info
    

#エンドフェイズ
def end_faze(info):
    for front_char in info["front_line"]:
        if front_char != None and front_char.active == False:
            front_char.active = True

            for effect in front_char.main_effect:
                effect[0] = 0
    
    for energy_char in info["energy_line"]:
        if energy_char != None and energy_char.active == False:
            energy_char.active = True

            for effect in energy_char.main_effect:
                effect[0] = 0
    
    while len(info["hand"]) > 9:
        print("手札が8枚を超えています。リムーブエリアに移動するカードを選んでください")
        for index,card in enumerate(info["hand"]):
            print(f"{index}. {card.No} ",end="")
        
        num = int(input("インデックス番号で入力してください"))
        info["remove"].append(info["hand"].pop(num))


def display_info(ally_info,enemy_info):
    print(f"""{split_gui}
{[i if i == None else i.No for i in enemy_info["energy_line"]]}  
      
{[i if i == None else i.No for i in enemy_info["front_line"]]}  
enemy
------------------------------------------------------
ally              
{[i if i == None else i.No for i in ally_info["front_line"]]} 
            
{[i if i == None else i.No for i in ally_info["energy_line"]]}

hand               
{[i.No for i in ally_info["hand"]]}    

AP:{ally_info["action_point"]}
life:{len(ally_info["life"])}

{split_gui}""")

    
def display_trash(info):
    print(f"""

trash:{[i.No for i in info["trash"]]}

""")
    
def display_remove(info):
    print(f"""

remove:{[i.No for i in info["remove"]]}

""")



#完成までは関数のテストに使用
if __name__ == "__main__":
    p1_info, p2_info= make_bord(decks[0],decks[1])
    turn_num = 0
    counter = 0
    ally_info = p2_info
    enemy_info = p1_info
    split_turn = "============================================================"
    split_gui = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" 
    winner = None 
    loser = None

    print(split_turn)
    print("p1の準備です。")
    standby(p1_info)
    print(split_turn)
    print("p2の準備です。")
    standby(p2_info)
    print(split_turn)

    print(f"\n<ゲームを開始します！！>\n")
    
    while True:
        print(split_turn)
        counter += 1
        if counter % 2 == 0:
            first = "後攻"
            print(f"{first}{turn_num}ターン目！\n")
        else:
            turn_num += 1
            first = "先行"
            print(f"{first}{turn_num}ターン目！\n")
        
        temp = ally_info 
        ally_info = enemy_info
        enemy_info = temp

        ally_info = start_phaze(ally_info,first,turn_num)
        ally_info = move_faze(ally_info)
        ally_info, enemy_info = main_faze(ally_info,enemy_info)
        ally_info, enemy_info = attack_faze(ally_info,enemy_info)
        ally_info = end_faze(ally_info)









    
    


#テスト用コピペ
#    print([i.No for i in info["hand"]])
#    print([i.No for i in info["deck"]])