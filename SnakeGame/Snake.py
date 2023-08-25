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
                                                 fill="lightgrey", outline="black")

    def change_color(self, color):
        self.canvas.itemconfig(self.rect, fill=color)


class Snake:
    def __init__(self, game):
        self.game = game
        self.body = [self.game.board[10][10]]
        self.direction = "Right"
        self.grow = False

    def move(self):
        head = self.body[0]
        new_x, new_y = head.x, head.y

        # Determine new head position based on direction
        if self.direction == "Right": new_x = (new_x + 1) % 20
        elif self.direction == "Left": new_x = (new_x - 1) % 20
        elif self.direction == "Up": new_y = (new_y - 1) % 20
        elif self.direction == "Down": new_y = (new_y + 1) % 20

        new_head = self.game.board[new_x][new_y]

        # Check for collisions
        if new_head in self.body:
            for square in self.body:
                square.change_color("lightgrey")  # Clear the snake's body color
            self.game.restart()

        # Add new head
        self.body.insert(0, new_head)
        new_head.change_color("green")

        # Remove tail if not growing
        if not self.grow:
            tail = self.body.pop()
            tail.change_color("lightgrey")
        else:
            self.grow = False

    def change_direction(self, direction):
        self.direction = direction

    def eat_apple(self):
        self.grow = True


class Apple:
    def __init__(self, game):
        self.game = game
        self.spawn()

    def spawn(self):
        empty_squares = [square for row in self.game.board for square in row if square not in self.game.snake.body]
        square = random.choice(empty_squares)
        square.change_color("red")
        self.square = square



class Game:
    def __init__(self, root):
        pygame.mixer.init()
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        self.score_label = tk.Label(root, text="Score: 0 | Top Score: 0")
        self.score_label.pack()
        self.top_score = 0
        self.start_game()

    def start_game(self):
        #this makes some music run in background, just some generated stuff I found
        pygame.mixer.music.load('AmientMusic1.mp3')
        pygame.mixer.music.play(-1)
        self.board = [[Square(self.canvas, x, y, 20) for y in range(20)] for x in range(20)]
        for row in self.board:
            for square in row:
                square.change_color("lightgrey")
        self.snake = Snake(self)
        self.apple = Apple(self)
        self.score = 0
        self.is_running = False
        self.start_text = self.canvas.create_text(200, 200, text="Press any key to start", font=("Helvetica", 16))
        root.bind("<Key>", self.key_press)

    def key_press(self, event):
        if not self.is_running:
            self.is_running = True
            self.canvas.delete(self.start_text)
            self.run()
        else:
            directions = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
            current_direction = self.snake.direction
            new_direction = event.keysym
            # Prevent snake from moving in opposite direction
            if new_direction in directions and directions[new_direction] != current_direction:
                self.snake.change_direction(new_direction)

    def run(self):
        while self.is_running:
            self.snake.move()
            head = self.snake.body[0]

            # Check if snake eats an apple
            if head == self.apple.square:
                self.snake.eat_apple()
                self.apple.spawn()
                self.score += 1
                self.score_label.config(text=f"Score: {self.score} | Top Score: {self.top_score}")

            self.canvas.update()
            time.sleep(0.1)

    def restart(self):
        # Restart the game and update the top scores
        self.top_score = max(self.score, self.top_score)
        if self.score == self.top_score:
            restart_text = "Congratulations! New top score!"
        else:
            restart_text = "Game restarting"

        # Display the restart text on the canvas
        self.canvas.create_text(200, 200, text=restart_text, font=("Helvetica", 16))
        self.canvas.update()
        time.sleep(2)
        self.canvas.delete("all")
        self.is_running = False  # Reset the running state
        self.start_game()
        self.score_label.config(text=f"Score: 0 | Top Score: {self.top_score}")


root = tk.Tk()
game = Game(root)
root.mainloop()
