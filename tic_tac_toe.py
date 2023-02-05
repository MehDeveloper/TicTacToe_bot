#a solved game but this is for learning purposes
from tkinter import *
import random, time
from tictactoe_bot import *

size = 500
third_size = size/3

root = Tk()
root.resizable(False, False)
root.title("Chikezie's TicTacToe")
root.geometry(f"{size}x{size+20}")

canvas = Canvas(root, width=size, height=size, bg="white")
score = StringVar()
score.set("You are gonna lose! :<\nPlayer is X")
score_label = Label(root, textvariable=score)

board = [ #1 == X & 10 == O
0,0,0,
0,0,0,
0,0,0,
]
canvas_board = []
moved = False
first = moved #if false then player is x vise versa
bot_wins = 0
draws = 0
player_wins = 0

def on_press(event):
	global moved
	board_index = (event.x+50)//200 + (event.y+50)//200*3
	if board[board_index] == 0 and moved == False:
		if first: board[board_index] = 10
		elif not first: board[board_index] = 1

		moved = True

	update_canvas_board()

def bot_move_loop():
	global moved, bot_wins, player_wins, draws
	#print('e')
	if moved == True and not check_if_board_full(board):
		if first: board[bot_move(board, 1, 'X')] = 1
		elif not first: board[bot_move(board, 10, 'O')] = 10
		update_canvas_board()
		moved = False

	#Check For Winner
	winner = check_for_win()
	if winner[0]:
		if first: #means bot is x
			bot_wins += 1
		else:
			player_wins += 1
		clear_board()
	elif winner[1]:
		if first: #still means bot is x
			player_wins += 1
		else:
			bot_wins += 1
		clear_board()
	elif check_if_board_full(board):
		draws += 1
		clear_board()

	root.after(100, bot_move_loop)

def update_canvas_board():
	for index, text in enumerate(canvas_board):
		if board[index] == 1:
			canvas.itemconfigure(text, text='X')
		elif board[index] == 10:
			canvas.itemconfigure(text, text='O')
		elif board[index] == 0:
			canvas.itemconfigure(text, text='')

def clear_board():
	global first, board, moved
	board = [0,0,0,0,0,0,0,0,0]
	update_canvas_board()
	first = not first
	moved = first
	if first: var = 'O'
	else: var = 'X' #tells the player what letter they are
	score.set(f"Bot Wins: {bot_wins} | Draws: {draws} | Player Wins: {player_wins}\nPlayer is {var}")

def check_for_win(): # returns x won, o won
	#horizontal and vertical check
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
	return None, None

#create board - lines
for i in range(0,2):
	canvas.create_line(0, i*third_size+third_size, 500, i*third_size+third_size, fill="red")
	canvas.create_line(i*third_size+third_size, 0, i*third_size+third_size, 500, fill="red")
#canvas_board
for y in range(0,3):
	for x in range(0,3):
		canvas_board.append(
			canvas.create_text(x*third_size+third_size/2,y*third_size+third_size/2, text = "")
			)

update_canvas_board()

canvas.bind("<Button-1>", on_press)
score_label.pack()
canvas.pack()

root.after(1000, bot_move_loop)
root.mainloop()