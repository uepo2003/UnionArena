split_turn = "============================================================"
split_pop = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" 
split_faze = "____________________________________________________________"

#メインフェイズ時の盤面表示。手札、ライフ、APも完備
def display_info(ally_info,enemy_info):
    print(f"""\n{split_pop}
{[[index,char] if char == None else [index, char.No, char.active] for index, char in enumerate(enemy_info["energy_line"])]}  
      
{[[index,char] if char == None else [index, char.No, char.active] for index, char in enumerate(enemy_info["front_line"])]}  
enemy
------------------------------------------------------
ally              
{[[index,char] if char == None else [index, char.No, char.active] for index, char in enumerate(ally_info["front_line"])]} 
            
{[[index,char] if char == None else [index, char.No, char.active] for index, char in enumerate(ally_info["energy_line"])]}

AP:{ally_info["action_point"]}
life:{len(ally_info["life"])}
hand:{[i.No for i in ally_info["hand"]]}
{split_pop}""")


#アタックフェイズなどの盤面の情報のみを要求する盤面で使用
def display_bord(ally_info,enemy_info):
    print(f"""{split_pop}
{[[index,char] if char == None else [index, char.No, char.active] for index, char in enumerate(enemy_info["energy_line"])]}  
      
{[[index,char] if char == None else [index, char.No, char.active] for index, char in enumerate(enemy_info["front_line"])]}  
enemy
------------------------------------------------------
ally              
{[[index,char] if char == None else [index, char.No, char.active] for index, char in enumerate(ally_info["front_line"])]} 
            
{[[index,char] if char == None else [index, char.No, char.active] for index, char in enumerate(ally_info["energy_line"])]}
{split_pop}""")
    

#ハンドのみの表示    
def display_hand(info):
    print(f"""

hand:{[i.No for i in info["hand"]]}    

""")

#墓地の表示
def display_trash(info):
    print(f"""

trash:{[i.No for i in info["trash"]]}

""")


#リムーブエリアの表示
def display_remove(info):
    print(f"""

remove:{[i.No for i in info["remove"]]}

""")
    

#自分目線から見える敵の情報の表示
def display_enemy(info):
    print(f"""\n

hand:{len(info["hand"])}枚
life:{len(info["life"])}

trash:{[i.No for i in info["trash"]]}
remove:{[i.No for i in info["remove"]]}
                    
""")