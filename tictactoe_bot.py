#Chikezie is cool
import random

class Board_Tree:
	def __init__(self, board, depth, turn, move=None, is_winner=False, play_as = 'O'):
		self.board = board
		self.possible_boards = []
		self.depth = depth
		self.turn = turn
		self.move = move
		self.winner = is_winner
		self.loser_overide = 1
		self.play_as = play_as

	def check_board_for_win(self, board):# returns x won, o won
		for i in range(3):
			if board[0+i*3] + board[1+i*3] + board[2+i*3] == 3 or board[0+i] + board[3+i] + board[6+i] == 3:
				return True, False
			elif board[0+i*3] + board[1+i*3] + board[2+i*3] == 30 or board[0+i] + board[3+i] + board[6+i] == 30:
				return False, True
		#diagonal check
		if board[0] + board[4] + board[8] == 3 or board[2] + board[4] + board[6] == 3:
			return True, False
		elif board[0] + board[4] + board[8] == 30 or board[2] + board[4] + board[6] == 30:
			return False, True
		return False, False

	def get_possible_moves(self):
		possible_moves = []
		for index, value in enumerate(self.board):
			if value == 0:
				possible_moves.append(index)

		return possible_moves

	def get_possible_boards(self):
		for move in self.get_possible_moves():
			new_board = self.board.copy()
			new_board[move] = self.turn
			winner = self.check_board_for_win(new_board)

			if winner[0] and self.play_as == 'O': #if X won
				self.loser_overide = 0
				break
			if winner[1] and self.play_as == 'X': #if X won
				self.loser_overide = 0
				break

			if self.play_as == 'O':
				if self.turn == 1:
					self.possible_boards.append(Board_Tree(board = new_board, depth = self.depth-1, turn = 10, move = move, is_winner = winner[1], play_as=self.play_as))
				elif self.turn == 10:
					self.possible_boards.append(Board_Tree(board = new_board, depth = self.depth-1, turn = 1, move = move, is_winner = winner[1], play_as=self.play_as))

			elif self.play_as == 'X':
				if self.turn == 1:
					self.possible_boards.append(Board_Tree(board = new_board, depth = self.depth-1, turn = 10, move = move, is_winner = winner[0], play_as=self.play_as))
				elif self.turn == 10:
					self.possible_boards.append(Board_Tree(board = new_board, depth = self.depth-1, turn = 1, move = move, is_winner = winner[0], play_as=self.play_as))

	def get_childrens_possible_boards(self):
		for board in self.possible_boards:
			board.get_tree()

	def count_total_combinations(self):
		amount = len(self.possible_boards)
		amount_of_winners = int(self.winner)

		for board in self.possible_boards:
			board_combinations = board.count_total_combinations()
			amount += board_combinations[0]
			amount_of_winners += board_combinations[1]

		return amount, amount_of_winners*self.loser_overide

	def get_tree(self):
		winner = self.check_board_for_win(self.board)
		if not winner[0] and not winner[1]:
			self.get_possible_boards()
			if self.depth > 1 and self.loser_overide == 1: self.get_childrens_possible_boards()

def get_display_board(board):
	board_string = ""
	for index, i in enumerate(board):
		if i == 1:
			board_string += 'X'
		elif i == 10:
			board_string += 'O'
		elif i == 0:
			board_string += '#'

		if (index+1)%3 == 0:
			board_string += '\n'

	return board_string

def bot_move(input_board, input_turn, input_play_as):
	if input_board == [0,0,0,0,0,0,0,0,0]: return 0

	bot_brain = Board_Tree(board = input_board, depth = 8, turn = input_turn, play_as = input_play_as)

	bot_brain.get_tree()

	best_move = None
	amount_of_wining_moves = 0

	for thing in bot_brain.possible_boards:
		thing_winning_moves = thing.count_total_combinations()[1]+thing.loser_overide
		if thing_winning_moves > amount_of_wining_moves:
			amount_of_wining_moves = thing_winning_moves
			best_move = thing

		if thing.winner:
			best_move = thing
			break

	return best_move.move

def get_random_possible_move(board):
	#gets possible moves
	possible_moves = []
	for index, value in enumerate(board):
		if value == 0:
			possible_moves.append(index)
	#returns random index from possible moves
	return possible_moves[random.randint(0,len(possible_moves)-1)]

def check_if_board_full(board):
	for i in board:
		if i == 0:
			return False
	return True

def test_check_for_win(board): # returns x won, o won
	#horizontal and vertical check
	o_won = False
	for i in range(3):
		if board[0+i*3] + board[1+i*3] + board[2+i*3] == 3 or board[0+i] + board[3+i] + board[6+i] == 3:
			return True, False
		elif board[0+i*3] + board[1+i*3] + board[2+i*3] == 30 or board[0+i] + board[3+i] + board[6+i] == 30:
			o_won = True
	if o_won: return False, True #Because if O has 3 in a row in a row looped through before x it will win even though x would have placed first
	#diagonal check
	if board[0] + board[4] + board[8] == 3 or board[2] + board[4] + board[6] == 3:
		return True, False
	elif board[0] + board[4] + board[8] == 30 or board[2] + board[4] + board[6] == 30:
		return False, True
	return None, None

if __name__ == "__main__":
	board = [
	0,0,0,
	0,0,0,
	0,0,0
	] #1 == X and 10 == O
	amount_of_games_to_play = 10 #Games Played: 10000| Bot Wins: 9578| Draws: 422| Random Wins: 0
	games_played = amount_of_games_to_play
	bot_wins = 0
	draws = 0
	random_wins = 0
	while amount_of_games_to_play>0:
		winner = test_check_for_win(board)
		if winner[0]:
			bot_wins += 1
			board = [0,0,0,0,0,0,0,0,0]
			amount_of_games_to_play -= 1

		elif winner[1]:
			print(get_display_board(board), winner)
			random_wins += 1
			board = [0,0,0,0,0,0,0,0,0]
			amount_of_games_to_play -= 1

		elif check_if_board_full(board):
			board = [0,0,0,0,0,0,0,0,0]
			draws += 1
			amount_of_games_to_play -= 1


		board[bot_move(board, 1, 'X')] = 1
		if not check_if_board_full(board): board[get_random_possible_move(board)] = 10

	print(f"Games Played: {games_played}| Bot Wins: {bot_wins}| Draws: {draws}| Random Wins: {random_wins}")