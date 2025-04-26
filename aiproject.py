import tkinter as tk
from tkinter import messagebox
import random
import pygame
import os
import json
pygame.init()

if not os.path.exists("scores.json"):
    with open("scores.json", "w") as f:
        json.dump({"TicTacToe": 0, "Snake": 0, "Pong": 0, "MemoryMatch": 0}, f)

with open("scores.json", "r") as f:
    scores = json.load(f)

def save_scores():
    with open("scores.json", "w") as f:
        json.dump(scores, f)
root = tk.Tk()
root.title("Game Hub")
root.geometry("600x700")
root.resizable(False, False)

theme = "light"

def set_theme():
    if theme == "light":
        root.configure(bg="#ffffff")
    else:
        root.configure(bg="#2b2b2b")

set_theme()

title = tk.Label(root, text="Game Hub", font=("Arial", 28, "bold"))
title.pack(pady=20)


def play_tictactoe():
    window = tk.Toplevel()
    window.title("Tic Tac Toe")
    window.geometry("400x450")
    window.resizable(False, False)

    current_player = "X"
    board = [""] * 9
    playing_vs_ai = False

    def check_winner():
        wins = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b,c in wins:
            if board[a] == board[b] == board[c] and board[a] != "":
                return board[a]
        if "" not in board:
            return "Draw"
        return None

    def ai_move():
        empty = [i for i, val in enumerate(board) if val == ""]
        move = random.choice(empty)
        click(move)

    def click(i):
        nonlocal current_player
        if board[i] == "":
            board[i] = current_player
            buttons[i].config(text=current_player)
            winner = check_winner()
            if winner:
                if winner != "Draw":
                    messagebox.showinfo("Winner!", f"{winner} wins!")
                    if winner == "X":
                        scores["TicTacToe"] += 1
                else:
                    messagebox.showinfo("Draw", "It's a draw!")
                save_scores()
                window.destroy()
            else:
                current_player = "O" if current_player == "X" else "X"
                if playing_vs_ai and current_player == "O":
                    ai_move()

    buttons = []
    for i in range(9):
        btn = tk.Button(window, text="", font=("Arial", 30), width=5, height=2, command=lambda i=i: click(i))
        btn.grid(row=i//3, column=i%3)
        buttons.append(btn)

    def toggle_ai():
        nonlocal playing_vs_ai
        playing_vs_ai = not playing_vs_ai
        if playing_vs_ai and current_player == "O":
            ai_move()

    ai_button = tk.Button(window, text="Toggle AI", font=("Arial", 12), command=toggle_ai)
    ai_button.grid(row=3, column=0, columnspan=3)


def play_snake():
    window = tk.Toplevel()
    window.title("Snake")

    WIDTH, HEIGHT = 400, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    snake = [(20,20)]
    direction = (20, 0)
    food = (random.randrange(0, WIDTH, 20), random.randrange(0, HEIGHT, 20))

    running = True
    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                save_scores()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = (0, -20)
                elif event.key == pygame.K_DOWN:
                    direction = (0, 20)
                elif event.key == pygame.K_LEFT:
                    direction = (-20, 0)
                elif event.key == pygame.K_RIGHT:
                    direction = (20, 0)

        head = (snake[0][0]+direction[0], snake[0][1]+direction[1])
        snake.insert(0, head)

        if head == food:
            food = (random.randrange(0, WIDTH, 20), random.randrange(0, HEIGHT, 20))
            scores["Snake"] += 1
            save_scores()
        else:
            snake.pop()

        if head[0]<0 or head[1]<0 or head[0]>=WIDTH or head[1]>=HEIGHT or head in snake[1:]:
            running = False

        screen.fill((0,0,0))
        for s in snake:
            pygame.draw.rect(screen, (0,255,0), pygame.Rect(s[0],s[1],20,20))
        pygame.draw.rect(screen, (255,0,0), pygame.Rect(food[0],food[1],20,20))
        pygame.display.update()

def play_pong():
    window = tk.Toplevel()
    window.title("Pong")

    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    ball = pygame.Rect(WIDTH//2, HEIGHT//2, 20, 20)
    ball_speed = [5, 5]
    player = pygame.Rect(WIDTH-20, HEIGHT//2-60, 10, 120)
    ai = pygame.Rect(10, HEIGHT//2-60, 10, 120)

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                save_scores()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.top > 0:
            player.move_ip(0, -6)
        if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
            player.move_ip(0, 6)

        if ai.centery < ball.centery:
            ai.move_ip(0, 5)
        elif ai.centery > ball.centery:
            ai.move_ip(0, -5)

        ball.move_ip(ball_speed)
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed[1] *= -1

        if ball.colliderect(player) or ball.colliderect(ai):
            ball_speed[0] *= -1

        if ball.left <= 0:
            scores["Pong"] += 1
            save_scores()
            running = False
        if ball.right >= WIDTH:
            running = False

        screen.fill((0,0,0))
        pygame.draw.rect(screen, (255,255,255), player)
        pygame.draw.rect(screen, (255,255,255), ai)
        pygame.draw.ellipse(screen, (255,0,0), ball)
        pygame.draw.aaline(screen, (255,255,255), (WIDTH//2, 0), (WIDTH//2, HEIGHT))
        pygame.display.update()

def play_memory():
    window = tk.Toplevel()
    window.title("Memory Match")
    window.geometry("500x600")
    window.resizable(False, False)

    playing_vs_ai = False
    current_player = "Player 1"
    cards = list("AABBCCDDEEFFGGHH")
    random.shuffle(cards)
    revealed = [False] * 16
    selected = []
    player_scores = {"Player 1": 0, "Player 2": 0}

    def update_board():
        for i in range(16):
            if revealed[i]:
                buttons[i].config(text=cards[i])
            else:
                buttons[i].config(text="")

    def ai_turn():
        hidden = [i for i in range(16) if not revealed[i]]
        if len(hidden) >= 2:
            choice = random.sample(hidden, 2)
            click(choice[0])
            window.after(500, lambda: click(choice[1]))

    def click(i):
        nonlocal selected, current_player
        if not revealed[i]:
            selected.append(i)
            buttons[i].config(text=cards[i])
            if len(selected) == 2:
                if cards[selected[0]] == cards[selected[1]]:
                    revealed[selected[0]] = revealed[selected[1]] = True
                    player_scores[current_player] += 1
                else:
                    window.after(1000, lambda: hide_cards(selected))
                    current_player = "Player 2" if current_player == "Player 1" else "Player 1"
                    if playing_vs_ai and current_player == "Player 2":
                        window.after(1500, ai_turn)
                selected = []
                update_board()
                if all(revealed):
                    winner = max(player_scores, key=player_scores.get)
                    messagebox.showinfo("Winner!", f"{winner} wins!")
                    if winner == "Player 1":
                        scores["MemoryMatch"] += 1
                    save_scores()
                    window.destroy()

    def hide_cards(sel):
        for idx in sel:
            buttons[idx].config(text="")
    
    buttons = []
    for i in range(16):
        btn = tk.Button(window, text="", font=("Arial", 20), width=5, height=2, command=lambda i=i: click(i))
        btn.grid(row=i//4, column=i%4, padx=5, pady=5)
        buttons.append(btn)

    def toggle_ai():
        nonlocal playing_vs_ai
        playing_vs_ai = not playing_vs_ai
        if playing_vs_ai and current_player == "Player 2":
            ai_turn()

    ai_button = tk.Button(window, text="Toggle AI", font=("Arial", 12), command=toggle_ai)
    ai_button.pack(pady=10)

btn1 = tk.Button(root, text="Play Tic Tac Toe", font=("Arial", 16), command=play_tictactoe, width=25)
btn1.pack(pady=10)

btn2 = tk.Button(root, text="Play Snake", font=("Arial", 16), command=play_snake, width=25)
btn2.pack(pady=10)

btn3 = tk.Button(root, text="Play Pong", font=("Arial", 16), command=play_pong, width=25)
btn3.pack(pady=10)

btn4 = tk.Button(root, text="Play Memory Match", font=("Arial", 16), command=play_memory, width=25)
btn4.pack(pady=10)

def show_scores():
    score_text = "\n".join([f"{k}: {v}" for k,v in scores.items()])
    messagebox.showinfo("Scores", score_text)

btn_score = tk.Button(root, text="View Scores", font=("Arial", 14), command=show_scores)
btn_score.pack(pady=10)

def toggle_theme():
    global theme
    theme = "dark" if theme == "light" else "light"
    set_theme()

btn_theme = tk.Button(root, text="Toggle Light/Dark", font=("Arial", 14), command=toggle_theme)
btn_theme.pack(pady=10)

root.mainloop()
