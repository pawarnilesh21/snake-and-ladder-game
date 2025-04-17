import tkinter as tk
from tkinter import messagebox, simpledialog
import random

class SnakeAndLadderGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake and Ladder")

        # Game configuration
        self.square_size = 40
        self.board_size = 10
        self.canvas_size = self.board_size * self.square_size
        self.player_colors = ["red", "blue", "green", "yellow"]
        self.num_players = 2
        self.player_positions = [1] * self.num_players

        # Prompt for starting player
        self.current_player = self.ask_starting_player()

        # Define snakes and ladders (start: end)
        self.snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
        self.ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

        # Create game elements
        self.create_board()
        self.create_snakes_and_ladders()
        self.create_players()
        self.create_controls()

    def ask_starting_player(self):
        while True:
            try:
                player = simpledialog.askinteger("Starting Player",
                                                 f"Which player will start first? (1 to {self.num_players})")
                if player is None:
                    player = 1  # default to player 1
                    break
                if 1 <= player <= self.num_players:
                    return player - 1
                else:
                    messagebox.showwarning("Invalid Input", f"Please enter a number between 1 and {self.num_players}.")
            except:
                messagebox.showerror("Error", "Invalid input. Please enter a number.")
        return 0

    def create_board(self):
        self.canvas = tk.Canvas(self.master, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack(side=tk.LEFT)

        for position in range(1, 101):
            row, col = self.position_to_coords(position)
            x1 = col * self.square_size
            y1 = row * self.square_size
            x2 = x1 + self.square_size
            y2 = y1 + self.square_size

            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
            self.canvas.create_text(x1 + self.square_size / 2, y1 + self.square_size / 2, text=str(position))

    def create_snakes_and_ladders(self):
        for start, end in self.ladders.items():
            self.draw_connection(start, end, "green")
        for start, end in self.snakes.items():
            self.draw_connection(start, end, "red")

    def draw_connection(self, start, end, color):
        start_row, start_col = self.position_to_coords(start)
        end_row, end_col = self.position_to_coords(end)

        start_x = (start_col + 0.5) * self.square_size
        start_y = (start_row + 0.5) * self.square_size
        end_x = (end_col + 0.5) * self.square_size
        end_y = (end_row + 0.5) * self.square_size

        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=3)
        self.canvas.create_line(end_x, end_y, end_x - 5, end_y - 10, end_x + 5, end_y - 10, fill=color, width=3)

    def create_players(self):
        self.player_tokens = []
        for i in range(self.num_players):
            row, col = self.position_to_coords(1)
            x = (col + 0.5) * self.square_size + (i - 0.5) * 8
            y = (row + 0.5) * self.square_size
            token = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=self.player_colors[i], outline="black")
            self.player_tokens.append(token)

    def create_controls(self):
        control_frame = tk.Frame(self.master)
        control_frame.pack(side=tk.RIGHT, padx=20)

        self.dice_label = tk.Label(control_frame, text="Dice: 0", font=("Arial", 14))
        self.dice_label.pack(pady=10)

        self.roll_button = tk.Button(control_frame, text="Roll Dice", command=self.roll_dice)
        self.roll_button.pack(pady=10)

        self.turn_label = tk.Label(control_frame, text=f"Player {self.current_player + 1}'s turn", font=("Arial", 12))
        self.turn_label.pack(pady=10)

    def position_to_coords(self, position):
        position -= 1
        row = 9 - (position // 10)
        col = position % 10
        if row % 2 == 0:
            col = 9 - col
        return row, col

    def move_player(self, player, new_position):
        if new_position > 100:
            return False
        if new_position in self.snakes:
            new_position = self.snakes[new_position]
        elif new_position in self.ladders:
            new_position = self.ladders[new_position]

        self.player_positions[player] = new_position
        row, col = self.position_to_coords(new_position)
        x = (col + 0.5) * self.square_size + (player - 0.5) * 8
        y = (row + 0.5) * self.square_size
        self.canvas.coords(self.player_tokens[player], x - 10, y - 10, x + 10, y + 10)

        if new_position == 100:
            messagebox.showinfo("Game Over", f"Player {player + 1} wins!")
            self.master.destroy()
        return True

    def roll_dice(self):
        dice = random.randint(1, 6)
        self.dice_label.config(text=f"Dice: {dice}")

        current_pos = self.player_positions[self.current_player]
        new_position = current_pos + dice

        if new_position <= 100:
            success = self.move_player(self.current_player, new_position)
            if not success:
                return

        self.current_player = (self.current_player + 1) % self.num_players
        self.turn_label.config(text=f"Player {self.current_player + 1}'s turn")


if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeAndLadderGame(root)
    root.mainloop()