import random
import tkinter as tk

# Core Game Logic
class Game2048:
    def __init__(self):
        self.mat = [[0] * 4 for _ in range(4)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(r, c) for r in range(4) for c in range(4) if self.mat[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.mat[r][c] = random.choice([2, 4])

    def get_current_state(self):
        if any(2048 in row for row in self.mat):
            return 'WON'
        if any(0 in row for row in self.mat):
            return 'GAME NOT OVER'
        for i in range(4):
            for j in range(3):
                if self.mat[i][j] == self.mat[i][j + 1] or self.mat[j][i] == self.mat[j + 1][i]:
                    return 'GAME NOT OVER'
        return 'LOST'

    def compress(self):
        changed = False
        new_mat = [[0] * 4 for _ in range(4)]
        for i in range(4):
            pos = 0
            for j in range(4):
                if self.mat[i][j] != 0:
                    new_mat[i][pos] = self.mat[i][j]
                    if j != pos:
                        changed = True
                    pos += 1
        self.mat = new_mat
        return changed

    def merge(self):
        changed = False
        for i in range(4):
            for j in range(3):
                if self.mat[i][j] == self.mat[i][j + 1] and self.mat[i][j] != 0:
                    self.mat[i][j] *= 2
                    self.score += self.mat[i][j]
                    self.mat[i][j + 1] = 0
                    changed = True
        return changed

    def reverse(self):
        self.mat = [row[::-1] for row in self.mat]

    def transpose(self):
        self.mat = [[self.mat[j][i] for j in range(4)] for i in range(4)]

    def move_left(self):
        changed1 = self.compress()
        changed2 = self.merge()
        self.compress()
        return changed1 or changed2

    def move_right(self):
        self.reverse()
        changed = self.move_left()
        self.reverse()
        return changed

    def move_up(self):
        self.transpose()
        changed = self.move_left()
        self.transpose()
        return changed

    def move_down(self):
        self.transpose()
        changed = self.move_right()
        self.transpose()
        return changed

# GUI Implementation
class Game2048GUI:
    def __init__(self, root):
        self.game = Game2048()
        self.root = root
        self.root.title("2048 Game")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        self.create_widgets()
        self.update_grid()
        self.root.bind("<Key>", self.handle_key)

    def create_widgets(self):
        self.frame = tk.Frame(self.root, bg="black")
        self.frame.place(relx=0.5, rely=0.4, anchor="center")
        self.grid_labels = [[tk.Label(self.frame, text="", font=("Helvetica", 24), width=4, height=2, borderwidth=1, relief="solid") for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                self.grid_labels[i][j].grid(row=i, column=j, padx=5, pady=5)
        self.score_label = tk.Label(self.root, text="Score: 0", font=("Helvetica", 18))
        self.score_label.place(relx=0.5, rely=0.85, anchor="center")

    def update_grid(self):
        for i in range(4):
            for j in range(4):
                value = self.game.mat[i][j]
                self.grid_labels[i][j].config(text=str(value) if value != 0 else "", bg=self.get_color(value))
        self.score_label.config(text=f"Score: {self.game.score}")

    def get_color(self, value):
        colors = {
            0: "#CCC0B3", 2: "#EEE4DA", 4: "#EDE0C8", 8: "#F2B179",
            16: "#F59563", 32: "#F67C5F", 64: "#F65E3B", 128: "#EDCF72",
            256: "#EDCC61", 512: "#EDC850", 1024: "#EDC53F", 2048: "#E8BE2E",
            4096: "#E8A700", 8192: "#E59500"
        }
        return colors.get(value, "#CCC0B3")

    def handle_key(self, event):
        key = event.keysym.lower()
        changed = False
        if key == "up":
            changed = self.game.move_up()
        elif key == "down":
            changed = self.game.move_down()
        elif key == "left":
            changed = self.game.move_left()
        elif key == "right":
            changed = self.game.move_right()

        if changed:
            self.game.add_new_tile()
            self.update_grid()
            status = self.game.get_current_state()
            if status != "GAME NOT OVER":
                self.end_game(status)

    def end_game(self, status):
        popup = tk.Toplevel()
        popup.title("Game Over")
        tk.Label(popup, text=status, font=("Helvetica", 24)).pack(pady=20)
        tk.Button(popup, text="OK", command=self.root.quit).pack(pady=10)

# Run the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = Game2048GUI(root)
    root.mainloop()
