import tkinter as tk
import random

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")
        self.grid = [[0] * 4 for _ in range(4)]
        self.labels = [[None] * 4 for _ in range(4)]
        self.create_ui()
        self.initialize_grid()
        self.root.bind("<Key>", self.handle_keypress)
        self.root.bind("<Return>", self.restart_game)
        self.game_over_label = None

    def initialize_grid(self):
        self.grid = [[0] * 4 for _ in range(4)]
        self.add_new_number()
        self.add_new_number()
        self.update_ui()

    def create_ui(self):
        self.frame = tk.Frame(self.root, bg='azure3')
        self.frame.grid(sticky='nsew')

        for i in range(4):
            for j in range(4):
                label = tk.Label(self.frame, text="", width=4, height=2, font=("Helvetica", 24),
                                 bg="lightgrey", fg="black", borderwidth=2, relief="groove")
                label.grid(row=i, column=j, padx=5, pady=5, sticky='nsew')
                self.labels[i][j] = label

        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_game, font=("Helvetica", 16))
        self.restart_button.grid(row=5, column=0, columnspan=4, pady=10)

    def add_new_number(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = random.choice([2, 4])

    def update_ui(self):
        for i in range(4):
            for j in range(4):
                value = self.grid[i][j]
                self.labels[i][j].config(text=str(value) if value != 0 else "", bg=self.get_tile_color(value))

    def get_tile_color(self, value):
        colors = {
            0: "lightgrey",
            2: "papaya whip",
            4: "peach puff",
            8: "light salmon",
            16: "orange",
            32: "tomato",
            64: "red",
            128: "yellow",
            256: "gold",
            512: "light goldenrod",
            1024: "light yellow",
            2048: "light green"
        }
        return colors.get(value, "white")

    def merge_left(self, row):
        new_row = [num for num in row if num != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                new_row[i + 1] = 0
        new_row = [num for num in new_row if num != 0]
        return new_row + [0] * (4 - len(new_row))

    def move_left(self):
        moved = False
        for i in range(4):
            original_row = self.grid[i]
            new_row = self.merge_left(self.grid[i])
            if original_row != new_row:
                self.grid[i] = new_row
                moved = True
        return moved

    def move_right(self):
        moved = False
        for i in range(4):
            original_row = self.grid[i]
            new_row = self.merge_left(self.grid[i][::-1])[::-1]
            if original_row != new_row:
                self.grid[i] = new_row
                moved = True
        return moved

    def move_up(self):
        moved = False
        for j in range(4):
            col = self.merge_left([self.grid[i][j] for i in range(4)])
            for i in range(4):
                if self.grid[i][j] != col[i]:
                    moved = True
                self.grid[i][j] = col[i]
        return moved

    def move_down(self):
        moved = False
        for j in range(4):
            col = self.merge_left([self.grid[i][j] for i in range(4)][::-1])[::-1]
            for i in range(4):
                if self.grid[i][j] != col[i]:
                    moved = True
                self.grid[i][j] = col[i]
        return moved

    def handle_keypress(self, event):
        key = event.keysym
        if key in ["Up", "Down", "Left", "Right"]:
            moved = False
            if key == "Up":
                moved = self.move_up()
            elif key == "Down":
                moved = self.move_down()
            elif key == "Left":
                moved = self.move_left()
            elif key == "Right":
                moved = self.move_right()

            if moved:
                self.add_new_number()
                self.update_ui()
                if self.is_game_over():
                    self.show_game_over()
                if self.has_won():
                    self.show_win_message()

    def is_game_over(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return False
                if i < 3 and self.grid[i][j] == self.grid[i + 1][j]:
                    return False
                if j < 3 and self.grid[i][j] == self.grid[i][j + 1]:
                    return False
        return True

    def has_won(self):
        for row in self.grid:
            if 2048 in row:
                return True
        return False

    def show_game_over(self):
        self.clear_message()
        self.game_over_label = tk.Label(self.root, text="Game Over!", font=("Helvetica", 24), fg="red")
        self.game_over_label.grid(row=6, column=0, columnspan=4)

    def show_win_message(self):
        self.clear_message()
        win_label = tk.Label(self.root, text="You got 2048!", font=("Helvetica", 24), fg="green")
        win_label.grid(row=6, column=0, columnspan=4)

    def clear_message(self):
        if self.game_over_label:
            self.game_over_label.destroy()
            self.game_over_label = None

    def restart_game(self, event=None):
        self.initialize_grid()
        self.update_ui()
        self.clear_message()

# Run the game
root = tk.Tk()
game = Game2048(root)
root.mainloop()
