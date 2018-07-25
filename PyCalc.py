#!python
#
# PyCalc - Calculadora simples 
# Tiago B. 
# tdsb.contato@gmail.com
# 05/10/2017
#
import tkinter as tk
class Calc():
    def __init__(self, parent=tk.Tk()):
        self.parent = parent
        self.parent.title("PyCalc - Calculadora")
        self.parent.option_add("*Font", "Verdana 12 normal")
        self.parent.iconbitmap("icones/calc_icon.ico")        
        #variável contendo a expressão pronta para calculo
        self.math_expression = None
        #menubar
        menu_bar = tk.Menu(self.parent)
        menu_bar.add_command(label="Sobre", command=self.about)
        self.parent.config(menu=menu_bar)
        
        #elementos do display
        self.display_stringvar = tk.StringVar()
        display_entry_validate = (self.parent.register(self.only_number_entry), '%S', '%d')
        self.display = tk.Entry(self.parent, font=("Verdana", 20, "normal"), validate="key", validatecommand=display_entry_validate, textvariable=self.display_stringvar)
        self.display.bind('<Return>', self.command_calc)
        
        #criação do teclado numerico
        #Gera os botões de forma dinâmica
        #refatorado 25/07/2018
        self.buttons = []
        simbols = ['7','8','9','*','4','5','6','-','1','2','3','+','0','.','=','/','Sair','Limpar','Del']
        for simbol in simbols:
            new_button = tk.Button(self.parent, text=simbol, command=lambda simbol=simbol:self.button_press(simbol))
            self.buttons.append(new_button)

        self.parent.bind("<Escape>", lambda event=None: self.parent.destroy())
    
    def run(self):
        self.mount_gui()
        self.parent.mainloop()

    #monta e configura os componentes gráficos
    def mount_gui(self):
        
        self.display.grid(row=0, column=0, columnspan=4, sticky="ewns", ipady=5, padx=2, pady=2)
        
        #Posiciona os botões dinâmicamente
        #Refatorado 25/07/2018
        row, column = 1, 0
        for button in self.buttons:
            #A posição 5x2 não deve ser ocupada, Limpar irá ocupa-la 
            if row==5 and column==2:
                column+=1
            #Posiciona o Limpar em 5x1
            if row==5 and column==1:
                button.grid(row=row, column=column, columnspan=2,sticky="ewns", padx=2, pady=2)
            else:
                button.grid(row=row, column=column,sticky="ewns", padx=2, pady=2)

            if column == 3:
                column = 0
                row+=1
            else:
                column+=1

    #limpa o display    
    def clear(self):
        self.display_stringvar.set("")
        self.math_expression = None
            
    #tela sobre
    def about(self):
        about_window = tk.Toplevel(self.parent)
        about_window.title("PyCalc - Sobre")
        about_window.iconbitmap("icones/about_icon.ico")
        tk.Label(about_window, text="PyCalc", font=("Verdana", 15, "bold")).grid(row=0, column=0, padx=5, pady=5, sticky="s")
        tk.Label(about_window, text="Calculadora simples").grid(row=1, column=0, padx=5, pady=5, sticky="s")
        tk.Label(about_window, text="Desenvolvida em Python 3 e Tkinter").grid(row=2, column=0, sticky="s", padx=5)
        tk.Label(about_window, text="tdsb.contato@gmail.com").grid(row=3, column=0, sticky="s", padx=5)

    #validador de entrys somente expressões matemáticas válidas
    def only_number_entry(self, button, operation):
        isvalid = False
        numbers = "0123456789"
        operators = "+-*/" 
        string = self.display_stringvar.get()
        index = len(string)
        str_size = index
        #permite remoção
        if operation == '0':
            index-=1
            isvalid = True
        #primeira posição aceita apenas numeros
        if str_size == 0:
            isvalid = button in numbers
        else:
            #pega o ultimo caractere na string
            last_char = string[index-1]
            #se ultimo caracter é numero e o pressionado é numero, operador ou ponto
            if last_char in numbers and button in numbers or last_char in numbers and button in operators or last_char in numbers and button  == ".":
                isvalid = True
            elif last_char == "." and button in numbers:
                isvalid = True
            elif last_char in operators and button in numbers:
                isvalid = True 
        return isvalid

    #botão da interface pressionado
    def button_press(self, button):
        index = len(self.display_stringvar.get())
        if button == "Del":
            index-=1
            self.display.delete(index,'end')
        elif button == 'Limpar':
            self.clear()
        elif button == 'Sair':
            self.parent.destroy()
        elif button == "=" and self.expression_check():         
            self.calc_expression()
        else:   
            self.display.insert(index, button)
    
    #enter no display equivalente ao '='
    def command_calc(self,event=None):
        if self.expression_check():
            self.calc_expression()

    #antes de começar o calculo, checa se o final da expressão é válida
    def expression_check(self):
        isvalid = False
        string = self.display_stringvar.get()
        index = len(string)
        if index == 0:
            isvalid = False
        else:
            index -= 1
            last_char = string[index]   
            if last_char in "+-*/.":
                isvalid = False
            elif last_char in "0123456789":
                isvalid = True
        return isvalid

    #prepara a expressão para o calculo
    def prepare_expression(self):
        elements = []
        index = 0
        operators = "+-*/"
        for char in self.display_stringvar.get():
            #inicializa a lista com o primeiro numero
            if len(elements) == 0 and char in "0123456789":
                elements.append(char)
            #operador como novo elemento da lista
            elif len(elements) > 0 and char in operators:
                elements.append(char)
                index += 1
            elif elements[index] in operators:
                elements.append(char)
                index += 1
            else:
                elements[index] += char
        #salva a expressão preparada como atributo do objeto
        self.math_expression = elements

    #efetua o calculo da expressão
    def calc_expression(self, event=None):
        self.prepare_expression()
        #multiplicação e divisão
        #precedencia: o que vier primeiro da esquerda para a direita
        while "*" in self.math_expression or "/" in self.math_expression:
            index = 0
            for element in self.math_expression:
                if element in '/*':
                    value1 = float(self.math_expression[index - 1])
                    value2 = float(self.math_expression[index + 1])
                    if element == '*':
                        result = str(value1 * value2)
                    elif element == '/':
                        result = str(value1 / value2)
                    self.math_expression[index] = result
                    self.math_expression.pop(index + 1)
                    self.math_expression.pop(index - 1)
                    break
                index += 1
        # soma e subtração
        # repete até que sobre apenas o resultado
        while len(self.math_expression) > 1:
            index = 0
            for element in self.math_expression:
                if element in '+-':
                    value1 = float(self.math_expression[index - 1])
                    value2 = float(self.math_expression[index + 1])
                    if element == '+':
                        result = str(value1 + value2)
                    elif element == '-':
                        result = str(value1 - value2)
                    self.math_expression[index] = result
                    self.math_expression.pop(index + 1)
                    self.math_expression.pop(index - 1)
                    break
                index += 1
        final_result = round(float(self.math_expression[0]), 1)
        if final_result % 1 == 0:
            final_result = int(final_result)
        final_result = str(final_result)
        #insere o resultado no display
        self.display_stringvar.set(final_result)

if __name__ == "__main__":
    calc = Calc()
    calc.run()
