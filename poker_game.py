import sys
import random
from operator import itemgetter
from itertools import chain
import collections

# Global Variables
cardNum = ['2','3','4','5','6','7','8','9','10','J','Q','K','A'] # for printing only
numValues = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":11, "Q":12, "K":13, "A":14} # for comparing values
suits = ['Clubs', 'Spades', 'Hearts', 'Diamonds'] # suits

# Dealer Class
class Dealer:
  def __init__(self, players):
    print("Dealer's dealing \n")

    # Class Variables
    self.used = []
    self.players = players
    self.player_hands = {}

    # Run functions automatically
    self.deal()
    self.pretty_print()
    self.determine_hand_type()

    # Figure out results
    self.find_winner()
    pass
  
  def find_winner(self):
    winner = None
    highest_type = 0
    # Check for highest card type
    for s in self.player_hands:
      if self.player_hands[s] > highest_type:
        winner = s
        highest_type = self.player_hands[s]

    # Check for duplicates
    rev_dict = {} 
    for key, value in self.player_hands.items(): 
        rev_dict.setdefault(value, set()).add(key)
    result = set(chain.from_iterable( 
            values for key, values in rev_dict.items() 
            if len(values) > 1))
    # No duplicates
    if len(result) == 0:
      winner = max(self.player_hands.items(), key=itemgetter(1))[0]
      print(("The winner is {} ! Winner won by {}").format(winner.name, winner.type))
      exit(0)
    else:
      # Compare the one's with duplicate suits
      if self.player_hands[list(result)[0]] < highest_type:
        print(("The winner is {} ! Winner won by {}").format(winner.name, winner.type))
        exit(0)
      else:
        # Naive implementation of just comparing high cards once we find the duplicate card type. Needs fix.
        self.compare_high_card(result)
    pass

  def determine_hand_type(self):
    for player in self.players:
      if player.isRoyalFlush():
        self.player_hands[player] = 10
      elif player.isStraightFlush():
        self.player_hands[player] = 9
      elif player.isFOAK():
        self.player_hands[player] = 8
      elif player.isFH():
        self.player_hands[player] = 7
      elif player.isFlush():
        self.player_hands[player] = 6
      elif player.isStraight():
        self.player_hands[player] = 5
      elif player.isTOAK():
        self.player_hands[player] = 4
      elif player.isTwoPair():
        self.player_hands[player] = 3
      elif player.isOnePair():
        self.player_hands[player] = 2
      else:
        self.player_hands[player] = 1

  def compare_high_card(self, total_players):
    player_vals = {}

    for player in total_players:
      player.high_card_val()
      player_vals[player] = player.high_card

    rev_dict = {} 
    for key, value in player_vals.items(): 
        rev_dict.setdefault(value, set()).add(key)
        
    result = set(chain.from_iterable( 
            values for key, values in rev_dict.items() 
            if len(values) > 1))

    # No duplicates
    if len(result) == 0:
      winner = max(player_vals.items(), key=itemgetter(1))[0]
      print(("The winner is {} ! Winner won by High Card").format(winner.name))
      exit(0)
    # Duplicates
    else:
      print("Duplicate, breaking ties...")
      for player in result:
        player.cardsComp.pop(0)
      self.compare_high_card(result)
      exit(0)
      
  def deal(self):
    for player in self.players:
      while len(player.cards) < 5:
        randNum = random.choice(cardNum)
        randSuit = random.choice(suits)
        card = (randNum, randSuit)
        if card not in self.used:
          player.cards.append(card)
          player.cardsComp.append(numValues[card[0]])
          self.used.append(card)
      # sort cards compare val array for easier popping
      player.cardsComp.sort(reverse=True)

  def pretty_print(self):
    for player in self.players:
      print(("{}'s hand: \n").format(player.name))
      for card in player.cards:
        cardNum, cardSuit = card
        print(("{} of {}").format(cardNum, cardSuit))
      print('\n')
    pass

# Player Class
class Player:
  def __init__(self, name):
    self.name = name
    self.cards = []
    self.cardsComp = []
    self.type = ""
    self.high_card = 0

  # Determine high card
  def high_card_val(self):
    self.high_card = (self.cardsComp[0])

  # Royal Flush
  def isRoyalFlush(self):
    if self.isFlush():
      ranks = [c[0] for c in self.cards]
      if (('A' in ranks) and ('2' in ranks)
        and ('3' in ranks) and ('4' in ranks)
        and ('5' in ranks)):
        self.type = "Royal Flush"
        return True
      else:
        return False

  # Straight Flush
  def isStraightFlush(self):
    if self.isFlush() and self.isStraight():
      self.type = "Straight Flush"
      return True
    else:
      return False
  
  # Flush
  def isFlush(self):
    suits = [c[1] for c in self.cards]
    if len(set(suits)) == 1:
      self.type = "Flush"
      return True
    else:
      return False
  
  # Four of a kind
  def isFOAK(self):
    ranks = [c[0] for c in self.cards]
    counter = collections.Counter(ranks)
    if ((counter.most_common(1))[0][1]) == 4:
      self.type = "Four of a Kind"
      return True
    else:
      return False
  
  # Full House
  def isFH(self):
    ranks = [c[0] for c in self.cards]
    counter = collections.Counter(ranks)
    res = (counter.most_common(2))
    if ((res[0][1]) == 3) and ((res[1][1]) == 2):
      self.type = "Full House"
      return True
    else:
      return False
  
  # Three of a kind
  def isTOAK(self):
    ranks = [c[0] for c in self.cards]
    counter = collections.Counter(ranks)
    if ((counter.most_common(1))[0][1]) == 3:
      self.type = "Three of a Kind"
      return True
    else:
      return False
  
  # Straight
  def isStraight(self):
    ranks = [c for c in self.cardsComp]
    set_of_ranks = set(ranks)
    if ((len(set_of_ranks) == len(self.cards))
      and (max(set_of_ranks) - min(set_of_ranks) + 1) == len(self.cards)):
      self.type = "Straight"
      return True
    else:
      return False
  
  # Two Pair
  def isTwoPair(self):
    ranks = [c[0] for c in self.cards]
    rank_count = collections.defaultdict(lambda:0)
    for c in ranks:
        rank_count[c]+=1
    if sorted(rank_count.values())==[1,2,2]:
      self.type = "Two Pair"
      return True
    else:
      return False
  
  # One Pair
  def isOnePair(self):
    ranks = [c[0] for c in self.cards]
    rank_count = collections.defaultdict(lambda:0)
    for c in ranks:
      rank_count[c]+=1
    if 2 in rank_count.values():
      self.type = "One Pair"
      return True
    else:
      return False

if __name__ == "__main__":
  # Setup
  number_of_players = int(sys.argv[1])
  users = []

  # Take input
  for i in range(number_of_players):
    player = Player(input("Your name please: "))
    users.append(player)

  # Deal cards
  dealer = Dealer(users)
  
  exit(0)