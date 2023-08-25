import tkinter as tk
import random
import time
import pygame

class Square:
    def __init__(self, canvas, x, y, size):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.rect = self.canvas.create_rectangle(self.x * self.size, self.y * self.size,
                                                 (self.x + 1) * self.size, (self.y + 1) * self.size,
                                                 fill="lightgrey", outline="lightgrey")

    def change_color(self, color):
        self.canvas.itemconfig(self.rect, fill=color)

class Bird:
    def __init__(self, game):
        self.game = game
        self.x = 5
        self.y = 30
        self.square = self.game.board[self.x][self.y]
        self.square.change_color("blue")
        self.velocity = 0

    def move(self):
        # Apply gravity
        self.velocity += 1
        self.y += self.velocity
        self.y = max(0, min(59, self.y))

        # Check for collisions
        if self.game.board[self.x][self.y] in self.game.pipes or self.y == 59:
            self.game.restart()

        # Update bird's position
        self.square.change_color("lightgrey")
        self.square = self.game.board[self.x][self.y]
        self.square.change_color("blue")

    def jump(self):
        self.velocity = -5

class Game:
    def __init__(self, root):
        pygame.mixer.init()
        self.canvas = tk.Canvas(root, width=800, height=600)  # Restore original height
        self.canvas.pack()
        self.score_label = tk.Label(root, text="Score: 0 | Top Score: 0")
        self.score_label.pack()
        self.top_score = 0
        self.start_game()

    def start_game(self):
        pygame.mixer.music.load('AmientMusic1.mp3')
        pygame.mixer.music.play(-1)
        self.board = [[Square(self.canvas, x, y, 10) for y in range(60)] for x in range(80)]  # Double pixel concentration
        self.bird = Bird(self)
        self.pipes = []
        self.score = 0
        self.is_running = False
        self.start_text = self.canvas.create_text(400, 300, text="Press any key to start", font=("Helvetica", 16))
        root.bind("<Key>", self.key_press)
        self.pipe_counter = 0

    def key_press(self, event):
        if not self.is_running:
            self.is_running = True
            self.canvas.delete(self.start_text)
            self.run()
        else:
            if event.keysym == "space":
                self.bird.jump()

    def run(self):
        while self.is_running:
            self.bird.move()
            self.move_pipes()
            if self.pipe_counter % 40 == 0:
                self.spawn_pipe()
            self.pipe_counter += 1
            self.canvas.update()
            time.sleep(0.1)

    def spawn_pipe(self):
        gap_size = 5
        gap_start = random.randint(1, 54)
        pipe = []
        for y in range(60):
            if y < gap_start or y > gap_start + gap_size:
                for x in range(79, 77, -1):  # Two pixels thick
                    square = self.board[x][y]
                    square.change_color("brown")
                    pipe.append(square)
        self.pipes += pipe

    def move_pipes(self):
        for pipe_square in self.pipes:
            pipe_square.change_color("lightgrey")
        new_pipes = []
        for pipe_square in self.pipes:
            x, y = pipe_square.x - 1, pipe_square.y
            if x >= 0:
                square = self.board[x][y]
                square.change_color("brown")
                new_pipes.append(square)
        self.pipes = new_pipes
        if self.pipes and self.pipes[0].x == 0:
            self.score += 1
            self.top_score = max(self.score, self.top_score)
            self.score_label.config(text=f"Score: {self.score} | Top Score: {self.top_score}")

    def restart(self):
        self.top_score = max(self.score, self.top_score)
        restart_text = "Game restarting"
        self.canvas.create_text(400, 300, text=restart_text, font=("Helvetica", 16))
        self.canvas.update()
        time.sleep(2)
        self.canvas.delete("all")
        self.is_running = False
        self.start_game()
        self.score_label.config(text=f"Score: 0 | Top Score: {self.top_score}")

root = tk.Tk()
game = Game(root)
root.mainloop()
