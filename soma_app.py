import tkinter as tk
from tkinter import ttk
from decimal import Decimal, InvalidOperation


def calcular_soma():
    valor1 = entrada_numero1.get().strip()
    valor2 = entrada_numero2.get().strip()
    try:
        numero1 = Decimal(valor1.replace(',', '.'))
        numero2 = Decimal(valor2.replace(',', '.'))
        resultado = numero1 + numero2
        resultado_label.config(text=str(resultado).replace('.', ','))
    except InvalidOperation:
        resultado_label.config(text='Entrada inválida')


app = tk.Tk()
app.title('Super Soma')
app.geometry('380x290')
app.resizable(False, False)
app.configure(bg='#2C3E50')

style = ttk.Style(app)
style.theme_use('clam')
style.configure('TLabel', background='#34495E', foreground='#ECF0F1', font=('Segoe UI', 11))
style.configure('TEntry', fieldbackground='#ECF0F1', foreground='#2C3E50', font=('Segoe UI', 11))

frame = tk.Frame(app, bg='#34495E', padx=22, pady=22)
frame.pack(expand=True, fill='both')

titulo = ttk.Label(frame, text='Super Soma', font=('Segoe UI', 18, 'bold'))
titulo.pack(pady=(0, 8))

subtitulo = ttk.Label(frame, text='Digite o número 1 e o número 2, depois clique em Calcular', font=('Segoe UI', 10))
subtitulo.pack(pady=(0, 20))

label_numero1 = ttk.Label(frame, text='Número 1:')
label_numero1.pack(anchor='w', pady=(0, 6))
entrada_numero1 = ttk.Entry(frame, width=28)
entrada_numero1.pack(pady=(0, 12))

label_numero2 = ttk.Label(frame, text='Número 2:')
label_numero2.pack(anchor='w', pady=(0, 6))
entrada_numero2 = ttk.Entry(frame, width=28)
entrada_numero2.pack(pady=(0, 16))

botao_somar = tk.Button(
    frame,
    text='Calcular',
    command=calcular_soma,
    bg='#3498DB',
    fg='#FFFFFF',
    activebackground='#2980B9',
    activeforeground='#FFFFFF',
    font=('Segoe UI', 11, 'bold'),
    bd=0,
    relief='ridge',
    padx=12,
    pady=8,
)
botao_somar.pack(pady=(0, 18))

resultado_label = tk.Label(
    frame,
    text='Resultado aparecerá aqui',
    bg='#ECF0F1',
    fg='#2C3E50',
    font=('Segoe UI', 12, 'bold'),
    relief='sunken',
    padx=12,
    pady=12,
    anchor='center',
)
resultado_label.pack(fill='x')

app.mainloop()
