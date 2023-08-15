from copy import *
from ginfo import *
#構築済みのデッキのデータを取得
from deck_list import decks


#新デッキをリストに追加
def add_decks(deck):
    decks.append(deck)

#完成した構築をデッキ化
##引数のフォーマット:[[カードのNo,カードの枚数],……]
def pack_deck(card_list):
    deck = []
    for card_info in card_list:
        for _ in range(card_info[1]):
            deck.append(deepcopy(card_info[0]))
    return deck

#デッキリストのデータを更新
##デッキデータの更新をpythonファイルに直接書き込むことで実現。後々データの管理方法を変える必要あり。
def update_list():
    with open('deck_list.py', 'w') as f:
        f.write(f"""from ginfo import *
decks = [      
""")
        for index,sublist in enumerate(decks):
            if index == 0:
                line = "[" + ", ".join(item.No for item in sublist) + "]\n"
                f.write(line)
            else:
                line = "[" + ", ".join(item.No for item in sublist) + "]\n"
                f.write(","+line)
        f.write("]")


if __name__ == "__main__":
    add_decks(pack_deck([[JJK043,10],[JJK036,10],[JJK038,10]]))
    add_decks(pack_deck([[JJK001,10],[JJK006,10],[JJK024,10]]))
    
    update_list()
