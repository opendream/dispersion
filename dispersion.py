from collections import deque

import numpy as np
import random
import math

# =========================
# Define
# =========================

# Define size of board
N, M = (10, 15)

# Define number for each player
number_of_players = {
	1: 25,
	2: 25,
	3: 25
}

# =========================
# Calculation
# =========================

# New board
board = np.zeros((N, M))

# Suffle players ordering
players_ordering = number_of_players.keys()
random.shuffle(players_ordering)

# Tern manager
players_ordering = deque(players_ordering)


while sum(number_of_players.values()) > 0:

	# This turn for first player in ordering
	current_player = players_ordering[0]

	# New popability board for current player, at the first time, every point popability = 1.0
	popability_board = np.ones((N, M))
	# Set no popability on stamp point
	popability_board[np.where(board != 0)] = -np.inf

	max_distance = math.sqrt(math.pow(N-1, 2) + math.pow(M-1, 2))

	# Loop on current user stamp point
	for n, m in np.transpose(np.where(board == current_player)):
		# Loop on non stamp point
		for i, j in np.transpose(np.where(board == 0)):

			# Calculate distance from each stamp point of current player
			distance1 = math.sqrt(math.pow(n-i, 2) + math.pow(m-j, 2))
			distance2 = math.sqrt(math.pow(n-(N-i), 2) + math.pow(m-j, 2))
			distance3 = math.sqrt(math.pow(n-i, 2) + math.pow(m-(M-j), 2))
			distance4 = math.sqrt(math.pow(n-(N-i), 2) + math.pow(m-(M-j), 2))
			distance = min(distance1, distance2, distance3, distance4)

			# Reduce score for each point (max reduce score is 1)
			reduce_score = 1 - (distance/max_distance)
			popability_board[i, j] -= reduce_score


	# Select best point for current player
	indices = np.where(popability_board == popability_board.max())
	max_index = random.randrange(0, len(indices[0]))
	point = (indices[0][max_index], indices[1][max_index])



	# Finish turn
	board[point] = current_player
	number_of_players[current_player] -= 1

	# Check for winner and winner out of game 
	if number_of_players[current_player] == 0:
		del(players_ordering[0])

	# Prepare next turn for next player
	players_ordering.rotate(-1)


# End game
print board