from random import shuffle
import time

RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
SUITS = ['clubs', 'diamonds', 'hearts', 'spades']
DECK_VISUAL = [' ---- ', '|////|', '|////|', '|////|', '|////|', ' ---- ']
suits_graphic = {'clubs':['()', 'oo'], 'diamonds':['/\\', '\\/'], 'hearts':['^^', '\\/'], 'spades':['/\\', 'ˇˇ']}
ranks_values = {'A': 0, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
DECK = []
PLAYER_HAND = []
DEALER_HAND = []

class Card():
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def __str__(self):
        return f'{self.rank} of {self.suit}.'

    def turn(self):
        self.visual = []
        self.visual.append(' ----  ')
        self.visual.append(f'|{self.rank}' + ' '*(4-len(self.rank))+'| ')
        self.visual.append(f'| {suits_graphic[self.suit][0]} | ')
        self.visual.append(f'| {suits_graphic[self.suit][1]} | ')
        self.visual.append('|'+' '*(4-len(self.rank))+f'{self.rank}| ')
        self.visual.append(' ----  ' )

class Reserve():
    def __init__(self, balance):
        self.balance = balance

    def bet(self):
        while True:
            try:
                amount = int(input("How much would you like to bet? "))
            except:
                print("That's not a number!")
            else:
                if (amount > self.balance) or (amount > dealer_reserve.balance):
                    print("Your bet exceeds your or dealer's balance!")
                else:
                    break
        self.balance -= amount
        return amount

    def deposit(self, amount):
        self.balance += amount




def generate_deck():
    for suit in SUITS:
        for rank in RANKS:
            DECK.append(Card(rank, suit))
    shuffle(DECK)

def draw(hand, num):
	card_sum = 0
	for n in range(0, num):
	    try:
	    	hand.append(DECK.pop())
	    	hand[-1].turn()
	    except:
	    	print("The deck was empty, shuffling now ...")
	    	generate_deck()
	    	draw(hand, 1)
	    card_sum += ranks_values[hand[-1].rank]
	return card_sum

def validate_ace_input():
    while True:
        try:
            num = int(input("Do you wish this ace to be of value 1 or 11? "))
        except:
            print("That's not a number.")
        else:
            if num in [1, 11]:
                break
            else:
                num = int(input("That's not a valid number."))
    return num

def choose_aces(hand, num):
	ace_sum = 0
	for card in hand[len(hand)-num:]:
		if card.rank == 'A':
			ace_sum += validate_ace_input()
	return ace_sum

def choose_aces_auto(hand, num):
    ace_sum = 0
    for card in hand[len(hand)-num:]:
        if card.rank == 'A':
            if player_sums['dealer'] < 10:
                ace_sum += 11
            else:
                ace_sum += 1
    return ace_sum

def board():
    print('\n'*16)
    print("Balance:{:4}".format(dealer_reserve.balance) + " "*50 + "Bet: {}".format(current_bet))
    if len(DEALER_HAND) == 0:
        print("\n"*5)
    elif len(DEALER_HAND) == 1:
        for row in range(0,6):
            print(end = ' '*13)
            print(f'{DEALER_HAND[0].visual[row]}{DECK_VISUAL[row]}')
    else:
	    for row in range(0,6):
	        print(end = ' '*13)
	        for card in DEALER_HAND:
	            print(card.visual[row][:(7-2*int(len(DEALER_HAND)/5))], end = '')
	        print(DEALER_HAND[-1].visual[row][(7-2*int(len(DEALER_HAND)/5)):])

    for row in range(0,6):
        print(end = DECK_VISUAL[row])
        if row == 2:
            print(end = "{:4}".format(len(DECK)))
        if row == 3:
            print(end = " left")
        print("")

    if len(PLAYER_HAND) == 0:
        print("\n"*5) 
    else:   
        for row in range(0,6):
            print(end = ' '*13)
            for card in PLAYER_HAND:
                print(card.visual[row][:(7-2*int(len(PLAYER_HAND)/5))], end = '')
            print(PLAYER_HAND[-1].visual[row][(7-2*int(len(PLAYER_HAND)/5)):])

    print("Balance:{:4}".format(player_reserve.balance) + "\n")

def is_bust(player_sum):
	return player_sum > 21

def stay():
	result = input("Hit or Stay? (H/S)")
	while True:
		if result.upper() in ['H', 'S']:
			break
		else:
			result = input("That's not a valid input. Try again: ")
	if result.upper() == 'S':
		return True
	else:
		return False


#GAME CODE
player_reserve = Reserve(100)
dealer_reserve = Reserve(100)
generate_deck()

while True:
    current_bet = 0
    PLAYER_HAND = []
    DEALER_HAND = []
    board()
    current_bet = player_reserve.bet()
    dealer_reserve.deposit(current_bet * (-1))
    player_sums = {'player': 0, 'dealer': 0}
    victory = True
    go = True

    player_sums['dealer'] += draw(DEALER_HAND, 1)
    player_sums['player'] += draw(PLAYER_HAND, 2)

    board()

    player_sums['dealer'] += choose_aces_auto(DEALER_HAND, 1)
    player_sums['player'] += choose_aces(PLAYER_HAND, 2)

    if is_bust(player_sums['player']):
        go = False
        print(end = "BUST! ")

#PLAYER TURN
    while go:
        if stay():
            break
        player_sums['player'] += draw(PLAYER_HAND, 1)
        board()
        player_sums['player'] += choose_aces(PLAYER_HAND, 1)
        if is_bust(player_sums['player']):
            go = False
            victory = False
            print("BUST! You lost your bet.")

#DEALER TURN
    while go:
        time.sleep(1)
        player_sums['dealer'] += draw(DEALER_HAND, 1)
        board()
        player_sums['dealer'] += choose_aces_auto(DEALER_HAND, 1)
        if is_bust(player_sums['dealer']):
            victory = True
            break
        if player_sums['dealer'] > player_sums['player']:
            victory = False
            break

    if victory:
        print("You won the bet!")
        player_reserve.deposit(current_bet * 2)
        time.sleep(2)
    else:
        print("You lost your bet.")
        dealer_reserve.deposit(current_bet * 2)
        time.sleep(2)

    if player_reserve.balance == 0 or dealer_reserve.balance == 0:
        break

if dealer_reserve.balance == 0:
    board()
    print("Congratulations, you won!")
elif player_reserve.balance == 0:
    board()
    print("Game over. Bring more cash next time!")
else:
    print("Something went wrong ...")