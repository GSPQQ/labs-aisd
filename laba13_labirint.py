import tkinter as tk
from tkinter import messagebox
import random

root = None
canvas = None
timer_label = None

COLS = 20 
ROWS = 20 
CELL_SIZE = 20
TIME_LIMIT_SEC = 60  

maze = []
player_pos = (1, 1)
exit_pos = []
_player_id = None

game_over = False
moving = False
remaining = TIME_LIMIT_SEC
stack = []
visited = set()

def generate_maze():
    global maze, player_pos, exit_positions, COLS, ROWS
    
    COLS = COLS if COLS % 2 == 1 else COLS + 1
    ROWS = ROWS if ROWS % 2 == 1 else ROWS + 1
    
    maze = [[True for _ in range(COLS)] for _ in range(ROWS)]

    def gen(x, y):
        maze[y][x] = False
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < COLS - 1 and 0 < ny < ROWS - 1 and maze[ny][nx]:
                maze[y + dy // 2][x + dx // 2] = False
                gen(nx, ny)

    gen(1, 1)

    passages = []
    for y in range(1, ROWS - 1):
        for x in range(1, COLS - 1):
            if not maze[y][x]:
                passages.append((x, y))

    if len(passages) >= 2:
        random.shuffle(passages)
        num_exits = random.randint(1, min(3, len(passages) - 1))
        exit_positions = [passages.pop() for _ in range(num_exits)]
        player_pos = passages.pop()
    else:
        player_pos = (1, 1)
        exit_positions = [(COLS - 2, ROWS - 2)]

def draw_maze():
    """Рисует лабиринт на холсте."""
    global canvas, maze, exit_positions, COLS, ROWS, CELL_SIZE # <-- Обновлено
    canvas.delete("all")
    canvas.config(bg="#f9fbe7") 
    
    for y in range(ROWS):
        for x in range(COLS):
            cx, cy = x * CELL_SIZE, y * CELL_SIZE
            if maze[y][x]:
                canvas.create_rectangle(
                    cx, cy, cx + CELL_SIZE, cy + CELL_SIZE,
                    fill="#1a237e", outline="" 
                )
    for ex, ey in exit_positions:
        cx = ex * CELL_SIZE + CELL_SIZE // 2
        cy = ey * CELL_SIZE + CELL_SIZE // 2
        canvas.create_text(cx, cy, text="EXIT", fill="#ff1744", font=("Arial", 10, "bold"))

def draw_player():
    """Рисует паучка на текущей позиции."""
    global canvas, player_pos, CELL_SIZE, _player_id
    if _player_id:
        canvas.delete(_player_id)
    x, y = player_pos
    cx = x * CELL_SIZE + CELL_SIZE // 2
    cy = y * CELL_SIZE + CELL_SIZE // 2
    r = CELL_SIZE * 0.40 # Чуть больший размер
    _player_id = canvas.create_oval(
        cx - r, cy - r, cx + r, cy + r,
        # ИЗМЕНЕНИЕ: Цвет паучка - ярко-зеленый
        fill="#64dd17", outline="black", width=1 
    )

def end_game(win):
    """Завершение игры."""
    global game_over, moving
    game_over = True
    moving = False
    msg = "Ура, паучок выбрался!" if win else "Паучок не выбрался (("
    messagebox.showinfo("Победа!" if win else "Проигрыш", msg)

def tick_timer():
    """Обновляет таймер."""
    global root, game_over, remaining, timer_label
    if not game_over:
        remaining = max(0, remaining - 1)
        timer_label.config(text=f"Время: {remaining:02d} с")
        if remaining == 0:
            end_game(win=False)
    if not game_over:
        root.after(1000, tick_timer)

def step():
    """Один шаг алгоритма DFS для движения паучка."""
    global root, game_over, moving, stack, visited, player_pos, exit_pos, maze, canvas, CELL_SIZE
    if game_over or not moving or not stack:
        return
    current = stack[-1]
    player_pos = current
    draw_player()
    x, y = current
    cx = x * CELL_SIZE + CELL_SIZE // 2
    cy = y * CELL_SIZE + CELL_SIZE // 2
    r = CELL_SIZE * random.uniform(0.1, 0.2) 
    canvas.create_oval(
        cx - r, cy - r, cx + r, cy + r,
        fill="#ff6d00", outline="", tags="trail"
    )

    if current in exit_positions:
        end_game(win=True)
        return

    neighbors = []
    for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < COLS and 0 <= ny < ROWS:
            if not maze[ny][nx] and (nx, ny) not in visited:
                neighbors.append((nx, ny))

    if neighbors:
        next_cell = random.choice(neighbors) 
        visited.add(next_cell)
        stack.append(next_cell)
    else:
        stack.pop()

    root.after(150, step) 

def start_step():
    
    global moving, game_over, stack, visited, player_pos
    if moving or game_over:
        return
    moving = True
    # Сброс стека и посещенных клеток
    stack = [player_pos]
    visited = {player_pos}
    
    tick_timer()
    step()

def reset_game():
    global moving, game_over, remaining, TIME_LIMIT_SEC, timer_label, canvas
    if moving:
        return  
    game_over = False
    moving = False
    remaining = TIME_LIMIT_SEC
    timer_label.config(text="Время: -- с")
    generate_maze()
    draw_maze()
    draw_player()
    canvas.delete("trail")
    
def setup_gui():
    """Настраивает графический интерфейс."""
    global root, canvas, timer_label, COLS, ROWS, CELL_SIZE, TIME_LIMIT_SEC
    root = tk.Tk()
    root.title("Паук в лабиринте (Усложненная версия)")
    canvas = tk.Canvas(root, width=COLS * CELL_SIZE,
                            height=ROWS * CELL_SIZE, bg="#f9fbe7")
    canvas.pack(pady=10)
    btn_frame = tk.Frame(root)
    btn_frame.pack()
    tk.Button(btn_frame, text="Новый лабиринт", command=reset_game).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Запустить", command=start_step).pack(side=tk.LEFT, padx=5)
    timer_label = tk.Label(root, text="Время: -- с", font=("Arial", 12))
    timer_label.pack()
    reset_game()
    root.mainloop()

if __name__ == "__main__":
    setup_gui()
