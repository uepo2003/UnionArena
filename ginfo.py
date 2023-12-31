#キャラクターカードクラス
class Character:
    def __init__(self,
                 No,
                 image,
                 name,
                 type,
                 color,
                 need_energy,
                 action_point,
                 buttle_point,
                 out_energy,
                 active,
                 damage,
                 impact,
                 unimpact,
                 step,
                 append_effect,
                 main_effect,
                 attack_effect,
                 block_effect,
                 trash_effect,
                 never_effect,
                 trigger_effect):
        
        #基礎ステータス
        self.No = No
        self.image = image
        self.name = name
        self.type = type
        self.color = color
        self.need_energy = need_energy
        self.actioin_point = action_point
        self.buttle_point = buttle_point
        self.out_energy = out_energy
        self.active = active
        self.damage = damage

        #キーワード効果
        self.impact = impact
        self.unimpact = unimpact
        self.step = step

        #カード効果
        self.append_effect = append_effect
        self.main_effect = main_effect
        self.attack_effect = attack_effect
        self.block_effect = block_effect
        self.trash_effect = trash_effect
        self.never_efect = never_effect
        self.trriger_efffect = trigger_effect

#呪術廻戦/青/キャラクター
JJK036 = Character("JJK036",None,"伊地知 潔高",None,"Blue",0,1,1000,1,False,1,0,False,False,None,None,None,None,None,None,None)
JJK037 = Character("JJK037",None,"虎杖 悠仁",None,"Blue",0,1,1500,1,False,1,0,False,False,None,None,None,None,None,None,None)
JJK038 = Character("JJK038",None,"虎杖 悠仁",None,"Blue",2,1,3000,1,False,1,0,False,False,None,None,None,None,None,None,None)
JJK043 = Character("JJK043",None,"釘崎 野薔薇",None,"Blue",0,1,1500,1,False,1,0,False,False,None,None,None,None,None,None,None)

#呪術廻戦/黄/キャラクター
JJK001 = Character("JJK001",None,"虎杖 悠仁",None,"Yellow",0,1,1000,1,False,1,0,False,False,None,None,None,None,None,None,None)
JJK006 = Character("JJK006",None,"釘崎 野薔薇",None,"Yellow",0,1,1500,1,False,1,0,False,False,None,None,None,None,None,None,None)
JJK024 = Character("JJK024",None,"玉犬:黒＆白","式神","Yellow",0,1,2000,1,False,1,0,False,False,None,None,None,None,None,None,None)


#呪術廻戦リスト
Blue_JJK = ["呪術廻戦/青",JJK036,JJK037,JJK038,JJK043]
Yellow_JJK = ["呪術廻戦/黄",JJK001,JJK006,JJK024]




