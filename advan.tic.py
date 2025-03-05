# Tic Tac Toe Project
import tkinter as tk
from tkinter import messagebox
import pygame
import random

class TicTacToe:
    def __init__(self, root):
        # Initialize the Tic-Tac-Toe game.
        self.root = root
        self.root.title("Tic-Tac-Toe")

        # Initializing sound system
        pygame.mixer.init()

        # Game variables
        self.board = [""] * 9  #3x3 board represented as a list
        self.current_player = "X"  # Start with player X
        self.player_scores = {"X": 0, "O": 0}  # Scoreboard
        self.vs_ai = False  # Default mode: Player vs. Player
        self.game_over = False

        # Set up UI
        self.setup_ui()
        self.reset_game()

    def setup_ui(self):
        # Creating the game interface.
        # Scoreboard
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(pady=10)
        self.score_x = tk.StringVar(value="Player X: 0")
        self.score_o = tk.StringVar(value="Player O: 0")

        tk.Label(self.score_frame, textvariable=self.score_x, font=("Helvetica", 12), fg="blue").pack(side=tk.LEFT, padx=20)
        tk.Label(self.score_frame, textvariable=self.score_o, font=("Helvetica", 12), fg="red").pack(side=tk.RIGHT, padx=20)

        # Game board
        self.buttons = []
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        for i in range(9):
            btn = tk.Button(
                self.board_frame,
                text="",
                font=("Helvetica", 18),
                width=6,
                height=3,
                command=lambda idx=i: self.handle_click(idx),
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        # Control frame with buttons for starting a new game and resetting player scores, added padding for spacing and alignment
        self.control_frame = tk.Frame(self.root)
        self.control_frame.pack(pady=10)

        tk.Button(self.control_frame, text="New Game", font=("Helvetica", 12), command=self.new_game).pack(side=tk.LEFT, padx=10)
        tk.Button(self.control_frame, text="Reset Scores", font=("Helvetica", 12), command=self.reset_scores).pack(side=tk.RIGHT, padx=10)

        # Mode selection frame with buttons to switch between Player vs. Player and Player vs. AI modes
        self.mode_frame = tk.Frame(self.root)
        self.mode_frame.pack(pady=10)

        tk.Button(self.mode_frame, text="Player vs. Player", font=("Helvetica", 12), command=self.set_player_mode).pack(side=tk.LEFT, padx=10)
        tk.Button(self.mode_frame, text="Player vs. AI", font=("Helvetica", 12), command=self.set_ai_mode).pack(side=tk.RIGHT, padx=10)

    def handle_click(self, idx):
        if self.game_over or self.board[idx]:  # Ignore clicks on taken spots or after game ends
            return

        # Updating board and button
        self.board[idx] = self.current_player
        self.update_button(idx)

        # Checking for win or draw
        if self.check_winner():
            self.end_game(f"Player {self.current_player} wins!")
        elif "" not in self.board:
            self.end_game("It's a draw!")
        else:
            self.switch_player()
            if self.vs_ai and self.current_player == "O":  #AI's turn
                self.root.after(500, self.ai_move)

    def ai_move(self):
        # AI makes a move
        available_moves = [i for i, cell in enumerate(self.board) if cell == ""]
        if available_moves:
            move = random.choice(available_moves)
            self.board[move] = self.current_player
            self.update_button(move)

            # Checking for AI win or draw
            if self.check_winner():
                self.end_game("AI wins!")
            elif "" not in self.board:
                self.end_game("It's a draw!")
            else:
                self.switch_player()

    def update_button(self, idx):
        # Changing the appearance of the button based on the player's move
        color = "blue" if self.current_player == "X" else "red"
        self.buttons[idx].config(text=self.current_player, fg=color)

    def switch_player(self):
        # Switching to the next player
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        # Checking if the current player has won
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  
            [0, 4, 8], [2, 4, 6]            
        ]
        for condition in win_conditions:
            if all(self.board[i] == self.current_player for i in condition):
                # Highlight winning cells
                for idx in condition:
                    self.buttons[idx].config(bg="lightgreen")
                return True
        return False

    def end_game(self, message):
        # Ends the game by marking it as over, playing a sound, and displaying a message to the user
        self.game_over = True
        self.play_sound("win.mp3")
        messagebox.showinfo("Game Over", message)

        if "wins" in message:
            self.player_scores[self.current_player] 
            self.update_scores()

    def update_scores(self):
        # Updating the scoreboard
        self.score_x.set(f"Player X: {self.player_scores['X']}")
        self.score_o.set(f"Player O: {self.player_scores['O']}")

    def reset_game(self):
        # Resetting the game board for a new game
        self.board = [""] * 9
        self.current_player = "X"
        self.game_over = False
        for btn in self.buttons:
            btn.config(text="", bg="SystemButtonFace")

    def new_game(self):
        # Starting a new game
        self.reset_game()

    def reset_scores(self):
        # Resetting scores and start a new game
        self.player_scores = {"X": 0, "O": 0}
        self.update_scores()
        self.reset_game()

    def set_player_mode(self):
        # Switching to Player vs. Player mode
        self.vs_ai = False
        self.new_game()

    def set_ai_mode(self):
        # Switching to Player vs. AI mode
        self.vs_ai = True
        self.new_game()

    def play_sound(self, sound_file):
        # Playing a sound
        try:
            pygame.mixer.music.load(sound_file)
            pygame.mixer.music.play()
        except pygame.error:
            print(f"Sound file '{sound_file}' not found.")


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()