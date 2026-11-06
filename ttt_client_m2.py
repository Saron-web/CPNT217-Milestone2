# Simple Networked Tic-Tac-Toe Client - Milestone 2

# This program is an incomplete client-side application for the Tic-tac-toe application
# we are working on in the project for CPNT217. It is NOT complete as given to you.

import requests

# The address of the Tic-Tac-Toe server.
SERVER_URL = "http://127.0.0.1:5000"


# This function displays the current game board.
# The board is supplied by the server, not changed by the client.
def display_board(board):

    print()
    print(f" {board[0]:1} | {board[1]:1} | {board[2]:1} ")
    print("---+---+---")
    print(f" {board[3]:1} | {board[4]:1} | {board[5]:1} ")
    print("---+---+---")
    print(f" {board[6]:1} | {board[7]:1} | {board[8]:1} ")
    print()


# This function requests the current game state from the server.
def get_game_state():
        response = requests.get(SERVER_URL + "/game/state")
        data = response.json()
        return data


# This function sends a player's move to the server.
def send_move(position):
     response = requests.post(
        SERVER_URL + "/game/move",
        json={"position": position}
    )

     data = response.json()
     return data
# Display the game title.
print("TIC-TAC-TOE")

# Show the players how the board positions are numbered.
print()
print("Board positions:")
print("0 | 1 | 2")
print("--+---+--")
print("3 | 4 | 5")
print("--+---+--")
print("6 | 7 | 8")

# Start the main game loop.
while True:

    # Request the latest board and current player from the server.
    game_state = get_game_state()
    board = game_state["board"]
    current_player = game_state["current_player"]
    status = game_state["status"]

    # Display the board before each move.
    display_board(board)

    # Stop when the server reports a completed game.
    if status == "won":
        print("Player " + current_player + " wins!")
        break

    if status == "draw":
        print("The game is a draw!")
        break

    # Ask the current player to enter a board position.
    position = input("Player " + current_player +
                     ", enter a position (0-8): ")

    # Check that the user entered digits.
    if not position.isdigit():
        print("Please enter a number.")
        continue

    # Convert the input from a string to an integer.
    position = int(position)

    # Make sure the number is a valid board position.
    if position < 0 or position > 8:
        print("Please enter a position from 0 to 8.")
        continue

    # Check whether the selected position is already occupied.
    if board[position] != "":
        print("That position is already occupied.")
        continue

    # Send the move to the server; the server changes the game state.
    result = send_move(position)

    # The next loop iteration retrieves the updated board from the server.
