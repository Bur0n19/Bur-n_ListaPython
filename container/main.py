from tkinter import *
import customtkinter as ctk
app = ctk.CTk()
ancho = 850
alto = 700

#Centra la pantalla con
pantalla_ancho = app.winfo_screenwidth()
pantalla_alto = app.winfo_screenheight()
x = int((pantalla_ancho / 2) - (ancho / 2))
y = int((pantalla_alto / 2) - (alto / 2))
app.geometry(f"{ancho}x{alto}+{x}+{y}")

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')
app.title('Burón_EjerciciosPython')

btn1 = ctk.CTkButton(app, text='1.-')
btn2 = ctk.CTkButton(app, text='2.-')
btn3 = ctk.CTkButton(app, text='3.-')
btn4 = ctk.CTkButton(app, text='4.-')
btn5 = ctk.CTkButton(app, text='5.-')
btn6 = ctk.CTkButton(app, text='6.-')
btn7 = ctk.CTkButton(app, text='7.-')
btn8 = ctk.CTkButton(app, text='8.-')
btn9 = ctk.CTkButton(app, text='9.-')
btn10 = ctk.CTkButton(app, text='10.-')


btn1.grid(row=0, column=0, padx=20, pady=20)
btn2.grid(row=0, column=1, padx=20, pady=20)
btn3.grid(row=0, column=2, padx=20, pady=20)
btn4.grid(row=1, column=0, padx=20, pady=20)
btn5.grid(row=1, column=1, padx=20, pady=20)
btn6.grid(row=1, column=2, padx=20, pady=20)
btn7.grid(row=2, column=0, padx=20, pady=20)
btn8.grid(row=2, column=1, padx=20, pady=20)
btn9.grid(row=2, column=2, padx=20, pady=20)
btn10.grid(row=3, column=1, padx=20, pady=20)

app.mainloop()













