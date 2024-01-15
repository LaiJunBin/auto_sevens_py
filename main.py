import math
import time
import random
import pyautogui


class Card:
    def __init__(self, i, location):
        self.i = i
        self.suit = math.floor((i - 1) / 13)
        self.location = location

    @property
    def number(self):
        return 13 if self.i % 13 == 0 else self.i % 13

def flatten(l):
    return [item for sublist in l for item in sublist]

def get_user_cards():
    cards = []
    for i in range(1, 52 + 1):
        location = pyautogui.locateOnScreen(f'./new_images/{i}.jpg', region=(620, 650, 540, 270))
        if location is not None:
            cards.append(Card(i, location))

    return cards

def get_game_cards():
    cards = []
    for i in range(1, 52 + 1):
        location = pyautogui.locateOnScreen(f'./new_images/{i}.jpg', region=(460, 290, 1000, 360))
        if location is not None:
            cards.append(Card(i, location))

    return cards

for i in range(13):
    cards = get_user_cards()
    print(len(cards))
    
    while len(cards) != 13 - i:
        time.sleep(1)
        cards = get_user_cards()
        print(len(cards))

    for card in cards:
        print('user: ', card.i, card.number)

    game_cards = get_game_cards()
    for card in game_cards:
        print('game card:', card.i, card.number)

    can_play_cards = [[],[],[],[]]
    for card in game_cards:
        can_play_cards[card.suit].append(card.i)
 
    for i in range(len(can_play_cards)):
        can_play_cards[i].sort()
        if len(can_play_cards[i]) == 0:
            can_play_cards[i].append(13*i+7)
        elif len(can_play_cards[i]) == 1:
            can_play_cards[i].append(can_play_cards[i][0])
            can_play_cards[i][0] -= 1
            can_play_cards[i][1] += 1
        elif len(can_play_cards[i]) == 2:
            can_play_cards[i][0] -= 1
            can_play_cards[i][1] += 1
            if can_play_cards[i][0] % 13 == 0:
                can_play_cards[i][0] = -1
            if can_play_cards[i][1] % 13 == 1:
                can_play_cards[i][1] = -1

    flatted_can_play_cards = flatten(can_play_cards)
    flatted_can_play_cards = list(filter(lambda x: x != -1, flatted_can_play_cards))
    for card in flatted_can_play_cards:
        print('flat can play:', card, 13 if card % 13 == 0 else card % 13)

    user_can_play_cards = []
    for card in cards:
        if card.i in flatted_can_play_cards:
            user_can_play_cards.append(card)

    if len(user_can_play_cards) == 0:
        sorted_cards = sorted(cards, key=lambda card: card.number)
        print('蓋牌: ', sorted_cards[0].i, sorted_cards[0].number)
        pyautogui.moveTo(sorted_cards[0].location)
        time.sleep(0.5)
        pyautogui.click()
        time.sleep(0.5)
        pyautogui.moveTo(100, 100)
        continue

    random_card = random.choice(user_can_play_cards)
    print('出牌: ', random_card.i, random_card.number)
    pyautogui.moveTo(random_card.location)
    time.sleep(0.5)
    pyautogui.click()
    time.sleep(0.5)
    pyautogui.moveTo(100, 100)
