class Cards:
    def __init__(self, No, image, name, color, summon_E, summon_AP, trigger_EF, hand_never_EF):
        self.No = No
        self.image = image
        self.name = name
        self.color = color
        self.summon_E = summon_E
        self.summon_AP = summon_AP
        self.trigger_EF = trigger_EF
        self.hand_never_EF = hand_never_EF

class Character(Cards):
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
        
        super().__init__(No, image, name, color, summon_E, summon_AP, trigger_EF, hand_never_EF)
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

    def use(self,ally_info,enemy_info,char_num,des_line,des_index):
        for func in self.append_EF:
            ally_info, enemy_info = func(ally_info,enemy_info)
        ally_info[des_line][des_index] = ally_info["hand"].pop(char_num)
        ally_info["action_point"] -= 1
        return ally_info, enemy_info
    
    def attack(self,ally_info,enemy_info,char_index):
        ally_info["front_line"][char_index].active = False
        for func in self.attack_EF:
            ally_info, enemy_info = func(ally_info,enemy_info)
        print(f"^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        print("相手のフロントライン")
        print([[index,char] if char == None else [index,char.No,char.active] for index,char in enumerate(enemy_info["front_line"])])
        print(f"相手側へのプリントです。\n0.ブロックする 1.ライフで受ける")
        num = int(input("0か1で入力してください"))
        if num == 0:
            if len([C for C in enemy_info["front_line"] if not (C == None) and C.active == True]) == 0:
                print("ブロック可能なキャラクターがいません。")
                num = 1
            else:
                print("フロントライン")
                for element in ([index,char] if char == None else [index, char.No, char.active] for index, char in enumerate(enemy_info["front_line"])):
                    print(element)
                while True:
                    num1 = int(input("ブロックするキャラクターを選択をインデックス番号で入力してください"))
                    if enemy_info["front_line"][num1] == None:
                        print("キャラクターが存在しません")
                    elif not enemy_info["front_line"][num1].active:
                        print("アクティブのキャラクターのみブロックできます")
                    else:
                        break
                ally_info, enemy_info = self.block(ally_info,enemy_info,char_index,num1)
        
        if num == 1:
            ally_info, enemy_info = self.trigger(ally_info,enemy_info,"normal")
        
        return ally_info, enemy_info
    
    
    def block(self,ally_info,enemy_info,attack_char_index,block_char_index):
        enemy_info["front_line"][block_char_index].active = False
        block_char = enemy_info["front_line"][block_char_index]
        for func in block_char.block_EF:
                ally_info, enemy_info = func(ally_info,enemy_info)
        
        if ally_info["front_line"][attack_char_index].BP >= enemy_info["front_line"][block_char_index].BP:
            ally_info, enemy_info = block_char.void(ally_info,enemy_info)
            enemy_info["trash"].append(block_char)
            enemy_info["front_line"][block_char_index] = None
            if self.impact > 0:
                ally_info, enemy_info = self.trigger(ally_info,enemy_info,"impact")
        
        return ally_info,enemy_info
    
    
    def trigger(self,ally_info,enemy_info,mode):
        global winner

        if mode == "normal":
            damage = self.damage
        elif mode == "impact":
            damage = self.impact
        
        life_of_enemy = len(enemy_info["life"])
        if life_of_enemy < damage:
            range_of_damage = life_of_enemy
        else:
            range_of_damage = range(damage)

        broken_life = []
        for _ in range_of_damage:
            print(f"削るライフの場所を0~{life_of_enemy-1}で選択してください⚠二回目以降は重複する数字を避けてください")
            broken_life.append(enemy_info["life"].pop(int(input())))
        
        
        print("削られたライフを公開します")
        print([i.No for i in broken_life])

        have_trigger = [char for char in broken_life if not char.trigger_EF == []]
        if len(have_trigger) == 0:
            pass
        elif len(have_trigger) == 1:
            ally_info, enemy_info = have_trigger[0].trigger_EF(ally_info,enemy_info)
        else:
            while len(have_trigger) > 0:
                print([[index,char.No] for index,char in have_trigger])
                num2 = int(input("トリガーを発動したいキャラクターのインデックス番号を入力してください"))
                ally_info, enemy_info = have_trigger.pop(num2).trigger_EF(ally_info,enemy_info)

        for char in broken_life:
            enemy_info["trash"].append(char)

        if len(enemy_info["life"]) == 0:
            winner = 1 
        
        return ally_info,enemy_info
    

    def void(self,ally_info,enemy_info):
        for func in self.void_EF:
            ally_info, enemy_info = func(ally_info,enemy_info)
        return ally_info, enemy_info

            



        


#呪術廻戦/青/キャラクター
JJK036 = Character("JJK036",None,["伊地知 潔高"],"Bule",0,1000) 
JJK037 = Character("JJK037",None,["虎杖 悠仁"],"Blue",0,1500)
JJK038 = Character("JJK038",None,["虎杖 悠仁"],"Blue",2,3000)
JJK043 = Character("JJK043",None,["釘崎 野薔薇"],"Blue",0,1500)

#呪術廻戦/黄/キャラクター
JJK001 = Character("JJK001",None,["虎杖 悠仁"],"Yellow",0,1000)
JJK006 = Character("JJK006",None,["釘崎 野薔薇"],"Yellow",0,1500)
JJK016 = Character("JJK016",None,["パンダ"],"Yellow",3,3000,out_E=2)
JJK024 = Character("JJK024",None,["玉犬:黒＆白"],"Yellow",0,2000,attribute=["式神"])



#呪術廻戦リスト
Blue_JJK = ["呪術廻戦/青",JJK036,JJK037,JJK038,JJK043]
Yellow_JJK = ["呪術廻戦/黄",JJK001,JJK006,JJK016,JJK024]



