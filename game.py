import tkinter as tk
from tkinter import ttk, messagebox
import random


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0
        self.button = None


class MinesweeperGame:
    # Couleurs pour chaque nombre
    NUMBER_COLORS = {
        1: '#0000FF',  # Bleu
        2: '#008000',  # Vert
        3: '#FF0000',  # Rouge
        4: '#000080',  # Bleu foncé
        5: '#800000',  # Bordeaux
        6: '#008080',  # Cyan
        7: '#000000',  # Noir
        8: '#808080'  # Gris
    }

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Démineur")
        self.root.geometry("800x600")
        self.create_main_menu()

    def create_main_menu(self):
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        title_label = ttk.Label(self.main_frame, text="Démineur", font=('Arial', 24))
        title_label.grid(row=0, column=0, columnspan=2, pady=20)

        ttk.Label(self.main_frame, text="Hauteur:").grid(row=1, column=0, pady=5)
        self.height_var = tk.StringVar(value="10")
        ttk.Entry(self.main_frame, textvariable=self.height_var).grid(row=1, column=1, pady=5)

        ttk.Label(self.main_frame, text="Largeur:").grid(row=2, column=0, pady=5)
        self.width_var = tk.StringVar(value="10")
        ttk.Entry(self.main_frame, textvariable=self.width_var).grid(row=2, column=1, pady=5)

        ttk.Label(self.main_frame, text="Nombre de mines:").grid(row=3, column=0, pady=5)
        self.mines_var = tk.StringVar(value="15")
        ttk.Entry(self.main_frame, textvariable=self.mines_var).grid(row=3, column=1, pady=5)

        start_button = ttk.Button(self.main_frame, text="Nouvelle Partie", command=self.start_game)
        start_button.grid(row=4, column=0, columnspan=2, pady=20)

    def start_game(self):
        try:
            self.height = int(self.height_var.get())
            self.width = int(self.width_var.get())
            self.mines = int(self.mines_var.get())

            if self.height <= 0 or self.width <= 0 or self.mines <= 0:
                raise ValueError("Les valeurs doivent être positives")
            if self.mines >= self.height * self.width:
                raise ValueError("Trop de mines pour la taille du terrain")

            messagebox.showinfo("Nouvelle partie", "La partie va commencer!")
            self.create_game_board()

        except ValueError as e:
            messagebox.showerror("Erreur", str(e))

    def create_game_board(self):
        self.main_frame.grid_remove()

        self.game_frame = ttk.Frame(self.root, padding="10")
        self.game_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Initialisation du plateau
        self.cells = []
        self.first_click = True

        # Création de la grille de cellules
        for x in range(self.height):
            row = []
            for y in range(self.width):
                cell = Cell(x, y)
                cell.button = tk.Button(
                    self.game_frame,
                    width=2,
                    height=1,
                    text="",
                    bg='lightgray',
                    relief=tk.RAISED
                )
                cell.button.grid(row=x, column=y)
                cell.button.bind('<Button-1>', lambda e, x=x, y=y: self.on_cell_click(x, y))
                cell.button.bind('<Button-3>', lambda e, x=x, y=y: self.on_right_click(x, y))
                row.append(cell)
            self.cells.append(row)

        # Bouton retour au menu
        back_button = ttk.Button(self.game_frame, text="Retour au menu", command=self.return_to_menu)
        back_button.grid(row=self.height, column=0, columnspan=self.width, pady=10)

    def place_mines(self, first_x, first_y):
        # Place les mines aléatoirement, en évitant la première case cliquée
        positions = [(x, y) for x in range(self.height) for y in range(self.width)
                     if (x, y) != (first_x, first_y)]
        mine_positions = random.sample(positions, self.mines)

        for x, y in mine_positions:
            self.cells[x][y].is_mine = True

        # Calcul du nombre de mines adjacentes pour chaque cellule
        for x in range(self.height):
            for y in range(self.width):
                if not self.cells[x][y].is_mine:
                    self.cells[x][y].adjacent_mines = self.count_adjacent_mines(x, y)

    def count_adjacent_mines(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                new_x, new_y = x + dx, y + dy
                if (0 <= new_x < self.height and
                        0 <= new_y < self.width and
                        self.cells[new_x][new_y].is_mine):
                    count += 1
        return count

    def on_cell_click(self, x, y):
        cell = self.cells[x][y]

        if cell.is_flagged or cell.is_revealed:
            return

        if self.first_click:
            self.place_mines(x, y)
            self.first_click = False

        if cell.is_mine:
            self.game_over()
        else:
            self.reveal_cell(x, y)
            if self.check_win():
                self.win_game()

    def reveal_cell(self, x, y):
        cell = self.cells[x][y]
        if cell.is_revealed or cell.is_flagged:
            return

        cell.is_revealed = True

        # Configuration commune pour toutes les cellules révélées
        cell.button.config(
            relief=tk.SUNKEN,
            bg='white',
            state='disabled'  # Désactive le bouton une fois révélé
        )

        if cell.adjacent_mines > 0:
            cell.button.config(
                text=str(cell.adjacent_mines),
                fg=self.NUMBER_COLORS.get(cell.adjacent_mines, 'black')  # Couleur selon le nombre
            )
        else:
            # Pour les cellules vides, révéler récursivement les voisines
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    new_x, new_y = x + dx, y + dy
                    if (0 <= new_x < self.height and
                            0 <= new_y < self.width):
                        self.reveal_cell(new_x, new_y)

    def on_right_click(self, x, y):
        cell = self.cells[x][y]
        if not cell.is_revealed:
            cell.is_flagged = not cell.is_flagged
            cell.button.config(
                text='🚩' if cell.is_flagged else '',
                bg='red' if cell.is_flagged else 'lightgray',
                relief=tk.RAISED
            )

            if self.check_win():
                self.win_game()

    def check_win(self):
        for row in self.cells:
            for cell in row:
                if cell.is_mine and not cell.is_flagged:
                    return False
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def game_over(self):
        # Révéler toutes les mines
        for row in self.cells:
            for cell in row:
                if cell.is_mine:
                    cell.button.config(
                        text='💣',
                        bg='red',
                        relief=tk.SUNKEN,
                        state='disabled'  # Désactive toutes les cases à la fin
                    )
                else:
                    cell.button.config(state='disabled')  # Désactive aussi les cases non-mines

        messagebox.showinfo("Game Over", "Vous avez perdu!")
        self.return_to_menu()

    def win_game(self):
        # Désactive toutes les cases à la victoire
        for row in self.cells:
            for cell in row:
                cell.button.config(state='disabled')

        messagebox.showinfo("Victoire", "Félicitations! Vous avez gagné!")
        self.return_to_menu()

    def return_to_menu(self):
        self.game_frame.destroy()
        self.create_main_menu()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = MinesweeperGame()
    game.run()