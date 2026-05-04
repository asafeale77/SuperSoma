import tkinter as tk
from tkinter import ttk


class CalculadoraCompleta:
    def __init__(self, raiz):
        self.raiz = raiz
        self.raiz.title('Calculadora Completa')
        self.raiz.geometry('360x600')
        self.raiz.resizable(False, False)
        self.raiz.configure(bg='#2B2D42')

        self.expressao = ''
        self.resultado_var = tk.StringVar(value='0')

        self._criar_layout()

    def _criar_layout(self):
        painel = tk.Frame(self.raiz, bg='#2B2D42', padx=12, pady=12)
        painel.pack(expand=True, fill='both')

        titulo = tk.Label(
            painel,
            text='Calculadora Completa',
            bg='#2B2D42',
            fg='#EDF2F4',
            font=('Segoe UI', 16, 'bold'),
        )
        titulo.pack(pady=(0, 12))

        self.display = tk.Entry(
            painel,
            textvariable=self.resultado_var,
            font=('Segoe UI', 20, 'bold'),
            bd=0,
            relief='flat',
            justify='right',
            bg='#8D99AE',
            fg='#2B2D42',
            insertbackground='#2B2D42',
        )
        self.display.pack(fill='x', ipady=12, pady=(0, 18))

        botoes = [
            ['C', 'CE', '%', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '(', ')'],
            ['⌫', 'x^2', '√', '='],
        ]

        for linha in botoes:
            linha_frame = tk.Frame(painel, bg='#2B2D42')
            linha_frame.pack(fill='x', pady=2)
            for botao_texto in linha:
                botao = tk.Button(
                    linha_frame,
                    text=botao_texto,
                    command=lambda valor=botao_texto: self._acao_botao(valor),
                    font=('Segoe UI', 12, 'bold'),
                    fg='#EDF2F4',
                    bg='#4C5C68',
                    activebackground='#6D7E92',
                    activeforeground='#EDF2F4',
                    bd=0,
                    relief='ridge',
                    height=3,
                    width=7,
                )
                botao.pack(side='left', expand=True, fill='x', padx=2)

    def _acao_botao(self, valor):
        if valor == 'C':
            self.expressao = ''
            self.resultado_var.set('0')
            return
        if valor == 'CE':
            self.expressao = self.expressao[:-1]
            self.resultado_var.set(self.expressao or '0')
            return
        if valor == '⌫':
            self.expressao = self.expressao[:-1]
            self.resultado_var.set(self.expressao or '0')
            return
        if valor == 'x^2':
            if self.expressao:
                try:
                    valor_calc = str(eval(self.expressao))
                    self.expressao = f'({valor_calc})**2'
                    self._calcular_expressao()
                except Exception:
                    self.resultado_var.set('Erro')
            return
        if valor == '√':
            if self.expressao:
                try:
                    valor_calc = float(eval(self.expressao))
                    if valor_calc < 0:
                        raise ValueError
                    self.expressao = str(valor_calc ** 0.5)
                    self.resultado_var.set(self.expressao)
                except Exception:
                    self.resultado_var.set('Erro')
            return
        if valor == '%':
            self.expressao += '/100'
            self.resultado_var.set(self.expressao)
            return
        if valor == '=':
            self._calcular_expressao()
            return

        if valor == '.':
            if not self.expressao or self.expressao[-1] in '+-*/()':
                self.expressao += '0.'
            else:
                self.expressao += '.'
        else:
            self.expressao += valor

        self.resultado_var.set(self.expressao)

    def _calcular_expressao(self):
        try:
            resultado = eval(self.expressao)
            if resultado == int(resultado):
                resultado = int(resultado)
            self.resultado_var.set(str(resultado))
            self.expressao = str(resultado)
        except Exception:
            self.resultado_var.set('Erro')
            self.expressao = ''


if __name__ == '__main__':
    raiz = tk.Tk()
    CalculadoraCompleta(raiz)
    raiz.mainloop()
