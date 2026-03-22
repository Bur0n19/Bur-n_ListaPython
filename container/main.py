import customtkinter as ctk

from ejercicio1 import Ejercicio1
from ejercicio2 import Ejercicio2
from ejercicio3 import Ejercicio3
from ejercicio4 import Ejercicio4
from ejercicio5 import Ejercicio5
from ejercicio6 import Ejercicio6
from ejercicio7 import Ejercicio7
from ejercicio8 import Ejercicio8
from ejercicio9 import Ejercicio9
from ejercicio10 import Ejercicio10


class MenuPrincipal(ctk.CTkFrame):

    def __init__(self, parent, controlador):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="MENÚ PRINCIPAL", font=("Arial", 25))
        label.pack(pady=20)

        marca = ctk.CTkLabel(self, text="César A. Burón M. 6IV8_Fundamentos IA", font=("Arial", 20))
        marca.pack(pady=15)

        btn1 = ctk.CTkButton(self, text="Ejercicio 1", command=lambda: controlador.mostrar_frame("ej1"))
        btn1.pack(pady=12)

        btn2 = ctk.CTkButton(self, text="Ejercicio 2", command=lambda: controlador.mostrar_frame("ej2"))
        btn2.pack(pady=12)

        btn3 = ctk.CTkButton(self, text="Ejercicio 3", command=lambda: controlador.mostrar_frame("ej3"))
        btn3.pack(pady=12)

        btn4 = ctk.CTkButton(self, text="Ejercicio 4", command=lambda: controlador.mostrar_frame("ej4"))
        btn4.pack(pady=12)

        btn5 = ctk.CTkButton(self, text="Ejercicio 5", command=lambda: controlador.mostrar_frame("ej5"))
        btn5.pack(pady=12)

        btn6 = ctk.CTkButton(self, text="Ejercicio 6", command=lambda: controlador.mostrar_frame("ej6"))
        btn6.pack(pady=12)

        btn7 = ctk.CTkButton(self, text="Ejercicio 7", command=lambda: controlador.mostrar_frame("ej7"))
        btn7.pack(pady=12)

        btn8 = ctk.CTkButton(self, text="Ejercicio 8", command=lambda: controlador.mostrar_frame("ej8"))
        btn8.pack(pady=12)

        btn9 = ctk.CTkButton(self, text="Ejercicio 9", command=lambda: controlador.mostrar_frame("ej9"))
        btn9.pack(pady=12)

        btn10 = ctk.CTkButton(self, text="Ejercicio 10", command=lambda: controlador.mostrar_frame("ej10"))
        btn10.pack(pady=12)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Burón Ejercicios Python')
        self.geometry('850x700')

        self.contenedor = ctk.CTkFrame(self)
        self.contenedor.pack(fill="both", expand=True)
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)

        self.frames={}

        vistas = { "menu": MenuPrincipal,
                  "ej1": Ejercicio1, "ej2": Ejercicio2, "ej3": Ejercicio3,
                  "ej4": Ejercicio4, "ej5": Ejercicio5, "ej6": Ejercicio6,
                  "ej7": Ejercicio7, "ej8": Ejercicio8, "ej9": Ejercicio9,
                  "ej10": Ejercicio10
                  }

        for nombre, clase in vistas.items():
            frame = clase(parent = self.contenedor, controlador = self)
            self.frames[nombre] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame("menu")

    def mostrar_frame(self, nombre):
        frame = self.frames[nombre]
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()





