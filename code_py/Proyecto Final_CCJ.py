import tkinter as tk
from tkinter import messagebox
import random
import time

class Game:
    def __init__(self, root, size, num_turns):
        self.root = root
        self.size = size
        self.num_turns = num_turns
        self.current_player = 0
        self.players = []
        self.points = []
        self.timer_running = False
        self.timer_start = 0
        self.timer_limit = 25
        
        self.board = []
        for _ in range(size):
            row = []
            for _ in range(size):
                row.append(0)
            self.board.append(row)
        
        self.create_widgets()
    
    def create_widgets(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        
        self.size_label = tk.Label(self.frame, text="Tamaño del tablero:")
        self.size_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.size_entry = tk.Entry(self.frame)
        self.size_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.start_button = tk.Button(self.frame, text="Iniciar juego", command=self.start_game)
        self.start_button.grid(row=0, column=2, padx=5, pady=5)
        
    def start_game(self):
        size = self.size_entry.get()
        if not size.isdigit() or int(size) < 3:
            messagebox.showerror("Error", "Ingrese un tamaño válido (entero mayor o igual a 3).")
            return
        
        self.size = int(size)
        
        self.frame.destroy()
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        
        self.players_label = tk.Label(self.frame, text="Nombres de los jugadores:")
        self.players_label.grid(row=0, column=0, padx=5, pady=5)
        
        self.players_entry = tk.Entry(self.frame)
        self.players_entry.grid(row=0, column=1, padx=5, pady=5)
        
        self.players_button = tk.Button(self.frame, text="Agregar jugador", command=self.add_player)
        self.players_button.grid(row=0, column=2, padx=5, pady=5)
        
    def add_player(self):
        player_name = self.players_entry.get()
        if not player_name:
            messagebox.showerror("Error", "Ingrese un nombre válido para el jugador.")
            return
        
        self.players.append(player_name)
        self.points.append(0)
        self.players_entry.delete(0, tk.END)
        
        if len(self.players) == 2:
            self.frame.destroy()
            self.frame = tk.Frame(self.root)
            self.frame.pack()
            
            self.turn_label = tk.Label(self.frame, text="Turno del jugador: {}".format(self.players[self.current_player]))
            self.turn_label.pack(padx=5, pady=5)
            
            self.timer_label = tk.Label(self.frame, text="Tiempo restante: {}".format(self.timer_limit))
            self.timer_label.pack(padx=5, pady=5)
            
            self.options_frame = tk.Frame(self.frame)
            self.options_frame.pack(padx=5, pady=5)
            
            self.result_label = tk.Label(self.frame, text="")
            self.result_label.pack(padx=5, pady=5)
            
            self.create_board()
            self.next_turn()
        
    def create_board(self):
        self.board_buttons = []
        
        for i in range(self.size):
            row = []
            for j in range(self.size):
                button = tk.Button(self.frame, text="", width=5, height=2, command=lambda i=i, j=j: self.choose_cell(i, j))
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            self.board_buttons.append(row)
    
    def choose_cell(self, i, j):
        if not self.timer_running:
            self.timer_start = time.time()
            self.timer_running = True
            
        self.board_buttons[i][j]['state'] = tk.DISABLED
        
        neighbors = []
        for x in range(max(0, i-1), min(self.size, i+2)):
            for y in range(max(0, j-1), min(self.size, j+2)):
                neighbors.append(self.board[x][y])
                self.board_buttons[x][y]['text'] = str(self.board[x][y])
        
        result = sum(neighbors) * self.board[i][j]
        options = [result, result + random.randint(1, 5), result - random.randint(1, 5), random.randint(0, 100)]
        random.shuffle(options)
        
        self.show_options(options)
    
    def show_options(self, options):
        for widget in self.options_frame.winfo_children():
            widget.destroy()
        
        for i, option in enumerate(options):
            button = tk.Button(self.options_frame, text=str(option), width=5, height=2, command=lambda option=option: self.check_answer(option))
            button.grid(row=0, column=i, padx=5, pady=5)
    
    def check_answer(self, option):
        self.timer_running = False
        self.timer_start = 0
        
        if option == sum(self.board[i][j] for i in range(self.size) for j in range(self.size)):
            self.points[self.current_player] += 3
            self.result_label.config(text="¡Respuesta correcta! +3 puntos")
        else:
            self.result_label.config(text="Respuesta incorrecta. No se suman puntos")
        
        self.next_turn()
    
    def next_turn(self):
        self.current_player = (self.current_player + 1) % 2
        self.num_turns -= 1
        
        if self.num_turns == 0:
            self.end_game()
        else:
            self.frame.after(1000, self.start_turn)
    
    def start_turn(self):
        self.turn_label.config(text="Turno del jugador: {}".format(self.players[self.current_player]))
        self.result_label.config(text="")
        
        for i in range(self.size):
            for j in range(self.size):
                self.board_buttons[i][j]['text'] = ""
                self.board_buttons[i][j]['state'] = tk.NORMAL
        
        self.timer_running = True
        self.timer_start = time.time()
        self.update_timer()
    
    def update_timer(self):
        if self.timer_running:
            elapsed_time = int(time.time() - self.timer_start)
            remaining_time = max(0, self.timer_limit - elapsed_time)
            self.timer_label.config(text="Tiempo restante: {}".format(remaining_time))
            
            if remaining_time == 0:
                self.timer_running = False
                self.check_answer(None)
            else:
                self.frame.after(1000, self.update_timer)
    
    def end_game(self):
        winner = self.players[self.points.index(max(self.points))]
        messagebox.showinfo("Fin del juego", "El ganador es: {}".format(winner))
        self.root.destroy()

root = tk.Tk()
root.title("Juego de Matrices")
game = Game(root, 3, 2)  # Tamaño del tablero: 3x3, 2 turnos por jugador
root.mainloop()
