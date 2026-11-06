# Simple Networked Tic-Tac-Toe Server - Milestone 2

# This program is the complete server-side application for the Tic-tac-toe application
# we are working on in the project for CPNT217. It does not need to be edited.

from flask import Flask, jsonify, request

# Create the Flask web application.
app = Flask(__name__)

# Create the game board.
# The board is a one-dimensional list containing 9 positions.
# The positions are indexed from 0 to 8.
# An empty string "" means that the position is empty.
board = ["", "", "", "", "", "", "", "", ""]

# X will be the first player.
# This variable keeps track of whose turn it is.
current_player = "X"

# This variable records whether the game is playing, won, or a draw.
status = "playing"


# This function checks whether a player has won.
# The player parameter will contain either "X" or "O".
def check_winner(player):

    # Check the first row.
    if board[0] == player and board[1] == player and board[2] == player:
        return True

    # Check the second row.
    if board[3] == player and board[4] == player and board[5] == player:
        return True

    # Check the third row.
    if board[6] == player and board[7] == player and board[8] == player:
        return True

    # Check the first column.
    if board[0] == player and board[3] == player and board[6] == player:
        return True

    # Check the second column.
    if board[1] == player and board[4] == player and board[7] == player:
        return True

    # Check the third column.
    if board[2] == player and board[5] == player and board[8] == player:
        return True

    # Check the diagonal from top-left to bottom-right.
    if board[0] == player and board[4] == player and board[8] == player:
        return True

    # Check the diagonal from top-right to bottom-left.
    if board[2] == player and board[4] == player and board[6] == player:
        return True

    # If none of the winning combinations were found,
    # the player has not won.
    return False


# Return the game state as JSON when a client sends HTTP GET.
@app.route("/game/state", methods=["GET"])
def get_state():
    return jsonify({
        "board": board,
        "current_player": current_player,
        "status": status
    })


# Accept a move sent by a client using HTTP POST.
# For Milestone 2, assume that the client sends JSON with an integer position.
@app.route("/game/move", methods=["POST"])
def make_move():
    #"global" allows code in this method to update the values of current_player and status.
    global current_player, status

    #Get the position location from the JSON data in the request, store it in the position variable below.
    data = request.get_json()
    position = data["position"]

    # Make sure the number is a valid board position.
    if position < 0 or position > 8:
        return jsonify({"error": "Invalid position"}), 400

    # Check whether the selected position is already occupied.
    if board[position] != "":
        return jsonify({"error": "Position occupied"}), 409

    # Store the current player's symbol in the selected position.
    board[position] = current_player

    # Check whether the current player has won.
    if check_winner(current_player):
        status = "won"

    # Check whether the game is a draw.
    elif "" not in board:
        status = "draw"

    else:
        status = "playing"

        # Change to the other player, as in the standalone game.
        if current_player == "X":
            current_player = "O"
        else:
            current_player = "X"

    return jsonify({
        "board": board,
        "current_player": current_player,
        "status": status
    })


# Start the server on port 5000.
if __name__ == "__main__":
    app.run(port=5000)
