from func_display import *
import datetime
import json
from copy import *


#ゲームログクラス
class GameLog:
    def __init__(self):
        self.logs = []
        
    def add_log(self, player_name, card_used, turn_number):
        log_entry = {
            "player_name": player_name,
            "card_used": card_used,
            "turn_number": turn_number,
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.logs.append(log_entry)
    
    def save_to_file(self, filename="game_logs.json"):
        with open(filename, "w") as file:
            json.dump(self.logs, file, indent=4)

    def load_from_file(self, filename="game_logs.json"):
        with open(filename, "r") as file:
            self.logs = json.load(file)

#キャラクターカードクラス
class Character:
    def __init__(self, 
                 #基礎ステータス(入力必須)
                 No,
                 image, 
                 name, 
                 color, 
                 summon_E, 
                 BP, 
                 
                 #基礎ステータス(入力任意)
                 type="char", 
                 active = False,
                 summon_AP=1, 
                 out_E=1, 
                 attribute=[],  
                 damage=1, 
                 under_card = [],
                 
                 #キーワード効果
                 impact=0, 
                 unimpact=False, 
                 step=False, 

                 #カード効果
                 trigger_EF=[], 
                 hand_never_EF=[], 
                 append_EF=[], 
                 main_EF=[], 
                 attack_EF=[], 
                 block_EF=[], 
                 void_EF=[], 
                 line_never_EF=[]):
        
        self.No = No
        self.image = image
        self.name = name
        self.color = color
        self.summon_E = summon_E
        self.summon_AP = summon_AP
        self.trigger_EF = trigger_EF
        self.hand_never_EF = hand_never_EF
        self.type = type
        self.BP = BP
        self.out_E = out_E
        self.active = active
        self.attribute = attribute
        self.damage = damage
        self.impact = impact
        self.unimpact = unimpact
        self.step = step
        self.append_EF = append_EF
        self.main_EF = main_EF
        self.attack_EF = attack_EF
        self.block_EF = block_EF
        self.void_EF = void_EF
        self.line_never_EF = line_never_EF
        self.under_card = under_card

    def __repr__(self):
        return (f"Card("
                f"No={self.No}, "
                f"image={repr(self.image)}, "
                f"name={repr(self.name)}, "
                f"color={repr(self.color)}, "
                f"summon_E={self.summon_E}, "
                f"BP={self.BP}, "
                f"type={repr(self.type)}, "
                f"active={self.active}, "
                f"summon_AP={self.summon_AP}, "
                f"out_E={self.out_E}, "
                f"attribute={self.attribute}, "
                f"damage={self.damage}, "
                f"impact={self.impact}, "
                f"unimpact={self.unimpact}, "
                f"step={self.step}, "
                f"trigger_EF={self.trigger_EF}, "
                f"hand_never_EF={self.hand_never_EF}, "
                f"append_EF={self.append_EF}, "
                f"main_EF={self.main_EF}, "
                f"attack_EF={self.attack_EF}, "
                f"block_EF={self.block_EF}, "
                f"void_EF={self.void_EF}, "
                f"line_never_EF={self.line_never_EF})"
                )

        
    #カード使用の処理
    def summon(self,ally_info,enemy_info,char_num,des_line,des_index):
        print(f"{self.name}を召喚！")
        #手札から該当のカードを削除＆場に召喚
        ally_info[des_line][des_index] = ally_info["hand"].pop(char_num)
        #APをsummon_AP分消費
        ally_info["action_point"] -= self.summon_AP
        #登場時効果の発動
        for func in self.append_EF:
            ally_info, enemy_info = func(ally_info,enemy_info)
        
        return ally_info, enemy_info
    
    
    #アタック処理
    def attack(self,ally_info,enemy_info,char_index):
        #レストにする
        ally_info["front_line"][char_index].active = False
        print(f"{self.name}でアタック！")
        #アタック時効果を発動
        for func in self.attack_EF:
            ally_info, enemy_info = func(ally_info,enemy_info)
        #対戦相手にブロック非ブロックを要求
        print(f"\n>>>>>>>>>>>>>>>>>>>>>>>>>")
        #ブロックできるキャラクターがいない場合直接ライフを選択させる
        if len([C for C in enemy_info["front_line"] if not (C == None) and C.active == True]) == 0:
            print("ブロックできるキャラクターがいないためライフで受けます。")
            num = 1
        #ブロックするかの選択を選択させる
        else:
            print(f"{enemy_info['player_name']}はどうする！？")
            display_bord(enemy_info,ally_info)
            print(f"\n[0.ブロックする 1.ライフで受ける]")
            num = int(input("0か1で入力してください:"))
            #ブロックする場合
            if num == 0:
                print(f"⚠{enemy_info['player_name']}目線です")
                display_bord(enemy_info,ally_info)
                #ブロック対象の選択のループ
                ##例外が発生した場合にブロック対象の選択まで戻るためのループ。なお一度ブロックするを選んだ場合キャンセルはできない
                while True:
                    num1 = int(input("ブロックするキャラクターのインデックス番号を入力してください:"))
                    #Noneの場合
                    if enemy_info["front_line"][num1] == None:
                        print("キャラクターが存在しません。")
                    #レストの場合
                    elif not enemy_info["front_line"][num1].active:
                        print("アクティブのキャラクターを選択して下さい。")
                    else:
                        break
                #原則処理
                ally_info, enemy_info = self.block(ally_info,enemy_info,char_index,num1)
        #ライフで受ける場合の処理
        ##ブロックできるキャラがいない場合とライフで受けるを選択した場合の二通りで受けるためelifではなくif
        if num == 1:
            print("ライフで受ける！")
            ally_info, enemy_info = self.trigger(ally_info,enemy_info,"normal")
        
        print("<<<<<<<<<<<<<<<<<<<<<<<<<")
        return ally_info, enemy_info
    
    
    def block(self,ally_info,enemy_info,attack_char_index,block_char_index):
        #ブロックするキャラクターをレストにする
        enemy_info["front_line"][block_char_index].active = False
        print(f"{self.name}でブロック！")
        #ブロックするキャラクターを取得
        block_char = enemy_info["front_line"][block_char_index]
        #ブロック時効果を使用
        for func in block_char.block_EF:
                ally_info, enemy_info = func(ally_info,enemy_info)
        #BPを比べる
        ##相手のBPの方が高い場合、レストになるだけで他の処理は起きないのでelseを記述しない
        #BPで勝った場合
        if ally_info["front_line"][attack_char_index].BP >= enemy_info["front_line"][block_char_index].BP:
            print("バトルに敗北した…。")
            #ブロックしたキャラクターに退場処理を行う
            enemy_info, ally_info = block_char.void(enemy_info,ally_info,"front_line",block_char_index)
            #インパクト持ちの場合ライフを削る
            if self.impact > 0:
                #ブロック側がインパクト無効を持っているか判定
                #持っている場合
                if block_char.unimpact:
                    print("インパクト無効発動！インパクトを防いだ！")
                #持っていない場合
                else:
                    print("インパクト発動！")
                    ally_info, enemy_info = self.trigger(ally_info,enemy_info,"impact")
        
        return ally_info,enemy_info
    
    
    def trigger(self,ally_info,enemy_info,mode):
        ##アタックした側がally、ライフを削られる側がenemyである点に注意する
        global winner
        #通常時かインパクト時かでダメージの値を判断する
        if mode == "normal":
            damage = self.damage
        elif mode == "impact":
            damage = self.impact
        #ダメージの値が残りライフをうわまわっていないか判定、上回っている場合は残りのライフ分だけライフを削る
        num_of_life = len(enemy_info["life"])
        if num_of_life < damage:
            range_of_damage = num_of_life
        else:
            range_of_damage = range(damage)
        #削らるライフを選択→broken_lifeに該当カードを格納→ダメージ分だけ繰り返す
        broken_life = []
        for _ in range_of_damage:
            print(f"削るライフの場所を0~{num_of_life-1}で選択してください⚠二回目以降は重複する数字を避けてください")
            broken_life.append(enemy_info["life"].pop(int(input(":"))))
        #broken_lifeを公開することで削られた全てのカードを同時に公開
        print("\n削られたライフを公開します。")
        print([i.No for i in broken_life])
        #トリガー持ちのみを別途リストに格納
        have_trigger = [char for char in broken_life if not char.trigger_EF == []]
        #トリガーを持っているカードの数で分岐
        #トリガーを持っているカードがない場合
        if len(have_trigger) == 0:
            #なにもしない
            pass
        #トリガーを持っているカードが1つの場合
        elif len(have_trigger) == 1:
            #そのまま該当カードを選択してトリガーを発動
            ally_info, enemy_info = have_trigger[0].trigger_EF(ally_info,enemy_info)
        #トリガーを持っているカードが2つ以上の場合
        else:
            #好きな順番で効果を発動させる
            #トリガー未使用のカードがある限りループ
            while len(have_trigger) > 0:
                print([[index,char.No] for index,char in have_trigger])
                num2 = int(input(f"\nトリガーを発動したいカードのインデックス番号を入力してください:"))
                #選ばれたカードをリストから削除＆トリガーを発動
                ally_info, enemy_info = have_trigger.pop(num2).trigger_EF(ally_info,enemy_info)
        #ライフとして削られたカードを墓地に追加
        for char in broken_life:
            enemy_info["trash"].append(deepcopy(ally_info["origins"][char.No]))
        #ライフが0の場合に勝利判定
        if len(enemy_info["life"]) == 0:
            winner = 1 
        
        return ally_info,enemy_info
    
    
    #退場処理
    def void(self,ally_info,enemy_info,target_line,target_index):
        #該当のキャラクターを墓地に追加
        ally_info["trash"].append(deepcopy(ally_info["origins"][self.No]))
        #場から削除
        ally_info[target_line][target_index] = None
        #退場時効果を発動
        for func in self.void_EF:
            ally_info, enemy_info = func(ally_info,enemy_info)
        
        return ally_info, enemy_info
    
    #リムーブ処理
    def remove(self,ally_info,enemy_info,target_line,target_index):
        print("要検討")


class Raid(Character):
    def __init__(self,
                 #基礎ステータス（入力任意）
                 No,
                 image,
                 name,
                 color,
                 summon_E,
                 BP,

                 #レイド専用要素
                 raid_char,
                 raid_EF,
                 
                 #基礎ステータス(入力任意)
                 type="raid", 
                 active=False,
                 summon_AP=1, 
                 out_E=1, 
                 attribute=[],  
                 damage=1, 
                 under_card=[],
                 
                 #キーワード効果
                 impact=0,
                 unimpact=False, 
                 step=False, 

                 #カード効果
                 trigger_EF=[], 
                 hand_never_EF=[], 
                 append_EF=[], 
                 main_EF=[], 
                 attack_EF=[], 
                 block_EF=[], 
                 void_EF=[], 
                 line_never_EF=[]):
        
        super().__init__(No, image, name, color, summon_E, BP, type, active, summon_AP, out_E, attribute, damage, under_card, impact, unimpact, step, trigger_EF, hand_never_EF, append_EF, main_EF, attack_EF, block_EF, void_EF, line_never_EF)
        self.raid_char = raid_char
        self.raid_EF = raid_EF

    def unpack_raid(self,list):
        for char in list:
            if char[0] == "append":
                self.append_EF = char[1]
            elif char[0] == "main":
                self.main_EF = char[1]
            elif char[0] == "attack":
                self.attack_EF = char[1]
            elif char[0] == "void":
                self.void_EF = char[1]
            elif char[0] == "trigger":
                self.trigger_EF = char[1]
            elif char[0] == "block":
                self.block_EF = char[1]
            elif char[0] == "line_never":
                self.line_never_EF = char[1]
    
    def raid(self,ally_info,enemy_info,card_index,raid_line,raid_index,moved_line,moved_index):
        self.unpack_raid(self.raid_EF)


