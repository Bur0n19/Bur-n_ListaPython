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

class LoginFrame(ctk.CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        self.controlador = controlador

        self.USUARIO_VALIDO = "a"
        self.CONTRASENA_VALIDA = "a"

        label_titulo = ctk.CTkLabel(self, text="INICIAR SESIÓN", font=("Arial", 25, "bold"))
        label_titulo.pack(pady=(80, 40))

        self.entry_user = ctk.CTkEntry(self, placeholder_text="Usuario", width=250)
        self.entry_user.pack(pady=10)

        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=250)
        self.entry_pass.pack(pady=10)

        self.lbl_msg = ctk.CTkLabel(self, text="", text_color="red")
        self.lbl_msg.pack(pady=5)

        btn_login = ctk.CTkButton(self, text="Login", command=self.verificar_login, width=250)
        btn_login.pack(pady=20)

        self.entry_user.bind("<Return>", lambda e: self.verificar_login())
        self.entry_pass.bind("<Return>", lambda e: self.verificar_login())

    def verificar_login(self):
        user = self.entry_user.get()
        pwd = self.entry_pass.get()

        if user == self.USUARIO_VALIDO and pwd == self.CONTRASENA_VALIDA:
            self.lbl_msg.configure(text="")
            self.entry_user.delete(0, 'end')
            self.entry_pass.delete(0, 'end')

            self.controlador.mostrar_frame("menu")
        else:
            self.lbl_msg.configure(text="Usuario o contraseña incorrectos")


class MenuPrincipal(ctk.CTkFrame):
    def __init__(self, parent, controlador):
        super().__init__(parent)
        label = ctk.CTkLabel(self, text="MENÚ PRINCIPAL", font=("Arial", 25))
        label.pack(pady=20)

        marca = ctk.CTkLabel(self, text="César A. Burón M. 6IV8_Fundamentos IA", font=("Arial", 20))
        marca.pack(pady=15)

        btn1 = ctk.CTkButton(self, text="Ejercicio 1", command=lambda: controlador.mostrar_frame("ej1"))
        btn1.pack(pady=5)

        btn2 = ctk.CTkButton(self, text="Ejercicio 2", command=lambda: controlador.mostrar_frame("ej2"))
        btn2.pack(pady=5)

        btn3 = ctk.CTkButton(self, text="Ejercicio 3", command=lambda: controlador.mostrar_frame("ej3"))
        btn3.pack(pady=5)

        btn4 = ctk.CTkButton(self, text="Ejercicio 4", command=lambda: controlador.mostrar_frame("ej4"))
        btn4.pack(pady=5)

        btn5 = ctk.CTkButton(self, text="Ejercicio 5", command=lambda: controlador.mostrar_frame("ej5"))
        btn5.pack(pady=5)

        btn6 = ctk.CTkButton(self, text="Ejercicio 6", command=lambda: controlador.mostrar_frame("ej6"))
        btn6.pack(pady=5)

        btn7 = ctk.CTkButton(self, text="Ejercicio 7", command=lambda: controlador.mostrar_frame("ej7"))
        btn7.pack(pady=5)

        btn8 = ctk.CTkButton(self, text="Ejercicio 8", command=lambda: controlador.mostrar_frame("ej8"))
        btn8.pack(pady=5)

        btn9 = ctk.CTkButton(self, text="Ejercicio 9", command=lambda: controlador.mostrar_frame("ej9"))
        btn9.pack(pady=5)

        btn10 = ctk.CTkButton(self, text="Ejercicio 10", command=lambda: controlador.mostrar_frame("ej10"))
        btn10.pack(pady=5)

        btn_logout = ctk.CTkButton(self, text="Cerrar Sesión", fg_color="red", hover_color="darkred",command=lambda: controlador.mostrar_frame("login"))
        btn_logout.pack(pady=(2, 15))

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Burón Ejercicios Python')
        self.geometry('850x750')

        self.contenedor = ctk.CTkFrame(self)
        self.contenedor.pack(fill="both", expand=True)
        self.contenedor.grid_rowconfigure(0, weight=1)
        self.contenedor.grid_columnconfigure(0, weight=1)

        self.frames = {}

        vistas = {"login": LoginFrame, "menu": MenuPrincipal,
                  "ej1": Ejercicio1, "ej2": Ejercicio2, "ej3": Ejercicio3,
                  "ej4": Ejercicio4, "ej5": Ejercicio5, "ej6": Ejercicio6,
                  "ej7": Ejercicio7, "ej8": Ejercicio8, "ej9": Ejercicio9,
                  "ej10": Ejercicio10
                  }

        for nombre, clase in vistas.items():
            frame = clase(parent=self.contenedor, controlador=self)
            self.frames[nombre] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_frame("login")

    def mostrar_frame(self, nombre):
        frame = self.frames[nombre]
        frame.tkraise()

        if nombre == "login":
            frame.entry_user.focus()


if __name__ == "__main__":
    app = App()
    app.mainloop()