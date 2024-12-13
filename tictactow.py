import tkinter as tk
from tkinter import messagebox
import math

# Constants
PLAYER = "X"
AI = "O"
EMPTY = " "
GRID_SIZE = 3
FONT = ("Helvetica", 24, "bold")
BUTTON_FONT = ("Helvetica", 20, "bold")
BG_COLOR = "#F0F0F0"
PLAYER_COLOR = "#1E90FF"  # Dodger Blue
AI_COLOR = "#FF4500"      # Orange Red
HIGHLIGHT_COLOR = "#90EE90"  # Light Green
BUTTON_COLOR = "#FFFFFF"
BUTTON_ACTIVE_COLOR = "#D3D3D3"

class TicTacToe:
    def __init__(self, root):
        """
        __init__ constructor method for TicTacToe class

        Parameters
        ----------
        root : tkinter.Tk
            The root window of the application

        Attributes
        ----------
        root : tkinter.Tk
            The root window of the application
        board : list
            A list of length 9 containing the current state of the board
        buttons : list
            A list of 9 tkinter.Button widgets, one for each cell of the board
        current_turn : str
            Either PLAYER or AI, indicating whose turn it is
        player_score : int
            The number of games won by the player
        ai_score : int
            The number of games won by the AI
        draws : int
            The number of draws
        games_played : int
            The total number of games played

        Methods
        -------
        create_widgets
        """
        self.root = root
        self.root.title("Enhanced Tic Tac Toe with AI")
        self.root.configure(bg=BG_COLOR)
        
        self.board = [EMPTY for _ in range(9)]
        self.buttons = []
        self.current_turn = PLAYER  # Player starts first

        # Score Tracking
        self.player_score = 0
        self.ai_score = 0
        self.draws = 0
        self.games_played = 0

        self.create_widgets()

    def create_widgets(self):
        # Create Score Frame
        """
        Create all the widgets for the game window.

        This method creates the following widgets:

        1. A score frame with a label displaying the current score.
        2. A grid frame containing 9 buttons for the Tic Tac Toe game.
        3. A control frame containing two buttons, one to reset the game and
           one to exit the game.

        The method also configures the grid weights of the grid frame for
        responsiveness.
        """
        score_frame = tk.Frame(self.root, bg=BG_COLOR)
        score_frame.pack(pady=10)

        self.score_label = tk.Label(score_frame, text=self.get_score_text(), font=("Helvetica", 14), bg=BG_COLOR)
        self.score_label.pack()

        # Create Tic Tac Toe Grid
        grid_frame = tk.Frame(self.root, bg=BG_COLOR)
        grid_frame.pack(pady=10)

        for i in range(9):
            button = tk.Button(grid_frame, text=EMPTY, font=BUTTON_FONT, width=6, height=3,
                               bg=BUTTON_COLOR, activebackground=BUTTON_ACTIVE_COLOR,
                               command=lambda i=i: self.on_button_click(i))
            button.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="nsew")
            self.buttons.append(button)

        # Configure grid weights for responsiveness
        for i in range(3):
            grid_frame.rowconfigure(i, weight=1)
            grid_frame.columnconfigure(i, weight=1)

        # Create Control Buttons
        control_frame = tk.Frame(self.root, bg=BG_COLOR)
        control_frame.pack(pady=10)

        reset_button = tk.Button(control_frame, text="Reset Game", font=("Helvetica", 12, "bold"),
                                 bg="#FFA07A", fg="#FFFFFF", activebackground="#FA8072",
                                 command=self.reset_board)
        reset_button.grid(row=0, column=0, padx=10)

        exit_button = tk.Button(control_frame, text="Exit", font=("Helvetica", 12, "bold"),
                                bg="#B0C4DE", fg="#FFFFFF", activebackground="#ADD8E6",
                                command=self.root.quit)
        exit_button.grid(row=0, column=1, padx=10)

    def get_score_text(self):
        """
        Returns a formatted string representing the current game statistics.

        The string includes the total number of games played, the number of games
        won by the player, the number of games won by the AI, and the number of draws.
        """
        return (f"Games Played: {self.games_played}    "
                f"Player (X) Wins: {self.player_score}    "
                f"AI (O) Wins: {self.ai_score}    "
                f"Draws: {self.draws}")

    def on_button_click(self, index):
        if self.board[index] == EMPTY and self.current_turn == PLAYER:
            self.make_move(index, PLAYER)
            if not self.check_game_over():
                self.current_turn = AI
                self.root.after(500, self.ai_move)

    def make_move(self, index, player):
        self.board[index] = player
        button = self.buttons[index]
        button.config(text=player)
        if player == PLAYER:
            button.config(fg=PLAYER_COLOR)
        else:
            button.config(fg=AI_COLOR)
        self.animate_button(button)
        winner = self.check_winner()
        if winner:
            self.end_game(winner)
        elif EMPTY not in self.board:
            self.end_game(None)

    def animate_button(self, button):
        # Simple animation: change color briefly
        original_color = button.cget("bg")
        button.config(bg=HIGHLIGHT_COLOR)
        self.root.after(200, lambda: button.config(bg=original_color))

    def ai_move(self):
        """
        AI's turn: make a move using the minimax algorithm.

        Call minimax to find the best move, then call make_move to
        execute it. If the game is not over, switch to the player's turn.
        """
        index = self.minimax(self.board, True)['index']
        self.make_move(index, AI)
        if not self.check_game_over():
            self.current_turn = PLAYER

    def check_game_over(self):
        """
        Returns True if the game is over, False otherwise.

        The game is over if there is a winner (check_winner returns a winner),
        or if all cells on the board are filled (i.e., there are no more EMPTY cells).
        If the game is over, end_game is called to update the score and display
        a message to the user.

        Returns
        -------
        bool
            True if the game is over, False otherwise
        """
        winner = self.check_winner()
        if winner:
            self.end_game(winner)
            return True
        elif EMPTY not in self.board:
            self.end_game(None)
            return True
        return False

    def end_game(self, winner):
        """
        Ends the game by updating the score, displaying the result, and resetting the board.

        Parameters
        ----------
        winner : str or None
            The winner of the game. It can be PLAYER, AI, or None if it's a draw.

        This method increments the total number of games played. If there is a winner,
        it updates the corresponding score for the player or AI. If there is no winner,
        it increments the number of draws. A messagebox is shown to inform the user of
        the result, and the game board is reset for a new game.
        """
        self.games_played += 1
        if winner == PLAYER:
            self.player_score += 1
            message = "You win!"
        elif winner == AI:
            self.ai_score += 1
            message = "AI wins!"
        else:
            self.draws += 1
            message = "It's a draw!"
        
        self.score_label.config(text=self.get_score_text())
        messagebox.showinfo("Game Over", message)
        self.reset_board()

    def reset_board(self):
        """
        Resets the game board to its initial state.

        The board is reset to be empty, and the current turn is set to the player.
        All buttons are reset to display nothing, and their foreground color is set to black.
        The score display is not changed.
        """
        self.board = [EMPTY for _ in range(9)]
        for button in self.buttons:
            button.config(text=EMPTY, fg="#000000")
        self.current_turn = PLAYER

    def check_winner(self):
        """
        Determines if there is a winner on the current game board.

        This method checks all possible winning combinations (rows, columns, diagonals)
        to see if there are three identical markers (either PLAYER or AI) in a line.
        If a winning combination is found, it highlights the winning buttons and returns
        the marker of the winner.

        Returns
        -------
        str or None
            The marker of the winner (PLAYER or AI) if a winner exists, otherwise None.
        """
        win_combinations = [
            [0,1,2], [3,4,5], [6,7,8],  # Rows
            [0,3,6], [1,4,7], [2,5,8],  # Columns
            [0,4,8], [2,4,6]            # Diagonals
        ]
        for combo in win_combinations:
            if self.board[combo[0]] != EMPTY and \
               self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]]:
                self.highlight_winning_combo(combo)
                return self.board[combo[0]]
        return None

    def highlight_winning_combo(self, combo):
        """
        Highlights the buttons in a winning combination by setting their
        background color to HIGHLIGHT_COLOR.

        Parameters
        ----------
        combo : list
            A list of three indices of the buttons to be highlighted
        """
        for index in combo:
            self.buttons[index].config(bg=HIGHLIGHT_COLOR)

    def minimax(self, new_board, is_maximizing):
        """
        A recursive function that implements the Minimax algorithm.

        This function is used to determine the best move for the AI player by
        recursively exploring all possible moves and their outcomes.

        Parameters
        ----------
        new_board : list
            A list of length 9 representing the current state of the game board.
        is_maximizing : bool
            A boolean indicating whether the current player is the AI (maximizing)
            or the user (minimizing).

        Returns
        -------
        dict
            A dictionary containing the score of the best move and the index
            of the best move in the game board.
        """
        winner = self.check_winner_minimax(new_board)
        if winner == AI:
            return {'score': 1}
        elif winner == PLAYER:
            return {'score': -1}
        elif EMPTY not in new_board:
            return {'score': 0}

        if is_maximizing:
            best = {'score': -math.inf}
            for i in range(9):
                if new_board[i] == EMPTY:
                    new_board[i] = AI
                    score = self.minimax(new_board, False)
                    new_board[i] = EMPTY
                    score['index'] = i
                    if score['score'] > best['score']:
                        best = score
            return best
        else:
            best = {'score': math.inf}
            for i in range(9):
                if new_board[i] == EMPTY:
                    new_board[i] = PLAYER
                    score = self.minimax(new_board, True)
                    new_board[i] = EMPTY
                    score['index'] = i
                    if score['score'] < best['score']:
                        best = score
            return best

    def check_winner_minimax(self, board):
        """
        Checks if there is a winner on the given game board.

        This method takes a list of length 9 representing the current state of the game board
        and checks all possible winning combinations (rows, columns, diagonals) to see
        if there are three identical markers (either PLAYER or AI) in a line.
        If a winning combination is found, it returns the marker of the winner.

        Returns
        -------
        str or None
            The marker of the winner (PLAYER or AI) if a winner exists, otherwise None.
        """
        win_combinations = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]
        for combo in win_combinations:
            if board[combo[0]] != EMPTY and \
               board[combo[0]] == board[combo[1]] == board[combo[2]]:
                return board[combo[0]]
        return None

def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()
