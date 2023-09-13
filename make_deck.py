from copy import *
from class_list import *
import pickle
from card_list import *
#構築済みのデッキのデータを取得


#新デッキをリストに追加
def add_decks(deck):
    decks.append(deck)
    
#デッキリストのデータを解凍するための関数   
def unpack_deck(card_list):
    deck = []
    for card_info in card_list:
        for _ in range(card_info[1]):
            deck.append(deepcopy(card_info[0]))
    deck_parts = {char[0].No:char[0] for char in card_list}
    return deck, deck_parts

#デッキリストを保存
def save_deck_to_pickle(deck, filename):
    with open(filename, 'wb') as file:
        pickle.dump(deck, file)

#保存されたリストをロード
def load_deck_from_pickle(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)


if __name__ == "__main__":
    decks = []
    #デッキのフォーマット:[[カードのNo,カードの枚数],……]
    decks.append([[JJK001,10],[JJK006,10],[JJK016,10]])
    decks.append([[JJK036,10],[JJK037,10],[JJK038,10]])
    save_deck_to_pickle(decks,'deck_list')
