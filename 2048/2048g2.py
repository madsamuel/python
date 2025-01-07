# logic.py
# This file contains all the core logic functions for the 2048 game. It will be imported and used in the main game file.

import random

# Function to get the cell color based on value
def get_color(value):
    colors = {
        0: "#CCC0B3",   # Empty cell - neutral beige
        2: "#EEE4DA",   # Light beige
        4: "#EDE0C8",   # Slightly darker beige
        8: "#F2B179",   # Light orange
        16: "#F59563",  # Soft orange
        32: "#F67C5F",  # Bright orange
        64: "#F65E3B",  # Darker orange
        128: "#EDCF72", # Golden yellow
        256: "#EDCC61", # Rich golden yellow
        512: "#EDC850", # Deep gold
        1024: "#EDC53F", # Vibrant gold
        2048: "#E8BE2E", # Radiant gold with more depth
        4096: "#E8A700", # Bold golden-yellow for higher tiles
        8192: "#E59500", # Orange-gold for very high tiles
    }
    return colors.get(value, "#CCC0B3")

# Initialize the game grid with zeros and add a new '2' tile to start the game
def start_game():
    mat = [[0] * 4 for _ in range(4)]
    print("Commands are as follows:")
    print("'W' or 'w' : Move Up")
    print("'S' or 's' : Move Down")
    print("'A' or 'a' : Move Left")
    print("'D' or 'd' : Move Right")
    add_new_2(mat)
    return mat

# Add a new '2' tile at a random empty position in the grid
def add_new_2(mat):
    empty_cells = [(r, c) for r in range(4) for c in range(4) if mat[r][c] == 0]
    if empty_cells:
        r, c = random.choice(empty_cells)
        mat[r][c] = 2

# Get the current state of the game ('WON', 'GAME NOT OVER', 'LOST')
def get_current_state(mat):
    for row in mat:
        if 2048 in row:
            return 'WON'
    if any(0 in row for row in mat):
        return 'GAME NOT OVER'
    for i in range(4):
        for j in range(3):
            if mat[i][j] == mat[i][j + 1] or mat[j][i] == mat[j + 1][i]:
                return 'GAME NOT OVER'
    return 'LOST'

# Shift non-zero values to the left, filling with zeros
def compress(mat):
    changed = False
    new_mat = [[0] * 4 for _ in range(4)]
    for i in range(4):
        pos = 0
        for j in range(4):
            if mat[i][j] != 0:
                new_mat[i][pos] = mat[i][j]
                if j != pos:
                    changed = True
                pos += 1
    return new_mat, changed

# Merge adjacent cells with the same value
def merge(mat):
    changed = False
    for i in range(4):
        for j in range(3):
            if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                mat[i][j] *= 2
                mat[i][j + 1] = 0
                changed = True
    return mat, changed

# Reverse the rows of the matrix
def reverse(mat):
    return [row[::-1] for row in mat]

# Transpose the matrix (swap rows with columns)
def transpose(mat):
    return [[mat[j][i] for j in range(4)] for i in range(4)]

# Perform the left move operation
def move_left(mat):
    new_mat, changed1 = compress(mat)
    new_mat, changed2 = merge(new_mat)
    new_mat, _ = compress(new_mat)
    return new_mat, changed1 or changed2

# Perform the right move operation
def move_right(mat):
    new_mat = reverse(mat)
    new_mat, changed = move_left(new_mat)
    new_mat = reverse(new_mat)
    return new_mat, changed

# Perform the up move operation
def move_up(mat):
    new_mat = transpose(mat)
    new_mat, changed = move_left(new_mat)
    new_mat = transpose(new_mat)
    return new_mat, changed

# Perform the down move operation
def move_down(mat):
    new_mat = transpose(mat)
    new_mat, changed = move_right(new_mat)
    new_mat = transpose(new_mat)
    return new_mat, changed

# GUI implementation for 2048 using Tkinter
import tkinter as tk

# Create the GUI window
root = tk.Tk()
root.title("2048 Game")
root.geometry("500x600")
root.resizable(False, False)

# Create a frame to hold the grid and center it
frame = tk.Frame(root, bg="black", borderwidth=2, relief="solid")
frame.place(relx=0.5, rely=0.3, anchor="center")

# Create a 4x4 grid of labels
grid_labels = [[tk.Label(frame, text="", font=("Helvetica", 24), width=4, height=2, borderwidth=1, relief="solid") for _ in range(4)] for _ in range(4)]

# Display the labels on the grid
for i in range(4):
    for j in range(4):
        grid_labels[i][j].grid(row=i, column=j, padx=5, pady=5)

# Initialize the game
mat = start_game()

# Instructions label
instructions = tk.Label(root, text="Use W/A/S/D keys to move tiles. Combine tiles to reach 2048!", font=("Helvetica", 14), wraplength=400)
instructions.place(relx=0.5, rely=0.7, anchor="center")

# Function to update the grid visually
def update_grid(mat):
    for i in range(4):
        for j in range(4):
            value = mat[i][j]
            grid_labels[i][j].config(text=str(value) if value != 0 else "", bg=get_color(value))

# Handle key presses
def handle_key(event):
    global mat
    key = event.keysym.lower()
    if key in ["w", "a", "s", "d"]:
        if key == "w":
            mat, changed = move_up(mat)
        elif key == "s":
            mat, changed = move_down(mat)
        elif key == "a":
            mat, changed = move_left(mat)
        elif key == "d":
            mat, changed = move_right(mat)

        if changed:
            add_new_2(mat)
            update_grid(mat)
            status = get_current_state(mat)
            if status != "GAME NOT OVER":
                end_game(status)

# End game popup
def end_game(status):
    popup = tk.Toplevel()
    popup.title("Game Over")
    tk.Label(popup, text=status, font=("Helvetica", 24)).pack(pady=20)
    tk.Button(popup, text="OK", command=root.quit).pack(pady=10)

# Bind key events
root.bind("<Key>", handle_key)

# Update the initial grid
update_grid(mat)

# Run the GUI loop
root.mainloop()
