from collections import deque

import numpy as np
import random
import math

# =========================
# Define
# =========================

# Define size of board
N, M = (6, 10)

# Define number for each player
number_of_players = 3
number_of_player_objects = 10


# =========================
# Calculation
# =========================

number_of_players_map = {p: number_of_player_objects for p in range(1, number_of_players+1)}

number_of_bots = ((N*M) - (number_of_players*number_of_player_objects))/number_of_player_objects
for i in range(1, number_of_bots+1):
	number_of_players_map[-i] = number_of_player_objects

print number_of_players_map

# New board
board = np.zeros((N, M))

# Suffle players ordering
players_ordering = number_of_players_map.keys()
random.shuffle(players_ordering)

# Tern manager
players_ordering = deque(players_ordering)


while sum(number_of_players_map.values()) > 0:

	# This turn for first player in ordering
	current_player = players_ordering[0]

	# New popability board for current player, at the first time, every point popability = 1.0
	popability_board = np.ones((N, M))
	# Set no popability on stamp point
	popability_board[np.where(board != 0)] = -np.inf

	max_distance = math.sqrt(math.pow(N-1, 2) + math.pow(M-1, 2))

	if current_player > 0:
		current_player_stamps_indices = np.where(board == current_player)
	else:
		current_player_stamps_indices = np.where(board < 0)

	# Loop on current user stamp point
	for n, m in np.transpose(current_player_stamps_indices):
		# Loop on non stamp point
		for i, j in np.transpose(np.where(board == 0)):

			# Calculate distance from each stamp point of current player
			distance = math.sqrt(math.pow(n-i, 2) + math.pow(m-j, 2))

			# Reduce score for each point (max reduce score is 1)
			score = math.log(distance, 100)
			popability_board[i, j] += score


	# Select best point for current player
	indices = np.where(popability_board == popability_board.max())
	max_index = random.randrange(0, len(indices[0]))
	point = (indices[0][max_index], indices[1][max_index])



	# Finish turn
	board[point] = current_player
	number_of_players_map[current_player] -= 1

	# Check for winner and winner out of game 
	if number_of_players_map[current_player] == 0:
		del(players_ordering[0])

	# Prepare next turn for next player
	players_ordering.rotate(-1)

board[np.where(board < 0)] = 0

# End game
print board