import tkinter as tk
import math
import re

# ── Paleta ──────────────────────────────────────────────────────────────────
BG        = "#0d0d0f"
SURFACE   = "#18181c"
SURFACE2  = "#222228"
ACCENT    = "#c8ff00"        # verde-limão neon
ACCENT2   = "#7c3aed"        # roxo vibrante
TEXT      = "#f0f0f0"
TEXT_DIM  = "#666680"
BTN_NUM   = "#1e1e26"
BTN_OP    = "#2a1f3d"
BTN_EQ    = ACCENT
BTN_SPEC  = "#1a1a22"
DANGER    = "#ff4d6d"

FONT_DISPLAY  = ("Courier New", 38, "bold")
FONT_EXPR     = ("Courier New", 13)
FONT_BTN      = ("Courier New", 15, "bold")
FONT_BTN_SM   = ("Courier New", 11, "bold")
FONT_HIST     = ("Courier New", 10)

# ── Estado ──────────────────────────────────────────────────────────────────
class CalcState:
    def __init__(self):
        self.expr      = ""
        self.result    = "0"
        self.history   = []
        self.mem       = 0.0
        self.just_eval = False
        self.deg_mode  = True   # True=DEG, False=RAD

state = CalcState()

# ── Avaliador seguro ─────────────────────────────────────────────────────────
def safe_eval(expr: str) -> str:
    expr = expr.replace("×", "*").replace("÷", "/").replace("^", "**")
    expr = expr.replace("π", str(math.pi)).replace("e", str(math.e))

    def trig(fn, x):
        x = float(x)
        if state.deg_mode:
            x = math.radians(x)
        return fn(x)

    allowed = {
        "__builtins__": {},
        "sin":   lambda x: trig(math.sin, x),
        "cos":   lambda x: trig(math.cos, x),
        "tan":   lambda x: trig(math.tan, x),
        "asin":  lambda x: math.degrees(math.asin(float(x))) if state.deg_mode else math.asin(float(x)),
        "acos":  lambda x: math.degrees(math.acos(float(x))) if state.deg_mode else math.acos(float(x)),
        "atan":  lambda x: math.degrees(math.atan(float(x))) if state.deg_mode else math.atan(float(x)),
        "sqrt":  math.sqrt,
        "log":   math.log10,
        "ln":    math.log,
        "abs":   abs,
        "floor": math.floor,
        "ceil":  math.ceil,
        "factorial": math.factorial,
        "exp":   math.exp,
        "pi":    math.pi,
        "math":  math,
    }
    result = eval(expr, allowed)
    if isinstance(result, float):
        if result == int(result) and abs(result) < 1e15:
            return str(int(result))
        return f"{result:.10g}"
    return str(result)

# ── Lógica dos botões ────────────────────────────────────────────────────────
def press(value):
    expr_var.set(state.expr)
    res = state.result

    if value == "C":
        state.expr = ""; state.result = "0"; state.just_eval = False
    elif value == "⌫":
        state.expr = state.expr[:-1] if state.expr else ""
        state.result = state.expr or "0"
        state.just_eval = False
    elif value == "=":
        if not state.expr:
            return
        try:
            ans = safe_eval(state.expr)
            state.history.append(f"{state.expr} = {ans}")
            if len(state.history) > 50:
                state.history.pop(0)
            update_history()
            state.result = ans
            state.expr   = ans
            state.just_eval = True
        except Exception as e:
            state.result = "Erro"
            state.expr   = ""
            state.just_eval = False
    elif value == "+/-":
        if state.expr:
            if state.expr.startswith("-"):
                state.expr = state.expr[1:]
            else:
                state.expr = "-" + state.expr
            state.result = state.expr
    elif value == "%":
        try:
            val = safe_eval(state.expr)
            state.expr   = str(float(val) / 100)
            state.result = state.expr
        except:
            pass
    elif value == "DEG/RAD":
        state.deg_mode = not state.deg_mode
        mode_btn.config(text="DEG" if state.deg_mode else "RAD")
    elif value == "MC":
        state.mem = 0.0; mem_label.config(text="M: 0")
    elif value == "MR":
        state.expr += str(state.mem); state.result = state.expr; state.just_eval = False
    elif value == "M+":
        try: state.mem += float(safe_eval(state.expr)); mem_label.config(text=f"M: {state.mem:.4g}")
        except: pass
    elif value == "M-":
        try: state.mem -= float(safe_eval(state.expr)); mem_label.config(text=f"M: {state.mem:.4g}")
        except: pass
    elif value == "x²":
        state.expr += "**2"; state.result = state.expr; state.just_eval = False
    elif value == "x³":
        state.expr += "**3"; state.result = state.expr; state.just_eval = False
    elif value == "1/x":
        state.expr = f"1/({state.expr})"; state.result = state.expr; state.just_eval = False
    elif value == "10ˣ":
        state.expr = f"10**({state.expr})"; state.result = state.expr; state.just_eval = False
    elif value in ("sin(", "cos(", "tan(", "asin(", "acos(", "atan(",
                   "sqrt(", "log(", "ln(", "abs(", "floor(", "ceil(", "factorial(", "exp("):
        if state.just_eval:
            state.expr = value; state.just_eval = False
        else:
            state.expr += value
        state.result = state.expr
    else:
        if state.just_eval and value not in ("+", "-", "*", "/", "×", "÷", "^", "(", ")"):
            state.expr = ""
        state.just_eval = False
        state.expr += value
        state.result = state.expr

    display_result.set(state.result if len(state.result) < 20 else state.result[:18] + "…")
    expr_var.set(state.expr)
    animate_display()

def update_history():
    hist_text.config(state="normal")
    hist_text.delete("1.0", tk.END)
    for h in reversed(state.history[-12:]):
        hist_text.insert(tk.END, h + "\n")
    hist_text.config(state="disabled")

def animate_display():
    display_lbl.config(fg=ACCENT)
    root.after(80, lambda: display_lbl.config(fg=TEXT))

# ── Janela principal ─────────────────────────────────────────────────────────
root = tk.Tk()
root.title("CALC PRO")
root.configure(bg=BG)
root.resizable(False, False)
root.geometry("520x780")

display_result = tk.StringVar(value="0")
expr_var       = tk.StringVar(value="")

# ── Título ────────────────────────────────────────────────────────────────────
header = tk.Frame(root, bg=BG)
header.pack(fill="x", padx=20, pady=(18, 0))
tk.Label(header, text="◈ CALC PRO", bg=BG, fg=ACCENT,
         font=("Courier New", 13, "bold")).pack(side="left")
mem_label = tk.Label(header, text="M: 0", bg=BG, fg=TEXT_DIM,
                     font=("Courier New", 10))
mem_label.pack(side="right")

# ── Display ───────────────────────────────────────────────────────────────────
disp_frame = tk.Frame(root, bg=SURFACE, bd=0, highlightthickness=1,
                      highlightbackground=ACCENT2)
disp_frame.pack(fill="x", padx=16, pady=(8, 0), ipady=12)

expr_lbl = tk.Label(disp_frame, textvariable=expr_var, bg=SURFACE, fg=TEXT_DIM,
                    font=FONT_EXPR, anchor="e", padx=14)
expr_lbl.pack(fill="x")

display_lbl = tk.Label(disp_frame, textvariable=display_result, bg=SURFACE,
                       fg=TEXT, font=FONT_DISPLAY, anchor="e", padx=14)
display_lbl.pack(fill="x")

# ── Histórico ─────────────────────────────────────────────────────────────────
hist_frame = tk.Frame(root, bg=SURFACE2, bd=0)
hist_frame.pack(fill="x", padx=16, pady=(6, 0))
tk.Label(hist_frame, text="HISTÓRICO", bg=SURFACE2, fg=TEXT_DIM,
         font=("Courier New", 8, "bold")).pack(anchor="w", padx=8, pady=(4,0))
hist_text = tk.Text(hist_frame, bg=SURFACE2, fg=TEXT_DIM, font=FONT_HIST,
                    height=3, bd=0, state="disabled", wrap="none")
hist_text.pack(fill="x", padx=8, pady=(0, 4))

# ── Fábrica de botões ─────────────────────────────────────────────────────────
def make_btn(parent, text, color_bg, color_fg, col, row, colspan=1, small=False):
    font = FONT_BTN_SM if small else FONT_BTN
    fg   = "#0d0d0f" if color_bg == BTN_EQ else color_fg

    btn = tk.Button(
        parent, text=text, bg=color_bg, fg=fg,
        font=font, bd=0, relief="flat", cursor="hand2",
        activebackground=ACCENT if color_bg == BTN_EQ else ACCENT2,
        activeforeground="#000",
        command=lambda v=text: press(v)
    )
    btn.grid(row=row, column=col, columnspan=colspan,
             sticky="nsew", padx=3, pady=3, ipady=10 if not small else 6)

    def on_enter(e):
        btn.config(bg=ACCENT if color_bg == BTN_EQ else "#333345")
    def on_leave(e):
        btn.config(bg=color_bg)

    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

# ── Grid de botões ────────────────────────────────────────────────────────────
btn_frame = tk.Frame(root, bg=BG)
btn_frame.pack(fill="both", expand=True, padx=12, pady=10)

for i in range(10):
    btn_frame.rowconfigure(i, weight=1)
for i in range(5):
    btn_frame.columnconfigure(i, weight=1)

# Linha 0 — Memória
make_btn(btn_frame, "MC",  BTN_SPEC, TEXT_DIM, 0, 0, small=True)
make_btn(btn_frame, "MR",  BTN_SPEC, TEXT_DIM, 1, 0, small=True)
make_btn(btn_frame, "M+",  BTN_SPEC, TEXT_DIM, 2, 0, small=True)
make_btn(btn_frame, "M-",  BTN_SPEC, TEXT_DIM, 3, 0, small=True)
mode_btn = make_btn(btn_frame, "DEG", BTN_SPEC, ACCENT, 4, 0, small=True)
mode_btn.config(command=lambda: press("DEG/RAD"))

# Linha 1 — Funções científicas
make_btn(btn_frame, "sin(",  BTN_OP, "#a78bfa", 0, 1, small=True)
make_btn(btn_frame, "cos(",  BTN_OP, "#a78bfa", 1, 1, small=True)
make_btn(btn_frame, "tan(",  BTN_OP, "#a78bfa", 2, 1, small=True)
make_btn(btn_frame, "log(",  BTN_OP, "#a78bfa", 3, 1, small=True)
make_btn(btn_frame, "ln(",   BTN_OP, "#a78bfa", 4, 1, small=True)

# Linha 2 — Funções científicas 2
make_btn(btn_frame, "sqrt(", BTN_OP, "#a78bfa", 0, 2, small=True)
make_btn(btn_frame, "x²",    BTN_OP, "#a78bfa", 1, 2, small=True)
make_btn(btn_frame, "x³",    BTN_OP, "#a78bfa", 2, 2, small=True)
make_btn(btn_frame, "^",     BTN_OP, "#a78bfa", 3, 2, small=True)
make_btn(btn_frame, "1/x",   BTN_OP, "#a78bfa", 4, 2, small=True)

# Linha 3 — Funções especiais
make_btn(btn_frame, "(",       BTN_SPEC, TEXT_DIM, 0, 3, small=True)
make_btn(btn_frame, ")",       BTN_SPEC, TEXT_DIM, 1, 3, small=True)
make_btn(btn_frame, "π",       BTN_SPEC, ACCENT2,  2, 3, small=True)
make_btn(btn_frame, "e",       BTN_SPEC, ACCENT2,  3, 3, small=True)
make_btn(btn_frame, "factorial(", BTN_OP, "#a78bfa", 4, 3, small=True).config(text="n!")

# Linha 4 — Operadores básicos superiores
make_btn(btn_frame, "C",   DANGER,   "#fff",     0, 4)
make_btn(btn_frame, "+/-", BTN_SPEC, TEXT_DIM,   1, 4)
make_btn(btn_frame, "%",   BTN_SPEC, TEXT_DIM,   2, 4)
make_btn(btn_frame, "⌫",   BTN_OP,   ACCENT,     3, 4)
make_btn(btn_frame, "÷",   BTN_OP,   "#a78bfa",  4, 4)

# Linha 5
make_btn(btn_frame, "7", BTN_NUM, TEXT, 0, 5)
make_btn(btn_frame, "8", BTN_NUM, TEXT, 1, 5)
make_btn(btn_frame, "9", BTN_NUM, TEXT, 2, 5)
make_btn(btn_frame, "abs(",BTN_OP,"#a78bfa",3, 5, small=True)
make_btn(btn_frame, "×",   BTN_OP, "#a78bfa", 4, 5)

# Linha 6
make_btn(btn_frame, "4", BTN_NUM, TEXT, 0, 6)
make_btn(btn_frame, "5", BTN_NUM, TEXT, 1, 6)
make_btn(btn_frame, "6", BTN_NUM, TEXT, 2, 6)
make_btn(btn_frame, "exp(", BTN_OP,"#a78bfa",3, 6, small=True)
make_btn(btn_frame, "-",    BTN_OP, "#a78bfa", 4, 6)

# Linha 7
make_btn(btn_frame, "1", BTN_NUM, TEXT, 0, 7)
make_btn(btn_frame, "2", BTN_NUM, TEXT, 1, 7)
make_btn(btn_frame, "3", BTN_NUM, TEXT, 2, 7)
make_btn(btn_frame, "10ˣ", BTN_OP,"#a78bfa",3, 7, small=True)
make_btn(btn_frame, "+",   BTN_OP, "#a78bfa", 4, 7)

# Linha 8
make_btn(btn_frame, "0",   BTN_NUM, TEXT, 0, 8, colspan=2)
make_btn(btn_frame, ".",   BTN_NUM, TEXT, 2, 8)
make_btn(btn_frame, "asin(",BTN_OP,"#a78bfa",3, 8, small=True)
make_btn(btn_frame, "=",   BTN_EQ,  "#000", 4, 8)

# ── Rodapé ────────────────────────────────────────────────────────────────────
tk.Label(root, text="◈ powered by python", bg=BG, fg=TEXT_DIM,
         font=("Courier New", 8)).pack(pady=(0, 6))

# ── Teclado físico ────────────────────────────────────────────────────────────
key_map = {
    "Return": "=", "BackSpace": "⌫", "Escape": "C",
    "plus": "+", "minus": "-", "asterisk": "×", "slash": "÷",
    "percent": "%", "parenleft": "(", "parenright": ")",
    "period": ".", "comma": ".",
}
for c in "0123456789":
    key_map[c] = c

def on_key(event):
    k = event.keysym
    if k in key_map:
        press(key_map[k])
    elif event.char in "0123456789.+-*/()%^":
        ch = event.char
        if ch == "*": ch = "×"
        if ch == "/": ch = "÷"
        press(ch)

root.bind("<Key>", on_key)
root.mainloop()