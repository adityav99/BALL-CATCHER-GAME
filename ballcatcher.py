import tkinter as tk
from tkinter import messagebox
import csv
import os
import random

# Define CSV filenames for users and scores
USERS_CSV = 'users.csv'
SCORES_CSV = 'scores.csv'

# Initialize CSV files with empty data
def setup_csv():
    if not os.path.exists(USERS_CSV):
        with open(USERS_CSV, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["username", "password"])  # Header for Users

    if not os.path.exists(SCORES_CSV):
        with open(SCORES_CSV, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["username", "score"])  # Header for Scores

# Register a new user
def register():
    username = entry_username.get()
    password = entry_password.get()
    if username and password:
        with open(USERS_CSV, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Check for existing username
            reader = csv.reader(open(USERS_CSV, 'r'))
            for row in reader:
                if row[0] == username:
                    messagebox.showerror("Error", "Username already exists!")
                    return
            
            # Append new user to the Users CSV
            writer.writerow([username, password])
            messagebox.showinfo("Registration", "Registration successful!")
    else:
        messagebox.showwarning("Input Error", "Please enter both username and password")

# Login existing user
def login():
    username = entry_username.get()
    password = entry_password.get()
    with open(USERS_CSV, mode='r') as file:
        reader = csv.reader(file)
        # Check for valid username and password
        for row in reader:
            if row[0] == username and row[1] == password:
                messagebox.showinfo("Login", "Login successful!")
                open_game_window(username)
                return

    messagebox.showerror("Error", "Invalid username or password")

# Ball-catching game
def open_game_window(username):
    game_window = tk.Toplevel(root)
    game_window.title("Ball Catching Game")

    # Set up the canvas
    canvas = tk.Canvas(game_window, width=400, height=400, bg="lightblue")
    canvas.pack()

    # Create a catcher (basket) and score display
    catcher = canvas.create_rectangle(170, 370, 230, 390, fill="darkorange")
    score = 0
    score_text = canvas.create_text(50, 20, text="Score: 0", font=("Arial", 14), fill="black")

    current_ball = None  # Track the current ball on the screen

    # Move catcher
    def move_left(event):
        if canvas.coords(catcher)[0] > 0:  # Prevent moving out of bounds
            canvas.move(catcher, -20, 0)

    def move_right(event):
        if canvas.coords(catcher)[2] < 400:  # Prevent moving out of bounds
            canvas.move(catcher, 20, 0)

    game_window.bind("<Left>", move_left)
    game_window.bind("<Right>", move_right)

    # Drop balls
    def drop_ball():
        nonlocal current_ball
        if current_ball is None:  # Only create a new ball if none exists
            x = random.randint(20, 380)
            ball_color = random.choice(["#FF6347", "#FFD700", "#00FA9A", "#1E90FF", "#FF69B4"])
            current_ball = canvas.create_oval(x, 10, x + 20, 30, fill=ball_color)
        game_window.after(1500, drop_ball)  # Attempt to drop a new ball every 1.5 seconds

    # Update game mechanics
    def update_game():
        nonlocal score, current_ball
        if current_ball:
            canvas.move(current_ball, 0, 5)
            ball_pos = canvas.coords(current_ball)
            catcher_pos = canvas.coords(catcher)

            # Check for collision with catcher
            if (catcher_pos[0] < ball_pos[0] < catcher_pos[2] and
                catcher_pos[1] < ball_pos[1] < catcher_pos[3]):
                canvas.delete(current_ball)
                current_ball = None
                score += 1
                canvas.itemconfig(score_text, text=f"Score: {score}")

            # Remove ball if it hits the bottom
            elif ball_pos[3] >= 400:
                canvas.delete(current_ball)
                current_ball = None
                game_over(username, score)  # End game if a ball reaches the bottom
                return  # Stop the game loop on game over

        game_window.after(50, update_game)

    drop_ball()
    update_game()

# Game over and saving score
def game_over(username, score):
    with open(SCORES_CSV, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Append new score to the Scores CSV
        writer.writerow([username, score])
    
    messagebox.showinfo("Game Over", f"Game Over! Your score: {score}")

# Main login/register interface
root = tk.Tk()
root.title("Ball Catching Game Login")
root.geometry("300x200")

tk.Label(root, text="Username").pack()
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Password").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Login", command=login).pack()
tk.Button(root, text="Register", command=register).pack()

# Initialize the CSV files
setup_csv()

# Start the main loop
root.mainloop()
