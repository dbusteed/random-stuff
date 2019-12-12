from random import randint
from brule import randomFirst
from os import system
from time import sleep

## to-do
# high card scoring
# overall layout
# multiple bets
# saying what the winner had
# logic on bet limits

# constants
SUITS = ['♥', '♣', '♦', '♠',]
VALUES = {'2 ': 2, '3 ': 3, '4 ': 4, '5 ': 5, '6 ': 6, '7 ': 7, '8 ': 8, '9 ': 9, '10': 10, 'J ': 11, 'Q ': 12, 'K ': 13, 'A ': 14}
BLIND_BET = 3
MENU_CHOICES = [1,2,3]

clear = lambda: system('cls')

# classes
class Card():
    def __init__(self, s, pv, v,):
        self.suit = s
        self.print_value = pv
        self.value = v

class Player():
    def __init__(self, n, h: bool):
        self.name = n
        self.money = 50
        self.hand = []
        self.all_cards = []
        self.hand_points = 0
        self.human = h
        self.bet = 0
        self.active = True
        self.check = False
        self.blind = False
        self.hand_status = {'Four of a Kind': False, 'Full House': False, 'Flush': False, 'Straight': False, 'Three of a Kind': False, 'Pair': False, 'High card': False}

class Hand():
    def __init__(self, v, c=1):
        self.value = v
        self.count = c

# methods
def deal_card(deck): # returns a card object
    return deck.pop(randint(0,len(deck)-1))

def shuffle():
    deck = master_deck[:]
    return deck

def print_cards(player:list, table:list, pot):
    if table is None:
        print(' ------    ------')
        print('|      |  |      |')
        print('| %s %s |  | %s %s |' %(player[0].print_value, player[0].suit, player[1].print_value, player[1].suit))
        print('|      |  |      |')
        print(' ------    ------')
    else:
        if(len(table) == 3):
            print('         Table Cards        Pot: %3d      Your Cards' %(pot))
            print(' ------    ------    ------           ------    ------')
            print('|      |  |      |  |      |         |      |  |      |')
            print('| %s %s |  | %s %s |  | %s %s |         | %s %s |  | %s %s |' %(table[0].print_value, table[0].suit, table[1].print_value, table[1].suit, table[2].print_value, table[2].suit, player[0].print_value, player[0].suit, player[1].print_value, player[1].suit))
            print('|      |  |      |  |      |         |      |  |      |')
            print(' ------    ------    ------           ------    ------')
        elif(len(table) == 4):
            print('         Table Cards                  Pot: %3d      Your Cards' %(pot))
            print(' ------    ------    ------    ------           ------    ------')
            print('|      |  |      |  |      |  |      |         |      |  |      |')
            print('| %s %s |  | %s %s |  | %s %s |  | %s %s |         | %s %s |  | %s %s |' %(table[0].print_value, table[0].suit, table[1].print_value, table[1].suit, table[2].print_value, table[2].suit, table[3].print_value, table[3].suit, player[0].print_value, player[0].suit, player[1].print_value, player[1].suit))
            print('|      |  |      |  |      |  |      |         |      |  |      |')
            print(' ------    ------    ------    ------           ------    ------')
        elif(len(table) == 5):
            print('         Table Cards                            Pot: %3d      Your Cards' %(pot))
            print(' ------    ------    ------    ------    ------           ------    ------')
            print('|      |  |      |  |      |  |      |  |      |         |      |  |      |')
            print('| %s %s |  | %s %s |  | %s %s |  | %s %s |  | %s %s |         | %s %s |  | %s %s |' %(table[0].print_value, table[0].suit, table[1].print_value, table[1].suit, table[2].print_value, table[2].suit, table[3].print_value, table[3].suit,  table[4].print_value, table[4].suit, player[0].print_value, player[0].suit, player[1].print_value, player[1].suit))
            print('|      |  |      |  |      |  |      |  |      |         |      |  |      |')
            print(' ------    ------    ------    ------    ------           ------    ------')

def print_ai_cards(bots: list):
    for b in bots:
        print("    %5s              " %(b.name), end='')
    print()
    for b in bots:
        print(' ------    ------           ', end='')
    print()
    for b in bots:
        print('|      |  |      |          ', end='')
    print()
    for b in bots:
        print('| %s %s |  | %s %s |          ' %(b.hand[0].print_value, b.hand[0].suit, b.hand[1].print_value, b.hand[1].suit), end='')
    print()
    for b in bots:
        print('|      |  |      |          ', end='')
    print()
    for b in bots:
        print(' ------    ------           ', end='')
    print('\n')

def check_for_straight(cards: list):
    for c in cards:
        if((c+1) in cards):
            if((c+2) in cards):
                if((c+3) in cards):
                    if((c+4) in cards):
                        return True

def display_monies(players: list):
    print('\nTotal Money: ')
    for p in players:
        print('%s: %d \t' %(p.name, p.money), end=' ')
    print('\n')

def display_bets(players: list):
    print('\nCurrent Bets: ')
    for p in players:
        if p.active:
            m = ''
        else:
            m = '(folded)'
        print('%s: %d %s\t' %(p.name, p.bet, m), end=' ')
    print('\n\n')

def reset_players(players: list):
    for p in players:
        p.hand = []
        p.all_cards = []
        p.hand_points = 0
        p.bet = 0
        p.active = True
        p.check = False
        p.hand_status = {'Four of a Kind': False, 'Full House': False, 'Flush': False, 'Straight': False, 'Three of a Kind': False, 'Pair': False, 'High card': False}

    # rotates the blind bet
    for i in range(0, len(players)):
        if players[i].blind:
            if(i == (len(players)-1)):
                players[i].blind = False
                players[0].blind = True
            else:
                players[i].blind = False
                players[i+1].blind = True
                break

def first_blind_guy(players):
    players[randint(0,len(players)-1)].blind = True


# later organize
master_deck = []
deck = []


for suit in SUITS:
     for print_value, value in VALUES.items():
         master_deck.append(Card(suit, print_value, value))

players = [Player('Davis', True), Player(randomFirst(), False), Player(randomFirst(), False), Player(randomFirst(), False)]

play_choice = ''
first_blind_guy(players)

while play_choice != 'q':
    pot, bet_level, new_bet = 0, 0, 0
    deck = shuffle()
    reset_players(players)
    table = []

    clear()

    display_monies(players)

    # deal 2 cards to each player
    for p in players:
        p.hand.append(deal_card(deck))
        p.hand.append(deal_card(deck))
        if(p.human):
            print('Your cards: \n')
            print_cards(p.hand, None, 0)

    # initial blind bet
    blind_guy = [p for p in players if p.blind][0]
    pot += BLIND_BET
    bet_level = BLIND_BET
    blind_guy.bet = BLIND_BET
    blind_guy.money -= BLIND_BET

    ## FIRST BETTING ROUND ##
    while([p.check for p in players].count(False)>0):
        display_bets(players)

        if(players[0].active):
            if(players[0].bet == bet_level):
                print('\n1. Raise\n2. Check\n3. Fold\n')

                while True:
                    try:
                        ans = int(input('?: '))
                        if ans in MENU_CHOICES:
                            ans += 10
                            break
                        print('Please enter a valid menu choice')
                    except:
                        print('Please enter a valid menu choice')

                if(ans == 11):#raise
                    new_bet = int(input('Bet?: '))

                    #check if they have that much

                    players[0].bet += new_bet
                    players[0].money -= new_bet
                    bet_level += new_bet
                    pot += new_bet
                elif(ans == 12):#check
                    players[0].check = True
                elif(ans == 13):#fold
                    players[0].active = False
                    players[0].check = True

            else:
                print('\n1. Raise\n2. Call\n3. Fold\n')

                while True:
                    try:
                        ans = int(input('?: '))
                        if ans in MENU_CHOICES:
                            ans += 20
                            break
                        print('Please enter a valid menu choice')
                    except:
                        print('Please enter a valid menu choice')

                if(ans == 21):
                    call_needed = bet_level - players[0].bet
                    new_bet = int(input('Raise by how much?: '))
                    players[0].bet += (call_needed + new_bet)
                    players[0].money -= (call_needed + new_bet)
                    bet_level += new_bet
                    pot += (new_bet + call_needed)
                elif(ans == 22):
                    new_bet = (bet_level - players[0].bet)
                    players[0].bet += new_bet
                    players[0].money -= new_bet
                    pot += new_bet
                    players[0].check = True
                elif(ans == 23):
                    players[0].active = False
                    players[0].check = True

        for p in [p for p in players if (p.human == False and p.active == True)]:
            if(p.bet == bet_level):
                p.check = True
            else:
                #bounds?
                bound1 = 4
                bound2 = 9

                choice = randint(1,10)

                if(choice in range(1, bound1)): #Fold
                    p.active = False
                    p.check = True
                    print('%s folded.' %(p.name))
                elif(choice in range(bound1,bound2)): #check
                    new_bet = bet_level - p.bet
                    p.bet += new_bet
                    p.money -= new_bet
                    pot += new_bet
                    p.check = True
                elif(choice in range(bound2,10)): #raise
                    call_needed = (bet_level - p.bet)
                    new_bet = randint(1,6)
                    p.bet += (call_needed + new_bet)
                    p.money -= (call_needed + new_bet)
                    bet_level += new_bet
                    pot += (call_needed + new_bet)


        if(players[0].active):
            if(players[0].bet == bet_level):
                players[0].check = True

    print('\nDealing three cards...')
    sleep(1)

    clear()
    # deal three cards to table
    table.append(deal_card(deck))
    table.append(deal_card(deck))
    table.append(deal_card(deck))

    print_cards(players[0].hand, table, pot)

    for p in [p for p in players if p.active]:
        p.check = False

    ## Second betting round (after first three cards) ##
    while([p.check for p in players].count(False)>0):
        display_bets(players)

        if(players[0].active):
            if(players[0].bet == bet_level):
                print('\n1. Raise\n2. Check\n3. Fold\n')

                while True:
                    try:
                        ans = int(input('?: '))
                        if ans in MENU_CHOICES:
                            ans += 10
                            break
                        print('Please enter a valid menu choice')
                    except:
                        print('Please enter a valid menu choice')

                if(ans == 11):#raise
                    new_bet = int(input('Bet?: '))

                    #check if they have that much

                    players[0].bet += new_bet
                    players[0].money -= new_bet
                    bet_level += new_bet
                    pot += new_bet
                elif(ans == 12):#check
                    players[0].check = True
                elif(ans == 13):#fold
                    players[0].active = False
                    players[0].check = True

            else:
                print('\n1. Raise\n2. Call\n3. Fold\n')

                while True:
                    try:
                        ans = int(input('?: '))
                        if ans in MENU_CHOICES:
                            ans += 20
                            break
                        print('Please enter a valid menu choice')
                    except:
                        print('Please enter a valid menu choice')

                if(ans == 21):
                    call_needed = bet_level - players[0].bet
                    new_bet = int(input('Raise by how much?: '))
                    players[0].bet += (call_needed + new_bet)
                    players[0].money -= (call_needed + new_bet)
                    bet_level += new_bet
                    pot += (new_bet + call_needed)
                elif(ans == 22):
                    new_bet = (bet_level - players[0].bet)
                    players[0].bet += new_bet
                    players[0].money -= new_bet
                    pot += new_bet
                    players[0].check = True
                elif(ans == 23):
                    players[0].active = False
                    players[0].check = True

        for p in [p for p in players if (p.human == False and p.active == True)]:
            if(p.bet == bet_level):
                p.check = True
            else:
                #bounds?
                bound1 = 4
                bound2 = 9

                choice = randint(1,10)

                if(choice in range(1, bound1)): #Fold
                    p.active = False
                    p.check = True
                    print('%s folded.' %(p.name))
                elif(choice in range(bound1,bound2)): #check
                    new_bet = bet_level - p.bet
                    p.bet += new_bet
                    p.money -= new_bet
                    pot += new_bet
                    p.check = True
                elif(choice in range(bound2,10)): #raise
                    call_needed = (bet_level - p.bet)
                    new_bet = randint(1,6)
                    p.bet += (call_needed + new_bet)
                    p.money -= (call_needed + new_bet)
                    bet_level += new_bet
                    pot += (call_needed + new_bet)


        if(players[0].active):
            if(players[0].bet == bet_level):
                players[0].check = True

    clear()
    table.append(deal_card(deck))
    print_cards(players[0].hand, table, pot)

    for p in [p for p in players if p.active]:
        p.check = False

    ## Thrid betting round (after 4th card dealt)
    while([p.check for p in players].count(False)>0):
        display_bets(players)

        if(players[0].active):
            if(players[0].bet == bet_level):
                print('\n1. Raise\n2. Check\n3. Fold\n')

                while True:
                    try:
                        ans = int(input('?: '))
                        if ans in MENU_CHOICES:
                            ans += 10
                            break
                        print('Please enter a valid menu choice')
                    except:
                        print('Please enter a valid menu choice')

                if(ans == 11):#raise
                    new_bet = int(input('Bet?: '))

                    #check if they have that much

                    players[0].bet += new_bet
                    players[0].money -= new_bet
                    bet_level += new_bet
                    pot += new_bet
                elif(ans == 12):#check
                    players[0].check = True
                elif(ans == 13):#fold
                    players[0].active = False
                    players[0].check = True

            else:
                print('\n1. Raise\n2. Call\n3. Fold\n')

                while True:
                    try:
                        ans = int(input('?: '))
                        if ans in MENU_CHOICES:
                            ans += 20
                            break
                        print('Please enter a valid menu choice')
                    except:
                        print('Please enter a valid menu choice')

                if(ans == 21):
                    call_needed = bet_level - players[0].bet
                    new_bet = int(input('Raise by how much?: '))
                    players[0].bet += (call_needed + new_bet)
                    players[0].money -= (call_needed + new_bet)
                    bet_level += new_bet
                    pot += (new_bet + call_needed)
                elif(ans == 22):
                    new_bet = (bet_level - players[0].bet)
                    players[0].bet += new_bet
                    players[0].money -= new_bet
                    pot += new_bet
                    players[0].check = True
                elif(ans == 23):
                    players[0].active = False
                    players[0].check = True

        for p in [p for p in players if (p.human == False and p.active == True)]:
            if(p.bet == bet_level):
                p.check = True
            else:
                #bounds?
                bound1 = 4
                bound2 = 9

                choice = randint(1,10)

                if(choice in range(1, bound1)): #Fold
                    p.active = False
                    p.check = True
                    print('%s folded.' %(p.name))
                elif(choice in range(bound1,bound2)): #check
                    new_bet = bet_level - p.bet
                    p.bet += new_bet
                    p.money -= new_bet
                    pot += new_bet
                    p.check = True
                elif(choice in range(bound2,10)): #raise
                    call_needed = (bet_level - p.bet)
                    new_bet = randint(1,6)
                    p.bet += (call_needed + new_bet)
                    p.money -= (call_needed + new_bet)
                    bet_level += new_bet
                    pot += (call_needed + new_bet)


        if(players[0].active):
            if(players[0].bet == bet_level):
                players[0].check = True

    clear()
    table.append(deal_card(deck))
    print_cards(players[0].hand, table, pot)

    # for p in [p for p in players if p.active]:
    #     p.check = False
    #
    # ## Final betting round (after 5th card dealt)
    # while([p.check for p in players].count(False)>0):
    #     display_bets(players)
    #
    #     if(players[0].active):
    #         if(players[0].bet == bet_level):
    #             print('\n1. Raise\n2. Check\n3. Fold\n')
    #
    #             while True:
    #                 try:
    #                     ans = int(input('?: '))
    #                     if ans in MENU_CHOICES:
    #                         ans += 10
    #                         break
    #                     print('Please enter a valid menu choice')
    #                 except:
    #                     print('Please enter a valid menu choice')
    #
    #             if(ans == 11):#raise
    #                 new_bet = int(input('Bet?: '))
    #
    #                 #check if they have that much
    #
    #                 players[0].bet += new_bet
    #                 players[0].money -= new_bet
    #                 bet_level += new_bet
    #                 pot += new_bet
    #             elif(ans == 12):#check
    #                 players[0].check = True
    #             elif(ans == 13):#fold
    #                 players[0].active = False
    #                 players[0].check = True
    #
    #         else:
    #             print('\n1. Raise\n2. Call\n3. Fold\n')
    #
    #             while True:
    #                 try:
    #                     ans = int(input('?: '))
    #                     if ans in MENU_CHOICES:
    #                         ans += 20
    #                         break
    #                     print('Please enter a valid menu choice')
    #                 except:
    #                     print('Please enter a valid menu choice')
    #
    #             if(ans == 21):
    #                 call_needed = bet_level - players[0].bet
    #                 new_bet = int(input('Raise by how much?: '))
    #                 players[0].bet += (call_needed + new_bet)
    #                 players[0].money -= (call_needed + new_bet)
    #                 bet_level += new_bet
    #                 pot += (new_bet + call_needed)
    #             elif(ans == 22):
    #                 new_bet = (bet_level - players[0].bet)
    #                 players[0].bet += new_bet
    #                 players[0].money -= new_bet
    #                 pot += new_bet
    #                 players[0].check = True
    #             elif(ans == 23):
    #                 players[0].active = False
    #                 players[0].check = True
    #
    #     for p in [p for p in players if (p.human == False and p.active == True)]:
    #         if(p.bet == bet_level):
    #             p.check = True
    #         else:
    #             #bounds?
    #             bound1 = 4
    #             bound2 = 9
    #
    #             choice = randint(1,10)
    #
    #             if(choice in range(1, bound1)): #Fold
    #                 p.active = False
    #                 p.check = True
    #                 print('%s folded.' %(p.name))
    #             elif(choice in range(bound1,bound2)): #check
    #                 new_bet = bet_level - p.bet
    #                 p.bet += new_bet
    #                 p.money -= new_bet
    #                 pot += new_bet
    #                 p.check = True
    #             elif(choice in range(bound2,10)): #raise
    #                 call_needed = (bet_level - p.bet)
    #                 new_bet = randint(1,6)
    #                 p.bet += (call_needed + new_bet)
    #                 p.money -= (call_needed + new_bet)
    #                 bet_level += new_bet
    #                 pot += (call_needed + new_bet)
    #
    #
    #     if(players[0].active):
    #         if(players[0].bet == bet_level):
    #             players[0].check = True

    # hand scoring
    for p in [p for p in players if p.active]:
        p.all_cards = table + p.hand
        card_values = [c.value for c in p.all_cards]
        card_suits = [c.suit for c in p.all_cards]

        high_card = 0

        for val in card_values:
            if(card_values.count(val) > 1): # check for any kind of matching
                if(card_values.count(val) == 2):
                    p.hand_points += (10 + (val/2))
                    p.hand_status['Pair'] = True
                if(card_values.count(val) == 3):
                    p.hand_points += ((40) + (val/3))
                    p.hand_status['Three of a Kind'] = True
                if(card_values.count(val) == 4):
                    p.hand_points += ((4000) + (val/4)) ## come back to this one
                    p.hand_status['Four of a Kind'] = True
            #else: # if there has been no matches
            if val > high_card:
                high_card = val

        p.hand_points += high_card
        p.hand_status['High card'] = True

        is_straight = check_for_straight(card_values)
        if(is_straight):
            p.hand_points += (300) # add some sorta value?
            p.hand_status['Straight'] = True

        for suit in SUITS:
            if(card_suits.count(suit) >= 5):
                p.hand_points += 600
                p.hand_status['Flush'] = True

        if(p.hand_status['Pair'] and p.hand_status['Three of a Kind']):
            p.hand_status['Full House'] = True
            p.hand_points += 2000


    input('\nPress any key to see the winner\n\n')

    clear()
    print_cards(players[0].hand, table, pot)

    print('')

    bots = [p for p in players if p.active == True and p.human == False]
    print_ai_cards(bots)

    # determine the winner and do the money
    most_points = max([p.hand_points for p in players if p.active == True]) # better way to do this?
    winners = [p for p in players if p.hand_points == most_points]
    if(len(winners) == 1):
        winners[0].money += pot
        for hand in winners[0].hand_status:
            if winners[0].hand_status[hand]:
                winning_hand = hand
                break
        print('%s won with a %s' %(winners[0].name, winning_hand))

    else:
        share = (pot // len(winners))
        print('the pot was split between ',end=' ') #debug
        for w in winners:
            print('%s, ' %(w.name),end=' ')
            w.money += share
        print('\n')


    # for p in [p for p in players if p.active]:
    #     print(p.name + ': ' + str(p.hand_points) + ' -- ' + str(p.money))


    print('\nPress [enter] to play again, or [q] to quit')
    play_choice = input('')
