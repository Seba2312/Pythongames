import tkinter as tk
import random
import time
import pygame


class Minesweeper:
    def __init__(self, root):
        pygame.mixer.init()

        self.root = root
        self.frame = tk.Frame(root)
        self.frame.pack()
        self.canvas = tk.Canvas(self.root, width=400, height=50)
        self.canvas.pack()
        self.size_options = tk.Frame(root)
        self.size_options.pack()
        self.create_size_buttons()


    #three different size options to play the game
    def create_size_buttons(self):
        small_button = tk.Button(self.size_options, text="Small", command=lambda: self.start_game(20, 3, 2))
        small_button.pack(side=tk.LEFT)
        medium_button = tk.Button(self.size_options, text="Medium", command=lambda: self.start_game(30, 2, 1))
        medium_button.pack(side=tk.LEFT)
        large_button = tk.Button(self.size_options, text="Large", command=lambda: self.start_game(40, 1, 1))
        large_button.pack(side=tk.LEFT)

    def start_game(self, size, width, height):
        pygame.mixer.music.load('AmientMusic1.mp3')
        pygame.mixer.music.play(-1)
        self.size = size
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.mines = [[False for _ in range(size)] for _ in range(size)]
        self.revealed = [[False for _ in range(size)] for _ in range(size)]
        self.frame.destroy()
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.create_grid()
        self.place_mines()

    def create_grid(self):
        for row in range(self.size):
            for col in range(self.size):
                button = tk.Button(self.frame, text=" ", width=self.width, height=self.height, command=lambda r=row, c=col: self.click(r, c))
                button.grid(row=row, column=col)
                self.grid[row][col] = button

    def place_mines(self):
        mine_count = int(self.size * self.size * 0.15) # 15% of the grid will be mines
        while mine_count > 0:
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if not self.mines[row][col]:
                self.mines[row][col] = True
                mine_count -= 1

    def click(self, row, col):
        if self.mines[row][col]:
            self.grid[row][col].config(text="X", bg="red")
            self.game_over()
        else:
            self.reveal(row, col)

    def reveal(self, row, col):
        if row < 0 or row >= self.size or col < 0 or col >= self.size or self.revealed[row][col]:
            return
        self.revealed[row][col] = True
        count = sum(1 for r in range(row - 1, row + 2) for c in range(col - 1, col + 2) if 0 <= r < self.size and 0 <= c < self.size and self.mines[r][c])
        self.grid[row][col].config(text=str(count) if count > 0 else " ", state=tk.DISABLED)
        if count == 0:
            for r in range(row - 1, row + 2):
                for c in range(col - 1, col + 2):
                    self.reveal(r, c)

    def game_over(self):
        for row in range(self.size):
            for col in range(self.size):
                if self.mines[row][col]:
                    self.grid[row][col].config(text="X", bg="red")

        self.canvas.create_text(200, 25, text="Game Over, You hit a mine! Game over.", font=("Helvetica", 16))
        self.root.update()
        time.sleep(2)
        self.canvas.delete("all")

        self.frame.destroy()
        self.size_options.destroy()

        self.canvas.create_text(200, 25, text="Choose a map size to start again", font=("Helvetica", 16))
        self.root.update()
        time.sleep(2)
        self.canvas.delete("all")

        self.__init__(self.root)


root = tk.Tk()
game = Minesweeper(root)
root.mainloop()
