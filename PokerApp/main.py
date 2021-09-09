# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python38_app]
# [START gae_python3_app]
from flask import Flask, render_template, request
import random
import time
import math


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = ""
    if request.method == "POST":
        # get url that the user has entered
        try:
            data = request.form
            num_players = int(data['num-players'])
            my_cards = data['my-cards']
            other_cards = data['other-cards']
            cards = []
            for c in my_cards.strip().upper().split(" "):
                try:
                    cards.append(card_to_int(c))
                except:
                    pass
            
            if len(cards) != 2:
                errors.append("I need to know the two cards that you have!")
                raise Exception()
            for c in other_cards.strip().upper().split(" "):
                try:
                    cards.append(card_to_int(c))
                except:
                    pass
            cards_string = ints_to_cards(cards)
            time_allowed = 1
            num_w, total = wins(cards, time_allowed, num_players)
            results = [cards_string, str(round(num_w/total*100,1))+"% ± "+str(round(math.sqrt(num_w/total*(1-num_w/total)/total)*100, 2))+"%, from "+str(total)+" trials"]
        except:
            errors.append("Please make sure your input is valid and try again.")
    return render_template('index.html', errors=errors, results=results)

## for formatting and input/output ##
num_to_card = {0:'2',1:'3',2:'4',3:'5',4:'6',
			   5:'7',6:'8',7:'9',8:'10',9:'J',
			   10:'Q',11:'K',12:'A'} # using Ace-high rules
card_to_num = {}
for n in num_to_card:
	card_to_num[num_to_card[n]] = n
letter_to_suite = {'S':0,'H':1,'D':2,'C':3} # by letter rather than card
suite_to_card = {0:'♠',1:'♥',2:'♦',3:'♣'}
card_to_suite = {'♠':0,'♥':1,'♦':2,'♣':3} 

# output formatting
# go back to card from integer
def int_to_card(n):
	suite = n//13
	num = n%13
	return num_to_card[num]+suite_to_card[suite]

# output formatting
# go back to cards from list of integers
def ints_to_cards(ns):
	string = ""
	for n in ns:
		string += int_to_card(n)+" "
	return string

# input parsing
# use integers 0-51 to represent all 52 cards, without special chars for suites
def card_to_int(c):
	spl = (c[:-1],c[-1]) # number and suite
	n = letter_to_suite[spl[1]]*13+card_to_num[spl[0]]
	return n

# create all combinations with given length of objects from allowed 
def create_combos(allowed, length):
	all_combos = []
	indices = [] # keep track of which ones to include
	for n in range(length):
		indices.append(n)
	all_combos.append([allowed[i] for i in indices]) # add first combo manually
	while indices[0] < len(allowed)-length:
		for i in range(length-1,-1,-1): # go backwards through indices and try to move each
			if indices[i] < len(allowed)-length+i: # as long as this one can be moved, move it [black magic for index math :)]
				indices[i] += 1
				for j in range(i+1,length): # move the other indices backwards
					indices[j] = indices[i] + (j-i)
				break
			else: # need to move the one before this index
				pass
		all_combos.append([allowed[i] for i in indices])
	return all_combos

# calculate points for this set of 5 cards
# return a single integer by doing: (rank by hand)*16^5 + (tiebreaker1)*16^4 + ...
# i.e. shift over like (#1) << 20 + (#2) << 16 + (#3) << 12 + (#4) << 8 + (#5) << 4 + (#6)
def points_for_cards(combo):
	# find numbers and suites
	nums = []
	suites = []
	for c in combo:
		nums.append(c%13) # 0 to 12 = 2 to K=11 then A=12
		suites.append(c//13) # 0 to 3 = Spades to Clubs
	# test if it's a flush
	flush = True
	test_s = suites[0]
	for s in suites:
		if s != test_s:
			flush = False
			break
	# test if it's a straight
	min_card = min(nums)
	straight = True
	if min_card == 0 and 12 in nums: # if bottom is a two (0), should allow for straight from A (12) with min card of A (-1)
		min_card = -1
		for i in range(min_card+1,min_card+5):
			if not i in nums:
				straight = False
				break
	else:
		for i in range(min_card,min_card+5):
			if not i in nums:
				straight = False
				break
	# test for pairs/triples
	repeats = []
	nums_in_combo = set(nums)
	if len(nums_in_combo) != len(nums): # only look for repeats if necessary
		for test_n in nums_in_combo:
			count = 0
			for i in range(5):
				if nums[i] == test_n:
					count += 1
			if count != 1:
				repeats.append((count, test_n))
	repeats.sort()
	# straight flush
	if straight and flush:
		return  (8<<20) + (min_card<<16)
	# four of a kind
	if len(repeats) == 1 and repeats[-1][0] == 4:
		unrep = (nums_in_combo-{repeats[-1][1]}).pop() # find unrepeated num
		return (7<<20)+(repeats[-1][1]<<16)+(unrep<<12)
	# full house (three of a kind + a pair)
	if len(repeats) == 2 and repeats[-1][0] == 3 and repeats[-2][0] == 2:
		return (6<<20)+(repeats[-1][1]<<16)+(repeats[-2][1]<<12)
	# flush
	if flush:
		nums.sort() # sort so we can go highest to lowest
		return (5<<20)+(nums[-1]<<16)+(nums[-2]<<12)+(nums[-3]<<8)+(nums[-4]<<4)+(nums[-5])
	# straight
	if straight:
		return (4<<20)+(min_card<<16)
	# three of a kind
	if len(repeats) == 1 and repeats[-1][0] == 3:
		unrep = list(nums_in_combo-{repeats[-1][1]})
		unrep.sort()
		return (3<<20)+(repeats[-1][1]<<16)+(unrep[-1]<<12)+(unrep[-2]<<8)
	# two pairs
	if len(repeats) == 2 and repeats[-1][0] == 2 and repeats[-2][0] == 2:
		unrep = (nums_in_combo-{repeats[-1][1], repeats[-2][1]}).pop()
		return (2<<20)+(repeats[-1][1]<<16)+(repeats[-2][1]<<12)+(unrep<<8)
	# pair
	if len(repeats) == 1 and repeats[-1][0] == 2:
		unrep = list(nums_in_combo-{repeats[-1][1]})
		unrep.sort()
		return (1<<20)+(repeats[-1][1]<<16)+(unrep[-1]<<12)+(unrep[-2]<<8)+(unrep[-3]<<4)
	# nothing
	nums.sort()
	return (nums[-1]<<16)+(nums[-2]<<12)+(nums[-3]<<8)+(nums[-4]<<4)+(nums[-5])

# take a list of cards and find best five card combo
# return max hand value, using pts function above
def evaluate(cards):
	possible_combos = create_combos(cards, 5)
	max_val = 0
	for c in possible_combos:
		val = points_for_cards(c)
		if val > max_val:
			max_val = val
	return max_val	

# take a list of integer cards and run a game 
# first two cards are mine, next five are shared, remaining are opponents'
def run_game(all_cards, num_players):
	win = True
	my_eval = evaluate(all_cards[:7])
	for i in range(num_players-1):
		win *= my_eval > evaluate(all_cards[2:7]+all_cards[i*2+7:i*2+9])
	return win

# take given cards and make random combinations of remaining to find number of wins and number of total trials
# given cards should be inputted as first two cards are mine, next five are shared, last two are opponents
# t is allowed time to think in seconds
# also can change the number of players (which must be an int ;) )
def wins(known, t, num_players):
	remaining_cards = []
	for i in range(52): # find all remaining cards in deck
		if not i in known:
			remaining_cards.append(i)
	total_w = 0
	total_trials = 0
	cards_needed = 5+num_players*2 - len(known)
	start = time.time()
	while time.time() < start+t:
		new_cards = random.sample(remaining_cards, cards_needed)
		total_w += run_game(known+new_cards, num_players)
		total_trials += 1
	return total_w, total_trials

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python3_app]
# [END gae_python38_app]
