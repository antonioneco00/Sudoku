import random
import tkinter as tk
from tkinter import messagebox
from pprint import pprint
import time

def generate_sudoku():
    base = 3
    side = base * base

    def pattern(r, c):
        return (base * (r % base) + r // base + c) % side

    def shuffle(s):
        return random.sample(s, len(s))

    rBase = range(base)
    rows = [g * base + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g * base + c for g in shuffle(rBase) for c in shuffle(rBase)]
    nums = shuffle(range(1, base * base + 1))

    board = [[nums[pattern(r, c)] for c in cols] for r in rows]
    return board

def remove_numbers(board, clues):
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    for i in range(81 - clues):
        r, c = cells[i]
        board[r][c] = 0
    return board

def check_and_update_number(r, c, button, entry_var, solution):
    global errors
    def on_enter(event):
        global errors  # Marcar errors como global
        new_value = entry_var.get()
        if new_value.isdigit() and 1 <= int(new_value) <= 9:
            if int(new_value) == solution[r][c]:  # Si el número es correcto
                button.config(text=new_value, bg="#6f8ee7", state="disabled")  # Azul para correcto
                check_completion()
            else:  # Si el número es incorrecto
                button.config(bg="#f63535")  # Rojo para incorrecto
                errors += 1
                errors_label.config(text=f"Errores: {errors}")
                if errors >= 3:
                    end_game(success=False)
        entry.destroy()

    entry = tk.Entry(root, textvariable=entry_var, font=("Arial", 16), width=2, justify="center")
    entry.grid(row=r, column=c)
    entry.bind("<Return>", on_enter)  # Validar cuando se presiona Enter
    entry.focus_set()

def check_completion():
    for widget in root.grid_slaves():
        if isinstance(widget, tk.Button) and widget["state"] == "normal":
            return  # Si hay botones normales, el juego no ha terminado
    end_game(success=True)

def end_game(success):
    if success:
        messagebox.showinfo("¡Enhorabuena!", "¡Has completado el Sudoku correctamente!")
    else:
        messagebox.showinfo("Fin del juego", "Has alcanzado el límite de errores. Puedes intentarlo de nuevo.")
    
    restart = messagebox.askyesno("Reiniciar", "¿Quieres jugar de nuevo?")
    if restart:
        root.destroy()
        show_difficulty_window()
    else:
        root.destroy()

def create_button(root, r, c, value, solution):
    entry_var = tk.StringVar(value=value if value != 0 else "")
    btn = tk.Button(
        root,
        text=value if value != 0 else "",
        width=4,
        height=2,
        font=("Arial", 16),
        relief="solid",
        bd=1,
        bg="#FFFFFF",
        state="normal" if value == 0 else "disabled",
        command=lambda: check_and_update_number(r, c, btn, entry_var, solution)
    )
    return btn, entry_var

def create_sudoku_board_gui(sudoku_board, solution):
    global root, errors_label, time_label, errors
    root = tk.Tk()
    root.title("Sudoku")

    errors = 0
    errors_label = tk.Label(root, text=f"Errores: {errors}", font=("Arial", 12))
    errors_label.grid(row=10, column=0, columnspan=3, sticky="w")

    time_label = tk.Label(root, text="Tiempo: 0s", font=("Arial", 12))
    time_label.grid(row=10, column=6, columnspan=3, sticky="e")
    update_time()

    cell_size = 50
    padding = 5

    for r in range(9):
        for c in range(9):
            value = sudoku_board[r][c]
            padx = (0, padding) if (c + 1) % 3 == 0 and c != 8 else (0, 0)
            pady = (0, padding) if (r + 1) % 3 == 0 and r != 8 else (0, 0)

            btn, entry_var = create_button(root, r, c, value, solution)
            btn.grid(row=r, column=c, padx=padx, pady=pady)

    root.mainloop()

def update_time():
    global start_time
    elapsed_time = int(time.time() - start_time)
    time_label.config(text=f"Tiempo: {elapsed_time}s")
    root.after(1000, update_time)

def start_game(clues):
    global start_time
    start_time = time.time()
    
    sudoku_solution = generate_sudoku()
    sudoku_board_with_blanks = remove_numbers([row[:] for row in sudoku_solution], clues)
    pprint(sudoku_board_with_blanks)
    create_sudoku_board_gui(sudoku_board_with_blanks, sudoku_solution)

def set_difficulty(difficulty):
    difficulty_window.destroy()
    clues = 60 if difficulty == "fácil" else 50 if difficulty == "media" else 40
    start_game(clues)

def show_difficulty_window():
    global difficulty_window
    difficulty_window = tk.Tk()
    difficulty_window.title("Seleccionar Dificultad")

    label = tk.Label(difficulty_window, text="Selecciona la dificultad:", font=("Arial", 14))
    label.pack(pady=10)

    btn_easy = tk.Button(difficulty_window, text="Fácil (60 clues)", font=("Arial", 12), width=20,
                         command=lambda: set_difficulty("fácil"))
    btn_easy.pack(pady=5)

    btn_medium = tk.Button(difficulty_window, text="Media (50 clues)", font=("Arial", 12), width=20,
                           command=lambda: set_difficulty("media"))
    btn_medium.pack(pady=5)

    btn_hard = tk.Button(difficulty_window, text="Difícil (40 clues)", font=("Arial", 12), width=20,
                         command=lambda: set_difficulty("difícil"))
    btn_hard.pack(pady=5)

    difficulty_window.mainloop()

show_difficulty_window()
