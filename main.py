from class_list import *
from random import *
from func_display import *
from make_deck import *
#ゲームボードの作成
def make_bord(p1_name,player1_deck,p1_origin,p2_name,player2_deck,p2_origin):
    player1_info = {"player_name":p1_name,
                    "deck":player1_deck,
                    "front_line":[None,None,None,None],
                    "energy_line":[None,None,None,None],
                    "life":[],
                    "hand":[],
                    "trash":[],
                    "remove":[],
                    "observe":[],
                    "origins":p1_origin,
                    "action_point":0}

    player2_info = {"player_name":p2_name,
                    "deck":player2_deck,
                    "front_line":[None,None,None,None],
                    "energy_line":[None,None,None,None],
                    "life":[],
                    "hand":[],
                    "trash":[],
                    "remove":[],
                    "observe":[],
                    "origins":p2_origin,
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
    #タイトルコール
    print(f"\n{split_turn}")
    print(f"{info['player_name']}のバトルの準備を開始します。")
    #手札の設定
    shuffle(info["deck"])
    for _ in range(7):
        info["hand"].append(info["deck"].pop())
    #手札の表示
    print(f"\n手札\n{[i.No for i in info['hand']]}")
    #マリガン機能
    ##ここの処理軽くできる可能性あり
    if input("\nマリガンしますか？。0か1で入力してください:") == "1":
        for _ in range(7):
            info["deck"].insert(0,info["hand"].pop())
        for _ in range(7):
            info["hand"].append(info["deck"].pop())
        shuffle(info["deck"])
        #手札の表示
        print(f"\nマリガン後の手札\n{[i.No for i in info['hand']]}")
    #ライフの設定
    for _ in range(7):
        info["life"].append(info["deck"].pop())
    #終了処理
    input("\n準備を終了します。キーを入力してください:")    
    return info   
 

#スタートフェイズ
def start_phaze(info,first,turn):
    #タイトルコール
    print(f"{split_faze}\n")
    print("<スタートフェイズ！>")
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
    if first == "先行" and turn == 1:
        pass
    else:
        info["hand"].append(info["deck"].pop())
        print(f'ドローしたカード:{info["hand"][-1].No}')
    #エクストラドロー
    ##一枚目のカードを見せてからエクストラドローをするかどうか選択させる
    print(f"手札:{[i.No for i in info['hand']]}")
    if input("\nエクストラドローしますか？。0か1で入力してください:") == "1":
        info["action_point"] -= 1
        info["hand"].append(info["deck"].pop())
        print(f"ドローしたカード:{info['hand'][-1].No}")
    
    input("スタートフェイズを終了します。キーを入力してください")
    return info

#移動フェイズ
def move_faze(info):
    #タイトルコール
    print(f"{split_faze}\n")
    print("<移動フェイズ！>")
    #メニュー選択ループ
    while True: 
        print(f"""\n{split_pop}
{[[index,i] if i == None else [index,i.No] for index,i in enumerate(ally_info["front_line"])]} 
            
{[[index,i] if i == None else [index,i.No] for index,i in enumerate(ally_info["energy_line"])]}
{split_pop}""")              
        #移動フェイズ行動選択
        print("\n[0.移動フェイズを終わる 1.移動させるキャラクターを選択する]")
        num = int(input("0か1で選択してください:"))
        #行動分岐
        #移動フェイズ終了処理
        if num == 0:
            input("\n移動フェイズを終了します。キーを入力してください")
            break
        #移動処理
        if num == 1:
            #座標を確認
            print("\n移動させたいカードの座標を確認します。")
            target_line, target_index = get_point()
            #Noneじゃないかどうか確認
            if info[target_line][target_index] == None:
                print("移動対象を確認できなかったため移動をキャンセルします。")
                continue
            #座標を確認
            print("移動先の座標を確認します。")
            move_line, move_index = get_point()
            #移動用関数の実行
            move_char(info,target_line,target_index,move_line,move_index)

    return info
        
#移動用関数
def move_char(info,target_line,target_index,move_line,move_index):
    #該当座標のキャラクターを取得
    target_char = info[target_line][target_index]
    move_char = info[move_line][move_index]
    #一定の条件化における移動不可を判定
    #フィールドカードがフロントラインに移動しようとした時
    if target_char.type == "field" and move_line == "front_line":
        print("フィールドカードはフロントラインに移動できません。")
        return info
    #ステップをもたないカードがエナジーラインに移動しようとした時
    elif not (target_line == "front_line" and target_char.step) and move_line == "energy_line":
        print("ステップを持っていないフロントラインのキャラクターはエナジーラインに移動できません。")
        return info
    #カードが既に配置されている時
    elif not move_char == None:
        #リムーブするかどうか確認を入れる
        choice = input("移動先に他のカードがあります。リムーブしますか？0か1で入力してください:")
        #リムーブしない場合。座標の入れ替えを行う。
        if choice == "0":
            #結果としてフロントラインのカードがエナジーラインに移動してしまう場合の例外処理
            if  not (move_line == "front_line" and move_char.step) and target_line == "energy_line":
                print("ステップを持っていないフロントラインのキャラクターはエナジーラインに移動できません。")
                return info
            #座標の入れ替え処理
            else:
                print("移動先のカードと場所を入れ替えます。")
                info[target_line][target_index] = move_char
                info[move_line][move_index] = target_char
                return info
        #リムーブする場合
        elif choice == "1":
            info["remove"].append(deepcopy(info["origins"][move_char.No]))
            print("リムーブしました。")
    #原則処理
    info[move_line][move_index] = target_char
    info[target_line][target_index] = None
    print("移動が完了しました。")

    return info


#メインステップ
def main_faze(ally_info,enemy_info):
    #タイトルコール
    print(f"{split_faze}\n")
    print("<メインステップ！>")
    #メニュー制御ループ
    while True:
        #盤面の表示
        display_info(ally_info,enemy_info)
        #メインステップ行動選択
        print("\n[0.メインステップを終了する 1.手札からカードを使用する 2.起動メインを使う 3.墓地を確認する 4.リムーブエリアを確認する 5.相手の情報を確認する]" )
        num = int(input("0~5で入力してください:"))
        #選択分岐
        #終了処理
        if num == 0:
            input("\nメインステップを終了します。キーを入力してください")
            break
        #手札からカードを使用
        elif num == 1:
            #手札の一覧を表示→選ばれたカードを取得
            print(f"\n手札:{[[index,i.No] for index,i in enumerate(ally_info['hand'])]}")
            index_of_hand = int(input("使用したいカードのインデックス番号を入力してください:"))
            card = ally_info["hand"][index_of_hand]
            #カード使用時の関数を実行
            ally_info, enemy_info = use_card(ally_info,enemy_info,card,index_of_hand)
        #場のカードの起動メインを実行
        elif num == 2:
            print("起動メインを使用したいカードの座標を確認します。")
            #対象の座標を取得
            line, index = get_point()
            target_card = ally_info[line][index]
            #対象がない場合キャンセルを行う
            if target_card == None:
                print("対象が確認できません。キャンセルします。")
                return ally_info, enemy_info
            #対象の起動メインの数で分岐
            #0個の場合
            if target_card.EF == []:
                print("対象は起動メインを持っていません。")
                continue
            #1個の場合
            elif len(target_card.main_EF) == 1:
                ally_info, enemy_info = boot_main(ally_info,enemy_info,target_card,line,index,0)
            #複数個ある場合
            else:
                #起動メインの一覧を表示し、選択させる
                print(f"起動メインの一覧:{[[m_index,i] for m_index,i in enumerate(target_card.main_EF)]}")
                main_index = int(input("どの起動メインを使用するかインデックス番号で入力してください:"))
                ally_info, enemy_info = boot_main(ally_info,enemy_info,line,index,main_index)
        #トラッシュのカード一覧
        elif num == 3:
            display_trash(ally_info)
        #リムーブエリアのカード一覧
        elif num == 4:
            display_remove(ally_info)
        #相手の情報
        elif num == 5:
            display_enemy(enemy_info)
    
    return ally_info, enemy_info

#手札からカードを使用する
def use_card(ally_info,enemy_info,card,card_num):
    #コストを満たしているかどうか判定
    all_energy = sum([0 if char == None else char.out_E for char in ally_info["energy_line"]])
    AP = ally_info["action_point"]
    if not (card.summon_AP <= AP and card.summon_E <= all_energy):
        #偽の場合召喚をキャンセル
        print("必要コストを満たしていません。召喚をキャンセルします。")
        return ally_info,enemy_info
    #カードタイプ毎に処理を分ける
    #レイドカードの場合
    if card.type == "raid":
        raid_or_char = int(input("キャラクターとして召喚する場合は0を、レイドする場合は1を入力しください:\n"))
        #キャラクターとしての処理
        if raid_or_char == 0:
            #召喚先の座標を取得
            print("召喚先の座標を確認します。")
            line,index = get_point()
            #例外処理
            #召喚先にカードが有る場合リムーブの確認を行う
            if not ally_info[line][index] == None:
                choice = input("召喚先にカードがあります。リムーブしますか？0か1で入力してください:")
                #リムーブしない場合
                if choice == "0":
                    print("召喚をキャンセルします。")
                    return ally_info,enemy_info
                #リムーブする場合
                elif choice == "1":
                    ally_info["remove"].append(deepcopy(ally_info["origins"][ally_info[line][index].No]))
                    ally_info[line][index] = None
                    print("リムーブしました。")
            #原則処理
            ally_info, enemy_info = card.summon(ally_info,enemy_info,card_num,line,index)
        #レイドとしての処理
        if raid_or_char == 1:
            #レイド先の座標を取得
            print("レイドするキャタクターの座標を確認します。")
            line,index = get_point()
            #例外処理
            #レイド可能なキャラクター以外もしくはNoneの場合
            if not ally_info[line][index].name == card.raid_char:
                print("レイド可能なキャラクターではありません。召喚をキャンセルします。")
                return ally_info, enemy_info
            #原則処理
            else:
                #レイド後の移動を処理
                print("レイド後の移動先の座標を確認します。")
                moved_line,moved_index = get_point()
                #移動後の座標が同じではないかつNoneでもない＝リムーブが必要な場合の処理
                if not (moved_line == line and moved_index == index) and not ally_info[moved_line][moved_index] == None:
                    remove_or_not = int(input("移動先にカードが存在します。リムーブさせますか。0か1で入力してください:"))
                    if remove_or_not == 0:
                        print("召喚をキャンセルします。")
                        return ally_info,enemy_info
                    elif remove_or_not == 1:
                        ally_info["remove"].append(ally_info[moved_line].pop(moved_index))
                        ally_info[moved_line][moved_index] = None
                ally_info, enemy_info = card.raid(ally_info,enemy_info,card_num,line,index,moved_line,moved_index)

    #キャラクターカードの場合
    if card.type == "char":
        #召喚先の座標を取得
        print("召喚先の座標を確認します。")
        line,index = get_point()
        #例外処理
        #召喚先にカードが有る場合リムーブの確認を行う
        if not ally_info[line][index] == None:
            choice = input("召喚先にカードがあります。リムーブしますか？0か1で入力してください:")
            #リムーブしない場合
            if choice == "0":
                print("召喚をキャンセルします。")
                return ally_info,enemy_info
            #リムーブする場合
            elif choice == "1":
                ally_info["remove"].append(deepcopy(ally_info["origins"][ally_info[line][index].No]))
                ally_info[line][index] = None
                print("リムーブしました。")
        #原則処理
        ally_info, enemy_info = card.summon(ally_info,enemy_info,card_num,line,index)
    #フィールドカードの場合
    elif card.type == "field":
        #座標の取得
        print("召喚先の座標を確認します。")
        index = int(input("インデックス番号を入力してください:"))
        #例外処理
        #召喚先にカードが有る場合リムーブ処理をおこなう
        if not ally_info["energy_line"][index] == None:
            choice = input("召喚先にカードがあります。リムーブしますか？0か1で入力してください")
            #リムーブしない場合
            if choice == "0":
                print("召喚をキャンセルします。")
                return ally_info,enemy_info
            #リムーブする場合
            elif choice == "1":
                ally_info["remove"].append(deepcopy(ally_info["origins"][ally_info[line][index].No]))
                ally_info[line][index] = None 
                print("リムーブしました。")
        #原則処理
        ally_info, enemy_info = card.use(ally_info,enemy_info,card,card_num,index)
    #イベントカードの場合
    elif card.type == "event":
        #原則処理
        ally_info, enemy_info = card.use(ally_info,enemy_info,card,card_num)
    
    return ally_info, enemy_info

#起動メインを使う
def boot_main(ally_info,enemy_info,target_card,target_line,target_index,main_index):
    ally_info, enemy_info = target_card.EF[main_index][1](ally_info,enemy_info)
    ally_info[target_line][target_index].EF[main_index][0] += 1

    return ally_info,enemy_info


#アタックフェイズ
def attack_faze(ally_info,enemy_info):
    print(f"{split_faze}\n")
    print("<アタックフェイズ！>")
    #アタック可能なキャラクターがいるか確認＆いる限りループ
    while len([C for C in ally_info["front_line"] if not (C == None) and C.active == True]) > 0:
        #盤面の表示
        display_bord(ally_info,enemy_info)
        #選択肢の表示
        print("\n[0.アタックフェイズを終了する 1.アタックを行う]")
        num = int(input("0か1で入力してください:"))
        #選択分岐
        #終了処理
        if num == 0:
            input("アタックフェイズを終了します。キーを入力して下さい")
            return ally_info, enemy_info
        #アタック処理
        elif num == 1:
            #座標取得
            num1 = int(input("アタックしたいキャラクターのインデックス番号を入力してください:"))
            #例外処理
            #キャタクターがいない場合
            if ally_info["front_line"][num1] == None:
                print("キャラクターを確認できません。キャンセルします。")
                continue
            #対象のキャラクターがレストの場合
            elif not(ally_info["front_line"][num1].active):
                print("レストではアタックできません。キャンセルします。")
                continue
            #原則処理
            else:
                ally_info, enemy_info = ally_info["front_line"][num1].attack(ally_info,enemy_info,num1)
    #アタック可能なキャラクターがいない場合の処理
    input("アタック可能なキャラクターが存在しません。アタックフェイズを終了します。キーを入力してください")

    return ally_info,enemy_info
    

#エンドフェイズ
def end_faze(info):
    #タイトルコール
    print(f"{split_faze}\n")
    print("<エンドフェイズ！>")
    #リフレッシュステップ
    for front_char in info["front_line"]:
        if front_char != None and front_char.active == False:
            front_char.active = True
            #同時に起動メインの使用回数をリセット
            for effect in front_char.main_EF:
                effect[0] = 0
    for energy_char in info["energy_line"]:
        if energy_char != None and energy_char.active == False:
            energy_char.active = True
            #同上
            for effect in energy_char.main_EF:
                effect[0] = 0
    #手札が上限を超えている場合の処理
    #リムーブするカードを選択させて8枚以下になるまでループ
    while len(info["hand"]) > 9:
        print("\n手札が8枚を超えています。リムーブするカードを選んでください。")
        print([[index,i.No] for index, i in info["hand"]])
        num = int(input("インデックス番号を入力してください:"))
        info["remove"].append(deepcopy(info["origins"][info["hand"].pop(num).No]))

    
    input("\nエンドフェイズを終了します。キーを入力して下さい")
    return info


#選択したいカードの座標を入力要求する関数
def get_point():
    num = int(input("エナジーラインの場合は0を、フロントラインの場合は1を選択してください:"))
    line = "energy_line" if num == 0 else "front_line"
    index = int(input("インデックス番号を入力してください:"))
    return line,index
    


#完成までは関数のテストに使用
if __name__ == "__main__":
    #デッキの読み込み
    decks = load_deck_from_pickle('deck_list')
    deck1,deck1_origin = unpack_deck(decks[0])
    deck2,deck2_origin = unpack_deck(decks[1])
    #ゲームボードの作成
    p1_info, p2_info= make_bord("Sitrus",deck1,deck1_origin,"Noel",deck2,deck2_origin)
    #ターン数の制御変数を定義
    turn_num = 0
    counter = 0
    #勝利判定
    winner = None
    loser = None
    #バトル準備
    p1_info = standby(p1_info)
    p2_info = standby(p2_info)
    ##ゲーム開始時に先行後攻を入れ替えてしまうのでallyとenemyに逆のプレイヤー情報を代入することに注意
    #後攻のプレイヤー
    ally_info = p2_info
    #先行のプレイヤー
    enemy_info = p1_info
    #試合開始
    print(f"\n<ゲームを開始します！！>\n")
    #メインループ
    while True:
        #ターン開始宣言
        print(f"\n{split_turn}")
        #ターン数＆先行後攻制御
        counter += 1
        if counter % 2 == 0:
            first = "後攻"
            print(f"{first}{turn_num}ターン目！")
        else:
            turn_num += 1
            first = "先行"
            print(f"{first}{turn_num}ターン目！")
        #先行後攻の入れ替え
        temp = ally_info 
        ally_info = enemy_info
        enemy_info = temp
        #各フェイズの実行関数
        ally_info = start_phaze(ally_info,first,turn_num)
        ally_info = move_faze(ally_info)
        ally_info, enemy_info = main_faze(ally_info,enemy_info)
        ally_info, enemy_info = attack_faze(ally_info,enemy_info)
        ally_info = end_faze(ally_info)